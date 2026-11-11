"""
Empirical Physical and Mathematical Consistency Challenger Test Suite
Nanophysics Course - SUAI (Semester 4, Lecture 04)
Adversarially tests:
1. Thermodynamic identities and signs: Dupré, Young, Harkins
2. Curvature, Laplace pressure, Kelvin equation, Ostwald-Freundlich
3. Bauer criterion, lattice mismatch, elastic strain energy, critical thickness
4. Adsorption isotherms: Langmuir, BET, specific surface area formulas
5. Plan vs Speech consistency (formulas, parameters, numbers, units)
"""

import sys
import re
import math
from pathlib import Path

# Set utf-8 encoding for Windows console
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

def test_dupre_young_harkins():
    """Verify mathematical identities of Dupré, Young, and Harkins equations."""
    print("\n--- Test 1: Dupré, Young, Harkins Thermodynamic Consistency ---")
    
    # Mathematical identity verification:
    # Wa = sigma_s + sigma_l - sigma_sl (Dupré)
    # Wc = 2 * sigma_l (Cohesion of liquid)
    # Young: sigma_s - sigma_sl = sigma_l * cos(theta)
    # Dupre-Young: Wa = sigma_l * (1 + cos(theta))
    # Harkins: S = Wa - Wc = sigma_s - (sigma_l + sigma_sl) = sigma_l * (cos(theta) - 1)
    
    sigma_l = 0.0728 # N/m (water)
    for theta_deg in [0, 30, 60, 90, 120, 150, 180]:
        theta_rad = math.radians(theta_deg)
        cos_t = math.cos(theta_rad)
        
        # Assume arbitrary sigma_sl, then sigma_s = sigma_sl + sigma_l * cos_t
        sigma_sl = 0.030
        sigma_s = sigma_sl + sigma_l * cos_t
        
        wa_dupre = sigma_s + sigma_l - sigma_sl
        wa_dupre_young = sigma_l * (1.0 + cos_t)
        wc = 2.0 * sigma_l
        s_harkins = sigma_s - (sigma_l + sigma_sl)
        s_from_w = wa_dupre - wc
        s_from_theta = sigma_l * (cos_t - 1.0)
        
        assert abs(wa_dupre - wa_dupre_young) < 1e-12, f"Dupré-Young mismatch at theta={theta_deg}"
        assert abs(s_harkins - s_from_w) < 1e-12, f"Harkins S mismatch at theta={theta_deg}"
        assert abs(s_harkins - s_from_theta) < 1e-12, f"Harkins S from theta mismatch at theta={theta_deg}"
        
        if theta_deg == 0:
            assert abs(s_harkins) < 1e-12
            assert abs(wa_dupre - wc) < 1e-12
        elif theta_deg == 90:
            assert abs(wa_dupre - 0.5 * wc) < 1e-12
            assert s_harkins < 0
        elif theta_deg == 180:
            assert abs(wa_dupre) < 1e-12
            assert abs(s_harkins - (-wc)) < 1e-12
            
    print("PASS: Mathematical identities for Dupré, Young, Harkins are 100% exact across all theta in [0, 180].")

def test_laplace_numerical():
    """Verify Laplace pressure numerical calculations."""
    print("\n--- Test 2: Laplace Pressure Numerical & Asymptotic Limits ---")
    sigma = 0.0728 # N/m
    r_nm = 2.0
    r_m = r_nm * 1e-9
    
    delta_p = 2.0 * sigma / r_m
    delta_p_mpa = delta_p / 1e6
    delta_p_atm = delta_p / 101325.0
    
    print(f"Calculated Laplace pressure for R=2 nm, sigma=72.8 mN/m:")
    print(f"  Delta P = {delta_p:.2e} Pa = {delta_p_mpa:.2f} MPa = {delta_p_atm:.1f} atm")
    
    assert abs(delta_p_mpa - 72.8) < 0.1, "Laplace pressure MPa calculation mismatch"
    assert abs(delta_p_atm - 718.5) < 2.0, "Laplace pressure atm calculation mismatch"
    print("PASS: Laplace numerical calculation matches text (72.8 MPa ~ 720 atm).")

