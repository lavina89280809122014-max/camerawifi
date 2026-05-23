#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки всей системы
"""

import socket
import json
import sys
import os
from datetime import datetime

def print_header(text):
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def test_python_version():
    """Проверка версии Python"""
    print_header("✓ ПРОВЕРКА PYTHON")
    version = sys.version.split()[0]
    print(f"Python версия: {version}")
    if int(version.split('.')[0]) >= 3:
        print("✅ Python 3 установлен")
        return True
    else:
        print("❌ Нужен Python 3+")
        return False

def test_kivy():
    """Проверка Kivy"""
    print_header("✓ ПРОВЕРКА KIVY")
    try:
        import kivy
        print(f"Kivy версия: {kivy.__version__}")
        print("✅ Kivy установлен")
        return True
    except ImportError:
        print("❌ Kivy не установлен")
        print("   Установите: pip install kivy")
        return False

def test_socket():
    """Проверка сокетов"""
    print_header("✓ ПРОВЕРКА СОКЕТОВ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.close()
        print(f"✅ Сокеты работают (тестовый порт: {port})")
        return True
    except Exception as e:
        print(f"❌ Ошибка сокетов: {e}")
        return False

def test_network():
    """Проверка сети"""
    print_header("✓ ПРОВЕРКА СЕТИ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"✅ Локальный IP: {ip}")
        return True
    except Exception as e:
        print(f"❌ Нет доступа в сеть: {e}")
        return False

def test_server_files():
    """Проверка файлов"""
    print_header("✓ ПРОВЕРКА ФАЙЛОВ")
    files = ['server.py', 'client.py']
    all_ok = True
    for f in files:
        if os.path.exists(f):
            print(f"✅ {f} найден")
        else:
            print(f"❌ {f} НЕ найден")
            all_ok = False
    return all_ok

def test_json():
    """Проверка JSON"""
    print_header("✓ ПРОВЕРКА JSON")
    try:
        test_data = {
            'type': 'test',
            'timestamp': datetime.now().isoformat()
        }
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        print(f"✅ JSON работает")
        print(f"   Тест: {parsed}")
        return True
    except Exception as e:
        print(f"❌ Ошибка JSON: {e}")
        return False

def test_threading():
    """Проверка многопоточности"""
    print_header("✓ ПРОВЕРКА МНОГОПОТОЧНОСТИ")
    try:
        import threading
        def thread_test():
            return "OK"
        
        t = threading.Thread(target=thread_test)
        t.start()
        t.join(timeout=5)
        print("✅ Threading работает")
        return True
    except Exception as e:
        print(f"❌ Ошибка threading: {e}")
        return False

def simulate_connection():
    """Симуляция подключения"""
    print_header("✓ СИМУЛЯЦИЯ ПОДКЛЮЧЕНИЯ")
    try:
        # Создаем тестовый сервер
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 9999))
        server.listen(1)
        server.settimeout(2)
        
        print("✅ Сервер создан на localhost:9999")
        
        # Пытаемся подключиться
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 9999))
            print("✅ Клиент подключился успешно")
            
            # Отправляем тестовое сообщение
            test_msg = json.dumps({'type': 'test', 'data': 'hello'})
            client.sendall(test_msg.encode('utf-8'))
            print(f"✅ Сообщение отправлено: {test_msg}")
            
            client.close()
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False
        finally:
            server.close()
        
        return True
    except Exception as e:
        print(f"❌ Ошибка симуляции: {e}")
        return False

def main():
    """Главная функция"""
    print("\n" + "╔" + "="*48 + "╗")
    print("║" + " "*10 + "🔍 ПОЛНАЯ ПРОВЕРКА СИСТЕМЫ" + " "*12 + "║")
    print("╚" + "="*48 + "╝")
    
    results = []
    
    results.append(("Python версия", test_python_version()))
    results.append(("Kivy библиотека", test_kivy()))
    results.append(("Сокеты", test_socket()))
    results.append(("Сеть", test_network()))
    results.append(("Файлы проекта", test_server_files()))
    results.append(("JSON", test_json()))
    results.append(("Threading", test_threading()))
    results.append(("Симуляция подключения", simulate_connection()))
    
    # Итоги
    print_header("📊 ИТОГИ ПРОВЕРКИ")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print()
    print(f"Результат: {passed}/{total} тестов пройдено")
    print()
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("\n✅ СИСТЕМА ГОТОВА К РАБОТЕ")
        print("\nДалее:")
        print("  1. Запустите: python server.py")
        print("  2. Установите приложение на телефон")
        print("  3. Подключитесь с телефона")
        return 0
    else:
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ")
        print("\nОшибки выше помечены ❌")
        print("Установите необходимые компоненты и повторите тест")
        return 1

if __name__ == '__main__':
    sys.exit(main())
