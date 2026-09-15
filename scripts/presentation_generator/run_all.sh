#!/usr/bin/env bash
set -e

echo "=== Установка библиотек ==="
pip install -r requirements.txt

echo "=== Генерация физических графиков ==="
python generate_charts.py

echo "=== Загрузка диаграмм ==="
python download_diagrams.py

echo "=== Сборка презентации PowerPoint ==="
python build_presentation.py

echo "Готово: lecture_02_thermodynamics.pptx успешно создан!"
