#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Приложение для просмотра камер телефона на Python
Поддерживает переключение между передней и задней камерой
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
import os

# Установите размер окна для эмулятора (для телефона это не нужно)
Window.size = (480, 800)


class CameraApp(App):
    """Главное приложение камеры"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.using_back_camera = True
        self.title = "📷 Камера"
    
    def build(self):
        """Построение интерфейса приложения"""
        
        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Информационный лейбл
        self.info_label = Label(
            text='Задняя камера',
            size_hint_y=0.1,
            bold=True,
            font_size='18sp'
        )
        main_layout.add_widget(self.info_label)
        
        # Виджет камеры
        self.camera = Camera(
            resolution=(640, 480),
            play=True
        )
        main_layout.add_widget(self.camera)
        
        # Контейнер для кнопок
        button_layout = BoxLayout(
            size_hint_y=0.15,
            spacing=10,
            padding=10,
            orientation='horizontal'
        )
        
        # Кнопка переключения камеры
        switch_btn = Button(
            text='🔄 Переключить\nкамеру',
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint_x=0.5
        )
        switch_btn.bind(on_press=self.switch_camera)
        button_layout.add_widget(switch_btn)
        
        # Кнопка фото
        photo_btn = Button(
            text='📸 Фото',
            background_color=(0.2, 0.8, 0.4, 1),
            size_hint_x=0.5
        )
        photo_btn.bind(on_press=self.take_photo)
        button_layout.add_widget(photo_btn)
        
        main_layout.add_widget(button_layout)
        
        # Кнопка выхода
        exit_btn = Button(
            text='✕ Выход',
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_y=0.1
        )
        exit_btn.bind(on_press=self.stop)
        main_layout.add_widget(exit_btn)
        
        return main_layout
    
    def switch_camera(self, instance):
        """Переключение между передней и задней камерой"""
        try:
            if self.camera:
                # Останавливаем текущую камеру
                self.camera.play = False
                
                # Переключаем источник
                if self.using_back_camera:
                    self.camera.index = 1  # Передняя камера
                    self.info_label.text = '📱 Передняя камера'
                    self.using_back_camera = False
                else:
                    self.camera.index = 0  # Задняя камера
                    self.info_label.text = '📷 Задняя камера'
                    self.using_back_camera = True
                
                # Запускаем новую камеру
                self.camera.play = True
                
        except Exception as e:
            self.show_error(f'Ошибка: {str(e)}')
    
    def take_photo(self, instance):
        """Сохранение фотографии"""
        try:
            # Создаем папку для фото если её нет
            if not os.path.exists('photos'):
                os.makedirs('photos')
            
            # Сохраняем фото
            import time
            filename = f'photos/photo_{int(time.time())}.png'
            self.camera.export_to_png(filename)
            self.show_message(f'✅ Фото сохранено:\n{filename}')
            
        except Exception as e:
            self.show_error(f'Ошибка при сохранении: {str(e)}')
    
    def show_message(self, message):
        """Показать сообщение"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message, markup=True))
        
        close_btn = Button(text='ОК', size_hint_y=0.3)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(
            title='Сообщение',
            content=popup_layout,
            size_hint=(0.8, 0.3)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_error(self, message):
        """Показать ошибку"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message, markup=True, color=(1, 0, 0, 1)))
        
        close_btn = Button(text='ОК', size_hint_y=0.3)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(
            title='❌ Ошибка',
            content=popup_layout,
            size_hint=(0.8, 0.3)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    app = CameraApp()
    app.run()
