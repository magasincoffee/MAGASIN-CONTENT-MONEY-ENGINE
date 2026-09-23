param(
    [int]$Port = 9222,
    [string]$StartUrl = "https://affiliate.shopee.vn/"
)

$ErrorActionPreference = "Stop"

function Test-Cdp {
    param([int]$CdpPort)
    try {
        Invoke-RestMethod -Uri "http://127.0.0.1:$CdpPort/json/version" -TimeoutSec 2 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

if (Test-Cdp -CdpPort $Port) {
    Write-Host "[CDP] Chrome already available on 127.0.0.1:$Port"
    exit 0
}

$programFilesX86 = [Environment]::GetEnvironmentVariable("ProgramFiles(x86)")
$chromeCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "$programFilesX86\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromeCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $chrome) {
    throw "Google Chrome not found."
}

$profileDir = Join-Path $env:LOCALAPPDATA "MAGASIN\ChromeRobot"
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null

Write-Host "[CDP] Starting dedicated MAGASIN Chrome profile."
Start-Process -FilePath $chrome -ArgumentList @(
    "--remote-debugging-port=$Port",
    "--remote-debugging-address=127.0.0.1",
    "--user-data-dir=$profileDir",
    "--no-first-run",
    "--no-default-browser-check",
    $StartUrl
)

for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-Cdp -CdpPort $Port) {
        Write-Host "[CDP] Ready on http://127.0.0.1:$Port"
        Write-Host "[PROFILE] $profileDir"
        exit 0
    }
}

throw "Chrome started but CDP did not become ready on port $Port."
