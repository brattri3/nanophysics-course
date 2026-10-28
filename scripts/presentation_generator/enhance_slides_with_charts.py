import win32com.client
import os
import shutil

def enhance_slides():
    pptx_path = os.path.abspath("course_materials/semester_4/lectures/lecture_02_thermodynamics.pptx")
    out_dir = os.path.dirname(pptx_path)
    artifact_dir = os.path.join(out_dir, "previews_l02")
    os.makedirs(artifact_dir, exist_ok=True)
    base_dir = os.path.abspath("scripts/presentation_generator")
    
    app = win32com.client.Dispatch("PowerPoint.Application")
    p = None
    try:
        p = app.Presentations.Open(pptx_path, WithWindow=False)
        
        # -------------------------------------------------------------
        # Slide 12: Add chart_surface_energy.png on the right bottom
        # -------------------------------------------------------------
        s12 = p.Slides(12)
        # Find right shape
        for i in range(1, s12.Shapes.Count + 1):
            shp = s12.Shapes(i)
            if shp.HasTextFrame and shp != s12.Shapes.Title and shp.Left > 400:
                shp.Top = 96.0
                shp.Height = 175.0
                # shorten text slightly for image space
                tf = shp.TextFrame
                lines = [
                    "2. Конкуренция объёма и поверхности:",
                    "• Энергетический баланс образования зародыша:",
                    "  - Объемный выигрыш: ΔG_v = - (4/3) π r³ Δg_v < 0 (~ r³).",
                    "  - Поверхностные затраты: ΔG_s = + 4 π r² σ > 0 (~ r²).",
                    "• Полная свободная энергия кластера:",
                    "  ΔG(r) = - (4/3) π r³ Δg_v + 4 π r² σ",
                    "• При ультрамалых r преобладает поверхностный штраф (~ r²)."
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
                
        img_surf = os.path.join(base_dir, "chart_surface_energy.png")
        if os.path.exists(img_surf):
            # Delete any existing picture on slide 12
            for i in range(s12.Shapes.Count, 0, -1):
                if s12.Shapes(i).Type == 13:
                    s12.Shapes(i).Delete()
            pic = s12.Shapes.AddPicture(img_surf, False, True, 520.0, 275.0, 360.0, 220.0)
            
        # -------------------------------------------------------------
        # Slide 13: Add chart_nucleation.png on the right bottom
        # -------------------------------------------------------------
        s13 = p.Slides(13)
        for i in range(1, s13.Shapes.Count + 1):
            shp = s13.Shapes(i)
            if shp.HasTextFrame and shp != s13.Shapes.Title and shp.Left > 400:
                shp.Top = 96.0
                shp.Height = 175.0
                tf = shp.TextFrame
                lines = [
                    "2. Физический смысл и управление синтезом:",
                    "• Поведение кластеров разного размера:",
                    "  - r < r*: докритический зародыш нестабилен и растворяется.",
                    "  - r > r*: закритический зародыш лавинообразно растет.",
                    "• Контроль размера наночастиц в синтезе:",
                    "  - Глубокое переохлаждение (ΔT) снижает r* и барьер ΔG*.",
                    "  - ПАВ (лиганды) блокируют рост, фиксируя ансамбль наночастиц."
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
                
        img_nucl = os.path.join(base_dir, "chart_nucleation.png")
        if os.path.exists(img_nucl):
            for i in range(s13.Shapes.Count, 0, -1):
                if s13.Shapes(i).Type == 13:
                    s13.Shapes(i).Delete()
            pic = s13.Shapes.AddPicture(img_nucl, False, True, 490.0, 275.0, 420.0, 225.0)

        # -------------------------------------------------------------
        # Slide 14: Add chart_gibbs_thomson.png on the right bottom
        # -------------------------------------------------------------
        s14 = p.Slides(14)
        for i in range(1, s14.Shapes.Count + 1):
            shp = s14.Shapes(i)
            if shp.HasTextFrame and shp != s14.Shapes.Title and shp.Left > 400:
                shp.Top = 96.0
                shp.Height = 175.0
                tf = shp.TextFrame
                lines = [
                    "2. Физическая картина и эксперимент:",
                    "• Поверхностное предплавление:",
                    "  - Атомы поверхности имеют высокую амплитуду колебаний.",
                    "  - Плавление наночастицы начинается с жидкой оболочки (1–2 нм).",
                    "• Эксперимент (Au, Буффа и Борель):",
                    "  - Объемный Au: 1064 °C; d = 10 нм: ~950 °C; d = 3 нм: ~400 °C!",
                    "• Применение: печатная электроника (спекание при 150–200 °C)."
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
                
        img_gt = os.path.join(base_dir, "chart_gibbs_thomson.png")
        if os.path.exists(img_gt):
            for i in range(s14.Shapes.Count, 0, -1):
                if s14.Shapes(i).Type == 13:
                    s14.Shapes(i).Delete()
            pic = s14.Shapes.AddPicture(img_gt, False, True, 490.0, 275.0, 420.0, 225.0)

        p.Save()
        
        # Export updated previews
        for s_idx in [12, 13, 14]:
            preview_local = os.path.join(out_dir, f"slide_{s_idx}_preview.png")
            preview_art = os.path.join(artifact_dir, f"slide_{s_idx}_preview.png")
            p.Slides(s_idx).Export(preview_local, "PNG", 1440, 810)
            shutil.copy(preview_local, preview_art)
            print(f"Exported Slide {s_idx} preview to {preview_local}")
            
        print("Slides 12, 13, 14 enhanced successfully!")
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
    enhance_slides()