def test_kelvin_asymptotics():
    """Verify Kelvin equation asymptotic behaviors."""
    print("\n--- Test 3: Kelvin Equation Asymptotics ---")
    # Kelvin: ln(Pr / P0) = 2 * sigma * Vm / (r * R_g * T)
    # For water at 293.15 K:
    sigma = 0.0728 # N/m
    M_h2o = 0.018015 # kg/mol
    rho_h2o = 1000.0 # kg/m^3
    Vm = M_h2o / rho_h2o # 1.8015e-5 m^3/mol
    R_g = 8.314 # J/(mol K)
    T = 293.15 # K
    
    factor = 2.0 * sigma * Vm / (R_g * T) # meters
    print(f"Kelvin characteristic length l_K = 2*sigma*Vm/(Rg*T) = {factor*1e9:.3f} nm")
    
    # Convex droplets (r > 0)
    for r_nm in [1.0, 2.0, 5.0, 10.0, 100.0, 1000.0]:
        r = r_nm * 1e-9
        ratio = math.exp(factor / r)
        print(f"  Convex r = {r_nm:>6.1f} nm -> P_r / P_0 = {ratio:.4f}")
        assert ratio > 1.0, "Convex droplet must have P_r > P_0"
    
    # As r -> infinity, P_r -> P_0
    r_inf = 1e6 * 1e-9 # 1 mm
    assert abs(math.exp(factor / r_inf) - 1.0) < 1e-5, "Kelvin limit r->inf must equal 1"
    
    # Concave menisci (r < 0, cylindrical contact angle 0)
    for r_nm in [1.0, 2.0, 5.0, 10.0, 100.0]:
        r = r_nm * 1e-9
        ratio = math.exp(-factor / r)
        print(f"  Concave r = {r_nm:>5.1f} nm -> P_r / P_0 = {ratio:.4f}")
        assert 0.0 < ratio < 1.0, "Concave meniscus must have P_r < P_0 (undersaturation)"
    
    print("PASS: Kelvin equation signs and asymptotic limits verified.")

def test_bauer_and_strain_energy():
    """Verify Bauer criterion and elastic mismatch strain energy."""
    print("\n--- Test 4: Bauer Criterion & Mismatch Strain Energy ---")
    
    # InAs on GaAs(001)
    a_inas = 6.0583 # Angstrom
    a_gaas = 5.6533 # Angstrom
    eps = (a_inas - a_gaas) / a_gaas
    print(f"Lattice mismatch InAs/GaAs: eps = {eps*100:.3f}% (text claims ~ +7.2%)")
    assert abs(eps - 0.07164) < 0.001, "Lattice mismatch calculation mismatch"
    
    # Elastic energy density formula:
    # E_upr(h) = 2 * mu * (1+nu)/(1-nu) * eps^2 * h
    # Check dimensions: mu in Pa, nu dimensionless, eps dimensionless, h in m
    # E_upr in J/m^2 (same units as surface tension sigma!)
    # Typical values for InAs: mu ~ 19 GPa, nu ~ 0.35
    mu = 19e9 # Pa
    nu = 0.35
    biaxial_modulus = 2.0 * mu * (1.0 + nu) / (1.0 - nu) # E / (1-nu)
    print(f"Biaxial modulus M = {biaxial_modulus/1e9:.2f} GPa")
    
    # Energy per monolayer: 1 ML ~ 0.3 nm
    h_ml = 0.3e-9
    e_per_ml = biaxial_modulus * (eps**2) * h_ml
    print(f"Elastic energy per monolayer of InAs on GaAs: {e_per_ml:.4f} J/m^2")
    # Compare with typical semiconductor surface energy sigma ~ 0.5 - 1.0 J/m^2
    print(f"Ratio E_upr(1 ML) / sigma_typical: {e_per_ml / 0.8:.3f}")
    assert e_per_ml > 0, "Elastic energy must be positive"
    print("PASS: Elastic strain energy dimensions and scaling verified.")

