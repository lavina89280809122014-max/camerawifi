# 📷 Приложение Камера для Android на Python

Приложение для просмотра передней и задней камеры телефона на Python с использованием Kivy.

## 📋 Требования

- Python 3.7+
- Buildozer (для сборки APK)
- Android SDK и NDK

## 🚀 Установка зависимостей

### На компьютере (для разработки)

```bash
pip install kivy
pip install buildozer
pip install cython
```

### На Linux/Mac
```bash
sudo apt-get install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install kivy buildozer cython
```

### На Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install kivy buildozer cython
```

## 🔨 Запуск на компьютере (тестирование)

```bash
python camera_app.py
```

## 📱 Сборка для Android

### 1. Установите Buildozer

```bash
pip install buildozer
```

### 2. Создайте файл buildozer.spec

```bash
buildozer android debug
```

Это автоматически создаст `buildozer.spec`. Отредактируйте его:

```ini
[app]
title = Камера
package.name = camera_app
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,android,pyjnius
permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
orientation = portrait
fullscreen = 0
```

### 3. Установите Java и Android SDK

**На Windows:**
- Скачайте Android Studio: https://developer.android.com/studio
- Установите Java Development Kit (JDK)

**На Linux:**
```bash
sudo apt-get install openjdk-11-jdk
```

### 4. Соберите APK

```bash
buildozer android debug
```

APK файл будет в папке `bin/`

### 5. Установите на телефон

```bash
adb install -r bin/camera_app-1.0-debug.apk
```

## 🎮 Управление

- **📱 Передняя камера** / **📷 Задняя камера** - кнопка для переключения
- **📸 Фото** - сохраняет снимок в папку `photos/`
- **✕ Выход** - закрывает приложение

## ⚙️ Функции

✅ Переключение между передней и задней камерой
✅ Сохранение фотографий
✅ Простой и интуитивный интерфейс
✅ Поддержка всех Android устройств
✅ Русский язык интерфейса

## 📂 Структура

```
├── camera_app.py      # Основное приложение
├── buildozer.spec     # Конфигурация для сборки
└── photos/            # Папка с сохраненными фото
```

## 🐛 Решение проблем

### "No module named kivy"
```bash
pip install kivy --upgrade
```

### "Permission denied" при установке
```bash
sudo pip install buildozer
```

### Камера не работает на эмуляторе
Используйте реальный телефон для тестирования

## 📝 Альтернативный способ через Conda

```bash
conda create -n camera_app python=3.9
conda activate camera_app
conda install -c conda-forge kivy
python camera_app.py
```

## 📚 Полезные ссылки

- Документация Kivy: https://kivy.org/doc/stable/
- Buildozer: https://buildozer.readthedocs.io/
- Android SDK: https://developer.android.com/

Удачи! 🚀
