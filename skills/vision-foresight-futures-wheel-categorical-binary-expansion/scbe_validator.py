#!/usr/bin/env python3
"""
scbe_validator.py — SCBE (STEEPS Categorical Binary Expansion) 전용 결정론 검증기.

할루시네이션 구조적 차단 대상:
  - 노드 수 계산 및 검증 (per ring / per category / total with center)
  - 카테고리 균형 감사 (variance ±0 강제)
  - 균일 fan-out 검증 (정확히 2 children, senary leaf 제외)
  - Node ID 결정론 생성 및 파싱
  - Lineage path 깊이·형식 검증
  - SRS (Sewongjima Reversal Score) — 중립 부호 처리 포함 정밀 판정
  - PRRG SCBE-특화 최소 검색·아날로그 수 계산
  - Cross-domain influence matrix 계산
  - 최종 품질 게이트 (Success Metrics 일괄 검증)

CLI 사용법:
  python3 scbe_validator.py <command> '<json_args>'

Available commands:
  validate_node_counts    — SCBE 전체 노드 수 결정론 검증
  balance_audit           — 카테고리별 노드 균형 검사
  generate_id             — 결정론 Node ID 생성
  parse_id                — Node ID 파싱
  validate_lineage        — lineage path 깊이·형식 검증
  validate_fanout         — fan-out 수 강제 검증 (정확히 2)
  srs_reversal_rule       — 세옹지마 역전 판정 (single pair)
  srs_category            — 단일 카테고리 SRS 검증
  prrg_gate               — SCBE 특화 PRRG 최소 검색 수
  cross_domain_matrix     — cross-domain influence matrix 계산
  final_quality_gate      — 최종 품질 게이트 (전 항목 일괄 검증)

Note:
  마스터 스킬의 wheel_math.py (../vision-foresight-futures-wheel/wheel_math.py) 에도
  scbe_node_count, srs_score, prrg_min_searches 등이 있으나,
  본 validator는 SCBE 특화 상세 검증 (카테고리 균형, ID 형식, fan-out 등)을 담당.
"""

import json
import sys
import re

# ---------------------------------------------------------------------------
# 상수 정의 (변경 금지 — SKILL.md 사양과 1:1 매핑)
# ---------------------------------------------------------------------------

STEEPS_CATEGORIES = [
    "Society", "Technology", "Economy",
    "Environment", "Politics", "Spirituality"
]

V2_8_SECTOR = [
    "Political", "Cultural", "Environmental", "Psychological",
    "Technological", "Educational", "Public Welfare", "Economic"
]

RING_PREFIXES = {
    1: "P",    # Primary
    2: "S",    # Secondary
    3: "T",    # Tertiary
    4: "Q",    # Quaternary
    5: "Qn",   # Quinary
    6: "Sn",   # Senary
}
RING_PREFIX_TO_NUM = {v: k for k, v in RING_PREFIXES.items()}

STEEPS_LETTERS = {
    "Society":     "S",
    "Technology":  "T",
    "Economy":     "E",
    "Environment": "Env",
    "Politics":    "P",
    "Spirituality": "Sp",
}
STEEPS_LETTER_TO_NAME = {v: k for k, v in STEEPS_LETTERS.items()}

RING_NAMES = {
    1: "Primary", 2: "Secondary", 3: "Tertiary",
    4: "Quaternary", 5: "Quinary", 6: "Senary"
}

# Lineage 형식: "1"→ring1, "1a"→ring2, "1a1"→ring3, "1a1b"→ring4, ...
# Pattern: starts with "1", then alternates (a|b)(1|2) pairs, optional trailing (a|b)
LINEAGE_PATTERN = re.compile(r'^1([ab][12])*[ab]?$')

# SRS 기준
SRS_EXCELLENT_THRESHOLD = 1.5
SRS_ACCEPTABLE_THRESHOLD = 1.0
FORCED_REVERSAL_REQUIRED_RATE = 0.50  # 50% 강제

