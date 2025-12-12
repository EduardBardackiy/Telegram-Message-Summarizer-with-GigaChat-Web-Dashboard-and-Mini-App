"""
Скрипт для запуска CloudPub туннелей через Python SDK
Использует библиотеку cloudpub-python-sdk вместо CLI
Установка: pip install cloudpub-python-sdk
"""
import os
import sys
import time
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

def check_cloudpub_sdk():
    """Проверка установки CloudPub Python SDK"""
    try:
        import cloudpub_python_sdk
        return True
    except ImportError:
        return False

def main():
    """Главная функция"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🚀 Запуск CloudPub туннелей через Python SDK", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    # Проверка установки SDK
    print_colored("\n📦 Проверка CloudPub Python SDK...", Colors.OKCYAN)
    if not check_cloudpub_sdk():
        print_colored("❌ CloudPub Python SDK не установлен!", Colors.FAIL)
        print_colored("\nУстановите CloudPub Python SDK:", Colors.WARNING)
        print("   pip install cloudpub-python-sdk")
        print("\nПодробная инструкция: см. CLOUDPUB_SETUP.md")
        print("Документация SDK: https://cloudpub.ru/docs/python-sdk/")
        sys.exit(1)
    
    print_colored("✅ CloudPub Python SDK установлен", Colors.OKGREEN)
    
    # Импорт после проверки
    from cloudpub_python_sdk import Connection, Protocol, Auth, CloudPubError
    
    # Получение credentials
    print_colored("\n🔐 Получение учетных данных...", Colors.OKCYAN)
    
    # Попытка загрузить из .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        email = os.getenv('CLOUDPUB_EMAIL')
        password = os.getenv('CLOUDPUB_PASSWORD')
    except:
        email = None
        password = None
    
    # Если нет в .env, запрашиваем
    if not email or not password:
        print_colored("⚠️  Учетные данные CloudPub не найдены в .env", Colors.WARNING)
        print("\nДобавьте в файл .env:")
        print("CLOUDPUB_EMAIL=ваш_email@example.com")
        print("CLOUDPUB_PASSWORD=ваш_пароль")
        print("\nИли введите сейчас:")
        
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        if not email or not password:
            print_colored("❌ Не введены учетные данные", Colors.FAIL)
            sys.exit(1)
    
    print_colored("✅ Учетные данные получены", Colors.OKGREEN)
    
    # Подключение к CloudPub
    print_colored("\n" + "=" * 60, Colors.HEADER)
    print_colored("🌐 Подключение к CloudPub", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    try:
        print_colored("\n🔄 Создание соединения...", Colors.OKCYAN)
        conn = Connection(
            email=email,
            password=password,
            log_level="info",
            verbose=False
        )
        print_colored("✅ Успешно подключено к CloudPub!", Colors.OKGREEN)
    except CloudPubError as e:
        print_colored(f"❌ Ошибка подключения: {e}", Colors.FAIL)
        print_colored("\nПроверьте:", Colors.WARNING)
        print("1. Правильность email и пароля")
        print("2. Подключение к интернету")
        print("3. https://cloudpub.ru доступен")
        sys.exit(1)
    
    # Публикация туннелей
    print_colored("\n" + "=" * 60, Colors.HEADER)
    print_colored("📡 Публикация туннелей", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    endpoints = []
    
    try:
        # Flask Dashboard (порт 5000)
        print_colored("\n🔄 Публикация Flask Dashboard (порт 5000)...", Colors.OKCYAN)
        flask_endpoint = conn.publish(
            Protocol.HTTP,
            "localhost:5000",
            name="Flask Dashboard - TGBot",
            auth=Auth.NONE
        )
        endpoints.append(('Flask Dashboard', flask_endpoint))
        print_colored(f"✅ Flask Dashboard: {flask_endpoint.url}", Colors.OKGREEN)
        
        # Telegram Mini App (порт 5001)
        print_colored("\n🔄 Публикация Telegram Mini App (порт 5001)...", Colors.OKCYAN)
        miniapp_endpoint = conn.publish(
            Protocol.HTTP,
            "localhost:5001",
            name="Telegram Mini App - TGBot",
            auth=Auth.NONE
        )
        endpoints.append(('Telegram Mini App', miniapp_endpoint))
        print_colored(f"✅ Telegram Mini App: {miniapp_endpoint.url}", Colors.OKGREEN)
        
    except CloudPubError as e:
        print_colored(f"\n❌ Ошибка публикации: {e}", Colors.FAIL)
        print_colored("\nПроверьте:", Colors.WARNING)
        print("1. Flask и Mini App запущены (порты 5000 и 5001)")
        print("2. Порты не заняты другими приложениями")
        # Очистка уже созданных туннелей
        for name, ep in endpoints:
            try:
                conn.unpublish(ep.guid)
            except:
                pass
        sys.exit(1)
    
    # Информация
    print_colored("\n" + "=" * 60, Colors.HEADER)
    print_colored("✅ Туннели успешно запущены!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.HEADER)
    
    print_colored("\n📋 Активные туннели:", Colors.OKCYAN)
    for i, (name, endpoint) in enumerate(endpoints, 1):
        print(f"{i}. {Colors.BOLD}{name}{Colors.ENDC}")
        print(f"   URL: {Colors.OKBLUE}{endpoint.url}{Colors.ENDC}")
        print(f"   GUID: {endpoint.guid}")
        print()
    
    print_colored("📝 Важно:", Colors.WARNING)
    print("1. Для Mini App: скопируйте URL Mini App и настройте в @BotFather")
    print("2. @BotFather → /mybots → выберите бота → Bot Settings → Menu Button")
    print("3. Edit Menu Button URL → вставьте URL Mini App")
    print("\n4. Flask Dashboard доступен по первому URL")
    print("\n5. Для остановки нажмите Ctrl+C")
    
    print_colored("\n📖 Подробная инструкция: см. CLOUDPUB_SETUP.md", Colors.OKBLUE)
    
    # Ожидание
    try:
        print_colored("\n⏳ Туннели работают. Нажмите Ctrl+C для остановки...", Colors.OKCYAN)
        print_colored("─" * 60, Colors.OKCYAN)
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print_colored("\n\n🛑 Остановка туннелей...", Colors.WARNING)
        
        # Очистка
        for name, endpoint in endpoints:
            try:
                print_colored(f"   Остановка: {name}...", Colors.OKBLUE)
                conn.unpublish(endpoint.guid)
                print_colored(f"   ✅ Остановлен: {name}", Colors.OKGREEN)
            except Exception as e:
                print_colored(f"   ⚠️  Ошибка при остановке {name}: {e}", Colors.WARNING)
        
        print_colored("\n✅ Все туннели остановлены", Colors.OKGREEN)
        print_colored("До свидания! 👋", Colors.OKCYAN)

if __name__ == "__main__":
    main()

