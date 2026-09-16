import win32com.client
import os

def duplicate_slides(filepath):
    abs_path = os.path.abspath(filepath)
    app = win32com.client.Dispatch("PowerPoint.Application")
    prs = app.Presentations.Open(abs_path)
    
    # Duplicate slide 3 nine times
    for _ in range(9):
        prs.Slides(3).Duplicate()
        
    prs.Save()
    prs.Close()
    print("Duplicated slides successfully.")

if __name__ == "__main__":
    duplicate_slides('course_materials/semester_4/lectures/lecture_02_thermodynamics_extended.pptx')