# SCBE PRRG 최솟값 (per category × n_categories for types 1-3, fixed for 4-6)
SCBE_PRRG_SPEC = {
    1: {"type": "per_category", "base": 1,
        "description": "Gate_P1_Pre: WebSearch 카테고리당 1 (STEEPS6→6, V2_8→8)"},
    2: {"type": "per_category", "base": 1,
        "description": "Gate_P2_Pre: WebSearch 카테고리당 1"},
    3: {"type": "per_category", "base": 1, "extra": "historical analog per category",
        "description": "Gate_P3_Pre: Historical analog 카테고리당 1"},
    4: {"type": "fixed", "base": 3, "extra": "backlash analog per category",
        "description": "Gate_P4_Pre: WebSearch ≥3 + backlash analog 카테고리당 1"},
    5: {"type": "fixed", "base": 3, "extra": "paradigm shift analog per category",
        "description": "Gate_P5_Pre: WebSearch ≥3 + paradigm shift analog 카테고리당 1"},
    6: {"type": "fixed", "base": 2, "extra": "civilizational analog (모든 카테고리 공유)",
        "description": "Gate_P6_Pre: WebSearch ≥2 + civilizational analog"},
}


# ---------------------------------------------------------------------------
# 1. 노드 수 결정론 검증
# ---------------------------------------------------------------------------

def _ring_count(n_primary: int, ring: int, fan_out: int = 2) -> int:
    """ring r의 노드 수 = n_primary × fan_out^(r-1)"""
    return n_primary * (fan_out ** (ring - 1))


def validate_node_counts(n_primary: int = 6, rings: int = 6, fan_out: int = 2) -> dict:
    """
    SCBE 전체 노드 수 결정론 검증.
    total_with_center = 1 (center) + sum_{r=1}^{rings} n_primary × fan_out^(r-1)
    per_category_subtree = sum_{r=1}^{rings} fan_out^(r-1)  (= 2^0+2^1+...+2^(rings-1) = 2^rings - 1)
    """
    if n_primary < 1 or rings < 1 or fan_out < 2:
        raise ValueError("n_primary≥1, rings≥1, fan_out≥2 required")

    ring_counts = {RING_NAMES[r]: _ring_count(n_primary, r, fan_out) for r in range(1, rings + 1)}
    subtotal = sum(ring_counts.values())
    total_with_center = 1 + subtotal
    per_category = sum(fan_out ** (r - 1) for r in range(1, rings + 1))  # = 2^rings - 1

    formula_parts = " + ".join(str(_ring_count(n_primary, r, fan_out)) for r in range(1, rings + 1))

    return {
        "n_primary": n_primary,
        "rings": rings,
        "fan_out": fan_out,
        "center_node": 1,
        "ring_counts": ring_counts,
        "subtotal_without_center": subtotal,
        "total_with_center": total_with_center,
        "per_category_subtree": per_category,
        "formula": f"1(center) + {formula_parts} = {total_with_center}",
        "balance_formula": (
            f"{n_primary} categories × {per_category} nodes/category "
            f"= {n_primary * per_category} (+1 center = {total_with_center})"
        ),
        "senary_count": ring_counts.get("Senary", 0),
    }


# ---------------------------------------------------------------------------
# 2. 카테고리 균형 감사
# ---------------------------------------------------------------------------

def balance_audit(category_counts: dict) -> dict:
    """
    카테고리 균형 검사 (허용 분산 ±0).
    category_counts: {"Society": 63, "Technology": 63, ...}

    expected_per_category: 최빈값(mode) 사용.
      - 정상 시: 모든 값이 동일 → mode = 그 값
      - 위반 시: 가장 많이 등장하는 값을 expected로 사용해 이탈 노드 식별
    """
    if not category_counts:
        return {"error": "category_counts is empty"}

    counts = list(category_counts.values())
    variance = max(counts) - min(counts)

    # mode: 가장 빈번한 값 (ties 시 최솟값 선택 — 결정론적)
    from collections import Counter
    count_freq = Counter(counts)
    max_freq = max(count_freq.values())
    expected = min(k for k, v in count_freq.items() if v == max_freq)

    violations = {cat: cnt for cat, cnt in category_counts.items() if cnt != expected}

    return {
        "expected_per_category": expected,
        "actual_counts": category_counts,
        "variance": variance,
        "tolerance": 0,
        "violations": violations,
        "pass": variance == 0,
        "verdict": (
            "BALANCE PASS (±0 완벽 균형)"
            if variance == 0
            else f"BALANCE FAIL: variance={variance}, violations={violations}"
        ),
    }


