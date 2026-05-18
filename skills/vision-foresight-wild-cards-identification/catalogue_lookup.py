#!/usr/bin/env python3
"""
Deterministic P-XXX-NN catalogue lookup for vision-foresight-wild-cards-identification.
No LLM re-inference — codes are fixed from Petersen (1997) as catalogued in
master skill §10 (vision-foresight-wild-cards/SKILL.md).

Usage:
    python3 catalogue_lookup.py "antibiotic resistance"      # fuzzy title match
    python3 catalogue_lookup.py --code P-BIO-01              # code → title
    python3 catalogue_lookup.py --list                       # dump full catalogue
    python3 catalogue_lookup.py --stats                      # category statistics
"""
import sys
import json

# ── Catalogue: Petersen (1997) "Out of the Blue" 78-Wild-Card Catalogue ───────
# Source: Petersen & Steinmüller (2009) V3.0 Chapter 10 Appendix
# Master implementation: vision-foresight-wild-cards/SKILL.md §10
# NOTE on count: Petersen (1997) titles the catalogue "78 Wild Cards".
#   The master §10 extraction yields 79 entries across 6 categories.
#   Category counts as listed: EAS(9)+BIO(10)+GEO(26)+TIU(21)+NTH(8)+SPP(5)=79.
#   The 1-item discrepancy vs original "78" may reflect a category-crossing
#   entry in the original text; until the original is verified, all 79 are coded.

