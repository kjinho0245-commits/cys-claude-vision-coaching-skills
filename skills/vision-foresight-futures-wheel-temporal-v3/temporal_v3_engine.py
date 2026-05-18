#!/usr/bin/env python3
"""
temporal_v3_engine.py — vision-foresight-futures-wheel-temporal-v3 전용 결정론 엔진.

할루시네이션 구조적 차단 대상:
  - 연도 산술 (T+0년 기준 T-30y = 절대연도 계산)
  - 시간 범위 검증 (historic lookback / future lookahead 범위 내 여부)
  - 미래 차수별 표준 시간 범위 조회 (ring 1~6)
  - Future 노드 ID 결정론 생성 및 파싱
  - Historic 노드 ID 결정론 생성
  - Current Impact 강도(1-5) 척도 정의 및 검증
  - Recurring pattern 유형 분류 (5종)
  - Cross-temporal chain 유효성 검증
  - 3D cone 구조 검증 (3 team 산출 완전성)

CLI: python3 temporal_v3_engine.py <command> '<json_args>'

Available commands:
  temporal_year           — T+0 기준 offset 절대연도 계산
  validate_temporal_anchor — past_lookback / future_lookahead 범위 검증
  historic_time_in_range  — 역사적 항목이 lookback 범위 내인지 확인
  future_time_in_range    — 미래 항목이 ring 시간 범위 내인지 확인
  ring_time_range         — 미래 차수별 표준 시간 범위 조회 (ring 1~6)
  generate_future_id      — Future 노드 ID 결정론 생성 (F-P1, F-S1a, ...)
  parse_future_id         — Future 노드 ID 파싱
  generate_historic_id    — Historic 노드 ID 생성 (H_T30, H_T20, ...)
  validate_current_impact — Current Impact 항목 스키마 검증
  intensity_scale         — 강도(1-5) 척도 정의 조회
  classify_pattern        — Recurring pattern 5종 분류
  validate_ct_chain       — Cross-temporal chain 유효성 검증
  validate_cone_assembly  — 3D cone 3-team 완전성 검증
  cone_summary            — cone 전체 노드 수·구조 요약
"""

import json
import sys
import re

# ---------------------------------------------------------------------------
# 상수 정의 (SKILL.md + Glenn 2009 §VI + basic-v1 wheel_engine.py 기반)
# ---------------------------------------------------------------------------

# 미래 차수별 표준 시간 범위 (wheel_engine.py RING_TIME_FRAMES 동일)
FUTURE_RING_TIME_RANGES = {
    1: "T+1~5y",    # Primary
    2: "T+5~10y",   # Secondary
    3: "T+10~20y",  # Tertiary
    4: "T+15~25y",  # Quaternary (세옹지마 1차 반전) — Tertiary와 T+15~20y 중첩은 불확실성 확대 반영
    5: "T+20~30y",  # Quinary   (세옹지마 2차 반전) — Quaternary와 T+20~25y 중첩
    6: "T+25~50y",  # Senary    (세옹지마 3차 반전) — 문명 단위 변환
}

RING_NAMES = {
    1: "Primary", 2: "Secondary", 3: "Tertiary",
    4: "Quaternary", 5: "Quinary", 6: "Senary"
}

# Future ID prefix
FUTURE_RING_PREFIX = {
    1: "F-P", 2: "F-S", 3: "F-T",
    4: "F-Q", 5: "F-Qn", 6: "F-Sn"
}
FUTURE_PREFIX_TO_RING = {v: k for k, v in FUTURE_RING_PREFIX.items()}

# Lineage 패턴 (SCBE와 동일 — 할루시네이션 방지)
# "1" → ring1, "1a" → ring2, ..., "1a1a1a" → ring6
# ⚠️ 주의: α(Greek) 사용 금지 — Latin a/b만 허용
LINEAGE_PATTERN = re.compile(r'^1([ab][12])*[ab]?$')

# Temporal anchor 기본값 및 허용 범위
TEMPORAL_ANCHOR_DEFAULTS = {
    "past_lookback": 50,      # 기본 50년
    "future_lookahead": 30,   # 기본 30년
}
TEMPORAL_ANCHOR_VALID_RANGES = {
    "past_lookback": (10, 200),    # 최소 10년, 최대 200년
    "future_lookahead": (5, 100),  # 최소 5년, 최대 100년
}

