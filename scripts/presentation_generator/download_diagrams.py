import requests
import os

def download_file(url, filename):
    print(f"Скачивание {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Успешно скачан {filename}")
    except Exception as e:
        print(f"Ошибка скачивания {filename}: {e}")
        # Создаем заглушку, чтобы билд не упал
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (800, 600), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10,10), f"Заглушка для {filename}", fill=(0,0,0))
        img.save(filename)

download_file('https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Phase_diagram_of_water.svg/800px-Phase_diagram_of_water.svg.png', 'phase_water.png')
download_file('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Phase_diagram_of_a_binary_system_with_a_eutectic_point.svg/800px-Phase_diagram_of_a_binary_system_with_a_eutectic_point.svg.png', 'phase_eutectic.png')

print("Загрузка диаграмм завершена.")
