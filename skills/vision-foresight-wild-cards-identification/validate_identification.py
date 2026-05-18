#!/usr/bin/env python3
"""
Deterministic validator for vision-foresight-wild-cards-identification output.
Enforces structural rules without LLM re-inference.

Usage (Claude Code Bash tool):
    echo '<json>' | python3 validate_identification.py --stdin
    python3 validate_identification.py output.json
"""
import json
import sys

# ── Constants ─────────────────────────────────────────────────────────────────
VALID_STEEP_TAGS = {"S", "T", "E", "Env", "P", "Spi"}
VALID_TYPES = {"1", "2", "3"}
VALID_SOURCE_METHODS = {"brainstorm", "expert", "survey", "historical", "sf"}
VALID_QUALITY = {"+", "-", "±"}
VALID_VRMP_TIERS = {"R-1", "R-2", "R-3"}

MIN_CANDIDATES = 20
MAX_CANDIDATES = 40
TYPE3_MIN_RATIO = 0.20      # PDF: "The number of Wild Cards – at least in the third category – is essentially infinite."
MIN_LEAD_INDICATORS = 3
MAX_LEAD_INDICATORS = 5

# ── Petersen P-XXX-NN lookup (deterministic — no LLM re-inference) ────────────
PETERSEN_CODES = {
    # EARTH AND SKY (9)
    "P-EAS-01": "The Earth's Axis Shifts",
    "P-EAS-02": "Asteroid or Comet Hits Earth",
    "P-EAS-03": "Ice Cap Breaks Up",
    "P-EAS-04": "Gulf or Jet Stream Shifts Location Permanently",
    "P-EAS-05": "Global Food Shortage",
    "P-EAS-06": "Extraordinary West Coast Natural Disaster",
    "P-EAS-07": "Rapid Climate Change",
    "P-EAS-08": "Collapse of the World's Fisheries",
    "P-EAS-09": "Major Break in Alaskan Pipeline",
    # BIOMEDICAL DEVELOPMENTS (10)
    "P-BIO-01": "Bacteria Become Immune to Antibiotics",
    "P-BIO-02": "Worldwide Epidemic",
    "P-BIO-03": "Fetal Sex Selection Becomes the Norm",
    "P-BIO-04": "Human Mutation",
    "P-BIO-05": "Health and Medical Breakthrough",
    "P-BIO-06": "Long-term Side Effects of a Medication Are Discovered",
    "P-BIO-07": "Human Cloning Is Perfected",
    "P-BIO-08": "Life Expectancy Approaches 100",
    "P-BIO-09": "Birth Defects Are Eliminated",
    "P-BIO-10": "Collapse of the Sperm Count",
    # GEOPOLITICAL AND SOCIOLOGICAL CHANGES (26 per master §10 list)
    "P-GEO-01": "Civil War in the United States",
    "P-GEO-02": "U.S. Economy Fails",
    "P-GEO-03": "No-Carbon Economy Worldwide",
    "P-GEO-04": "Altruism Outbreak",
    "P-GEO-05": "Social Breakdown in the United States",
    "P-GEO-06": "Israel Defeated in War",
    "P-GEO-07": "Collapse of the U.S. Dollar",
    "P-GEO-08": "Economic and/or Environmental Criminals Are Prosecuted",
    "P-GEO-09": "Rise of an American Strong Man",
    "P-GEO-10": "Stock Market Crash",
    "P-GEO-11": "Civil War between Soviet States Goes Nuclear",
    "P-GEO-12": "Major U.S. Military Unit Mutinies",
    "P-GEO-13": "The Growth of Religious Environmentalism",
    "P-GEO-14": "End of Intergenerational Solidarity",
    "P-GEO-15": "New Age Attitudes Blossom",
    "P-GEO-16": "Religious Right Political Party Gains Power",
    "P-GEO-17": "Mass Migrations",
    "P-GEO-18": "Africa Unravels",
    "P-GEO-19": "U.S. Government Redesigned",
    "P-GEO-20": "Electronic Cash Enables Tax Revolt in the United States",
    "P-GEO-21": "Western State Secedes from the United States",
    "P-GEO-22": "Illiterate, Dysfunctional New Generation",
    "P-GEO-23": "Collapse of the United Nations",
    "P-GEO-24": "Mexican Economy Fails, United States Takes Over",
    "P-GEO-25": "End of the Nation-state",
    "P-GEO-26": "Society Turns away from the Military",
    # TECHNOLOGY AND INFRASTRUCTURE UPHEAVAL (21 per master §10 list)
    "P-TIU-01": "Long-term Global Communications Disruption",
    "P-TIU-02": "Massive, Lengthy Disruption of National Electrical Supply",
    "P-TIU-03": "Energy Revolution",
    "P-TIU-04": "Time Travel Invented",
    "P-TIU-05": "Y2K: The Year 2000 Problem",
    "P-TIU-06": "A New Chernobyl",
    "P-TIU-07": "Encryption Invalidated",
    "P-TIU-08": "Loss of Intellectual Property Rights",
    "P-TIU-09": "Fuel Cells Replace Internal Combustion Engines",
    "P-TIU-10": "Room Temperature Superconductivity Arrives",
    "P-TIU-11": "Developing Nation Demonstrates Nanotech Weapon",
    "P-TIU-12": "Cold Fusion Embraced by Developing Country",
    "P-TIU-13": "Global Financial Revolution (E-cash)",
    "P-TIU-14": "Faster-than-Light Travel",
    "P-TIU-15": "Virtual Reality, Holography Move Information, Instead of People",
    "P-TIU-16": "Virtual Reality Revolutionizes Education",
    "P-TIU-17": "Self-Aware Machine Intelligence Is Developed",
    "P-TIU-18": "Technology Gets out of Hand",
    "P-TIU-19": "Humans Directly Interface with the Net",
    "P-TIU-20": "Nanotechnology Takes Off",
    "P-TIU-21": "Computers/Robots Think Like Humans",
    # NEW THREATS (8)
    "P-NTH-01": "Information War Breaks Out",
    "P-NTH-02": "Major Information Systems Disruption",
    "P-NTH-03": "Nuclear Terrorists Attack the United States",
    "P-NTH-04": "Terrorism Swamps Government Defenses",
    "P-NTH-05": "Terrorism Goes Biological",
    "P-NTH-06": "Computer Manufacturer Blackmails the Country",
    "P-NTH-07": "Hackers Blackmail the Federal Reserve",
    "P-NTH-08": "Inner Cities Arm and Revolt",
    # SPIRITUAL AND PARANORMAL (5)
    "P-SPP-01": "The Arrival of Extraterrestrials",
    "P-SPP-02": "The Return of the Awaited One",
    "P-SPP-03": "Remote Viewing Becomes Widespread",
    "P-SPP-04": "Life is Discovered in Other Dimensions/Realms",
    "P-SPP-05": "Future Prediction Becomes Standard Business",
}
# Catalogue count per category
PETERSEN_CATEGORY_COUNTS = {
    "EAS": 9, "BIO": 10, "GEO": 26, "TIU": 21, "NTH": 8, "SPP": 5
}
PETERSEN_TOTAL = sum(PETERSEN_CATEGORY_COUNTS.values())  # 79 per master §10 listing