# 현재 영향 강도(1-5) 척도 정의 (Phase 3)
INTENSITY_SCALE = {
    1: {"label": "매우 약함", "description": "간접 관련, 영향 극히 미미, 전문가 의견 분분"},
    2: {"label": "약함",     "description": "관련성 있으나 통계적 유의성 낮음, 부분 영향"},
    3: {"label": "중간",     "description": "명확한 관련성, 대다수 전문가 인정, 측정 가능한 영향"},
    4: {"label": "강함",     "description": "강한 인과적 연관, 광범위 영향, R-1 수준 증거 존재"},
    5: {"label": "매우 강함", "description": "지배적 영향, 핵심 동인, 복수 독립 연구 확인"},
}

# Current Impact 유형 (Phase 3)
CURRENT_IMPACT_TYPES = {
    "direct_effect": "직접 인과적 결과 — center issue의 직접 산물",
    "correlation": "인과 불명의 상관관계 — 동시 발생하지만 방향 불분명 (§endnote4 준수)",
    "precondition": "선결 조건 — center issue 지속을 가능하게 하는 상태",
    "mediating_factor": "매개 요인 — historic force와 current state 사이를 중개",
    "contextual_factor": "맥락 요인 — center issue에 영향받지만 독립적으로 존재",
}

# Recurring Pattern 5종 (Section 6 표준)
PATTERN_TYPES = {
    "cycle": {
        "name": "Cycle Pattern",
        "description": "일정 주기로 반복. 예: 20년 경제위기, Kondratiev 파동, 정치 사이클",
        "detection": "과거 최소 2회 이상 반복, 주기 편차 ±30% 이내",
        "future_implication": "다음 cycle 시점 예측 가능",
    },
    "echo": {
        "name": "Echo Pattern",
        "description": "과거 한 사건의 영향이 N년 후 재반향. 예: 전쟁 후 20년 경제 재건",
        "detection": "원사건과 echo 사건 간 메커니즘 인과 추적 가능",
        "future_implication": "현재 사건의 echo 시점·규모 추정",
    },
    "compound_advantage": {
        "name": "Compound Advantage",
        "description": "과거 투자→현재 dominance→미래 confirmed. 누적 이점 강화",
        "detection": "각 시간대에서 우위 지표 상승 추세 확인",
        "future_implication": "leader position 유지 및 강화 예상",
    },
    "reversal": {
        "name": "Reversal Pattern",
        "description": "과거 trend가 임계점에서 역방향 전환. 세옹지마 효과 역사적 패턴",
        "detection": "임계점(tipper) 식별 + 역전 이후 신규 trend 형성 확인",
        "future_implication": "현재 trend의 역전 가능성 + 임계점 도달 시점 추정",
    },
    "phase_transition": {
        "name": "Phase Transition",
        "description": "양적 누적이 질적 도약으로 전환. 임계 질량 도달 후 비선형 변화",
        "detection": "S-커브 패턴, 티핑포인트 식별, 급격한 체제 변화 확인",
        "future_implication": "다음 도약 시점 추정, 전환 후 새 equilibrium 예측",
    },
}

# Phase 6 chain type → Section 6 pattern type 매핑
# (SKILL.md 불일치 해소: Phase 6 예시 표현 → Section 6 표준 분류)
CHAIN_TYPE_MAPPING = {
    "linear amplification": "cycle",        # 선형 증폭 = 사이클 중 강화 국면
    "compound advantage": "compound_advantage",
    "recurring cycle": "cycle",
    "recurring pattern": "cycle",
    "echo": "echo",
    "reversal": "reversal",
    "phase transition": "phase_transition",
    "tipping point": "phase_transition",
}


# ---------------------------------------------------------------------------
# 1. 연도 산술 (결정론)
# ---------------------------------------------------------------------------

