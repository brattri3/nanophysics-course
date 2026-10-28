import os
import shutil

def prepare_assets():
    target_dir = os.path.abspath("course_materials/semester_4/manuals/figures")
    os.makedirs(target_dir, exist_ok=True)
    
    asset_map = {
        "course_materials/semester_4/lectures/diagram_degrees_of_freedom.png": "fig_degrees_of_freedom.png",
        "course_materials/semester_4/lectures/diagram_thermal_analysis.png": "fig_thermal_analysis.png",
        "course_materials/semester_4/lectures/diagram_lever_rule_au_si.png": "fig_lever_anatomy.png",
        "course_materials/semester_4/lectures/diagram_lever_dynamics.png": "fig_lever_cooling_dynamics.png",
        "scripts/presentation_generator/diagram_alloys_comparison.png": "fig_alloys_comparison.png",
        "scripts/presentation_generator/chart_surface_energy.png": "fig_surface_energy_lattice.png",
        "scripts/presentation_generator/chart_nucleation.png": "fig_nucleation_barrier.png",
        "scripts/presentation_generator/chart_gibbs_thomson.png": "fig_gibbs_thomson_au.png",
        "scripts/presentation_generator/diagram_nano_eutectic.png": "fig_nano_eutectic_shift.png",
        "scripts/presentation_generator/diagram_vls_mechanism.png": "fig_vls_mechanism_stages.png",
    }
    
    print("Preparing manual figures...")
    for src_rel, dst_name in asset_map.items():
        src = os.path.abspath(src_rel)
        dst = os.path.join(target_dir, dst_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {dst_name} ({os.path.getsize(dst)} bytes)")
        else:
            print(f"WARNING: Source file not found: {src}")
            
    print("All assets prepared successfully in:", target_dir)

if __name__ == "__main__":
    prepare_assets()
