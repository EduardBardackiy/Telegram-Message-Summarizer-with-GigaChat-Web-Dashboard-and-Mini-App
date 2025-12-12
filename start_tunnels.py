"""
Скрипт для запуска CloudPub туннелей для Flask и Mini App
Требует установки: pip install cloudpub
"""
import os
import sys
import time
import subprocess
from pathlib import Path

# Цвета для красивого вывода
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color):
    """Вывод цветного текста"""
    print(f"{color}{text}{Colors.ENDC}")

def check_cloudpub_installed():
    """Проверка установки CloudPub CLI"""
    try:
        result = subprocess.run(['clo', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_cloudpub_auth():
    """Проверка авторизации в CloudPub"""
    try:
        result = subprocess.run(['clo', 'options'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return 'token' in result.stdout.lower() and result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def start_tunnel(port, name):
    """Запуск туннеля для указанного порта"""
    print_colored(f"\n🔄 Запуск туннеля для {name} (порт {port})...", Colors.OKCYAN)
    
    try:
        # Запуск туннеля
        process = subprocess.Popen(
            ['clo', 'publish', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного, чтобы получить URL
        time.sleep(3)
        
        # Проверяем, что процесс запустился
        if process.poll() is None:
            print_colored(f"✅ Туннель для {name} запущен!", Colors.OKGREEN)
            print_colored(f"   Порт: {port}", Colors.OKBLUE)
            print_colored(f"   Проверьте вывод команды для получения URL", Colors.WARNING)
            return process
        else:
            stdout, stderr = process.communicate()
            print_colored(f"❌ Ошибка запуска туннеля для {name}", Colors.FAIL)
            if stderr:
                print(f"   Ошибка: {stderr}")
            return None
            
    except Exception as e:
        print_colored(f"❌ Ошибка: {e}", Colors.FAIL)
        return None

def main():
    """Главная функция"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🚀 Запуск CloudPub туннелей для TGBot проекта", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    # Проверка установки CloudPub
    print_colored("\n📦 Проверка CloudPub CLI...", Colors.OKCYAN)
    if not check_cloudpub_installed():
        print_colored("❌ CloudPub CLI не установлен!", Colors.FAIL)
        print_colored("\nУстановите CloudPub CLI:", Colors.WARNING)
        print("   1. Перейдите на https://cloudpub.ru")
        print("   2. Скачайте клиент для вашей ОС")
        print("   3. Установите и добавьте в PATH")
        print("\nПодробная инструкция: см. CLOUDPUB_SETUP.md")
        sys.exit(1)
    
    print_colored("✅ CloudPub CLI установлен", Colors.OKGREEN)
    
    # Проверка авторизации
    print_colored("\n🔐 Проверка авторизации...", Colors.OKCYAN)
    if not check_cloudpub_auth():
        print_colored("❌ Вы не авторизованы в CloudPub!", Colors.FAIL)
        print_colored("\nВыполните авторизацию:", Colors.WARNING)
        print("   clo login")
        print("\nПодробная инструкция: см. CLOUDPUB_SETUP.md")
        sys.exit(1)
    
    print_colored("✅ Авторизация пройдена", Colors.OKGREEN)
    
    # Запуск туннелей
    print_colored("\n" + "=" * 60, Colors.HEADER)
    print_colored("🌐 Запуск туннелей", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    tunnels = []
    
    # Flask Dashboard (порт 5000)
    flask_process = start_tunnel(5000, "Flask Dashboard")
    if flask_process:
        tunnels.append(('Flask Dashboard', flask_process))
    
    # Mini App (порт 5001)
    miniapp_process = start_tunnel(5001, "Telegram Mini App")
    if miniapp_process:
        tunnels.append(('Mini App', miniapp_process))
    
    if not tunnels:
        print_colored("\n❌ Не удалось запустить ни одного туннеля", Colors.FAIL)
        sys.exit(1)
    
    # Информация
    print_colored("\n" + "=" * 60, Colors.HEADER)
    print_colored("✅ Туннели запущены!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.HEADER)
    print_colored("\n📝 Важно:", Colors.WARNING)
    print("1. URL туннелей выведены выше")
    print("2. Для Mini App: скопируйте URL и настройте в @BotFather")
    print("3. Для остановки нажмите Ctrl+C")
    print("\n📖 Подробная инструкция: см. CLOUDPUB_SETUP.md")
    
    # Ожидание
    try:
        print_colored("\n⏳ Туннели работают. Нажмите Ctrl+C для остановки...", Colors.OKCYAN)
        while True:
            time.sleep(1)
            # Проверяем, что процессы еще живы
            for name, proc in tunnels:
                if proc.poll() is not None:
                    print_colored(f"\n⚠️  Туннель {name} остановился!", Colors.WARNING)
                    tunnels.remove((name, proc))
            
            if not tunnels:
                print_colored("\n❌ Все туннели остановились", Colors.FAIL)
                break
                
    except KeyboardInterrupt:
        print_colored("\n\n🛑 Остановка туннелей...", Colors.WARNING)
        for name, proc in tunnels:
            proc.terminate()
            print_colored(f"   Остановлен: {name}", Colors.OKBLUE)
        print_colored("\n✅ Все туннели остановлены", Colors.OKGREEN)

if __name__ == "__main__":
    main()