def temporal_year(T0_year: int, offset: int) -> dict:
    """
    T+0 기준 offset 절대연도 계산.
    offset > 0: 미래, offset < 0: 과거, offset = 0: 현재

    Examples:
      T0_year=2026, offset=-30 → 1996
      T0_year=2026, offset=+15 → 2041
    """
    if not isinstance(T0_year, int) or not isinstance(offset, int):
        raise ValueError("T0_year and offset must be integers")
    absolute_year = T0_year + offset
    direction = "future" if offset > 0 else "past" if offset < 0 else "present"
    return {
        "T0_year": T0_year,
        "offset": offset,
        "offset_label": f"T{'+' if offset >= 0 else ''}{offset}y",
        "absolute_year": absolute_year,
        "direction": direction,
        "formula": f"{T0_year} + ({offset}) = {absolute_year}",
    }


# ---------------------------------------------------------------------------
# 2. Temporal Anchor 검증
# ---------------------------------------------------------------------------

def validate_temporal_anchor(past_lookback: int, future_lookahead: int, T0_year: int = 2026) -> dict:
    """
    Temporal anchor 범위 검증.
    past_lookback: 과거 조사 범위 (년)
    future_lookahead: 미래 예측 범위 (년)
    T0_year: 현재 기준 연도
    """
    issues = []
    pb_range = TEMPORAL_ANCHOR_VALID_RANGES["past_lookback"]
    fl_range = TEMPORAL_ANCHOR_VALID_RANGES["future_lookahead"]

    if not (pb_range[0] <= past_lookback <= pb_range[1]):
        issues.append(f"past_lookback={past_lookback} 범위 밖 ({pb_range[0]}~{pb_range[1]}년)")
    if not (fl_range[0] <= future_lookahead <= fl_range[1]):
        issues.append(f"future_lookahead={future_lookahead} 범위 밖 ({fl_range[0]}~{fl_range[1]}년)")

    historic_start = T0_year - past_lookback
    future_end = T0_year + future_lookahead

    return {
        "T0_year": T0_year,
        "past_lookback": past_lookback,
        "future_lookahead": future_lookahead,
        "historic_range": f"{historic_start}~{T0_year} ({past_lookback}년)",
        "future_range": f"{T0_year}~{future_end} ({future_lookahead}년)",
        "total_span_years": past_lookback + future_lookahead,
        "defaults": TEMPORAL_ANCHOR_DEFAULTS,
        "valid": len(issues) == 0,
        "issues": issues,
        "verdict": "VALID" if not issues else f"INVALID: {'; '.join(issues)}",
    }


def historic_time_in_range(T0_year: int, past_lookback: int, entry_year: int) -> dict:
    """Historic 항목이 lookback 범위 내인지 확인 (결정론)."""
    start = T0_year - past_lookback
    in_range = start <= entry_year <= T0_year
    return {
        "entry_year": entry_year,
        "T0_year": T0_year,
        "valid_range": f"{start}~{T0_year}",
        "in_range": in_range,
        "offset_from_T0": entry_year - T0_year,
        "verdict": "IN RANGE" if in_range else f"OUT OF RANGE (valid: {start}~{T0_year})",
    }


def future_time_in_range(ring_num: int, T0_year: int, entry_year: int) -> dict:
    """미래 항목이 해당 ring의 시간 범위 내인지 확인 (결정론)."""
    if ring_num not in FUTURE_RING_TIME_RANGES:
        raise ValueError(f"ring_num must be 1-6, got {ring_num}")
    time_range_str = FUTURE_RING_TIME_RANGES[ring_num]
    # Parse "T+1~5y" → min_offset=1, max_offset=5
    match = re.match(r'T\+(\d+)~(\d+)y', time_range_str)
    if not match:
        raise ValueError(f"Cannot parse time range: {time_range_str}")
    min_off, max_off = int(match.group(1)), int(match.group(2))
    min_year = T0_year + min_off
    max_year = T0_year + max_off
    in_range = min_year <= entry_year <= max_year
    return {
        "ring": ring_num,
        "ring_name": RING_NAMES[ring_num],
        "standard_range": time_range_str,
        "T0_year": T0_year,
        "entry_year": entry_year,
        "valid_range_abs": f"{min_year}~{max_year}",
        "in_range": in_range,
        "overlap_note": (
            "인접 ring과 시간 중첩은 의도적 — 불확실성 범위 확대 표현 (Glenn 2009 cone 특성)"
            if ring_num >= 4 else None
        ),
        "verdict": "IN RANGE" if in_range else f"OUT OF RANGE (valid: {min_year}~{max_year})",
    }