# ---------------------------------------------------------------------------
# 3. Node ID 생성 및 파싱 (결정론)
# ---------------------------------------------------------------------------

def generate_id(ring: int, category: str, lineage_path: str) -> dict:
    """
    결정론적 Node ID 생성.
    ring: 1-6
    category: "Society" | "Technology" | "Economy" | "Environment" | "Politics" | "Spirituality"
    lineage_path: "1" | "1a" | "1a1" | ... | "1a1a1a"

    Returns: {"node_id": "Sn_Sp_1a1a1a", "valid": True, ...}
    """
    ring_prefix = RING_PREFIXES.get(ring)
    if ring_prefix is None:
        raise ValueError(f"ring must be 1-6, got {ring}")
    cat_letter = STEEPS_LETTERS.get(category)
    if cat_letter is None:
        raise ValueError(f"Unknown category: '{category}'. Valid: {STEEPS_CATEGORIES}")
    lineage_check = validate_lineage(lineage_path)
    if not lineage_check["valid"]:
        raise ValueError(f"Invalid lineage_path: '{lineage_path}'. {lineage_check}")
    if lineage_check["depth"] != ring:
        raise ValueError(
            f"lineage_path depth ({lineage_check['depth']}) ≠ ring ({ring}). "
            f"Ring {ring} requires depth {ring} lineage."
        )
    node_id = f"{ring_prefix}_{cat_letter}_{lineage_path}"
    return {
        "node_id": node_id,
        "ring": ring,
        "ring_name": RING_NAMES[ring],
        "category": category,
        "category_letter": cat_letter,
        "lineage_path": lineage_path,
        "valid": True,
    }


def parse_id(node_id: str) -> dict:
    """
    Node ID 파싱.
    "Sn_Sp_1a1a1a" → {ring:6, ring_name:"Senary", category:"Spirituality", lineage:"1a1a1a"}

    주의: "S_S_1a" → ring=2(Secondary), category="Society" (prefix 우선 매핑)
    ID 충돌 해소 규칙: ring_prefix가 먼저 오므로 ring prefix 매핑 우선.
    """
    parts = node_id.split("_", 2)  # max 3 parts: ring_prefix, cat_letter, lineage
    if len(parts) < 3:
        return {"error": f"Invalid ID: '{node_id}'. Expected ring_cat_lineage.", "valid": False}

    ring_prefix = parts[0]
    cat_letter = parts[1]
    lineage = parts[2]

    ring_num = RING_PREFIX_TO_NUM.get(ring_prefix)
    category = STEEPS_LETTER_TO_NAME.get(cat_letter)
    lineage_info = validate_lineage(lineage)

    return {
        "node_id": node_id,
        "ring_prefix": ring_prefix,
        "ring": ring_num,
        "ring_name": RING_NAMES.get(ring_num, "Unknown"),
        "category_letter": cat_letter,
        "category": category,
        "lineage": lineage,
        "lineage_depth": lineage_info.get("depth"),
        "depth_ring_match": lineage_info.get("depth") == ring_num,
        "valid": ring_num is not None and category is not None and lineage_info.get("valid", False),
        "parse_notes": (
            "P = Primary ring / Politics category — ring_prefix takes priority."
            if ring_prefix == "P" else
            "S = Secondary ring / Society category — ring_prefix takes priority."
            if ring_prefix == "S" else
            "T = Tertiary ring / Technology category — ring_prefix takes priority."
            if ring_prefix == "T" else ""
        ),
    }


