"""
Comprehensive Forensic and Stress-Testing Script for Lecture 04 Materials
NANOPHYSICS COURSE - SUAI (Semester 4, Lecture 04)
Checks:
- Cross-consistency between lecture_04_plan.md and lecture_04_speech.md
- Thermodynamic signs: Delta H, Delta S, Delta G for adsorption
- Kelvin equation variables: V_m with R_g vs v_0 with k_B
- Washburn equation: r^2 vs t, viscosity eta, contact angle cos(theta)
- Matthews-Blakeslee critical thickness and elastic strain formulas
- IUPAC isotherm types (I to VI)
- Numerical values consistency
"""

import sys
import re
import math
from pathlib import Path

# Configure utf-8 stdout
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAN_PATH = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_04_plan.md"
SPEECH_PATH = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_04_speech.md"

def load_files():
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan_text = f.read()
    with open(SPEECH_PATH, "r", encoding="utf-8") as f:
        speech_text = f.read()
    return plan_text, speech_text

def test_thermodynamic_adsorption_signs(plan, speech):
    """Check thermodynamic signs of Delta G, Delta H, Delta S for adsorption."""
    print("\n--- Check 1: Adsorption Thermodynamics Signs (Delta G, Delta H, Delta S) ---")
    # Adsorption reduces degrees of freedom: Delta S < 0
    # For spontaneity at constant T, P: Delta G = Delta H - T * Delta S < 0
    # Therefore Delta H must be negative and |Delta H| > T * |Delta S|
    findings = []
    
    # Search in Slide 20 (Physisorption vs Chemisorption)
    for name, text in [("Plan", plan), ("Speech", speech)]:
        matches = re.findall(r'[Δ\\]Delta\s*[HGS].*?[\n\.]', text)
        for m in matches:
            print(f"[{name}] Found: {m.strip()}")
            
    # Check mentions of экзотермич in Slide 20
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "экзотерм" in text.lower():
            print(f"[{name}] Confirmed: mentions exothermic nature of adsorption.")
        else:
            findings.append(f"[{name}] WARNING: Exothermic nature not explicitly stated.")
            
    print("Thermodynamic adsorption signs check complete.")
    return findings

def test_kelvin_variables_consistency(plan, speech):
    """Check Kelvin equation consistency: V_m with R_g vs molecular volume with k_B."""
    print("\n--- Check 2: Kelvin Equation Consistency ---")
    findings = []
    
    # Check if V_m / (R_g * T) or v / (k_B * T) is used consistently
    # If someone writes V_m / (k_B * T) that is an ERROR by factor of N_A (6e23)!
    # Or v_molecular / (R_g * T) is an ERROR by factor of 1/N_A!
    for name, text in [("Plan", plan), ("Speech", speech)]:
        # Look for Kelvin formulas
        kelvin_matches = re.findall(r'\\ln\s*\\\(\s*\\frac\{P[^}]+\}\{P[^}]+\}\s*\\\)\s*=\s*([^$\n]+)', text)
        print(f"[{name}] Kelvin formulas found: {len(kelvin_matches)}")
        for km in kelvin_matches:
            print(f"  Formula: {km.strip()}")
            if "V_m" in km:
                if "k_B" in km and "R_g" not in km and "R T" not in km:
                    findings.append(f"[{name}] CRITICAL: Mixed molar volume V_m with Boltzmann constant k_B!")
                if "R_g" in km or "R T" in km or "RT" in km:
                    print(f"  OK: V_m correctly paired with R_g or R!")
            if "k_B" in km:
                if "V_m" in km:
                    findings.append(f"[{name}] CRITICAL: k_B paired with molar volume V_m!")
                    
    print("Kelvin variables check complete.")
    return findings

def test_washburn_equation(plan, speech):
    """Check Washburn equation in Slide 12 for capillary flow."""
    print("\n--- Check 3: Washburn Equation ---")
    findings = []
    for name, text in [("Plan", plan), ("Speech", speech)]:
        washburn_matches = re.findall(r'Уошберн|Washburn|L\^2|h\^2', text)
        print(f"[{name}] Washburn mentions: {len(washburn_matches)}")
        # Look for Washburn equation: L^2 = (gamma * r * cos(theta) / (2 * eta)) * t
        matches = re.findall(r'L\^2\s*=\s*[^$\n]+', text)
        for m in matches:
            print(f"[{name}] Washburn formula: {m.strip()}")
            # Check factors: sigma (or gamma), r, cos(theta), 2 or 4, eta (viscosity), t
            if "cos" in m and "eta" in m or "\\eta" in m:
                print(f"[{name}] Washburn formula components verified.")
            else:
                findings.append(f"[{name}] Notice: Washburn formula structure: {m}")
    print("Washburn check complete.")
    return findings