# ---------------------------------------------------------------------------
# 3. Ring 시간 범위 조회
# ---------------------------------------------------------------------------

def ring_time_range(ring_num: int, T0_year: int = None) -> dict:
    """미래 차수별 표준 시간 범위 조회 (결정론)."""
    if ring_num not in FUTURE_RING_TIME_RANGES:
        raise ValueError(f"ring_num must be 1-6, got {ring_num}")
    time_str = FUTURE_RING_TIME_RANGES[ring_num]
    result = {
        "ring": ring_num,
        "ring_name": RING_NAMES[ring_num],
        "time_range": time_str,
        "is_sewongjima_ring": ring_num >= 4,
    }
    if T0_year is not None:
        match = re.match(r'T\+(\d+)~(\d+)y', time_str)
        if match:
            result["absolute_range"] = f"{T0_year + int(match.group(1))}~{T0_year + int(match.group(2))}"
    # Overlap note for rings 4-6
    if ring_num >= 4:
        prev_range = FUTURE_RING_TIME_RANGES[ring_num - 1]
        result["overlap_with_prev"] = f"Ring {ring_num-1}({prev_range})와 시간 중첩 — 불확실성 cone 확대 표현 (의도적)"
    return result


# ---------------------------------------------------------------------------
# 4. Future 노드 ID 생성·파싱 (결정론)
# ---------------------------------------------------------------------------

def generate_future_id(ring: int, lineage_path: str) -> dict:
    """
    Future 노드 ID 결정론 생성.
    ring: 1-6
    lineage_path: "1" | "1a" | "1a1" | "1a1b" | "1a1b2" | "1a1b2a"

    ⚠️ Greek α(알파) 사용 금지 — SKILL.md §4 Phase 4의 'F-Sn1a1a1α'는 오류.
       반드시 Latin 'a'/'b'와 '1'/'2' 조합만 사용.

    Returns: {"node_id": "F-P1", "ring": 1, "lineage": "1", "valid": True}
    """
    prefix = FUTURE_RING_PREFIX.get(ring)
    if not prefix:
        raise ValueError(f"ring must be 1-6, got {ring}")
    if not LINEAGE_PATTERN.match(lineage_path):
        raise ValueError(
            f"Invalid lineage_path: '{lineage_path}'. "
            f"Only digits 1-2 and letters a-b allowed. "
            f"⚠️ Greek α is NOT allowed — use Latin 'a' instead."
        )
    lineage_depth = len(lineage_path)
    if lineage_depth != ring:
        raise ValueError(
            f"lineage_path depth ({lineage_depth}) ≠ ring ({ring}). "
            f"Ring {ring} requires depth-{ring} lineage."
        )
    node_id = f"{prefix}{lineage_path}"
    return {
        "node_id": node_id,
        "ring": ring,
        "ring_name": RING_NAMES[ring],
        "prefix": prefix,
        "lineage": lineage_path,
        "lineage_depth": lineage_depth,
        "time_range": FUTURE_RING_TIME_RANGES[ring],
        "valid": True,
        "alpha_warning": "⚠️ SKILL.md §4 'F-Sn1a1a1α' 오류 — 'F-Sn1a1a1a'가 올바른 표기",
    }


def parse_future_id(node_id: str) -> dict:
    """
    Future 노드 ID 파싱.
    "F-P1" → ring=1, lineage="1"
    "F-Sn1a1a1a" → ring=6, lineage="1a1a1a"
    """
    # Greek α 탐지 → 자동 경고
    has_greek_alpha = 'α' in node_id
    if has_greek_alpha:
        corrected = node_id.replace('α', 'a')
    else:
        corrected = node_id

    # 프리픽스 매핑 (길이 긴 것 먼저)
    sorted_prefixes = sorted(FUTURE_RING_PREFIX.values(), key=len, reverse=True)
    ring_num = None
    lineage = None
    matched_prefix = None
    for prefix in sorted_prefixes:
        if corrected.startswith(prefix):
            ring_num = FUTURE_PREFIX_TO_RING[prefix]
            lineage = corrected[len(prefix):]
            matched_prefix = prefix
            break

    if ring_num is None:
        return {"error": f"Unknown prefix in '{node_id}'", "valid": False}

    valid_lineage = bool(LINEAGE_PATTERN.match(lineage)) if lineage else False
    depth_match = len(lineage) == ring_num if lineage else False

    return {
        "node_id": node_id,
        "corrected_id": corrected if has_greek_alpha else node_id,
        "ring": ring_num,
        "ring_name": RING_NAMES.get(ring_num, "Unknown"),
        "prefix": matched_prefix,
        "lineage": lineage,
        "lineage_depth": len(lineage) if lineage else 0,
        "depth_ring_match": depth_match,
        "time_range": FUTURE_RING_TIME_RANGES.get(ring_num, "?"),
        "valid": valid_lineage and depth_match and not has_greek_alpha,
        "greek_alpha_error": has_greek_alpha,
        "fix": f"Replace 'α' with 'a': '{corrected}'" if has_greek_alpha else None,
    }