# ---------------------------------------------------------------------------
# 4. Lineage path 형식·깊이 검증
# ---------------------------------------------------------------------------

def validate_lineage(lineage: str) -> dict:
    """
    Lineage path 검증.
    Valid pattern: ^1([ab][12])*[ab]?$
    Depth = len(lineage)  (각 문자가 정확히 한 차수를 표현)

    Examples:
      "1"       → depth 1 (Primary)
      "1a"      → depth 2 (Secondary)
      "1a1"     → depth 3 (Tertiary)
      "1a1b"    → depth 4 (Quaternary)
      "1a1b2"   → depth 5 (Quinary)
      "1a1b2a"  → depth 6 (Senary)
    """
    if not lineage:
        return {"lineage": lineage, "depth": 0, "valid": False, "error": "Empty lineage"}

    valid_pattern = bool(LINEAGE_PATTERN.match(lineage))
    depth = len(lineage)
    valid_depth = 1 <= depth <= 6

    return {
        "lineage": lineage,
        "depth": depth,
        "valid_pattern": valid_pattern,
        "valid_depth": valid_depth,
        "valid": valid_pattern and valid_depth,
        "expected_ring": depth,
    }


# ---------------------------------------------------------------------------
# 5. Fan-out 검증
# ---------------------------------------------------------------------------

def validate_fanout(node_id: str, children: list) -> dict:
    """
    Fan-out 강제 검증: senary leaf(ring=6) 제외 모든 노드는 정확히 2 children.
    node_id: 부모 노드 ID
    children: 자식 노드 ID 리스트
    """
    parsed = parse_id(node_id)
    ring = parsed.get("ring", 0)

    if ring == 6:
        return {
            "node_id": node_id,
            "ring": ring,
            "is_leaf": True,
            "children_count": len(children),
            "pass": len(children) == 0,
            "verdict": (
                "Senary leaf — no children required (PASS)"
                if len(children) == 0
                else f"WARN: senary leaf has {len(children)} children (should be 0)"
            ),
        }

    expected = 2
    actual = len(children)
    pass_check = actual == expected

    return {
        "node_id": node_id,
        "ring": ring,
        "ring_name": RING_NAMES.get(ring, "?"),
        "is_leaf": False,
        "children_count": actual,
        "expected": expected,
        "children": children,
        "pass": pass_check,
        "verdict": (
            f"Fan-out PASS: exactly {actual} == {expected} children"
            if pass_check
            else f"Fan-out FAIL: {actual} children ≠ {expected} (SCBE uniform 2-fan-out violated)"
        ),
    }


# ---------------------------------------------------------------------------
# 6. SRS (Sewongjima Reversal Score) — 중립 처리 포함 정밀 판정
# ---------------------------------------------------------------------------

SIGN_MAP = {
    "🟢": "+", "+": "+", "positive": "+", "1": "+", 1: "+",
    "🔴": "-", "-": "-", "negative": "-", "-1": "-", -1: "-",
    "🟡": "0", "0": "0", "neutral": "0", 0: "0",
}


def srs_reversal_rule(parent_sign, child_sign) -> dict:
    """
    세옹지마 역전 판정 (결정론).

    규칙:
      REVERSAL = True  iff  parent='+' AND child='-'
                       OR   parent='-' AND child='+'
      REVERSAL = False if   parent='0' (중립은 방향 없음 → 역전 카운트 불가)
                 False if   child='0'  (중립 자식은 역전 아님)
                 False if   same sign

    이 규칙은 Pacinelli 세옹지마 원칙의 '완전한 부호 반전'만 역전으로 인정하는
    보수적(엄격한) 기준으로, 중립→음이나 양→중립을 역전으로 카운트하면
    실제 비선형성을 과장할 수 있어 채택하지 않음.
    """
    p = SIGN_MAP.get(parent_sign, str(parent_sign))
    c = SIGN_MAP.get(child_sign, str(child_sign))
    reversal = (p == "+" and c == "-") or (p == "-" and c == "+")

    rule_explanation = (
        "reversal: + → - (positive→negative full flip)"
        if (p == "+" and c == "-") else
        "reversal: - → + (negative→positive full flip)"
        if (p == "-" and c == "+") else
        "not reversal: neutral parent (🟡 → any: no direction to reverse from)"
        if p == "0" else
        "not reversal: neutral child (any → 🟡: no full flip)"
        if c == "0" else
        "not reversal: same sign"
    )

    return {
        "parent_sign": str(parent_sign),
        "child_sign": str(child_sign),
        "parent_canonical": p,
        "child_canonical": c,
        "reversal": reversal,
        "rule": rule_explanation,
    }


