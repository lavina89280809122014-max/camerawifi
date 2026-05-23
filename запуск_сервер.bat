@echo off
REM -*- coding: utf-8 -*-
REM Скрипт для быстрого запуска сервера на Windows

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ================================================
echo.       КАМЕРА WiFi - ЗАПУСК СЕРВЕРА
echo.
echo ================================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ^^!^^! ОШИБКА: Python не установлен или не добавлен в PATH
    echo.
    echo Установите Python с https://www.python.org/downloads/
    echo И отметьте "Add Python to PATH" при установке
    echo.
    pause
    exit /b 1
)

echo. ✓ Python найден

REM Проверка установки Kivy
pip show kivy >nul 2>&1
if errorlevel 1 (
    echo.
    echo Устанавливаю Kivy (первый раз)...
    echo.
    pip install kivy
    if errorlevel 1 (
        echo.
        echo ^^!^^! ОШИБКА при установке Kivy
        pause
        exit /b 1
    )
)

echo. ✓ Kivy установлен

REM Получение IP адреса
for /f "tokens=2 delims=: " %%a in ('ipconfig ^| findstr /R "IPv4 Address"') do (
    set "IP=%%a"
    goto found_ip
)

:found_ip
if defined IP (
    echo. ✓ IP адрес: %IP%
) else (
    echo. ⚠ IP адрес не найден, используется 127.0.0.1
    set "IP=127.0.0.1"
)

echo.
echo ================================================
echo.
echo 🌐 ВАЖНО: Подключайтесь к %IP%:5555
echo.
echo ================================================
echo.

REM Запуск сервера
python server.py

pause