# ---------------------------------------------------------------------------
# 5. Historic 노드 ID 생성 (결정론)
# ---------------------------------------------------------------------------

def generate_historic_id(T0_year: int, entry_year: int, seq: int = 1) -> dict:
    """
    Historic 노드 ID 결정론 생성.
    형식: H_T{abs_offset}_{seq} (예: H_T30_1, H_T20_2)

    T0_year: 기준연도
    entry_year: 역사적 항목 연도
    seq: 같은 연도의 항목 순서번호 (1부터)
    """
    offset = T0_year - entry_year  # 양수 = 과거
    if offset <= 0:
        raise ValueError(f"entry_year ({entry_year}) must be before T0_year ({T0_year})")
    node_id = f"H_T{offset}_{seq}"
    return {
        "node_id": node_id,
        "T0_year": T0_year,
        "entry_year": entry_year,
        "offset_years": offset,
        "offset_label": f"T-{offset}y",
        "seq": seq,
        "valid": True,
    }


# ---------------------------------------------------------------------------
# 6. Current Impact 검증
# ---------------------------------------------------------------------------

def validate_current_impact(impact: dict) -> dict:
    """
    Current Impact 항목 스키마 검증 (Phase 3).
    Required fields: id, text, type, intensity (1-5), tier
    """
    errors = []
    warnings = []

    # ID
    if "id" not in impact:
        errors.append("Missing 'id' (예: C1, C2, C3)")

    # text
    if not impact.get("text"):
        errors.append("Missing 'text'")

    # type
    t = impact.get("type", "")
    valid_types = list(CURRENT_IMPACT_TYPES.keys())
    if t not in valid_types:
        errors.append(f"Invalid type '{t}'. Valid: {valid_types}")

    # intensity
    intens = impact.get("intensity", 0)
    if not isinstance(intens, int) or not (1 <= intens <= 5):
        errors.append(f"intensity must be int 1-5, got {intens!r}")
    else:
        intensity_def = INTENSITY_SCALE[intens]

    # tier (R-1, R-2, R-3, H)
    tier = impact.get("tier", "")
    valid_tiers = ["R-1", "R-2", "R-3", "H"]
    if tier not in valid_tiers:
        errors.append(f"Invalid tier '{tier}'. Valid: {valid_tiers}")

    # causality vs correlation check
    if t == "correlation" and tier == "R-1":
        warnings.append(
            "correlation 유형에 R-1(검증된 사실) tier: "
            "Glenn §endnote4 준수 — '인과 불명' 명시 필요"
        )

    return {
        "impact": impact,
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0,
        "intensity_definition": INTENSITY_SCALE.get(intens, {}) if isinstance(intens, int) and 1 <= intens <= 5 else None,
        "type_definition": CURRENT_IMPACT_TYPES.get(t, "?"),
        "verdict": "VALID" if not errors else f"INVALID: {'; '.join(errors)}",
    }


def intensity_scale(level: int = None) -> dict:
    """강도(1-5) 척도 정의 조회. level 미지정 시 전체 반환."""
    if level is None:
        return {"scale": INTENSITY_SCALE, "note": "1=매우약함 ~ 5=매우강함"}
    if not (1 <= level <= 5):
        raise ValueError(f"level must be 1-5, got {level}")
    return {"level": level, **INTENSITY_SCALE[level]}