def srs_category(signs: list, category: str = "") -> dict:
    """
    단일 카테고리 SRS 검증.
    signs: length-6 list (ring1..ring6), each sign: "+" | "-" | "0" | "🟢" | "🔴" | "🟡"

    Forced reversal 강제 (SKILL.md Phase 6/7/8):
      ring3→ring4 (quaternary): 역전 강제
      ring4→ring5 (quinary): 역전 강제
      ring5→ring6 (senary): 역전 강제

    Per-category 기준으로는 각 ring 전환이 1개의 lineage spine이므로
    forced reversal = 해당 ring 전환이 역전 = True 여야 함.

    Category-level forced reversal requirement:
      50% threshold는 multi-lineage (all-category aggregate) 기준.
      Single-category spine에서는 각 forced ring이 반드시 역전이어야 PASS.
    """
    if len(signs) < 6:
        return {"error": f"Need 6 signs (ring1~ring6), got {len(signs)}", "valid": False}

    canonical = [SIGN_MAP.get(s, str(s)) for s in signs]
    ring_labels = ["Primary", "Secondary", "Tertiary", "Quaternary", "Quinary", "Senary"]

    reversals = []
    for i in range(5):
        r = srs_reversal_rule(canonical[i], canonical[i + 1])
        reversals.append({
            "transition": f"ring{i+1}({ring_labels[i]})→ring{i+2}({ring_labels[i+1]})",
            "reversal": r["reversal"],
            "rule": r["rule"],
        })

    # Forced rings (0-indexed in reversals list): idx=2 (T→Q), idx=3 (Q→Qn), idx=4 (Qn→Sn)
    forced_indices = {2: "ring3→ring4 (Tertiary→Quaternary)",
                      3: "ring4→ring5 (Quaternary→Quinary)",
                      4: "ring5→ring6 (Quinary→Senary)"}
    forced_check = {label: reversals[idx]["reversal"] for idx, label in forced_indices.items()}

    reversal_count = sum(1 for r in reversals if r["reversal"])
    sign_trace = " → ".join(
        f"ring{i+1}{'🟢' if canonical[i]=='+' else '🔴' if canonical[i]=='-' else '🟡'}"
        for i in range(6)
    )

    return {
        "category": category,
        "signs_input": signs,
        "canonical_signs": canonical,
        "sign_trace": sign_trace,
        "transitions": reversals,
        "reversal_count": reversal_count,
        "max_possible": 5,
        "forced_reversal_check": forced_check,
        "forced_pass": all(forced_check.values()),
        "srs_avg_this_category": reversal_count,
        "verdict": (
            "SRS PASS — all forced reversals present"
            if all(forced_check.values())
            else "SRS FAIL — forced reversal(s) missing: " +
                 ", ".join(k for k, v in forced_check.items() if not v)
        ),
    }


# ---------------------------------------------------------------------------
# 7. PRRG SCBE 특화 최소 검색 수
# ---------------------------------------------------------------------------

