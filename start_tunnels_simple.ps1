# PowerShell скрипт для запуска CloudPub туннелей
# Использование: .\start_tunnels_simple.ps1
# Кодировка: UTF-8 with BOM

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "Запуск CloudPub туннелей для TGBot проекта" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

# Проверка установки CloudPub CLI
Write-Host ""
Write-Host "Проверка CloudPub CLI..." -ForegroundColor Cyan

try {
    $cloVersion = clo --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] CloudPub CLI установлен" -ForegroundColor Green
    } else {
        throw "CloudPub not found"
    }
} catch {
    Write-Host "[ОШИБКА] CloudPub CLI не установлен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Установите CloudPub CLI:" -ForegroundColor Yellow
    Write-Host "  1. Перейдите на https://cloudpub.ru"
    Write-Host "  2. Скачайте клиент для Windows"
    Write-Host "  3. Установите и добавьте в PATH"
    Write-Host ""
    Write-Host "Подробная инструкция: CLOUDPUB_SETUP.md" -ForegroundColor Yellow
    exit 1
}

# Проверка авторизации
Write-Host ""
Write-Host "Проверка авторизации..." -ForegroundColor Cyan

try {
    $cloOptions = clo options 2>&1
    if ($LASTEXITCODE -eq 0 -and $cloOptions -match "token") {
        Write-Host "[OK] Авторизация пройдена" -ForegroundColor Green
    } else {
        throw "Not authorized"
    }
} catch {
    Write-Host "[ОШИБКА] Вы не авторизованы в CloudPub!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Выполните авторизацию:" -ForegroundColor Yellow
    Write-Host "  clo login"
    Write-Host ""
    Write-Host "Подробная инструкция: CLOUDPUB_SETUP.md" -ForegroundColor Yellow
    exit 1
}

# Запуск туннелей
Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "Запуск туннелей" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta

# Регистрация туннелей
Write-Host ""
Write-Host "Регистрация туннелей..." -ForegroundColor Cyan
Write-Host ""

Write-Host "[1] Flask Dashboard (порт 5000)" -ForegroundColor Yellow
clo register http 5000 2>&1

Write-Host ""
Write-Host "[2] Telegram Mini App (порт 5001)" -ForegroundColor Yellow
clo register http 5001 2>&1

# Запуск всех туннелей
Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "[OK] Туннели зарегистрированы! Запуск..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Magenta

Write-Host ""
Write-Host "ВАЖНО:" -ForegroundColor Yellow
Write-Host "  1. URL туннелей будут выведены ниже"
Write-Host "  2. Для Mini App: скопируйте URL и настройте в @BotFather"
Write-Host "  3. Для остановки нажмите Ctrl+C"
Write-Host ""
Write-Host "Подробная инструкция: CLOUDPUB_SETUP.md" -ForegroundColor Cyan

Write-Host ""
Write-Host "Запуск туннелей..." -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Gray
Write-Host ""

# Запуск
clo run