# ---------------------------------------------------------------------------
# 7. Recurring Pattern 분류
# ---------------------------------------------------------------------------

def classify_pattern(pattern_type_input: str) -> dict:
    """
    Recurring pattern 유형 분류 (결정론 — 5종 표준).

    SKILL.md Phase 6 예시의 비표준 표현도 자동 매핑:
      "linear amplification" → "cycle" (강화 국면)
      "recurring cycle" → "cycle"
      "compound advantage" → "compound_advantage"
    """
    key = pattern_type_input.lower().strip()

    # 직접 매핑 시도
    if key in PATTERN_TYPES:
        standard_key = key
    else:
        # 비표준 표현 매핑
        standard_key = CHAIN_TYPE_MAPPING.get(key)

    if standard_key and standard_key in PATTERN_TYPES:
        pattern = PATTERN_TYPES[standard_key]
        return {
            "input": pattern_type_input,
            "standard_key": standard_key,
            "pattern": pattern,
            "matched": True,
            "skill_md_note": (
                "Phase 6 예시 표현과 Section 6 표준 분류 자동 매핑 적용"
                if key != standard_key else None
            ),
        }

    return {
        "input": pattern_type_input,
        "standard_key": None,
        "matched": False,
        "valid_types": list(PATTERN_TYPES.keys()),
        "error": f"Unknown pattern type. Valid: {list(PATTERN_TYPES.keys())}",
    }


# ---------------------------------------------------------------------------
# 8. Cross-Temporal Chain 검증
# ---------------------------------------------------------------------------

def validate_ct_chain(chain: dict) -> dict:
    """
    Cross-temporal chain 유효성 검증 (Phase 6).
    Required: chain_id, historic, current, future, type
    """
    errors = []

    if "chain_id" not in chain:
        errors.append("Missing 'chain_id' (예: CT-1)")
    if not chain.get("historic"):
        errors.append("Missing 'historic' (과거 driving force)")
    if not chain.get("current"):
        errors.append("Missing 'current' (현재 correlation/impact)")
    if not chain.get("future"):
        errors.append("Missing 'future' (미래 consequence ID 또는 설명)")

    # pattern type 검증
    chain_type = chain.get("type", "")
    pattern_result = classify_pattern(chain_type)
    if not pattern_result["matched"]:
        errors.append(f"Unknown chain type: '{chain_type}'. Use: {list(PATTERN_TYPES.keys())}")

    return {
        "chain": chain,
        "errors": errors,
        "pattern_classification": pattern_result,
        "valid": len(errors) == 0,
        "verdict": "VALID" if not errors else f"INVALID: {'; '.join(errors)}",
    }


# ---------------------------------------------------------------------------
# 9. 3D Cone Assembly 검증
# ---------------------------------------------------------------------------

def validate_cone_assembly(
    historic_count: int,
    current_count: int,
    future_primary_count: int,
    future_rings_count: dict,
    past_lookback: int = 50,
    future_lookahead: int = 30,
) -> dict:
    """
    3D Cone 3-team 완전성 검증.

    historic_count: Historic Team 항목 수
    current_count: Contemporary Team 항목 수
    future_primary_count: Future Team Primary 노드 수
    future_rings_count: {"Secondary": N, "Tertiary": N, ...}
    """
    issues = []
    warnings = []

    # Historic Team: 최소 5개 이상 (SKILL.md Phase 2 표 예시 기준)
    if historic_count < 3:
        issues.append(f"Historic 항목 {historic_count}개 < 최소 3개")
    elif historic_count < 5:
        warnings.append(f"Historic 항목 {historic_count}개: 권장 5개 이상")

    # Contemporary Team: 최소 3개 이상
    if current_count < 3:
        issues.append(f"Current 항목 {current_count}개 < 최소 3개")

    # Future Primary: 최소 3개 (basic-v1의 ring_count_rules Primary min=5 대신 V3는 3개 허용)
    if future_primary_count < 3:
        issues.append(f"Future Primary {future_primary_count}개 < 최소 3개")

    # Future ring 연속성 (Primary 있으면 Secondary 있어야 함)
    ring_sequence = [("Primary", future_primary_count),
                     ("Secondary", future_rings_count.get("Secondary", 0)),
                     ("Tertiary", future_rings_count.get("Tertiary", 0))]
    for i in range(len(ring_sequence) - 1):
        curr_ring, curr_count = ring_sequence[i]
        next_ring, next_count = ring_sequence[i+1]
        if curr_count > 0 and next_count == 0:
            warnings.append(f"{curr_ring} 있지만 {next_ring} 없음 — 6차 깊이 권장")

    total_future = future_primary_count + sum(future_rings_count.values())

    return {
        "historic_count": historic_count,
        "current_count": current_count,
        "future_primary_count": future_primary_count,
        "future_rings_count": future_rings_count,
        "total_future_nodes": total_future,
        "total_all_nodes": historic_count + current_count + total_future + 1,  # +1 center
        "three_team_complete": historic_count > 0 and current_count > 0 and future_primary_count > 0,
        "issues": issues,
        "warnings": warnings,
        "valid": len(issues) == 0,
        "verdict": "CONE VALID" if not issues else f"CONE ISSUES: {'; '.join(issues)}",
    }