def prrg_gate(ring: int, n_categories: int = 6) -> dict:
    """
    SCBE 특화 PRRG 게이트 최소 검색·아날로그 수 계산.
    ring: 1-6
    n_categories: 6 (STEEPS default) or 8 (V2 8-sector)

    SCBE 특화 규칙:
      Rings 1-2: per_category × n_categories (카테고리당 1 WebSearch)
      Ring 3: per_category × n_categories (카테고리당 1 historical analog)
      Ring 4: fixed=3 + backlash analog n_categories개
      Ring 5: fixed=3 + paradigm shift analog n_categories개
      Ring 6: fixed=2 + civilizational analog (공유 1개)
    """
    if ring not in SCBE_PRRG_SPEC:
        raise ValueError(f"ring must be 1-6, got {ring}")
    spec = SCBE_PRRG_SPEC[ring]

    if spec["type"] == "per_category":
        min_count = spec["base"] * n_categories
        extra_count = n_categories if "extra" in spec else 0
    else:
        min_count = spec["base"]
        extra_count = n_categories if "extra" in spec and "per category" in spec.get("extra", "") else 1

    return {
        "ring": ring,
        "gate_label": f"Gate_P{ring}_Pre",
        "n_categories": n_categories,
        "min_searches": min_count,
        "extra_required": spec.get("extra"),
        "extra_count": extra_count,
        "description": spec["description"],
        "sign_reversal_forced": ring >= 4,
    }


# ---------------------------------------------------------------------------
# 8. Cross-Domain Influence Matrix
# ---------------------------------------------------------------------------

def cross_domain_matrix(nodes: list) -> dict:
    """
    Cross-domain influence matrix 계산.
    nodes: list of {"primary_tag": str, "secondary_tags": list[str]}

    Returns matrix[source_category][target_category] = count
    """
    categories = STEEPS_CATEGORIES
    matrix = {cat: {other: 0 for other in categories if other != cat} for cat in categories}

    total_cross = 0
    unknown_tags = []

    for node in nodes:
        src = node.get("primary_tag")
        if src not in categories:
            unknown_tags.append(src)
            continue
        for tgt in node.get("secondary_tags", []):
            if tgt in categories and tgt != src:
                matrix[src][tgt] = matrix[src].get(tgt, 0) + 1
                total_cross += 1

    # Find strongest connection
    strongest = None
    strongest_count = 0
    for src, targets in matrix.items():
        for tgt, cnt in targets.items():
            if cnt > strongest_count:
                strongest_count = cnt
                strongest = f"{src}→{tgt}"

    return {
        "matrix": matrix,
        "total_cross_domain_links": total_cross,
        "strongest_connection": strongest,
        "strongest_count": strongest_count,
        "unknown_tags_skipped": unknown_tags,
    }


# ---------------------------------------------------------------------------
# 9. 최종 품질 게이트 (Success Metrics 일괄 검증)
# ---------------------------------------------------------------------------

