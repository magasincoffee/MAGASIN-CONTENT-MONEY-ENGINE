"""Offline/local Cash Truth V1 ledger. No external calls or state inference."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from jsonschema import Draft202012Validator

DEFAULT_LEDGER = Path.home()/'.mcme_private'/'cash_truth'/'ledger.jsonl'
ENV_LEDGER='MCME_CASH_TRUTH_LEDGER'
LIFECYCLE={'COMMISSION_PENDING':'PENDING','COMMISSION_VALIDATED':'VALIDATED','COMMISSION_REVERSED':'REVERSED','COMMISSION_PAYABLE':'PAYABLE','PAYOUT_ISSUED':'PAYOUT_ISSUED','CASH_SETTLED':'CASH_SETTLED'}
COMMISSION=set(k for k in LIFECYCLE if k.startswith('COMMISSION_'))
FORBIDDEN_KEYS=('password','passwd','secret','api_key','apikey','access_token','refresh_token','session_cookie','sessionid','otp','mfa','recovery_code','tax_id','ssn','tin','bank_account','account_number','routing_number','card_number','identity_document','private_tracking_token')
FORBIDDEN_VALUE=re.compile(r'(?i)(bearer\s+\S{8,}|(?:password|passwd|token|api[_-]?key|session(?:id)?|otp|mfa|tax[_-]?id|bank[_-]?account|routing[_-]?number|card[_-]?number)\s*[=:]\s*\S+)')

class CashTruthError(ValueError): pass
class SchemaValidationError(CashTruthError): pass
class SemanticValidationError(CashTruthError): pass
class PrivacyValidationError(CashTruthError): pass
class LedgerIntegrityError(CashTruthError): pass
class IdempotencyConflictError(CashTruthError): pass

@dataclass(frozen=True)
class AppendResult:
    status:str; event_id:str; identity_key:str|None; ledger_path:str; event_count:int; reason:str|None=None
    def as_dict(self): return {'status':self.status,'event_id':self.event_id,'identity_key':self.identity_key,'ledger_path':self.ledger_path,'event_count':self.event_count,'reason':self.reason}

def schema_path(): return Path(__file__).resolve().parents[2]/'mcme_cash_truth_v1.schema.json'
def ledger_path(): return Path(os.environ.get(ENV_LEDGER,str(DEFAULT_LEDGER))).expanduser()
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def walk(v,path=()):
    yield path,v
    if isinstance(v,dict):
        for k,x in v.items(): yield from walk(x,path+(str(k),))
    elif isinstance(v,list):
        for i,x in enumerate(v): yield from walk(x,path+(str(i),))

def privacy_check(e):
    for p,v in walk(e):
        if p and any(x in p[-1].lower() for x in FORBIDDEN_KEYS): raise PrivacyValidationError('.'.join(p))
        if isinstance(v,str) and FORBIDDEN_VALUE.search(v): raise PrivacyValidationError('.'.join(p))

def load_schema(path=None):
    with Path(path or schema_path()).open(encoding='utf-8') as f: s=json.load(f)
    Draft202012Validator.check_schema(s); return s

def validate(e,path=None):
    privacy_check(e); v=Draft202012Validator(load_schema(path),format_checker=Draft202012Validator.FORMAT_CHECKER)
    errs=sorted(v.iter_errors(e),key=lambda x:list(x.path))
    if errs: raise SchemaValidationError('; '.join(f"{'.'.join(map(str,x.path)) or '<root>'}: {x.message}" for x in errs[:8]))
    typ=e['event_type']; expected=LIFECYCLE.get(typ); supplied=e.get('canonical_money_state')
    if supplied is not None and expected and supplied!=expected: raise SemanticValidationError('canonical_money_state conflicts with event_type')
    if typ=='PAYOUT_ISSUED' and (e.get('settlement') or {}).get('funds_actually_received') is True: raise SemanticValidationError('PAYOUT_ISSUED is not CASH_SETTLED')
    if typ=='NEGATIVE_ADJUSTMENT_RECORDED' and Decimal(e['money']['amount_decimal'])>=0: raise SemanticValidationError('negative adjustment amount must be negative')
    if typ=='CASH_SETTLED':
        st=e.get('settlement') or {}; rec=e.get('reconciliation') or {}
        if e['source']['source_system']!='OWNER_PAYOUT_RAIL': raise SemanticValidationError('CASH_SETTLED requires OWNER_PAYOUT_RAIL')
        if e['evidence']['status']!='VERIFIED': raise SemanticValidationError('CASH_SETTLED requires VERIFIED evidence')
        if not all(st.get(k) is True for k in ('funds_actually_received','owner_authorized_payout_rail','reconciled_to_payout')): raise SemanticValidationError('CASH_SETTLED guards must all be true')
        if not st.get('payout_source_record_id_sanitized') and not (rec.get('status')=='MATCHED' and rec.get('related_event_ids')): raise SemanticValidationError('CASH_SETTLED requires payout reconciliation reference')

validate_event = validate

def scope(e): return {k:e.get(k) for k in ('experiment_id','content_id','pin_id','framing_id','network','merchant','program_id_sanitized','attribution')}
def identity(e):
    strat=e['idempotency']['strategy']; src=e['source']; sid=src.get('source_record_id_sanitized')
    base=[src['source_system'],e.get('network'),e.get('merchant'),e.get('program_id_sanitized'),sid,e['event_type']]
    if strat=='PROVIDER_STABLE_ID':
        if not sid: raise SemanticValidationError('stable ID strategy requires source_record_id_sanitized')
        return digest(base),'STABLE'
    if strat=='PROVIDER_STATE_VERSION':
        if not sid: raise SemanticValidationError('state version requires source_record_id_sanitized')
        ver=e['idempotency'].get('provider_effective_at') or src.get('provider_state_label_sanitized')
        if not ver: raise SemanticValidationError('state version requires provider state/effective time')
        return digest(base+[ver]),'STABLE'
    if strat=='AGGREGATE_SNAPSHOT_KEY':
        if not e.get('metric'): raise SemanticValidationError('snapshot strategy requires metric')
        return digest([src['source_system'],e['event_type'],scope(e),e['metric'],e['idempotency'].get('provider_effective_at'),e['observed_at']]),'SNAPSHOT'
    if strat=='CONSERVATIVE_RECONCILIATION':
        return digest([src['source_system'],e['event_type'],src.get('provider_state_label_sanitized'),scope(e),e.get('money'),e.get('metric'),e.get('adjustment'),e.get('occurred_at'),e['idempotency'].get('provider_effective_at')]),'CONSERVATIVE'
    if strat=='MANUAL_REVIEW': return None,'MANUAL'
    raise SemanticValidationError('unsupported idempotency strategy')

def normalize(e,path=None):
    x=copy.deepcopy(e); validate(x,path); key,kind=identity(x); given=x['idempotency'].get('key_sanitized')
    if given is not None and key is not None and given!=key: raise IdempotencyConflictError('supplied idempotency key mismatch')
    if key is not None: x['idempotency']['key_sanitized']=key
    validate(x,path); return x,key,kind

def semantic_payload(e): return {k:e.get(k) for k in ('event_type','network','merchant','program_id_sanitized','canonical_money_state','metric','money','adjustment','cost','time','settlement','reconciliation')}

def read_events(path,path_schema=None):
    p=Path(path)
    if not p.exists(): return []
    out=[]
    with p.open(encoding='utf-8') as f:
        for n,line in enumerate(f,1):
            if not line.strip(): raise LedgerIntegrityError(f'blank JSONL line {n}')
            try: e=json.loads(line)
            except json.JSONDecodeError as ex: raise LedgerIntegrityError(f'invalid JSONL line {n}: {ex}') from ex
            validate(e,path_schema); out.append(e)
    return out

class Ledger:
    def __init__(self,path=None,path_schema=None): self.path=Path(path or ledger_path()).expanduser(); self.schema=path_schema
    def events(self): return read_events(self.path,self.schema)
    def _res(self,status,eid,key,count,reason=None): return AppendResult(status,eid,key,str(self.path),count,reason)
    def append(self,e):
        x,key,kind=normalize(e,self.schema); old=self.events()
        same_id=[r for r in old if r['event_id']==x['event_id']]
        if same_id:
            if any(canon(r)==canon(x) for r in same_id): return self._res('DUPLICATE_EVENT_ID',x['event_id'],key,len(old))
            raise IdempotencyConflictError('event_id exists with different immutable payload')
        if kind=='MANUAL': return self._res('REQUIRES_RECONCILIATION',x['event_id'],None,len(old))
        matches=[r for r in old if r.get('idempotency',{}).get('key_sanitized')==key]
        if matches:
            if kind=='CONSERVATIVE' or any(semantic_payload(r)!=semantic_payload(x) for r in matches): return self._res('REQUIRES_RECONCILIATION',x['event_id'],key,len(old))
            return self._res('DUPLICATE_SOURCE_EVENT',x['event_id'],key,len(old))
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(self.path,os.O_APPEND|os.O_CREAT|os.O_WRONLY,0o600)
        try: os.write(fd,(canon(x)+'\n').encode()); os.fsync(fd)
        finally: os.close(fd)
        return self._res('APPENDED_CONSERVATIVE' if kind=='CONSERVATIVE' else 'APPENDED',x['event_id'],key,len(old)+1)
    def replay(self): return replay(self.events())

def money_add(bucket,e):
    if e.get('money') and e['evidence']['status']=='VERIFIED': bucket[e['money']['currency']]+=Decimal(e['money']['amount_decimal'])
def fmt(bucket): return {k:format(v,'f') for k,v in sorted(bucket.items())}

def replay(events):
    counts=Counter(e['event_type'] for e in events); pos=defaultdict(Decimal); neg=defaultdict(Decimal); cost=defaultdict(Decimal); reversals=defaultdict(Decimal); adjustments=defaultdict(lambda:defaultdict(Decimal)); time=Counter(); current={}; ungrouped=0
    for e in events:
        t=e['event_type']
        if t=='CASH_SETTLED' and e['evidence']['status']=='VERIFIED':
            amt=Decimal(e['money']['amount_decimal']); (pos if amt>=0 else neg)[e['money']['currency']]+=amt
        if t=='COST_RECORDED': money_add(cost,e)
        if t=='COMMISSION_REVERSED': money_add(reversals,e)
        if t=='NEGATIVE_ADJUSTMENT_RECORDED' and e['evidence']['status']=='VERIFIED': money_add(adjustments[(e.get('adjustment') or {}).get('scope') or 'UNSCOPED'],e)
        if t=='TIME_RECORDED' and e['evidence']['status']=='VERIFIED': time[e['time']['category']]+=e['time']['minutes']
        if t in COMMISSION:
            sid=e['source'].get('source_record_id_sanitized')
            if sid: current[(e['source']['source_system'],e.get('network') or '',e.get('merchant') or '',e.get('program_id_sanitized') or '',sid)]=e
            else: ungrouped+=1
    states={s:defaultdict(Decimal) for s in ('PENDING','VALIDATED','PAYABLE')}; reversed_count=0
    for e in current.values():
        st=LIFECYCLE[e['event_type']]
        if st=='REVERSED': reversed_count+=1
        elif st in states and e.get('money') and e['evidence']['status']=='VERIFIED': states[st][e['money']['currency']]+=Decimal(e['money']['amount_decimal'])
    currencies=set(pos)|set(neg); net=defaultdict(Decimal,{c:pos[c]+neg[c] for c in currencies}); nc=defaultdict(Decimal,{c:net[c]-cost[c] for c in set(net)|set(cost)})
    return {'event_count':len(events),'event_counts':dict(sorted(counts.items())),'commission_current_amounts':{k.lower():fmt(v) for k,v in states.items()},'commission_current_reversed_record_count':reversed_count,'commission_ungroupable_event_count':ungrouped,'reversal_amounts_as_recorded':fmt(reversals),'negative_adjustments':{k:fmt(v) for k,v in sorted(adjustments.items())},'settled_cash_positive':fmt(pos),'settled_cash_negative':fmt(neg),'net_settled_cash':fmt(net),'direct_cash_cost':fmt(cost),'net_cash_contribution':fmt(nc),'time_minutes':dict(sorted(time.items())),'time_minutes_total':sum(time.values()),'inference_policy':{'pending_to_validated':'NEVER_INFER','payable_to_payout_issued':'NEVER_INFER','payout_issued_to_cash_settled':'NEVER_INFER','time_to_cash_conversion':'NEVER_INFER'}}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--ledger',type=Path); p.add_argument('--schema',type=Path); sub=p.add_subparsers(dest='cmd',required=True); v=sub.add_parser('validate'); v.add_argument('event',type=Path); a=sub.add_parser('append'); a.add_argument('event',type=Path); sub.add_parser('replay'); args=p.parse_args()
    def load(path):
        with path.open(encoding='utf-8') as f:return json.load(f)
    if args.cmd=='validate': e=load(args.event); validate(e,args.schema); print(json.dumps({'status':'VALID','event_id':e['event_id']},indent=2)); return
    ledger=Ledger(args.ledger,args.schema)
    out=ledger.append(load(args.event)).as_dict() if args.cmd=='append' else ledger.replay(); print(json.dumps(out,indent=2,ensure_ascii=False))
CashTruthLedger = Ledger

if __name__=='__main__': main()
