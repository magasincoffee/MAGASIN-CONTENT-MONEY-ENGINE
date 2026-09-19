"""MCME publish safety harness: MOCK/DRY-RUN ONLY; no network/browser/API."""
from __future__ import annotations
import hashlib,json,os,re,tempfile
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from pathlib import Path
from typing import Protocol

PREPARED='PREPARED'; SEND_STARTED='SEND_STARTED'; CONFIRMED='CONFIRMED'; BLOCKED_AUTH='BLOCKED_AUTH'; BLOCKED_AMBIGUOUS='BLOCKED_AMBIGUOUS'; FAILED_CONFIRMED='FAILED_CONFIRMED'
PRESENT='CONFIRMED_PRESENT'; ABSENT='CONFIRMED_ABSENT'; UNKNOWN='UNKNOWN'; AMBIGUOUS='AMBIGUOUS'
STATES={PREPARED,SEND_STARTED,CONFIRMED,BLOCKED_AUTH,BLOCKED_AMBIGUOUS,FAILED_CONFIRMED}; RECONS={None,PRESENT,ABSENT,UNKNOWN,AMBIGUOUS}
MAX_SEND_ATTEMPTS=2
DEFAULT_DIR=Path.home()/'.mcme_private'/'publish_safety'; ENV_DIR='MCME_PUBLISH_SAFETY_DIR'
SECRETISH=re.compile(r'(?i)(https?://|bearer\s+|password|passwd|token|cookie|session|otp|mfa|captcha|api[_-]?key|secret|bank|routing|card|tax[_-]?id)')
class Error(ValueError):pass
class PrivacyError(Error):pass
class IntegrityError(Error):pass
class MockTimeout(Error):pass
class MockAmbiguous(Error):pass
class MockAuth(Error):pass

