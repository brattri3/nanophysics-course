import subprocess
import os
import sys

def build_pdf():
    manuals_dir = os.path.abspath("course_materials/semester_4/manuals")
    tex_file = "chapter_02_thermodynamics.tex"
    pdf_file = "chapter_02_thermodynamics.pdf"
    
    print(f"Building LaTeX document in: {manuals_dir}")
    print(f"Target: {tex_file} -> {pdf_file}")
    
    # Run 1
    print("\n--- Pass 1: Initial compilation ---")
    res1 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file],
        cwd=manuals_dir,
        capture_output=True,
        text=True
    )
    print(f"Pass 1 exit code: {res1.returncode}")
    if res1.returncode != 0:
        print("Pass 1 errors (stdout tail):")
        print(res1.stdout[-1500:])
        return False
        
    # Run 2 (resolve references & cross-links)
    print("\n--- Pass 2: Resolving cross-references and citations ---")
    res2 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file],
        cwd=manuals_dir,
        capture_output=True,
        text=True
    )
    print(f"Pass 2 exit code: {res2.returncode}")
    if res2.returncode != 0:
        print("Pass 2 errors (stdout tail):")
        print(res2.stdout[-1500:])
        return False
        
    full_pdf_path = os.path.join(manuals_dir, pdf_file)
    if os.path.exists(full_pdf_path):
        size_kb = os.path.getsize(full_pdf_path) / 1024
        print(f"\nSUCCESS! PDF generated successfully: {full_pdf_path} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"\nERROR: PDF file was not created: {full_pdf_path}")
        return False

if __name__ == "__main__":
    success = build_pdf()
    if not success:
        sys.exit(1)
