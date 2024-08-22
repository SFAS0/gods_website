#!/bin/bash

# Проверяем, установлен ли Python 3.9
python3.9 --version > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
  echo "Python 3.9 уже установлен."
else
  # Устанавливаем Python 3.9
  echo "Устанавливаем Python 3.9..."
  sudo apt update
  sudo apt install python3.9
fi

# Устанавливаем зависимости из requirements.txt
echo "Устанавливаем зависимости..."
pip3.9 install -r requirements.txt
echo "Установка завершена!"

# Запуск main.py
python main.py
