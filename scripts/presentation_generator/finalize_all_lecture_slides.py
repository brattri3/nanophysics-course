import win32com.client
import os
import shutil

def finalize_lecture():
    pptx_path = os.path.abspath("course_materials/semester_4/lectures/lecture_02_thermodynamics.pptx")
    out_dir = os.path.dirname(pptx_path)
    artifact_dir = os.path.join(out_dir, "previews_l02")
    os.makedirs(artifact_dir, exist_ok=True)
    base_dir = os.path.abspath("scripts/presentation_generator")
    
    app = win32com.client.Dispatch("PowerPoint.Application")
    p = None
    try:
        p = app.Presentations.Open(pptx_path, WithWindow=False)
        
        # =============================================================
        # Slide 11: Add diagram_alloys_comparison.png
        # =============================================================
        s11 = p.Slides(11)
        for i in range(1, s11.Shapes.Count + 1):
            shp = s11.Shapes(i)
            if shp.HasTextFrame and shp != s11.Shapes.Title and shp.Left > 400:
                shp.Top = 96.0
                shp.Height = 175.0
                tf = shp.TextFrame
                lines = [
                    "2. Расчет структурных составляющих:",
                    "• Формулы правила рычага для структуры:",
                    "  - Доля эвтектики: W_эвт = (C_Si - C₀) / (C_Si - C_E).",
                    "  - Доля первичных кристаллов: W_перв = 1 - W_эвт.",
                    "• Практика: эвтектика Au–Si обеспечивает пайку кристаллов при 363 °C без перегрева p-n переходов микросхем."
                ]
                tf.TextRange.Text = "\r".join(lines)
                for p_idx in range(1, tf.TextRange.Paragraphs().Count + 1):
                    para = tf.TextRange.Paragraphs(p_idx)
                    if p_idx == 1:
                        para.Font.Name = "Arial"
                        para.Font.Size = 14
                        para.Font.Bold = -1
                        para.Font.Color.RGB = 6237184
                    else:
                        para.Font.Name = "Arial"
                        para.Font.Size = 11.5
                        para.Font.Bold = 0
                        para.Font.Color.RGB = 3418148
                        para.ParagraphFormat.SpaceBefore = 1.0
                        para.ParagraphFormat.SpaceAfter = 1.0
                break
                
        img_alloys = os.path.join(base_dir, "diagram_alloys_comparison.png")
        if os.path.exists(img_alloys):
            for i in range(s11.Shapes.Count, 0, -1):
                if s11.Shapes(i).Type == 13:
                    s11.Shapes(i).Delete()
            pic = s11.Shapes.AddPicture(img_alloys, False, True, 490.0, 275.0, 420.0, 225.0)

        # =============================================================
        # Slide 15: Add diagram_nano_eutectic.png
        # =============================================================
        s15 = p.Slides(15)
        for i in range(1, s15.Shapes.Count + 1):
            shp = s15.Shapes(i)
            if shp.HasTextFrame and shp != s15.Shapes.Title and shp.Left > 400:
                shp.Top = 96.0
                shp.Height = 175.0
                tf = shp.TextFrame
                lines = [
                    "2. Новые феномены в наносостоянии:",
                    "• Расширение взаимной растворимости:",
                    "  - Избыточная энергия границ раздела повышает предел растворимости компонентов в наносостоянии в разы.",
                    "• Стабилизация метастабильных модификаций:",
                    "  - Нанофазы с меньшей поверхностной энергией σ устойчивы при н.у. (например, тетрагональный ZrO₂ < 30 нм)."
                ]
                tf.TextRange.Text = "\r".join(lines)
                for p_idx in range(1, tf.TextRange.Paragraphs().Count + 1):
                    para = tf.TextRange.Paragraphs(p_idx)
                    if p_idx == 1:
                        para.Font.Name = "Arial"
                        para.Font.Size = 14
                        para.Font.Bold = -1
                        para.Font.Color.RGB = 6237184
                    else:
                        para.Font.Name = "Arial"
                        para.Font.Size = 11.5
                        para.Font.Bold = 0
                        para.Font.Color.RGB = 3418148
                        para.ParagraphFormat.SpaceBefore = 1.0
                        para.ParagraphFormat.SpaceAfter = 1.0
                break
                
        img_nano_eut = os.path.join(base_dir, "diagram_nano_eutectic.png")
        if os.path.exists(img_nano_eut):
            for i in range(s15.Shapes.Count, 0, -1):
                if s15.Shapes(i).Type == 13:
                    s15.Shapes(i).Delete()
            pic = s15.Shapes.AddPicture(img_nano_eut, False, True, 490.0, 275.0, 420.0, 225.0)

        # =============================================================
        # Slide 16: Add diagram_vls_mechanism.png across bottom
        # =============================================================
        s16 = p.Slides(16)
        # Left shape
        for i in range(1, s16.Shapes.Count + 1):
            shp = s16.Shapes(i)
            if shp.HasTextFrame and shp != s16.Shapes.Title and shp.Left < 400:
                shp.Top = 92.0
                shp.Height = 155.0
                tf = shp.TextFrame
                lines = [
                    "1. Механизм «Пар–Жидкость–Кристалл» (VLS):",
                    "• Открытие Вагнера–Эллиса в нанотехнологиях:",
                    "  - Жидкая нанокапля эвтектики Au–Si как катализатор направленного роста.",
                    "  - Прекурсор силан SiH₄ каталитически разлагается на капле: SiH₄ -> Si + 2H₂."
                ]
                tf.TextRange.Text = "\r".join(lines)
                for p_idx in range(1, tf.TextRange.Paragraphs().Count + 1):
                    para = tf.TextRange.Paragraphs(p_idx)
                    if p_idx == 1:
                        para.Font.Name = "Arial"
                        para.Font.Size = 14
                        para.Font.Bold = -1
                        para.Font.Color.RGB = 6237184
                    else:
                        para.Font.Name = "Arial"
                        para.Font.Size = 11.5
                        para.Font.Bold = 0
                        para.Font.Color.RGB = 3418148
                        para.ParagraphFormat.SpaceBefore = 1.0
                        para.ParagraphFormat.SpaceAfter = 1.0
                break

        # Right shape
        for i in range(1, s16.Shapes.Count + 1):
            shp = s16.Shapes(i)
            if shp.HasTextFrame and shp != s16.Shapes.Title and shp.Left > 400:
                shp.Top = 92.0
                shp.Height = 155.0
                tf = shp.TextFrame
                lines = [
                    "2. Движущая сила и контроль геометрии:",
                    "• Пересыщение и кристаллизация кремния:",
                    "  - Кремний кристаллизуется на границе раздела капля/подложка.",
                    "  - Растущий кристалл выталкивает каплю вверх; диаметр нити задается каплей Au.",
                    "  - Базовая технология для новейших транзисторов GAAFET и фотоники."
                ]
                tf.TextRange.Text = "\r".join(lines)
                for p_idx in range(1, tf.TextRange.Paragraphs().Count + 1):
                    para = tf.TextRange.Paragraphs(p_idx)
                    if p_idx == 1:
                        para.Font.Name = "Arial"
                        para.Font.Size = 14
                        para.Font.Bold = -1
                        para.Font.Color.RGB = 6237184
                    else:
                        para.Font.Name = "Arial"
                        para.Font.Size = 11.5
                        para.Font.Bold = 0
                        para.Font.Color.RGB = 3418148
                        para.ParagraphFormat.SpaceBefore = 1.0
                        para.ParagraphFormat.SpaceAfter = 1.0
                break

        img_vls = os.path.join(base_dir, "diagram_vls_mechanism.png")
        if os.path.exists(img_vls):
            for i in range(s16.Shapes.Count, 0, -1):
                if s16.Shapes(i).Type == 13:
                    s16.Shapes(i).Delete()
            pic = s16.Shapes.AddPicture(img_vls, False, True, 170.0, 255.0, 620.0, 245.0)

        p.Save()
        
        # Export all previews 11 to 17
        for s_idx in range(11, p.Slides.Count + 1):
            preview_local = os.path.join(out_dir, f"slide_{s_idx}_preview.png")
            preview_art = os.path.join(artifact_dir, f"slide_{s_idx}_preview.png")
            p.Slides(s_idx).Export(preview_local, "PNG", 1440, 810)
            shutil.copy(preview_local, preview_art)
            print(f"Exported Slide {s_idx} preview")
            
        print("Finalized all slides 11-17 successfully!")
    finally:
        if p is not None:
            try:
                p.Close()
            except Exception:
                pass
        try:
            app.Quit()
        except Exception:
            pass

if __name__ == "__main__":
    finalize_lecture()