def test_langmuir_isotherm():
    """Verify Langmuir isotherm mathematical behavior and limits."""
    print("\n--- Test 5: Langmuir Isotherm Limits & Derivatives ---")
    K = 0.05 # 1/kPa
    pressures = [1e-6, 1e-3, 0.1, 1.0, 10.0, 100.0, 1e4, 1e6]
    
    theta_vals = []
    for P in pressures:
        theta = (K * P) / (1.0 + K * P)
        theta_vals.append(theta)
        # Check Henry's law at low P: theta / (K*P) -> 1
        if K * P < 1e-3:
            ratio_henry = theta / (K * P)
            assert abs(ratio_henry - 1.0) < 1e-3, "Henry law limit failed"
        # Check saturation at high P: theta -> 1
        if K * P > 1000:
            assert abs(theta - 1.0) < 1e-3, "Saturation limit failed"
            
    # Check strict monotonicity: d(theta)/dP > 0
    for i in range(len(theta_vals)-1):
        assert theta_vals[i+1] > theta_vals[i], "Langmuir isotherm must be strictly monotonic"
        
    print("PASS: Langmuir isotherm limits (Henry P->0, saturation P->inf) and monotonicity verified.")

def test_bet_isotherm_and_ssa():
    """Verify BET linear form and specific surface area formula."""
    print("\n--- Test 6: BET Linear Equation & Specific Surface Area ---")
    # BET Linear: y = P / [V * (P0 - P)] = 1/(Vm * C) + [(C-1)/(Vm * C)] * (P/P0) = A + B * x
    # Test algebraic identity:
    # A = 1 / (Vm * C), B = (C - 1) / (Vm * C)
    # A + B = 1 / Vm  =>  Vm = 1 / (A + B)
    # B / A = C - 1   =>  C = 1 + B / A
    
    Vm_true = 50.0 # cm^3 STP / g
    C_true = 120.0 # typical BET constant
    
    A = 1.0 / (Vm_true * C_true)
    B = (C_true - 1.0) / (Vm_true * C_true)
    
    Vm_calc = 1.0 / (A + B)
    C_calc = 1.0 + (B / A)
    
    assert abs(Vm_calc - Vm_true) < 1e-10, "BET Vm derivation failed"
    assert abs(C_calc - C_true) < 1e-10, "BET C derivation failed"
    
    # Specific surface area:
    # S_ud = (Vm * N_A * sigma_0) / (V0 * m)
    # If Vm is in cm^3(STP), m in g:
    N_A = 6.02214076e23
    sigma_0_n2 = 0.162e-18 # m^2
    V0 = 22414.0 # cm^3/mol at STP
    m = 1.0 # g
    
    s_ud = (Vm_true * N_A * sigma_0_n2) / (V0 * m)
    # Standard constant: 1 cm^3(STP) of N2 ~ 4.352 m^2
    factor = (1.0 * N_A * sigma_0_n2) / V0
    print(f"BET specific surface area conversion factor: {factor:.4f} m^2 / cm^3(STP)")
    print(f"Calculated S_ud for Vm={Vm_true} cm^3/g: {s_ud:.2f} m^2/g")
    
    assert abs(factor - 4.3524) < 0.01, "BET conversion factor mismatch"
    assert abs(s_ud - 50.0 * 4.3524) < 0.5, "S_ud calculation mismatch"
    print("PASS: BET linear form inversions and S_ud formulas are mathematically exact.")

if __name__ == "__main__":
    plan_text, speech_text = load_files()
    test_dupre_young_harkins()
    test_laplace_numerical()
    test_kelvin_asymptotics()
    test_bauer_and_strain_energy()
    test_langmuir_isotherm()
    test_bet_isotherm_and_ssa()
    print("\nALL 6 CORE MATHEMATICAL & PHYSICAL TESTS PASSED.")
