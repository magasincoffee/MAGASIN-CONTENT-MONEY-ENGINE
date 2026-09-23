param(
    [Parameter(Mandatory = $true)]
    [string]$CommandFile
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$EvidenceDir = Join-Path $Root "evidence"
$VenvRoot = Join-Path $env:LOCALAPPDATA "MAGASIN\RunnerVenv"
$Python = Join-Path $VenvRoot "Scripts\python.exe"

& (Join-Path $Root "start_robot_chrome.ps1")
if ($LASTEXITCODE -ne 0) {
    throw "Dedicated Chrome/CDP could not be started."
}

if (-not (Test-Path $Python)) {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
        throw "Python launcher 'py' is missing. Run bootstrap_runner.ps1 first."
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $VenvRoot -Parent) | Out-Null
    py -3 -m venv $VenvRoot
}

& $Python -m pip install --disable-pip-version-check --quiet "playwright>=1.45,<2"
if ($LASTEXITCODE -ne 0) {
    throw "Could not install Playwright Python package."
}

if (Test-Path $EvidenceDir) {
    Remove-Item -Recurse -Force $EvidenceDir
}
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

& $Python (Join-Path $Root "runner.py") --command-file $CommandFile --evidence-dir $EvidenceDir

$code = $LASTEXITCODE
Write-Host "[RESULT] Browser robot exit code: $code"
exit $code