# ── Validator ─────────────────────────────────────────────────────────────────

def validate(output: dict) -> dict:
    errors = []
    warnings = []

    id_out = output.get("identification_output", {})
    candidates = id_out.get("candidates", [])
    meta = id_out.get("meta", {})
    cat_summary = id_out.get("catalogue_summary", {})
    n = len(candidates)

    # 1. Candidate count
    if n < MIN_CANDIDATES:
        errors.append(f"FAIL count_low: {n} candidates < minimum {MIN_CANDIDATES}")
    elif n > MAX_CANDIDATES:
        errors.append(f"FAIL count_high: {n} candidates > maximum {MAX_CANDIDATES}")

    # 2. Type 3 ratio (PDF mandate)
    type_counts = {"1": 0, "2": 0, "3": 0}
    for c in candidates:
        t = str(c.get("type", ""))
        if t in type_counts:
            type_counts[t] += 1
    type3_ratio = type_counts["3"] / n if n > 0 else 0
    if type3_ratio < TYPE3_MIN_RATIO:
        errors.append(
            f"FAIL type3_ratio: {type3_ratio:.1%} < {TYPE3_MIN_RATIO:.0%} "
            f"(PDF: 'number of Wild Cards in third category is essentially infinite')"
        )

    # 3. Required fields per candidate
    required_fields = [
        "id", "title", "domain", "type", "source_method",
        "petersen_ref", "steinmuller_ref", "seed_description",
        "positive_or_negative", "lead_indicators",
    ]
    seen_ids = set()
    for i, c in enumerate(candidates, 1):
        cid = c.get("id", f"WC-{i:03d}")
        # Duplicate ID check
        if cid in seen_ids:
            errors.append(f"FAIL dup_id: '{cid}' appears more than once")
        seen_ids.add(cid)

        for field in required_fields:
            if field not in c:
                errors.append(f"FAIL missing_field: {cid} missing '{field}'")

        # type
        if str(c.get("type", "")) not in VALID_TYPES:
            errors.append(f"FAIL invalid_type: {cid} type='{c.get('type')}'")

        # source_method
        if c.get("source_method", "") not in VALID_SOURCE_METHODS:
            errors.append(
                f"FAIL invalid_source_method: {cid} source_method='{c.get('source_method')}'"
            )

        # positive_or_negative
        if c.get("positive_or_negative", "") not in VALID_QUALITY:
            errors.append(
                f"FAIL invalid_quality: {cid} positive_or_negative='{c.get('positive_or_negative')}'"
            )

        # lead_indicators count
        li = c.get("lead_indicators", [])
        if not isinstance(li, list):
            errors.append(f"FAIL lead_indicators_type: {cid} must be list")
        elif not (MIN_LEAD_INDICATORS <= len(li) <= MAX_LEAD_INDICATORS):
            errors.append(
                f"FAIL lead_indicators_count: {cid} has {len(li)}, "
                f"required [{MIN_LEAD_INDICATORS},{MAX_LEAD_INDICATORS}]"
            )

        # STEEP tag validation
        domain_str = c.get("domain", "")
        tags = [t.strip() for t in domain_str.replace("+", " ").split() if t.strip()]
        for tag in tags:
            if tag not in VALID_STEEP_TAGS:
                warnings.append(f"WARN unknown_steep_tag: {cid} tag='{tag}' not in {VALID_STEEP_TAGS}")

        # petersen_ref format — strip "(adapted)" suffix before lookup
        pref = c.get("petersen_ref", "")
        if pref != "new":
            # Strip allowed suffix "(adapted)" before code lookup
            pref_base = pref.replace(" (adapted)", "").strip()
            if pref_base not in PETERSEN_CODES:
                warnings.append(
                    f"WARN petersen_ref_unknown: {cid} ref='{pref}' base='{pref_base}' not in 79-code lookup"
                )

        # seed_description length (2-3 sentences guideline)
        seed = c.get("seed_description", "")
        if len(seed) < 30:
            warnings.append(f"WARN seed_too_short: {cid} seed_description < 30 chars")

    # 4. meta fields
    for field in ["target_group", "catalogue_source", "surprise_type_mix", "n_candidates", "method_breakdown"]:
        if field not in meta:
            errors.append(f"FAIL missing_meta: 'meta.{field}' is absent")

    # 5. surprise_type_mix sums to ~100%
    stm = meta.get("surprise_type_mix", {})
    if stm:
        total_pct = sum(stm.values())
        if abs(total_pct - 100) > 2:
            errors.append(f"FAIL surprise_mix_sum: {total_pct} ≠ 100")

    # 6. n_candidates matches actual
    if meta.get("n_candidates") is not None and meta.get("n_candidates") != n:
        errors.append(
            f"FAIL n_candidates_mismatch: meta.n_candidates={meta.get('n_candidates')} ≠ actual={n}"
        )

    # 7. method_breakdown keys
    mb = meta.get("method_breakdown", {})
    for method in VALID_SOURCE_METHODS:
        if method not in mb:
            errors.append(f"FAIL missing_method_breakdown: '{method}' not in meta.method_breakdown")

    # 8. method_breakdown count consistency
    mb_total = sum(mb.values()) if mb else 0
    if mb and mb_total != n:
        warnings.append(
            f"WARN method_breakdown_sum: sum({mb_total}) ≠ n_candidates({n})"
        )

    # 9. catalogue_summary fields
    for field in ["new_invented", "petersen_adapted", "steinmuller_adapted", "historical_analogy", "sf_inspired"]:
        if field not in cat_summary:
            errors.append(f"FAIL missing_catalogue_summary: '{field}' absent")

    # 10. VRMP tier in return block
    vrmp = output.get("vrmp_tier", "")
    if vrmp not in VALID_VRMP_TIERS:
        errors.append(f"FAIL vrmp_tier: '{vrmp}' not in {VALID_VRMP_TIERS}")

    # 11. source_trail present
    if not output.get("source_trail"):
        warnings.append("WARN source_trail: empty or absent — VRMP requires source citations")

    # 12. next_skill field
    if output.get("next_skill") != "vision-foresight-wild-cards-assessment":
        errors.append(
            f"FAIL next_skill: must be 'vision-foresight-wild-cards-assessment', "
            f"got '{output.get('next_skill')}'"
        )

    # Summary
    return {
        "pass": len(errors) == 0,
        "n_candidates": n,
        "type3_ratio": f"{type3_ratio:.1%}",
        "type_distribution": {k: f"{v/n:.1%}" for k, v in type_counts.items()} if n else {},
        "errors": errors,
        "warnings": warnings,
        "petersen_catalogue_total": PETERSEN_TOTAL,
    }


def main():
    if "--stdin" in sys.argv:
        data = json.load(sys.stdin)
    elif len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        print("Usage: validate_identification.py <output.json>  OR  --stdin", file=sys.stderr)
        sys.exit(2)

    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
