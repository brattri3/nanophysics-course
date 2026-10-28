"""
Утилита для экспорта превью слайдов презентации (.pptx) в изображения PNG
через COM-интерфейс PowerPoint (Windows) для быстрой визуальной верификации верстки.
"""

import os
import sys
import win32com.client


def export_pptx_to_png(pptx_path: str, output_dir: str, slide_indices: list[int] | None = None):
    """
    Экспортирует указанные (или все) слайды презентации в PNG.
    slide_indices: список 1-базированных номеров слайдов (если None — экспортируются все).
    """
    abs_pptx = os.path.abspath(pptx_path)
    abs_out = os.path.abspath(output_dir)
    os.makedirs(abs_out, exist_ok=True)

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    deck = None
    try:
        deck = powerpoint.Presentations.Open(abs_pptx, WithWindow=False)
        total = deck.Slides.Count
        targets = slide_indices if slide_indices else list(range(1, total + 1))
        for idx in targets:
            if 1 <= idx <= total:
                out_file = os.path.join(abs_out, f"slide_{idx:02d}_preview.png")
                deck.Slides(idx).Export(out_file, "PNG", 1920, 1080)
                print(f"Exported slide {idx}/{total} -> {out_file}")
    finally:
        if deck is not None:
            try:
                deck.Close()
            except Exception:
                pass
        try:
            powerpoint.Quit()
        except Exception:
            pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python export_slide_previews.py <path_to_pptx> <output_dir>")
        sys.exit(1)
    export_pptx_to_png(sys.argv[1], sys.argv[2])