CATALOGUE = {
    # ── EARTH AND SKY (EAS) ─────────────────────────────────────────────────
    "P-EAS-01": {
        "title": "The Earth's Axis Shifts",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-02": {
        "title": "Asteroid or Comet Hits Earth",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-03": {
        "title": "Ice Cap Breaks Up",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-04": {
        "title": "Gulf or Jet Stream Shifts Location Permanently",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-05": {
        "title": "Global Food Shortage",
        "category": "Earth and Sky",
        "steep": ["Env", "S", "E"],
    },
    "P-EAS-06": {
        "title": "Extraordinary West Coast Natural Disaster",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-07": {
        "title": "Rapid Climate Change",
        "category": "Earth and Sky",
        "steep": ["Env"],
    },
    "P-EAS-08": {
        "title": "Collapse of the World's Fisheries",
        "category": "Earth and Sky",
        "steep": ["Env", "E"],
    },
    "P-EAS-09": {
        "title": "Major Break in Alaskan Pipeline",
        "category": "Earth and Sky",
        "steep": ["Env", "E"],
    },
    # ── BIOMEDICAL DEVELOPMENTS (BIO) ────────────────────────────────────────
    "P-BIO-01": {
        "title": "Bacteria Become Immune to Antibiotics",
        "category": "Biomedical Developments",
        "steep": ["T", "S"],
    },
    "P-BIO-02": {
        "title": "Worldwide Epidemic",
        "category": "Biomedical Developments",
        "steep": ["S", "E"],
    },
    "P-BIO-03": {
        "title": "Fetal Sex Selection Becomes the Norm",
        "category": "Biomedical Developments",
        "steep": ["S", "T"],
    },
    "P-BIO-04": {
        "title": "Human Mutation",
        "category": "Biomedical Developments",
        "steep": ["T", "S"],
    },
    "P-BIO-05": {
        "title": "Health and Medical Breakthrough",
        "category": "Biomedical Developments",
        "steep": ["T", "S"],
    },
    "P-BIO-06": {
        "title": "Long-term Side Effects of a Medication Are Discovered",
        "category": "Biomedical Developments",
        "steep": ["T", "S"],
    },
    "P-BIO-07": {
        "title": "Human Cloning Is Perfected",
        "category": "Biomedical Developments",
        "steep": ["T", "S", "Spi"],
    },
    "P-BIO-08": {
        "title": "Life Expectancy Approaches 100",
        "category": "Biomedical Developments",
        "steep": ["T", "S", "E"],
    },
    "P-BIO-09": {
        "title": "Birth Defects Are Eliminated",
        "category": "Biomedical Developments",
        "steep": ["T", "S"],
    },
    "P-BIO-10": {
        "title": "Collapse of the Sperm Count",
        "category": "Biomedical Developments",
        "steep": ["S", "Env"],
    },
    # ── GEOPOLITICAL AND SOCIOLOGICAL CHANGES (GEO) ──────────────────────────
    "P-GEO-01": {"title": "Civil War in the United States", "category": "Geopolitical and Sociological Changes", "steep": ["P", "S"]},
    "P-GEO-02": {"title": "U.S. Economy Fails", "category": "Geopolitical and Sociological Changes", "steep": ["E", "P"]},
    "P-GEO-03": {"title": "No-Carbon Economy Worldwide", "category": "Geopolitical and Sociological Changes", "steep": ["E", "Env", "P"]},
    "P-GEO-04": {"title": "Altruism Outbreak", "category": "Geopolitical and Sociological Changes", "steep": ["S", "Spi"]},
    "P-GEO-05": {"title": "Social Breakdown in the United States", "category": "Geopolitical and Sociological Changes", "steep": ["S", "P"]},
    "P-GEO-06": {"title": "Israel Defeated in War", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-07": {"title": "Collapse of the U.S. Dollar", "category": "Geopolitical and Sociological Changes", "steep": ["E"]},
    "P-GEO-08": {"title": "Economic and/or Environmental Criminals Are Prosecuted", "category": "Geopolitical and Sociological Changes", "steep": ["P", "E", "Env"]},
    "P-GEO-09": {"title": "Rise of an American Strong Man", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-10": {"title": "Stock Market Crash", "category": "Geopolitical and Sociological Changes", "steep": ["E"]},
    "P-GEO-11": {"title": "Civil War between Soviet States Goes Nuclear", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-12": {"title": "Major U.S. Military Unit Mutinies", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-13": {"title": "The Growth of Religious Environmentalism", "category": "Geopolitical and Sociological Changes", "steep": ["Spi", "Env", "S"]},
    "P-GEO-14": {"title": "End of Intergenerational Solidarity", "category": "Geopolitical and Sociological Changes", "steep": ["S", "E"]},
    "P-GEO-15": {"title": "New Age Attitudes Blossom", "category": "Geopolitical and Sociological Changes", "steep": ["S", "Spi"]},
    "P-GEO-16": {"title": "Religious Right Political Party Gains Power", "category": "Geopolitical and Sociological Changes", "steep": ["P", "Spi"]},
    "P-GEO-17": {"title": "Mass Migrations", "category": "Geopolitical and Sociological Changes", "steep": ["S", "P"]},
    "P-GEO-18": {"title": "Africa Unravels", "category": "Geopolitical and Sociological Changes", "steep": ["P", "S", "E"]},
    "P-GEO-19": {"title": "U.S. Government Redesigned", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-20": {"title": "Electronic Cash Enables Tax Revolt in the United States", "category": "Geopolitical and Sociological Changes", "steep": ["E", "T", "P"]},
    "P-GEO-21": {"title": "Western State Secedes from the United States", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-22": {"title": "Illiterate, Dysfunctional New Generation", "category": "Geopolitical and Sociological Changes", "steep": ["S"]},
    "P-GEO-23": {"title": "Collapse of the United Nations", "category": "Geopolitical and Sociological Changes", "steep": ["P"]},
    "P-GEO-24": {"title": "Mexican Economy Fails, United States Takes Over", "category": "Geopolitical and Sociological Changes", "steep": ["E", "P"]},
    "P-GEO-25": {"title": "End of the Nation-state", "category": "Geopolitical and Sociological Changes", "steep": ["P", "S"]},
    "P-GEO-26": {"title": "Society Turns away from the Military", "category": "Geopolitical and Sociological Changes", "steep": ["S", "P"]},
    # ── TECHNOLOGY AND INFRASTRUCTURE UPHEAVAL (TIU) ─────────────────────────
    "P-TIU-01": {"title": "Long-term Global Communications Disruption", "category": "Technology and Infrastructure Upheaval", "steep": ["T"]},
    "P-TIU-02": {"title": "Massive, Lengthy Disruption of National Electrical Supply", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E"]},
    "P-TIU-03": {"title": "Energy Revolution", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E", "Env"]},
    "P-TIU-04": {"title": "Time Travel Invented", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "Spi"]},
    "P-TIU-05": {"title": "Y2K: The Year 2000 Problem", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E"]},
    "P-TIU-06": {"title": "A New Chernobyl", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "Env"]},
    "P-TIU-07": {"title": "Encryption Invalidated", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E", "P"]},
    "P-TIU-08": {"title": "Loss of Intellectual Property Rights", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E", "P"]},
    "P-TIU-09": {"title": "Fuel Cells Replace Internal Combustion Engines", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "Env", "E"]},
    "P-TIU-10": {"title": "Room Temperature Superconductivity Arrives", "category": "Technology and Infrastructure Upheaval", "steep": ["T"]},
    "P-TIU-11": {"title": "Developing Nation Demonstrates Nanotech Weapon", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "P"]},
    "P-TIU-12": {"title": "Cold Fusion Embraced by Developing Country", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E"]},
    "P-TIU-13": {"title": "Global Financial Revolution (E-cash)", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "E"]},
    "P-TIU-14": {"title": "Faster-than-Light Travel", "category": "Technology and Infrastructure Upheaval", "steep": ["T"]},
    "P-TIU-15": {"title": "Virtual Reality, Holography Move Information, Instead of People", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "S"]},
    "P-TIU-16": {"title": "Virtual Reality Revolutionizes Education", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "S"]},
    "P-TIU-17": {"title": "Self-Aware Machine Intelligence Is Developed", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "S", "Spi"]},
    "P-TIU-18": {"title": "Technology Gets out of Hand", "category": "Technology and Infrastructure Upheaval", "steep": ["T"]},
    "P-TIU-19": {"title": "Humans Directly Interface with the Net", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "S"]},
    "P-TIU-20": {"title": "Nanotechnology Takes Off", "category": "Technology and Infrastructure Upheaval", "steep": ["T"]},
    "P-TIU-21": {"title": "Computers/Robots Think Like Humans", "category": "Technology and Infrastructure Upheaval", "steep": ["T", "S"]},
    # ── NEW THREATS AND OLD THREATS FROM NEW SOURCES (NTH) ───────────────────
    "P-NTH-01": {"title": "Information War Breaks Out", "category": "New Threats and Old Threats from New Sources", "steep": ["P", "T"]},
    "P-NTH-02": {"title": "Major Information Systems Disruption", "category": "New Threats and Old Threats from New Sources", "steep": ["T", "E"]},
    "P-NTH-03": {"title": "Nuclear Terrorists Attack the United States", "category": "New Threats and Old Threats from New Sources", "steep": ["P"]},
    "P-NTH-04": {"title": "Terrorism Swamps Government Defenses", "category": "New Threats and Old Threats from New Sources", "steep": ["P"]},
    "P-NTH-05": {"title": "Terrorism Goes Biological", "category": "New Threats and Old Threats from New Sources", "steep": ["P", "S"]},
    "P-NTH-06": {"title": "Computer Manufacturer Blackmails the Country", "category": "New Threats and Old Threats from New Sources", "steep": ["T", "P"]},
    "P-NTH-07": {"title": "Hackers Blackmail the Federal Reserve", "category": "New Threats and Old Threats from New Sources", "steep": ["T", "E"]},
    "P-NTH-08": {"title": "Inner Cities Arm and Revolt", "category": "New Threats and Old Threats from New Sources", "steep": ["P", "S"]},
    # ── SPIRITUAL AND PARANORMAL (SPP) ───────────────────────────────────────
    "P-SPP-01": {"title": "The Arrival of Extraterrestrials", "category": "Spiritual and Paranormal", "steep": ["Spi"]},
    "P-SPP-02": {"title": "The Return of the Awaited One", "category": "Spiritual and Paranormal", "steep": ["Spi", "S"]},
    "P-SPP-03": {"title": "Remote Viewing Becomes Widespread", "category": "Spiritual and Paranormal", "steep": ["Spi", "T"]},
    "P-SPP-04": {"title": "Life is Discovered in Other Dimensions/Realms", "category": "Spiritual and Paranormal", "steep": ["Spi"]},
    "P-SPP-05": {"title": "Future Prediction Becomes Standard Business", "category": "Spiritual and Paranormal", "steep": ["Spi", "E"]},
}

# ── Code → reversed index for fuzzy search ───────────────────────────────────
_TITLE_TO_CODE = {v["title"].lower(): k for k, v in CATALOGUE.items()}


def lookup_by_code(code: str) -> dict | None:
    return CATALOGUE.get(code.upper())


def lookup_by_title(title: str) -> dict | None:
    """Exact and fuzzy title match (case-insensitive, keyword search)."""
    key = title.lower().strip()
    if key in _TITLE_TO_CODE:
        code = _TITLE_TO_CODE[key]
        return {"code": code, **CATALOGUE[code]}
    # Fuzzy: return all entries whose title contains all words in query
    words = key.split()
    matches = []
    for code, entry in CATALOGUE.items():
        t = entry["title"].lower()
        if all(w in t for w in words):
            matches.append({"code": code, **entry})
    return matches if matches else None


def stats() -> dict:
    cats = {}
    for code, entry in CATALOGUE.items():
        cat = entry["category"]
        cats[cat] = cats.get(cat, 0) + 1
    return {
        "total": len(CATALOGUE),
        "categories": cats,
        "note": (
            "Petersen (1997) titles the catalogue '78 Wild Cards'. "
            "Master §10 extraction yields 79 entries. "
            "1-item discrepancy may reflect category-crossing in original text."
        ),
    }


def main():
    args = sys.argv[1:]
    if not args or "--help" in args:
        print(__doc__)
        return
    if "--list" in args:
        for code, entry in CATALOGUE.items():
            print(f"{code}: {entry['title']}")
        return
    if "--stats" in args:
        print(json.dumps(stats(), ensure_ascii=False, indent=2))
        return
    if "--code" in args:
        idx = args.index("--code")
        code = args[idx + 1] if idx + 1 < len(args) else ""
        result = lookup_by_code(code)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else f"Not found: {code}")
        return
    # Default: fuzzy title search
    query = " ".join(args)
    result = lookup_by_title(query)
    print(json.dumps(result, ensure_ascii=False, indent=2) if result else f"No match for: {query}")


if __name__ == "__main__":
    main()
