
from typing import Dict, List, Tuple
import os
import time


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(s: str, delay: float = 0.005):
    for ch in s:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


THRESHOLD_LULUS = 0.7  # >= ini dianggap LULUS


RULES = [
    # Strong rule: pendidikan IT + pengalaman >1 + skill coding baik + paham algoritma -> LULUS
    {"conditions": ["sarjana_it", "pengalaman_lebih_1_tahun", "skill_coding_baik", "menguasai_algoritma"],
     "conclusion": "LULUS", "weight": 0.95},

    # Alternatif: pendidikan IT + skill coding sangat baik + teamwork & komunikasi bisa mengimbangi pengalaman
    {"conditions": ["sarjana_it", "skill_coding_baik", "komunikasi_baik", "teamwork_baik"],
     "conclusion": "LULUS", "weight": 0.85},

    # Kandidat non-IT tapi sangat teknikal (python + alg + pengalaman) -> bisa LULUS
    {"conditions": ["sarjana_non_it", "menguasai_python", "pengalaman_lebih_1_tahun", "skill_coding_baik"],
     "conclusion": "LULUS", "weight": 0.8},

    # Jika tidak berpengalaman dan skill coding buruk -> kuat tidak lulus
    {"conditions": ["tidak_pengalaman", "skill_coding_buruk"], "conclusion": "TIDAK_LULUS", "weight": 0.9},

    # Jika bukan IT dan tidak berpengalaman -> cenderung tidak lulus
    {"conditions": ["sarjana_non_it", "tidak_pengalaman"], "conclusion": "TIDAK_LULUS", "weight": 0.8},

    # Rule tambahan: pengalaman + penguasaan backend -> mendukung LULUS
    {"conditions": ["pengalaman_lebih_1_tahun", "menguasai_backend", "skill_coding_baik"],
     "conclusion": "LULUS", "weight": 0.8},

    # Rule pendukung: paham algoritma + menguasai_python + skill coding baik -> dukungan sedang
    {"conditions": ["menguasai_python", "menguasai_algoritma", "skill_coding_baik"],
     "conclusion": "LULUS", "weight": 0.7},
]


def parse_answer_to_cf(ans: str) -> float:
    if not ans:
        return 0.0
    a = ans.strip().lower()
    if a in ("ya", "y", "yes"):
        return 0.9
    if a in ("tidak", "t", "no", "n"):
        return 0.1
    # coba parse angka
    try:
        val = float(a)
        if 0 <= val <= 100:
            return max(0.0, min(1.0, val / 100.0))
    except ValueError:
        pass
    return 0.0

def combine_cf(cf_old: float, cf_new: float) -> float:
    return cf_old + cf_new * (1.0 - cf_old)


def evaluate_rules(facts_cf: Dict[str, float]) -> Tuple[Dict[str, float], List[Tuple[str, float, Dict[str, float]]]]:
    conclusions_cf: Dict[str, float] = {}
    log_rules: List[Tuple[str, float, Dict[str, float]]] = []

    for idx, rule in enumerate(RULES):
        premises = rule["conditions"]
        premise_cfs = {p: facts_cf.get(p, 0.0) for p in premises}

        antecedent_cf = min(premise_cfs.values()) if premise_cfs else 0.0
        rule_support_cf = antecedent_cf * float(rule.get("weight", 1.0))
        if rule_support_cf > 0:
            concl = rule["conclusion"]
            prev = conclusions_cf.get(concl, 0.0)
            combined = combine_cf(prev, rule_support_cf)
            conclusions_cf[concl] = combined
            log_rules.append((f"rule_{idx+1}", rule_support_cf, premise_cfs))

    return conclusions_cf, log_rules


def ask_user_facts() -> Dict[str, float]:
    clear()
    slow_print("=== SISTEM PAKAR REKRUTMEN (CF + Forward Chaining) ===\n", 0.002)
    slow_print("Jawab dengan 'ya'/'tidak' atau masukkan angka 0-100 sebagai tingkat keyakinan.")
    slow_print("Contoh: 'ya' -> 90% yakin, '70' -> 70% yakin\n")

    facts: Dict[str, float] = {}

    a = input("Apakah Anda lulusan S1 Informatika / Teknik Komputer? ")
    if parse_answer_to_cf(a) >= 0.5:
        facts["sarjana_it"] = parse_answer_to_cf(a)
        facts["sarjana_informatika"] = parse_answer_to_cf(a)
    else:
        b = input("Jika tidak, apakah Anda lulusan non-IT? (jawab ya jika bukan IT) ")
        if parse_answer_to_cf(b) >= 0.5:
            facts["sarjana_non_it"] = parse_answer_to_cf(b)

    
    a = input("Apakah Anda memiliki pengalaman kerja di bidang software engineer lebih dari setahun? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) >= 0.5:
        facts["pengalaman_lebih_1_tahun"] = parse_answer_to_cf(a)
    else:
        facts["tidak_pengalaman"] = parse_answer_to_cf(a)

    
    a = input("Apakah Anda menguasai bahasa pemrograman Python? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) > 0:
        facts["menguasai_python"] = parse_answer_to_cf(a)

    a = input("Apakah Anda menguasai konsep algoritma dan struktur data dengan baik? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) > 0:
        facts["menguasai_algoritma"] = parse_answer_to_cf(a)

    a = input("Apakah Anda berpengalaman di pengembangan backend (server-side)? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) > 0:
        facts["menguasai_backend"] = parse_answer_to_cf(a)

    
    a = input("Apakah Anda memiliki kemampuan komunikasi yang baik? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) > 0:
        facts["komunikasi_baik"] = parse_answer_to_cf(a)

    a = input("Apakah Anda mampu bekerja dalam tim dengan baik? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) > 0:
        facts["teamwork_baik"] = parse_answer_to_cf(a)

    
    a = input("Apakah Anda mempunyai skill coding yang baik? (ya/tidak/0-100) ")
    if parse_answer_to_cf(a) >= 0.5:
        facts["skill_coding_baik"] = parse_answer_to_cf(a)
    else:
        facts["skill_coding_buruk"] = parse_answer_to_cf(a)

    return facts

# ---------------------------
# Main
# ---------------------------
def main():
    facts = ask_user_facts()
    conclusions, log_rules = evaluate_rules(facts)

    clear()
    slow_print("=== HASIL ANALISIS SISTEM PAKAR (CF) ===\n", 0.002)

    
    cf_lulus = conclusions.get("LULUS", 0.0)
    cf_tidak = conclusions.get("TIDAK_LULUS", 0.0)

    if cf_lulus >= THRESHOLD_LULUS:
        slow_print(f"✅ KEPUTUSAN: ANDA DINYATAKAN LULUS (keyakinan {cf_lulus:.2f})")
    else:
        slow_print(f"❌ KEPUTUSAN: ANDA TIDAK LULUS (keyakinan LULUS {cf_lulus:.2f})")


    print("\nFakta yang dimasukkan (fact: CF):")
    for k, v in facts.items():
        print(f" - {k}: {v:.3f}")

if __name__ == "__main__":
    main()
