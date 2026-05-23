#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мобильное приложение - запускается на телефоне
Подключается к серверу и управляет камерой
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import socket
import json
import threading
import time
import os
from datetime import datetime

# Размер для эмулятора
Window.size = (480, 800)


class CameraClient:
    """Клиент для подключения к серверу"""
    
    def __init__(self, callback):
        self.socket = None
        self.connected = False
        self.callback = callback
        self.receive_thread = None
        self.running = False
    
    def connect(self, host: str, port: int):
        """Подключение к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            self.running = True
            
            # Запускаем поток для получения сообщений
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            # Отправляем информацию об устройстве
            self.send_message({
                'type': 'device_info',
                'data': {
                    'model': 'Android Phone',
                    'timestamp': datetime.now().isoformat()
                }
            })
            
            return True
        except Exception as e:
            self.connected = False
            self.callback('error', f'Ошибка подключения: {str(e)}')
            return False
    
    def disconnect(self):
        """Отключение от сервера"""
        self.running = False
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def send_message(self, message: dict):
        """Отправка сообщения серверу"""
        try:
            if self.connected and self.socket:
                message_json = json.dumps(message)
                self.socket.sendall(message_json.encode('utf-8'))
        except Exception as e:
            self.callback('error', f'Ошибка отправки: {str(e)}')
    
    def _receive_messages(self):
        """Получение сообщений от сервера"""
        while self.running and self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    self.callback('message', message)
                else:
                    self.disconnect()
            except Exception as e:
                if self.running:
                    self.callback('error', f'Ошибка получения: {str(e)}')
                break


class MobileCamera(App):
    """Основное мобильное приложение"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.using_back_camera = True
        self.title = "📷 Камера WiFi"
        self.client = CameraClient(self.on_client_message)
        self.connection_status = "Отключено"
        self.status_label = None
        self.camera_widget = None
    
    def build(self):
        """Построение интерфейса"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ==================== БЛОК ПОДКЛЮЧЕНИЯ ====================
        connection_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.25,
            spacing=10,
            padding=10
        )
        
        # Заголовок
        title_label = Label(
            text='🌐 Подключение к серверу',
            size_hint_y=0.2,
            bold=True,
            font_size='16sp'
        )
        connection_layout.add_widget(title_label)
        
        # Поле для IP адреса
        ip_layout = BoxLayout(size_hint_y=0.3, spacing=5)
        ip_layout.add_widget(Label(text='IP:', size_hint_x=0.15))
        self.ip_input = TextInput(
            text='192.168.1.100',
            multiline=False,
            size_hint_x=0.85,
            background_color=(0.9, 0.9, 0.9, 1)
        )
        ip_layout.add_widget(self.ip_input)
        connection_layout.add_widget(ip_layout)
        
        # Поле для порта
        port_layout = BoxLayout(size_hint_y=0.3, spacing=5)
        port_layout.add_widget(Label(text='Порт:', size_hint_x=0.15))
        self.port_input = TextInput(
            text='5555',
            multiline=False,
            size_hint_x=0.85,
            input_filter='int',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        port_layout.add_widget(self.port_input)
        connection_layout.add_widget(port_layout)
        
        # Кнопки подключения
        button_layout = BoxLayout(size_hint_y=0.3, spacing=5)
        
        self.connect_btn = Button(
            text='✅ Подключить',
            background_color=(0.2, 0.8, 0.4, 1)
        )
        self.connect_btn.bind(on_press=self.connect_to_server)
        button_layout.add_widget(self.connect_btn)
        
        self.disconnect_btn = Button(
            text='❌ Отключить',
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True
        )
        self.disconnect_btn.bind(on_press=self.disconnect_from_server)
        button_layout.add_widget(self.disconnect_btn)
        
        connection_layout.add_widget(button_layout)
        
        main_layout.add_widget(connection_layout)
        
        # ==================== СТАТУС ====================
        self.status_label = Label(
            text='🔴 Статус: Отключено',
            size_hint_y=0.08,
            bold=True,
            color=(1, 0, 0, 1),
            font_size='14sp'
        )
        main_layout.add_widget(self.status_label)
        
        # ==================== КАМЕРА ====================
        self.camera_widget = Camera(
            resolution=(640, 480),
            play=True
        )
        main_layout.add_widget(self.camera_widget)
        
        # ==================== УПРАВЛЕНИЕ ====================
        control_layout = BoxLayout(
            size_hint_y=0.2,
            spacing=10,
            padding=10,
            orientation='vertical'
        )
        
        # Кнопки управления камерой
        camera_buttons_layout = BoxLayout(spacing=10, size_hint_y=0.5)
        
        switch_btn = Button(
            text='🔄 Переключить',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        switch_btn.bind(on_press=self.switch_camera)
        camera_buttons_layout.add_widget(switch_btn)
        
        photo_btn = Button(
            text='📸 Фото',
            background_color=(0.2, 0.8, 0.4, 1)
        )
        photo_btn.bind(on_press=self.take_photo)
        camera_buttons_layout.add_widget(photo_btn)
        
        control_layout.add_widget(camera_buttons_layout)
        
        # Кнопка выхода
        exit_btn = Button(
            text='✕ Выход',
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_y=0.5
        )
        exit_btn.bind(on_press=self.stop)
        control_layout.add_widget(exit_btn)
        
        main_layout.add_widget(control_layout)
        
        return main_layout
    
    def connect_to_server(self, instance):
        """Подключение к серверу"""
        try:
            ip = self.ip_input.text.strip()
            port = int(self.port_input.text.strip())
            
            if not ip:
                self.show_popup("⚠️ Ошибка", "Введите IP адрес")
                return
            
            self.show_popup("⏳ Подключение", f"Подключение к {ip}:{port}...")
            
            def connect_thread():
                if self.client.connect(ip, port):
                    Clock.schedule_once(lambda dt: self.on_connected(), 0.1)
                else:
                    Clock.schedule_once(lambda dt: self.on_disconnected(), 0.1)
            
            thread = threading.Thread(target=connect_thread)
            thread.daemon = True
            thread.start()
            
        except ValueError:
            self.show_popup("⚠️ Ошибка", "Неверный порт")
    
    def disconnect_from_server(self, instance):
        """Отключение от сервера"""
        self.client.disconnect()
        self.on_disconnected()
    
    def on_connected(self):
        """Выполняется при успешном подключении"""
        self.connection_status = "Подключено"
        self.status_label.text = '🟢 Статус: Подключено'
        self.status_label.color = (0, 1, 0, 1)
        self.connect_btn.disabled = True
        self.disconnect_btn.disabled = False
        self.show_popup("✅ Успешно", "Подключено к серверу!")
    
    def on_disconnected(self):
        """Выполняется при отключении"""
        self.connection_status = "Отключено"
        self.status_label.text = '🔴 Статус: Отключено'
        self.status_label.color = (1, 0, 0, 1)
        self.connect_btn.disabled = False
        self.disconnect_btn.disabled = True
        self.show_popup("❌ Отключено", "Соединение разорвано")
    
    def on_client_message(self, event_type: str, data):
        """Обработка сообщений от клиента"""
        if event_type == 'message':
            msg_type = data.get('type')
            
            if msg_type == 'pong':
                Clock.schedule_once(lambda dt: self.show_popup("📡 Пинг", "Сервер ответил"), 0)
            
            elif msg_type == 'command':
                command = data.get('command')
                if command == 'switch_camera':
                    Clock.schedule_once(lambda dt: self.switch_camera(None), 0)
                elif command == 'take_photo':
                    Clock.schedule_once(lambda dt: self.take_photo(None), 0)
            
            elif msg_type == 'notification':
                message = data.get('message', 'Уведомление')
                Clock.schedule_once(
                    lambda dt: self.show_popup("🔔 Уведомление", message),
                    0
                )
        
        elif event_type == 'error':
            Clock.schedule_once(
                lambda dt: self.show_popup("❌ Ошибка", str(data)),
                0
            )
    
    def switch_camera(self, instance):
        """Переключение камеры"""
        try:
            if self.camera_widget:
                self.camera_widget.play = False
                
                if self.using_back_camera:
                    self.camera_widget.index = 1
                    self.using_back_camera = False
                else:
                    self.camera_widget.index = 0
                    self.using_back_camera = True
                
                self.camera_widget.play = True
                
                # Отправляем уведомление серверу
                camera_name = "📱 Передняя" if not self.using_back_camera else "📷 Задняя"
                self.client.send_message({
                    'type': 'camera_switched',
                    'camera': camera_name
                })
        
        except Exception as e:
            self.show_popup("❌ Ошибка", f"Ошибка переключения: {str(e)}")
    
    def take_photo(self, instance):
        """Сохранение фото"""
        try:
            if not os.path.exists('photos'):
                os.makedirs('photos')
            
            filename = f'photos/photo_{int(time.time())}.png'
            self.camera_widget.export_to_png(filename)
            
            # Отправляем уведомление серверу
            self.client.send_message({
                'type': 'photo_saved',
                'data': filename
            })
            
            self.show_popup("✅ Успешно", f"Фото сохранено:\n{filename}")
        
        except Exception as e:
            self.show_popup("❌ Ошибка", f"Ошибка: {str(e)}")
    
    def show_popup(self, title: str, message: str):
        """Показание всплывающего окна"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, markup=True))
        
        close_btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.4)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def on_stop(self):
        """При закрытии приложения"""
        self.client.disconnect()
        return True


if __name__ == '__main__':
    app = MobileCamera()
    app.run()
