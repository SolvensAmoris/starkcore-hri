#!/usr/bin/env python3
# STARKCORE-Q v0.3 // COLOR EDITION - DISEÑO QUE VENDE

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
PINK = "\033[95m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

def pretty_bar(value, width=20, is_good=True):
    filled = int(value * width)
    color = GREEN if is_good else RED
    # invert for drift/noise: low is good
    return f"{color}{'█' * filled}{DIM}{'░' * (width - filled)}{RESET}"

def sat_check_ghz(counts, shots, tolerance=0.15):
    def p(s): return counts.get(s, 0) / shots
    ghz_mass = p('000') + p('111')
    balance = abs(p('000') - p('111'))
    noise_mass = sum(p(f"{a}{b}{c}") for a in '01' for b in '01' for c in '01' if f"{a}{b}{c}" not in ['000','111'])
    c1 = ghz_mass > (1.0 - tolerance)
    c2 = balance < tolerance
    c3 = noise_mass < tolerance
    return ghz_mass, balance, noise_mass, c1, c2, c3, (c1 and c2 and c3)

def print_report(name, counts):
    shots = sum(counts.values())
    ghz_mass, balance, noise_mass, c1, c2, c3, sat = sat_check_ghz(counts, shots)
    
    status = f"{GREEN}{BOLD}VALID{RESET}" if sat else f"{RED}{BOLD}FAIL-CLOSED{RESET}"
    icon = f"{GREEN}🦘{RESET}" if sat else f"{RED}💀{RESET}"
    
    print(f"\n{CYAN}┌─ {BOLD}{name}{RESET}{CYAN} ── {shots} shots ──────────────────────┐{RESET}")
    print(f"{CYAN}│{RESET}")
    
    c1_color = GREEN if c1 else RED
    print(f"{CYAN}│{RESET}  CORE 1 [GHZ MASS]   {pretty_bar(ghz_mass, is_good=c1)} {c1_color}{ghz_mass*100:5.1f}%  {c1_color}{'PASS' if c1 else 'FAIL'}{RESET}")
    print(f"{CYAN}│{RESET}  {DIM}   └─ P(000)+P(111) > 85%{RESET}")
    print(f"{CYAN}│{RESET}")
    
    c2_color = GREEN if c2 else RED
    bar2_val = 1-balance
    print(f"{CYAN}│{RESET}  CORE 2 [BALANCE]    {pretty_bar(bar2_val, is_good=c2)} {c2_color}{balance*100:5.1f}% drift  {c2_color}{'PASS' if c2 else 'FAIL'}{RESET}")
    print(f"{CYAN}│{RESET}  {DIM}   └─ |P(000)-P(111)| < 15%{RESET}")
    print(f"{CYAN}│{RESET}")
    
    c3_color = GREEN if c3 else RED
    bar3_val = 1-noise_mass
    print(f"{CYAN}│{RESET}  CORE 3 [ANTIFRAUD]  {pretty_bar(bar3_val, is_good=c3)} {c3_color}{noise_mass*100:5.1f}% noise  {c3_color}{'PASS' if c3 else 'FAIL'}{RESET}")
    print(f"{CYAN}│{RESET}  {DIM}   └─ noise < 15%{RESET}")
    print(f"{CYAN}│{RESET}")
    
    sat_str = f"{GREEN}1 ∧ 1 ∧ 1 = True{RESET}" if sat else f"{RED}{1 if c1 else 0} ∧ {1 if c2 else 0} ∧ {1 if c3 else 0} = False{RESET}"
    print(f"{CYAN}│{RESET}  SAT: {sat_str}")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {icon} VERDICT: {status}")
    if not sat:
        print(f"{CYAN}│{RESET}  {RED}> Ad cuántico mal inyectado. No paga. BLOCK.{RESET}")
    print(f"{CYAN}└──────────────────────────────────────────┘{RESET}")

print(f"{PINK}{BOLD}STARKCORE-Q v0.3{RESET} {DIM}// DEPENDENCY: NONE // PERSISTENCE: EXTREME{RESET}")
print(f"{DIM}Structure over Representation - Verify chain, not computation{RESET}")

print_report("GOOD GHZ", {'000': 4900, '111': 5100})
print_report("FRAUD (ruido)", {'000': 3000, '001': 2000, '010': 2000, '111': 3000})
print_report("BIAS (desbalanceado)", {'000': 8000, '111': 2000})

print(f"\n{PINK}400M years in prod. Baja MX. No cloud. No trust.{RESET}")
