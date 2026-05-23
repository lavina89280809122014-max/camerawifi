#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Серверная часть - запускается на компьютере
Слушает подключения телефонов и отправляет команды камере
"""

import socket
import json
import threading
import time
from datetime import datetime
from typing import Dict, List

class CameraServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients: Dict[str, socket.socket] = {}
        self.running = False
        self.commands_queue = []
        
    def start(self):
        """Запуск сервера"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🔧 Сервер запущен на {self.host}:{self.port}")
            print(f"📡 Ожидание подключений...")
            
            # Запускаем поток для принятия подключений
            accept_thread = threading.Thread(target=self._accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Главный цикл
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Ошибка сервера: {e}")
    
    def _accept_connections(self):
        """Принятие подключений от клиентов"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_id = f"{client_address[0]}:{client_address[1]}"
                self.clients[client_id] = client_socket
                
                print(f"\n✅ Новое подключение: {client_id}")
                print(f"📱 Всего устройств подключено: {len(self.clients)}")
                
                # Запускаем поток для этого клиента
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_id, client_socket)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"Ошибка при принятии подключения: {e}")
    
    def _handle_client(self, client_id: str, client_socket: socket.socket):
        """Обработка клиента"""
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                
                if not data:
                    break
                
                message = json.loads(data)
                self._process_message(client_id, message)
                
        except Exception as e:
            print(f"❌ Ошибка клиента {client_id}: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
                print(f"❌ Отключено: {client_id}")
                print(f"📱 Осталось устройств: {len(self.clients)}")
    
    def _process_message(self, client_id: str, message: dict):
        """Обработка сообщений от клиента"""
        msg_type = message.get('type')
        
        if msg_type == 'ping':
            response = {
                'type': 'pong',
                'timestamp': datetime.now().isoformat()
            }
            self.send_to_client(client_id, response)
            print(f"📡 Ping от {client_id}")
        
        elif msg_type == 'device_info':
            print(f"📱 Информация: {message.get('data')}")
            self.notify_user(f"Устройство подключено: {message.get('data', {}).get('model', 'Unknown')}")
        
        elif msg_type == 'photo_saved':
            print(f"📸 Фото сохранено: {message.get('data')}")
            self.notify_user(f"Фото сохранено: {message.get('data')}")
    
    def send_to_client(self, client_id: str, message: dict):
        """Отправка сообщения клиенту"""
        try:
            if client_id in self.clients:
                message_json = json.dumps(message)
                self.clients[client_id].sendall(message_json.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка отправки: {e}")
    
    def send_to_all(self, message: dict):
        """Отправка сообщения всем клиентам"""
        for client_id in self.clients:
            self.send_to_client(client_id, message)
    
    def notify_user(self, notification: str):
        """Уведомление пользователю"""
        print(f"\n🔔 {notification}")
    
    def send_command(self, client_id: str, command: str, data=None):
        """Отправка команды устройству"""
        message = {
            'type': 'command',
            'command': command,
            'data': data or {},
            'timestamp': datetime.now().isoformat()
        }
        self.send_to_client(client_id, message)
        print(f"📤 Команда отправлена на {client_id}: {command}")
    
    def list_devices(self):
        """Список подключённых устройств"""
        print("\n" + "="*50)
        print("📱 ПОДКЛЮЧЁННЫЕ УСТРОЙСТВА")
        print("="*50)
        if not self.clients:
            print("Нет подключённых устройств")
        else:
            for i, client_id in enumerate(self.clients, 1):
                print(f"{i}. {client_id}")
        print("="*50 + "\n")
        return list(self.clients.keys())
    
    def interactive_menu(self):
        """Интерактивное меню"""
        while self.running:
            print("\n" + "="*50)
            print("🎮 КОМАНДЫ УПРАВЛЕНИЯ")
            print("="*50)
            print("1. Список устройств")
            print("2. Отправить команду переключить камеру")
            print("3. Отправить команду сделать фото")
            print("4. Broadcast сообщение")
            print("5. Выход")
            print("="*50)
            
            choice = input("Выберите действие (1-5): ").strip()
            
            if choice == '1':
                self.list_devices()
            
            elif choice == '2':
                devices = self.list_devices()
                if devices:
                    device_num = input(f"Выберите номер устройства (1-{len(devices)}): ").strip()
                    try:
                        idx = int(device_num) - 1
                        if 0 <= idx < len(devices):
                            self.send_command(devices[idx], 'switch_camera')
                        else:
                            print("❌ Неверный номер")
                    except:
                        print("❌ Ошибка ввода")
            
            elif choice == '3':
                devices = self.list_devices()
                if devices:
                    device_num = input(f"Выберите номер устройства (1-{len(devices)}): ").strip()
                    try:
                        idx = int(device_num) - 1
                        if 0 <= idx < len(devices):
                            self.send_command(devices[idx], 'take_photo')
                        else:
                            print("❌ Неверный номер")
                    except:
                        print("❌ Ошибка ввода")
            
            elif choice == '4':
                message_text = input("Введите сообщение: ").strip()
                if message_text:
                    self.send_to_all({
                        'type': 'notification',
                        'message': message_text
                    })
            
            elif choice == '5':
                self.stop()
                break
            
            else:
                print("❌ Неверный выбор")
    
    def stop(self):
        """Остановка сервера"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("\n🛑 Сервер остановлен")


def get_local_ip():
    """Получение локального IP адреса"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🖥️  СЕРВЕР КАМЕР - КОМПЬЮТЕРНАЯ ЧАСТЬ")
    print("="*50)
    
    local_ip = get_local_ip()
    port = 5555
    
    print(f"IP адрес: {local_ip}")
    print(f"Порт: {port}")
    print(f"Адрес для подключения: {local_ip}:{port}")
    print("="*50 + "\n")
    
    server = CameraServer(host='0.0.0.0', port=port)
    
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    # Интерактивное меню в главном потоке
    try:
        server.interactive_menu()
    except KeyboardInterrupt:
        print("\n\n🛑 Выключение сервера...")
        server.stop()
