import os
from pptx import Presentation
from pptx.util import Inches

def fix_shapes(file_path):
    prs = Presentation(file_path)
    
    # Slides 1 to 6 (0-indexed) are content slides
    for i in range(1, 7):
        slide = prs.slides[i]
        
        # Collect shapes to keep
        shapes_to_delete = []
        for shape in slide.shapes:
            if shape.is_placeholder:
                continue
            shapes_to_delete.append(shape)
            
        for shape in shapes_to_delete:
            sp = shape._element
            sp.getparent().remove(sp)
            
    img_map = {
        3: 'phase_water.png',
        4: 'phase_eutectic.png',
        5: 'chart_nucleation.png',
        6: 'chart_gibbs_thomson.png'
    }
    
    left = Inches(6.0)
    top = Inches(1.5)
    width = Inches(5.8)
    
    for slide_idx, img_file in img_map.items():
        if os.path.exists(img_file):
            prs.slides[slide_idx].shapes.add_picture(img_file, left, top, width=width)
            print(f"Added {img_file} to slide {slide_idx}")
        
    prs.save(file_path)
    print("Fixed shapes.")

if __name__ == "__main__":
    fix_shapes('course_materials/semester_4/lectures/lecture_02_thermodynamics.pptx')
