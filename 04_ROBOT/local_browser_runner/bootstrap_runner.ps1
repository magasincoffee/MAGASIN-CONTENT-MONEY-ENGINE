param(
    [string]$Repository = "magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE",
    [string]$RunnerName = "MAGASIN-DELL",
    [string]$RunnerRoot = "C:\MAGASIN\github-runner",
    [string]$Label = "magasin-browser"
)

$ErrorActionPreference = "Stop"

function Ensure-Command {
    param(
        [string]$Name,
        [string]$WingetId
    )

    if (Get-Command $Name -ErrorAction SilentlyContinue) {
        return
    }

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "$Name is missing and winget is unavailable. Install $Name, then rerun."
    }

    Write-Host "[INSTALL] $Name"
    winget install --id $WingetId -e --source winget --accept-package-agreements --accept-source-agreements
}

Ensure-Command -Name "gh" -WingetId "GitHub.cli"
Ensure-Command -Name "py" -WingetId "Python.Python.3.12"

$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [Environment]::GetEnvironmentVariable("Path", "User")

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI was installed but is not available in PATH yet. Reopen PowerShell and rerun this script."
}

gh auth status --hostname github.com *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[OWNER ACTION] GitHub authentication is required once."
    Write-Host "A browser window may open. Complete GitHub login yourself."
    gh auth login --hostname github.com --web --git-protocol https
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub authentication did not complete."
    }
}

Write-Host "[TOKEN] Requesting short-lived repo-scoped runner registration token."
$token = gh api --method POST "repos/$Repository/actions/runners/registration-token" --jq ".token"
if (-not $token) {
    throw "Could not obtain a runner registration token. The GitHub account must have admin access to the repository."
}

$tag = gh api "repos/actions/runner/releases/latest" --jq ".tag_name"
if (-not $tag) {
    throw "Could not resolve latest GitHub Actions runner release."
}

$version = $tag.TrimStart("v")
$downloadUrl = "https://github.com/actions/runner/releases/download/$tag/actions-runner-win-x64-$version.zip"

New-Item -ItemType Directory -Force -Path $RunnerRoot | Out-Null
$zipPath = Join-Path $env:TEMP "actions-runner-win-x64-$version.zip"

if (-not (Test-Path (Join-Path $RunnerRoot "config.cmd"))) {
    Write-Host "[DOWNLOAD] GitHub Actions runner $tag"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $RunnerRoot -Force
}

Push-Location $RunnerRoot
try {
    if (-not (Test-Path ".runner")) {
        Write-Host "[CONFIG] Registering repo-scoped runner."
        & ".\config.cmd" --unattended --url "https://github.com/$Repository" --token $token --name $RunnerName --labels $Label --work "_work" --replace

        if ($LASTEXITCODE -ne 0) {
            throw "Runner registration failed."
        }
    }
    else {
        Write-Host "[CONFIG] Existing runner configuration detected. Reusing it."
    }
}
finally {
    Pop-Location
}

$startup = [Environment]::GetFolderPath("Startup")
$startupCmd = Join-Path $startup "MAGASIN-GitHub-Runner.cmd"
$runnerCmd = Join-Path $RunnerRoot "run.cmd"
@"
@echo off
cd /d "$RunnerRoot"
call "$runnerCmd"
"@ | Set-Content -Path $startupCmd -Encoding ASCII

$programFilesX86 = [Environment]::GetEnvironmentVariable("ProgramFiles(x86)")
$chromeCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "$programFilesX86\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $chrome) {
    throw "Google Chrome was not found. Install Chrome, then rerun."
}

$chromeProfile = Join-Path $env:LOCALAPPDATA "MAGASIN\ChromeRobot"
New-Item -ItemType Directory -Force -Path $chromeProfile | Out-Null

$debugOnline = $false
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 2 | Out-Null
    $debugOnline = $true
}
catch {
    $debugOnline = $false
}

if (-not $debugOnline) {
    Write-Host "[CHROME] Starting dedicated MAGASIN Chrome profile on local-only CDP port 9222."
    Start-Process -FilePath $chrome -ArgumentList @(
        "--remote-debugging-port=9222",
        "--remote-debugging-address=127.0.0.1",
        "--user-data-dir=$chromeProfile",
        "--no-first-run",
        "--no-default-browser-check",
        "https://affiliate.shopee.vn/"
    )
}

Write-Host "[RUNNER] Starting self-hosted runner in the logged-in Windows desktop session."
if (-not (Get-Process -Name "Runner.Listener" -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", "`"$runnerCmd`"") -WindowStyle Minimized
}

Write-Host ""
Write-Host "SETUP COMPLETE"
Write-Host "Runner label : $Label"
Write-Host "Runner root  : $RunnerRoot"
Write-Host "Chrome profile: $chromeProfile"
Write-Host ""
Write-Host "One-time Owner action:"
Write-Host "  In the dedicated Chrome window, log in to Shopee Affiliate and complete OTP/MFA/CAPTCHA yourself if requested."
Write-Host "  Keep that profile; future robot jobs reuse the authenticated local session."
Write-Host ""
Write-Host "Security:"
Write-Host "  - Runner is scoped to this repository."
Write-Host "  - Browser CDP binds only to 127.0.0.1."
Write-Host "  - No cookie/password/token export is implemented."
Write-Host "  - Workflow accepts only coded allowlisted actions, not arbitrary shell commands."