def final_quality_gate(
    node_counts_by_ring: dict,
    category_counts: dict,
    srs_avg: float,
    citation_rate: float,
    forced_reversal_pass: bool,
    n_primary: int = 6,
    rings: int = 6,
    fan_out: int = 2,
) -> dict:
    """
    SCBE 최종 품질 게이트. SKILL.md Section 12 Success Metrics 전 항목 검증.

    node_counts_by_ring: {"Primary": 6, "Secondary": 12, ..., "Senary": 192}
    category_counts: {"Society": 63, "Technology": 63, ...}
    srs_avg: aggregate SRS average reversal score
    citation_rate: 0.0~1.0
    forced_reversal_pass: bool (ring4/5/6 각각 ≥50% reversal 강제 통과 여부)
    """
    expected = validate_node_counts(n_primary, rings, fan_out)

    checks = {}

    # 1. 총 노드 수
    actual_subtotal = sum(node_counts_by_ring.values())
    actual_total = actual_subtotal + 1  # center 포함
    expected_total = expected["total_with_center"]
    checks["total_nodes"] = {
        "metric": "총 노드 수",
        "expected": expected_total,
        "actual": actual_total,
        "pass": actual_total == expected_total,
        "note": f"Center(1) + ring subtotal({actual_subtotal}) = {actual_total}",
    }

    # 2. 카테고리 균형 variance = 0
    bal = balance_audit(category_counts)
    checks["category_balance"] = {
        "metric": "카테고리 균형 variance",
        "expected_variance": 0,
        "actual_variance": bal["variance"],
        "pass": bal["pass"],
        "violations": bal.get("violations", {}),
    }

    # 3. 균일 fan-out 비율 (senary ring count = n_primary × 2^(rings-1))
    senary_expected = expected["ring_counts"]["Senary"]
    senary_actual = node_counts_by_ring.get("Senary", 0)
    checks["uniform_fanout"] = {
        "metric": "균일 fan-out 비율",
        "expected_senary": senary_expected,
        "actual_senary": senary_actual,
        "pass": senary_actual == senary_expected,
        "note": f"Senary ring = n_primary({n_primary}) × {fan_out}^{rings-1} = {senary_expected}",
    }

    # 4. SRS avg ≥1.5
    checks["srs_score"] = {
        "metric": "세옹지마 SRS",
        "expected_min": SRS_EXCELLENT_THRESHOLD,
        "actual_avg": round(srs_avg, 4),
        "pass": srs_avg >= SRS_EXCELLENT_THRESHOLD,
    }

    # 5. 강제 역전 비율 ≥50% (rings 4/5/6)
    checks["forced_reversal"] = {
        "metric": "강제 역전 (rings 4-5-6 ≥50%)",
        "pass": forced_reversal_pass,
    }

    # 6. Citation rate ≥95%
    checks["citation_rate"] = {
        "metric": "inline citation 비율",
        "expected_min": 0.95,
        "actual": round(citation_rate, 4),
        "pass": citation_rate >= 0.95,
    }

    # 7. 차수 깊이 = rings
    checks["depth"] = {
        "metric": "차수 깊이",
        "expected": rings,
        "actual": rings if senary_actual > 0 else "incomplete",
        "pass": senary_actual > 0,
    }

    all_pass = all(v["pass"] for v in checks.values())
    failed = [k for k, v in checks.items() if not v["pass"]]

    return {
        "checks": checks,
        "overall_pass": all_pass,
        "verdict": "SCBE QUALITY GATE PASS — 전 항목 SUCCESS METRICS 충족" if all_pass else
                   f"SCBE QUALITY GATE FAIL — 실패 항목: {failed}",
        "failed_checks": failed,
    }


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

_COMMANDS = {
    "validate_node_counts": lambda a: validate_node_counts(
        n_primary=a.get("n_primary", 6),
        rings=a.get("rings", 6),
        fan_out=a.get("fan_out", 2),
    ),
    "balance_audit": lambda a: balance_audit(a["category_counts"]),
    "generate_id": lambda a: generate_id(
        a["ring"], a["category"], a["lineage_path"]
    ),
    "parse_id": lambda a: parse_id(a["node_id"]),
    "validate_lineage": lambda a: validate_lineage(a["lineage"]),
    "validate_fanout": lambda a: validate_fanout(
        a["node_id"], a.get("children", [])
    ),
    "srs_reversal_rule": lambda a: srs_reversal_rule(a["parent"], a["child"]),
    "srs_category": lambda a: srs_category(
        a["signs"], category=a.get("category", "")
    ),
    "prrg_gate": lambda a: prrg_gate(
        a["ring"], n_categories=a.get("n_categories", 6)
    ),
    "cross_domain_matrix": lambda a: cross_domain_matrix(a.get("nodes", [])),
    "final_quality_gate": lambda a: final_quality_gate(
        a["node_counts_by_ring"],
        a["category_counts"],
        a.get("srs_avg", 0.0),
        a.get("citation_rate", 0.0),
        a.get("forced_reversal_pass", False),
        n_primary=a.get("n_primary", 6),
        rings=a.get("rings", 6),
        fan_out=a.get("fan_out", 2),
    ),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]
    args_raw = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        args = json.loads(args_raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if command not in _COMMANDS:
        result = {
            "error": f"Unknown command: {command!r}",
            "available": list(_COMMANDS.keys()),
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    try:
        result = _COMMANDS[command](args)
    except Exception as e:
        result = {"error": str(e), "command": command}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