def cone_summary(
    T0_year: int,
    past_lookback: int,
    future_lookahead: int,
    historic_count: int = 0,
    current_count: int = 0,
    future_rings: dict = None,
) -> dict:
    """3D Cone 전체 구조 요약."""
    future_rings = future_rings or {}
    total_future = sum(future_rings.values())
    historic_start = T0_year - past_lookback
    future_end = T0_year + future_lookahead

    return {
        "T0_year": T0_year,
        "historic_cone": {
            "start_year": historic_start,
            "end_year": T0_year,
            "span_years": past_lookback,
            "item_count": historic_count,
        },
        "current_ring": {
            "year": T0_year,
            "item_count": current_count,
        },
        "future_cone": {
            "start_year": T0_year,
            "end_year": future_end,
            "span_years": future_lookahead,
            "ring_counts": future_rings,
            "total_nodes": total_future,
        },
        "grand_total": historic_count + current_count + total_future + 1,
        "three_team_check": {
            "historic_team": historic_count > 0,
            "contemporary_team": current_count > 0,
            "future_team": total_future > 0,
            "all_present": historic_count > 0 and current_count > 0 and total_future > 0,
        },
    }


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

_COMMANDS = {
    "temporal_year": lambda a: temporal_year(a["T0_year"], a["offset"]),
    "validate_temporal_anchor": lambda a: validate_temporal_anchor(
        a["past_lookback"], a["future_lookahead"], T0_year=a.get("T0_year", 2026)
    ),
    "historic_time_in_range": lambda a: historic_time_in_range(
        a["T0_year"], a["past_lookback"], a["entry_year"]
    ),
    "future_time_in_range": lambda a: future_time_in_range(
        a["ring_num"], a["T0_year"], a["entry_year"]
    ),
    "ring_time_range": lambda a: ring_time_range(
        a["ring_num"], T0_year=a.get("T0_year")
    ),
    "generate_future_id": lambda a: generate_future_id(a["ring"], a["lineage_path"]),
    "parse_future_id": lambda a: parse_future_id(a["node_id"]),
    "generate_historic_id": lambda a: generate_historic_id(
        a["T0_year"], a["entry_year"], seq=a.get("seq", 1)
    ),
    "validate_current_impact": lambda a: validate_current_impact(a["impact"]),
    "intensity_scale": lambda a: intensity_scale(level=a.get("level")),
    "classify_pattern": lambda a: classify_pattern(a["pattern_type"]),
    "validate_ct_chain": lambda a: validate_ct_chain(a["chain"]),
    "validate_cone_assembly": lambda a: validate_cone_assembly(
        a["historic_count"],
        a["current_count"],
        a["future_primary_count"],
        a.get("future_rings_count", {}),
        past_lookback=a.get("past_lookback", 50),
        future_lookahead=a.get("future_lookahead", 30),
    ),
    "cone_summary": lambda a: cone_summary(
        a["T0_year"], a["past_lookback"], a["future_lookahead"],
        historic_count=a.get("historic_count", 0),
        current_count=a.get("current_count", 0),
        future_rings=a.get("future_rings", {}),
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
        print(json.dumps({
            "error": f"Unknown command: {command!r}",
            "available": list(_COMMANDS.keys())
        }, ensure_ascii=False))
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
