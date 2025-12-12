# PowerShell script for launching CloudPub tunnels
# Usage: .\start_tunnels.ps1

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "[>] Zapusk CloudPub tunneley dlya TGBot proekta" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

# Check CloudPub CLI installation
Write-Host "`n[*] Proverka CloudPub CLI..." -ForegroundColor Cyan

try {
    $cloVersion = clo --version 2>&1
    Write-Host "[OK] CloudPub CLI ustanovlen" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] CloudPub CLI ne ustanovlen!" -ForegroundColor Red
    Write-Host "`nUstanovite CloudPub CLI:" -ForegroundColor Yellow
    Write-Host "   1. Pereydite na https://cloudpub.ru"
    Write-Host "   2. Skachayte klient dlya Windows"
    Write-Host "   3. Ustanovite i dobavte v PATH"
    Write-Host "`nPodrobnaya instrukciya: sm. CLOUDPUB_SETUP.md"
    exit 1
}

# Check authorization
Write-Host "`n[*] Proverka avtorizacii..." -ForegroundColor Cyan

try {
    $cloOptions = clo options 2>&1
    if ($LASTEXITCODE -eq 0 -and $cloOptions -match "token") {
        Write-Host "[OK] Avtorizaciya proydena" -ForegroundColor Green
    } else {
        throw "Not authorized"
    }
} catch {
    Write-Host "[ERROR] Vy ne avtorizovany v CloudPub!" -ForegroundColor Red
    Write-Host "`nVypolnite avtorizaciyu:" -ForegroundColor Yellow
    Write-Host "   clo login"
    Write-Host "`nPodrobnaya instrukciya: sm. CLOUDPUB_SETUP.md"
    exit 1
}

# Launch tunnels
Write-Host "`n============================================================" -ForegroundColor Magenta
Write-Host "[*] Zapusk tunneley" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

# Register tunnels
Write-Host "`n[*] Registraciya tunneley..." -ForegroundColor Cyan

Write-Host "`n[1] Flask Dashboard (port 5000)" -ForegroundColor Yellow
clo register http 5000 2>&1

Write-Host "`n[2] Telegram Mini App (port 5001)" -ForegroundColor Yellow
clo register http 5001 2>&1

# Start all tunnels
Write-Host "`n============================================================" -ForegroundColor Magenta
Write-Host "[OK] Tunneli zaregistrirovany! Zapusk..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Magenta

Write-Host "`n[!] Vazhno:" -ForegroundColor Yellow
Write-Host "1. URL tunneley budut vyvedeny nizhe"
Write-Host "2. Dlya Mini App: skopiruyte URL i nastroyte v @BotFather"
Write-Host "3. Dlya ostanovki nazhmite Ctrl+C"
Write-Host "`n[i] Podrobnaya instrukciya: sm. CLOUDPUB_SETUP.md"

Write-Host "`n[...] Zapusk tunneley..." -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Gray

# Run
clo run