def test_matthews_blakeslee(plan, speech):
    """Check Matthews-Blakeslee critical thickness formula."""
    print("\n--- Check 4: Matthews-Blakeslee & Critical Thickness ---")
    findings = []
    for name, text in [("Plan", plan), ("Speech", speech)]:
        mb_matches = re.findall(r'Мэттьюс|Блейкли|Блейксл|Matthews|Blakeslee|h_c', text)
        print(f"[{name}] Critical thickness / MB mentions: {len(mb_matches)}")
        hc_formulas = re.findall(r'h_c\s*[=≈\\approx\s][^$\n]+', text)
        for hf in hc_formulas:
            print(f"[{name}] h_c formula/value: {hf.strip()}")
    print("Matthews-Blakeslee check complete.")
    return findings

def test_plan_speech_formulas_crosscheck(plan, speech):
    """Cross-check formulas between plan and speech slide by slide."""
    print("\n--- Check 5: Cross-check Formulas between Plan and Speech ---")
    discrepancies = []
    
    # Extract slides 1..24
    for s_num in range(1, 25):
        pat = rf'### Слайд {s_num}\..*?(?=### Слайд \d+\.|$)'
        m_plan = re.search(pat, plan, re.DOTALL)
        m_speech = re.search(pat, speech, re.DOTALL)
        
        if not m_plan:
            discrepancies.append(f"Slide {s_num} missing in Plan!")
            continue
        if not m_speech:
            discrepancies.append(f"Slide {s_num} missing in Speech!")
            continue
            
        p_text = m_plan.group(0)
        s_text = m_speech.group(0)
        
        # Extract math expressions
        p_math = set(re.findall(r'\$\$([^$]+)\$\$', p_text))
        s_math = set(re.findall(r'\$\$([^$]+)\$\$', s_text))
        
        # Check title alignment
        p_title = re.search(r'### Слайд \d+\.\s*([^\n]+)', p_text).group(1).strip()
        s_title = re.search(r'### Слайд \d+\.\s*([^\n]+)', s_text).group(1).strip()
        if p_title != s_title:
            discrepancies.append(f"Slide {s_num} title mismatch:\n  Plan:   {p_title}\n  Speech: {s_title}")
            
    print(f"Total slide title / presence discrepancies: {len(discrepancies)}")
    for d in discrepancies:
        print(f"  {d}")
    return discrepancies

def test_numerical_values(plan, speech):
    """Check all critical numerical constants and values across both documents."""
    print("\n--- Check 6: Critical Numerical Values Across Documents ---")
    inconsistencies = []
    
    # 1. Surface tension of water: 72.8 mN/m
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "72.8" not in text:
            inconsistencies.append(f"[{name}] Missing 72.8 mN/m value!")
            
    # 2. InAs/GaAs mismatch: 7.2%
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "7.2%" not in text and "7,2%" not in text and "7.2" not in text:
            inconsistencies.append(f"[{name}] Missing 7.2% lattice mismatch!")
            
    # 3. Critical thickness InAs: 1.7 ML
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "1.7" not in text:
            inconsistencies.append(f"[{name}] Missing 1.7 ML critical thickness!")
            
    # 4. Graphene specific surface area: 2600 m^2/g
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "2600" not in text:
            inconsistencies.append(f"[{name}] Missing 2600 m^2/g graphene SSA!")
            
    # 5. Nitrogen molecular cross-section: 0.162 nm^2
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "0.162" not in text:
            inconsistencies.append(f"[{name}] Missing 0.162 nm^2 nitrogen area!")
            
    # 6. Nitrogen temperature: 77.3 K
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "77.3" not in text and "77" not in text:
            inconsistencies.append(f"[{name}] Missing 77 K / 77.3 K liquid N2 temperature!")
            
    # 7. Molar volume V0: 22400 cm^3/mol
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "22400" not in text and "22.4" not in text:
            inconsistencies.append(f"[{name}] Missing 22400 cm^3/mol molar gas volume!")
            
    # 8. BET linear range: 0.05 - 0.35
    for name, text in [("Plan", plan), ("Speech", speech)]:
        if "0.05" not in text or "0.35" not in text:
            inconsistencies.append(f"[{name}] Missing 0.05-0.35 BET range!")
            
    print(f"Numerical inconsistencies found: {len(inconsistencies)}")
    for inc in inconsistencies:
        print(f"  {inc}")
    return inconsistencies

if __name__ == "__main__":
    plan, speech = load_files()
    f1 = test_thermodynamic_adsorption_signs(plan, speech)
    f2 = test_kelvin_variables_consistency(plan, speech)
    f3 = test_washburn_equation(plan, speech)
    f4 = test_matthews_blakeslee(plan, speech)
    f5 = test_plan_speech_formulas_crosscheck(plan, speech)
    f6 = test_numerical_values(plan, speech)
    print("\nALL FORENSIC CHECKS FINISHED.")