@dataclass(frozen=True)
class Intent:
    experiment_id:str; content_id:str; content_version:str; destination_version:str
    def validate(self):
        for k,v in asdict(self).items():
            if not isinstance(v,str) or not v.strip() or SECRETISH.search(v): raise PrivacyError(f'unsafe {k}')
    @classmethod
    def from_dict(cls,d):
        if set(d)!={'experiment_id','content_id','content_version','destination_version'}: raise PrivacyError('intent fields must be sanitized identity only')
        x=cls(**d); x.validate(); return x

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def key(intent):
    intent.validate(); return hashlib.sha256(canon(asdict(intent)).encode()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()

class Backend(Protocol):
    def send(self,k:str,intent:Intent)->str:...
class Reconciler(Protocol):
    def reconcile(self,k:str,intent:Intent)->tuple[str,str|None]:...

class Store:
    def __init__(self,root=None):self.root=Path(root or os.environ.get(ENV_DIR,DEFAULT_DIR)).expanduser()
    def path(self,k):
        if not re.fullmatch(r'[0-9a-f]{64}',k):raise IntegrityError('invalid key')
        return self.root/f'{k}.json'
    def load(self,k):
        p=self.path(k)
        if not p.exists():return None
        r=json.loads(p.read_text(encoding='utf-8')); self.check(r,k); return r
    def save(self,r):
        k=r['publish_key']; self.check(r,k); self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        try:os.chmod(self.root,0o700)
        except OSError:pass
        fd,tmp=tempfile.mkstemp(prefix=f'.{k}.',suffix='.tmp',dir=self.root); os.fchmod(fd,0o600)
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(canon(r)+'\n');f.flush();os.fsync(f.fileno())
            os.replace(tmp,self.path(k)); os.chmod(self.path(k),0o600)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    def prepare(self,intent):
        k=key(intent); old=self.load(k)
        if old:
            if old['intent']!=asdict(intent):raise IntegrityError('key collision')
            return old
        t=now(); r={'schema_version':'mcme.publish-safety-latch.v1','publish_key':k,'intent':asdict(intent),'state':PREPARED,'attempt_count':0,'published_id_sanitized':None,'reconciliation_status':None,'created_at':t,'updated_at':t,'transition_history':[{'state':PREPARED,'at':t}]}; self.save(r); return r
    def transition(self,r,state,published_id=None,recon=None,increment_attempt=False):
        if state not in STATES or recon not in RECONS:raise IntegrityError('invalid transition metadata')
        x=json.loads(canon(r)); x['attempt_count']+=1 if increment_attempt else 0; x['state']=state
        if published_id is not None:
            if SECRETISH.search(published_id):raise PrivacyError('unsafe published id')
            x['published_id_sanitized']=published_id
        x['reconciliation_status']=recon; t=now(); x['updated_at']=t;x['transition_history'].append({'state':state,'at':t});self.save(x);return x
    def check(self,r,k):
        req={'schema_version','publish_key','intent','state','attempt_count','published_id_sanitized','reconciliation_status','created_at','updated_at','transition_history'}
        if set(r)!=req or r['schema_version']!='mcme.publish-safety-latch.v1' or r['publish_key']!=k:raise IntegrityError('invalid latch')
        i=Intent.from_dict(r['intent'])
        if key(i)!=k or r['state'] not in STATES or r['reconciliation_status'] not in RECONS or not isinstance(r['attempt_count'],int) or not 0<=r['attempt_count']<=MAX_SEND_ATTEMPTS:raise IntegrityError('corrupt latch')
        if r['published_id_sanitized'] and SECRETISH.search(r['published_id_sanitized']):raise PrivacyError('unsafe persisted id')

class MockBackend:
    def __init__(self,path,outcomes=None):self.path=Path(path);self.outcomes=list(outcomes or []); self.path.exists() or self._save({'send_count':0,'published':{}})
    def _load(self):return json.loads(self.path.read_text())
    def _save(self,s):self.path.parent.mkdir(parents=True,exist_ok=True);self.path.write_text(canon(s)+'\n')
    @property
    def send_count(self):return self._load()['send_count']
    def send(self,k,intent):
        del intent;s=self._load();s['send_count']+=1;o=self.outcomes.pop(0) if self.outcomes else 'success'
        if o in {'success','timeout_after_create'}:
            pid='MOCKPIN-'+k[:16];s['published'][k]=pid;self._save(s)
            if o=='timeout_after_create':raise MockTimeout()
            return pid
        self._save(s)
        if o=='timeout_no_create':raise MockTimeout()
        if o=='ambiguous_no_create':raise MockAmbiguous()
        if o=='auth_block':raise MockAuth()
        raise Error('confirmed mock failure')
    def published_id(self,k):return self._load()['published'].get(k)
class MockReconciler:
    def __init__(self,backend,overrides=None):self.backend=backend;self.overrides=dict(overrides or {});self.calls=0
    def reconcile(self,k,intent):
        del intent;self.calls+=1;o=self.overrides.get(k)
        if o in {UNKNOWN,AMBIGUOUS,ABSENT}:return o,None
        pid=self.backend.published_id(k);return (PRESENT,pid) if pid else (ABSENT,None)

class Machine:
    def __init__(self,store:Store,backend:Backend,reconciler:Reconciler):self.store=store;self.backend=backend;self.reconciler=reconciler
    def run(self,intent):
        r=self.store.prepare(intent)
        if r['state']==CONFIRMED or r['state'] in {BLOCKED_AUTH,FAILED_CONFIRMED}:return r
        if r['state'] in {SEND_STARTED,BLOCKED_AMBIGUOUS}:
            r=self.reconcile(r,intent)
            if r['state']!=PREPARED:return r
        if r['state']!=PREPARED:raise IntegrityError('unexpected runnable state')
        if r['attempt_count']>=MAX_SEND_ATTEMPTS:return self.store.transition(r,FAILED_CONFIRMED)
        r=self.store.transition(r,SEND_STARTED,increment_attempt=True)
        try:pid=self.backend.send(r['publish_key'],intent)
        except MockAuth:return self.store.transition(r,BLOCKED_AUTH)
        except (MockTimeout,MockAmbiguous):return self.store.transition(r,BLOCKED_AMBIGUOUS,recon=UNKNOWN)
        except Error:return self.store.transition(r,FAILED_CONFIRMED)
        return self.store.transition(r,CONFIRMED,published_id=pid,recon=PRESENT)
    def reconcile(self,r,intent):
        status,pid=self.reconciler.reconcile(r['publish_key'],intent)
        if status==PRESENT:
            if not pid:raise IntegrityError('present requires id')
            return self.store.transition(r,CONFIRMED,published_id=pid,recon=status)
        if status in {UNKNOWN,AMBIGUOUS}:return self.store.transition(r,BLOCKED_AMBIGUOUS,recon=status)
        if status==ABSENT:
            if r['attempt_count']>=MAX_SEND_ATTEMPTS:return self.store.transition(r,FAILED_CONFIRMED,recon=status)
            return self.store.transition(r,PREPARED,recon=status)
        raise IntegrityError('bad reconciliation result')

PublishIntent=Intent; LatchStore=Store; PublishSafetyMachine=Machine
RECON_CONFIRMED_PRESENT=PRESENT; RECON_CONFIRMED_ABSENT=ABSENT; RECON_UNKNOWN=UNKNOWN; RECON_AMBIGUOUS=AMBIGUOUS
STATE_PREPARED=PREPARED;STATE_SEND_STARTED=SEND_STARTED;STATE_CONFIRMED=CONFIRMED;STATE_BLOCKED_AUTH=BLOCKED_AUTH;STATE_BLOCKED_AMBIGUOUS=BLOCKED_AMBIGUOUS;STATE_FAILED_CONFIRMED=FAILED_CONFIRMED
PrivacyValidationError=PrivacyError

publish_key=key
