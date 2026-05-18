#!/usr/bin/env python3
"""
validate_record.py — 환경 스캐닝 기록 결정론적 검증기

Gordon-Glenn (2009) KOC 10-field / UNDP 13-field 템플릿의 모든
사실 조회·번호 매핑·날짜 검사·범위 검사·존재 검증을 결정론적으로 처리.

사용법:
  python3 validate_record.py validate-date 2026-05-09
  python3 validate_record.py field-number KOC consequences
  python3 validate_record.py field-number KOC scanner
  python3 validate_record.py field-number UNDP actors
  python3 validate_record.py generate-id 2026-05-09 3
  python3 validate_record.py check-threshold 49 0.72
  python3 validate_record.py validate-domain KOC Technological Economical
  python3 validate_record.py validate-domain UNDP "Energy" "Science and Technology"
  python3 validate_record.py validate-domain UNDP "Spirituality"
  python3 validate_record.py spike-detect 11 3
  python3 validate_record.py list-fields KOC
  python3 validate_record.py list-fields UNDP
  python3 validate_record.py list-domains KOC
  python3 validate_record.py list-domains UNDP
  python3 validate_record.py cross-map
  python3 validate_record.py list-indicators
  echo '{"domain":"Technological","source":"Reuters","date":"2026-05-09"}' | python3 validate_record.py validate-completeness KOC
  echo '[{"classification":"Energy"},{"classification":"Science and Technology"}]' | python3 validate_record.py analyze-domain-freq UNDP
"""

import re
import sys
import json
from datetime import datetime
from collections import Counter


# ── 권위 있는 도메인 목록 — 정규 순서 보존 (Authoritative, 절대 LLM 재추론 금지) ──

# KOC 5 도메인 — Gordon-Glenn Section II 원전 순서 (TEEPS)
KOC_DOMAINS_ORDERED: list = [
    "Technological",
    "Economical",
    "Environmental",
    "Political",
    "Social",
]
KOC_DOMAINS: frozenset = frozenset(KOC_DOMAINS_ORDERED)

# UNDP 9+1 도메인 — Gordon-Glenn Section IV 원전 순서 + 박사님 Spirituality 추가
UNDP_DOMAINS_ORDERED: list = [
    "Conflict and Governance",
    "Science and Technology",
    "Agriculture and Food Security",
    "Natural Resources and Environment",
    "Energy",
    "Population, Education and Human Welfare",
    "Communications and Transportation",
    "Regional and International Economics",
    "Social Cultural Issues",
    "Spirituality",          # 박사님 추가 — STEEPS 6번째 차원
]
UNDP_DOMAINS: frozenset = frozenset(UNDP_DOMAINS_ORDERED)


# ── 필드 번호 매핑 (Authoritative — 절대 LLM이 재추론 금지) ───────────────────
# KOC 10-field (Gordon-Glenn Section II)
KOC_FIELD_MAP: dict = {
    "domain":            1,
    "leading_indicator": 2,
    "source":            3,
    "how_to_access":     4,
    "other_comments":    5,
    "significance":      6,
    "consequences":      7,
    "status":            8,
    "actors":            9,
    "date":              10,
    # KOC field 10 covers both Date AND Scanner (combined field)
}

# KOC 별칭 매핑 — field-number 조회용 (completeness 카운트에서 제외)
# "scanner"는 KOC field 10의 일부이므로 별칭으로만 처리
KOC_FIELD_ALIASES: dict = {
    "scanner": 10,
}

# UNDP 13-field (Gordon-Glenn Section IV)
UNDP_FIELD_MAP: dict = {
    "item":           1,
    "description":    2,
    "significance":   3,
    "importance":     4,
    "consequences":   5,
    "status":         6,
    "actors":         7,
    "misc":           8,
    "classification": 9,
    "source":         10,
    "location":       11,
    "date":           12,
    "scanner":        13,
}

KOC_TOTAL_FIELDS:  int = 10
UNDP_TOTAL_FIELDS: int = 13

# 필수 / 권고 필드
KOC_REQUIRED:    frozenset = frozenset(["domain", "source", "date"])
KOC_RECOMMENDED: frozenset = frozenset([
    "leading_indicator", "significance", "consequences", "status", "actors"
])

UNDP_REQUIRED:    frozenset = frozenset(["item", "description", "source", "date", "scanner"])
UNDP_RECOMMENDED: frozenset = frozenset([
    "significance", "importance", "consequences", "status", "actors", "classification"
])


# ── 날짜 형식 검증 ────────────────────────────────────────────────────────────
_DATE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")


def validate_date(date_str: str) -> tuple:
    """YYYY-MM-DD 형식 검증. 존재하는 날짜인지까지 확인."""
    if not date_str or not date_str.strip():
        return False, "날짜 없음"
    s = date_str.strip()
    if not _DATE_RE.match(s):
        return False, f"형식 오류: '{s}' (필요: YYYY-MM-DD)"
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True, "OK"
    except ValueError as e:
        return False, str(e)


# ── 도메인 입력 정규화 ────────────────────────────────────────────────────────

def _normalize_domain_input(domain_str: str, domain_set: frozenset) -> str:
    """대소문자 무시 + 괄호 접미사 제거로 도메인명 정규화.

    - "Spirituality (박사님 STEEPS 추가 차원)" → "Spirituality"
    - "technological" → "Technological"
    반환: 정규 도메인명 (매칭 실패 시 원본 반환 → 이후 invalid로 처리됨)
    """
    s = domain_str.strip()
    if s in domain_set:
        return s
    lower_map = {d.lower(): d for d in domain_set}
    # 대소문자 무시 정확 매칭
    if s.lower() in lower_map:
        return lower_map[s.lower()]
    # 괄호 접미사 제거 후 재시도
    if '(' in s:
        base = s[:s.index('(')].strip()
        if base in domain_set:
            return base
        if base.lower() in lower_map:
            return lower_map[base.lower()]
    return s  # 매칭 실패 — 호출자에서 invalid 처리


# ── 도메인 검증 ───────────────────────────────────────────────────────────────

def validate_koc_domains(domains: list) -> tuple:
    """KOC 도메인 목록 검증. 대소문자 정규화 후 5개 승인 도메인 중에서만 허용."""
    normalized = [_normalize_domain_input(d, KOC_DOMAINS) for d in domains]
    invalid = [domains[i] for i, d in enumerate(normalized) if d not in KOC_DOMAINS]
    return len(invalid) == 0, invalid


def validate_undp_classification(classifications: list) -> tuple:
    """UNDP 분류 검증. 대소문자 정규화 + 괄호 접미사 제거 후 9+1개 승인 도메인 중에서만 허용."""
    normalized = [_normalize_domain_input(c, UNDP_DOMAINS) for c in classifications]
    invalid = [classifications[i] for i, c in enumerate(normalized) if c not in UNDP_DOMAINS]
    return len(invalid) == 0, invalid


# ── 필드 번호 조회 ─────────────────────────────────────────────────────────────

def field_number(template: str, field_name: str):
    """필드 이름 → 번호 조회. 할루시네이션 방지 — 이 함수만 사용.

    KOC 별칭 (scanner=10 등)도 처리.
    """
    t = template.upper()
    fname = field_name.lower()
    if t == "KOC":
        # 정규 필드 맵 우선, 없으면 별칭 확인
        return KOC_FIELD_MAP.get(fname) or KOC_FIELD_ALIASES.get(fname)
    elif t == "UNDP":
        return UNDP_FIELD_MAP.get(fname)
    return None


def field_name_from_number(template: str, number: int):
    """필드 번호 → 이름 역조회."""
    t = template.upper()
    if t == "KOC":
        rev = {v: k for k, v in KOC_FIELD_MAP.items()}
    elif t == "UNDP":
        rev = {v: k for k, v in UNDP_FIELD_MAP.items()}
    else:
        return None
    return rev.get(number)


def cross_template_field_map() -> dict:
    """개념적으로 동일한 필드의 KOC↔UNDP 번호 매핑 테이블."""
    return {
        "domain / classification": {"KOC": 1,  "UNDP": 9},
        "consequences":            {"KOC": 7,  "UNDP": 5},
        "status":                  {"KOC": 8,  "UNDP": 6},
        "actors":                  {"KOC": 9,  "UNDP": 7},
        "source":                  {"KOC": 3,  "UNDP": 10},
        "date":                    {"KOC": 10, "UNDP": 12},
        "significance":            {"KOC": 6,  "UNDP": 3},
        # UNDP-only
        "item":                    {"KOC": None, "UNDP": 1},
        "description":             {"KOC": None, "UNDP": 2},
        "importance":              {"KOC": None, "UNDP": 4},
        "misc":                    {"KOC": 5,    "UNDP": 8},
        "location":                {"KOC": None, "UNDP": 11},
        "scanner":                 {"KOC": 10,   "UNDP": 13},
        # KOC-only
        "leading_indicator":       {"KOC": 2,   "UNDP": None},
        "how_to_access":           {"KOC": 4,   "UNDP": None},
    }


# ── Record ID 생성 ────────────────────────────────────────────────────────────

def generate_record_id(date_str: str, sequence: int) -> str:
    """결정론적 Record ID 생성: YYYY-MM-DD-NNN"""
    ok, msg = validate_date(date_str)
    if not ok:
        raise ValueError(f"record_id 생성 실패 — {msg}")
    return f"{date_str.strip()}-{sequence:03d}"


# ── 필드 충족도 검사 ──────────────────────────────────────────────────────────
_EMPTY_VALUES = frozenset(["", "tbd", "unknown", "n/a", "없음", "미정"])


def _is_empty(v) -> bool:
    if v is None:
        return True
    return str(v).strip().lower() in _EMPTY_VALUES


def field_completeness(record: dict, template: str) -> dict:
    """필드 충족도 보고서. 100% 결정론.

    템플릿 정의 필드만 카운트 (추가 key 무시).
    KOC scanner 별칭은 completeness 카운트에서 제외 (date와 동일 필드).
    """
    t = template.upper()
    if t == "KOC":
        total       = KOC_TOTAL_FIELDS
        required    = KOC_REQUIRED
        recommended = KOC_RECOMMENDED
        field_keys  = set(KOC_FIELD_MAP.keys())   # 10개 (scanner 별칭 제외)
    elif t == "UNDP":
        total       = UNDP_TOTAL_FIELDS
        required    = UNDP_REQUIRED
        recommended = UNDP_RECOMMENDED
        field_keys  = set(UNDP_FIELD_MAP.keys())  # 13개
    else:
        return {"error": "KOC 또는 UNDP 중 하나"}

    # 템플릿 정의 필드만 카운트
    filled          = sum(1 for f in field_keys if not _is_empty(record.get(f, "")))
    missing_req     = [f for f in required    if _is_empty(record.get(f, ""))]
    missing_rec     = [f for f in recommended if _is_empty(record.get(f, ""))]
    pct             = round(filled / total * 100, 1)

    return {
        "template":            t,
        "total_fields":        total,
        "filled":              filled,
        "missing_required":    missing_req,
        "missing_recommended": missing_rec,
        "completeness_pct":    pct,
        "pass":                len(missing_req) == 0,
    }


# ── Leading Indicator 임계치 카탈로그 + 검사 ─────────────────────────────────
# (leading_indicator_catalogue.md 기반 — 결정론적 고정값)
# ID는 카탈로그 번호와 일치. 수치 임계치가 명시된 지표만 포함.
INDICATOR_THRESHOLDS: dict = {
    # 1. Conflict and Governance
    1:   {"name": "미·중 GDP 격차 (PPP)",       "threshold": 110,       "unit": "%",          "cmp": "gte"},
    2:   {"name": "북한 핵·미사일 시험 빈도",   "threshold": 3,          "unit": "건/분기",    "cmp": "gte"},
    3:   {"name": "한국 국방비/GDP",             "threshold": 3.0,       "unit": "%",          "cmp": "gte"},
    # 2. Science and Technology
    12:  {"name": "AI 모델 release 빈도",        "threshold": 4,          "unit": "건/분기",    "cmp": "gte"},
    13:  {"name": "KMMLU 최고 점수",             "threshold": 85,         "unit": "점",         "cmp": "gte"},
    14:  {"name": "AI R&D 예산 비중",            "threshold": 15,         "unit": "%",          "cmp": "gte"},
    # 3. Agriculture and Food Security
    23:  {"name": "한국 식량 자급률",            "threshold": 40,         "unit": "%",          "cmp": "lte"},
    26:  {"name": "농촌 인구 비중",              "threshold": 4,          "unit": "%",          "cmp": "lte"},
    27:  {"name": "스마트팜 보급률",             "threshold": 10,         "unit": "%",          "cmp": "gte"},
    # 4. Natural Resources and Environment
    28:  {"name": "한국 평균 기온 상승",         "threshold": 2,          "unit": "×글로벌평균","cmp": "gte"},
    31:  {"name": "PM2.5 연평균 농도",           "threshold": 15,         "unit": "µg/m³",      "cmp": "lte"},
    # 5. Energy
    39:  {"name": "LNG 러시아 의존도",           "threshold": 5,          "unit": "%",          "cmp": "lte"},
    42:  {"name": "한국 재생에너지 비중",        "threshold": 30,         "unit": "%",          "cmp": "gte"},
    46:  {"name": "전기차 보급률 (신차)",        "threshold": 30,         "unit": "%",          "cmp": "gte"},
    # 6. Population, Education and Human Welfare
    49:  {"name": "합계출산율 (TFR)",            "threshold": 0.7,        "unit": "",           "cmp": "lte"},
    50:  {"name": "분기 신생아 수",              "threshold": 55_000,     "unit": "명",         "cmp": "lte"},
    51:  {"name": "25~29세 결혼 의향",           "threshold": 30,         "unit": "%",          "cmp": "lte"},
    53:  {"name": "외국인 비중 (인구 대비)",     "threshold": 5,          "unit": "%",          "cmp": "gte"},
    55:  {"name": "65세 이상 비율",              "threshold": 20,         "unit": "%",          "cmp": "gte"},
    59:  {"name": "대학 입학정원/입학자 비율",   "threshold": 1.0,        "unit": "배",         "cmp": "gte"},
    63:  {"name": "청년 우울증 진단율",          "threshold": 10,         "unit": "%",          "cmp": "gte"},
    64:  {"name": "자살률",                      "threshold": 25,         "unit": "명/10만",    "cmp": "gte"},
    65:  {"name": "정신건강 앱 사용자",          "threshold": 5_000_000,  "unit": "명",         "cmp": "gte"},
    66:  {"name": "외로움·고립 비율",            "threshold": 40,         "unit": "%",          "cmp": "gte"},
    # 7. Communications and Transportation
    71:  {"name": "데이터센터 전력 비중",        "threshold": 10,         "unit": "%",          "cmp": "gte"},
    # 8. Regional and International Economics
    77:  {"name": "한국 GDP 성장률",             "threshold": 1.5,        "unit": "%",          "cmp": "lte"},
    80:  {"name": "환율 (원/달러)",              "threshold": 1_400,      "unit": "원",         "cmp": "gte"},
    81:  {"name": "외환보유고",                  "threshold": 3_500,      "unit": "억 달러",    "cmp": "lte"},
    82:  {"name": "가계부채/GDP",                "threshold": 105,        "unit": "%",          "cmp": "gte"},
    85:  {"name": "서울 아파트 PIR",             "threshold": 18,         "unit": "배",         "cmp": "gte"},
    86:  {"name": "미분양 주택",                 "threshold": 100_000,    "unit": "호",         "cmp": "gte"},
    87:  {"name": "부동산 PF 부실률",            "threshold": 10,         "unit": "%",          "cmp": "gte"},
    91:  {"name": "무역수지 적자 지속",          "threshold": 6,          "unit": "개월",       "cmp": "gte"},
    # 9. Social Cultural Issues
    102: {"name": "1인 가구 비율",               "threshold": 40,         "unit": "%",          "cmp": "gte"},
    # 10. Spirituality
    106: {"name": "기독교 인구 비중",            "threshold": 22,         "unit": "%",          "cmp": "lte"},
    108: {"name": "가나안 성도 비중",            "threshold": 35,         "unit": "%",          "cmp": "gte"},
    109: {"name": "청년 기독교 정체성",          "threshold": 15,         "unit": "%",          "cmp": "lte"},
    110: {"name": "명상 앱 사용자",              "threshold": 5_000_000,  "unit": "명",         "cmp": "gte"},
    112: {"name": "SBNR 비율",                   "threshold": 25,         "unit": "%",          "cmp": "gte"},
    114: {"name": "신학교 신입생 모집률",        "threshold": 70,         "unit": "%",          "cmp": "lte"},
}


def check_indicator_threshold(indicator_id: int, current_value: float) -> dict:
    """Leading indicator 임계치 검사. 결정론 — LLM 재추론 금지."""
    if indicator_id not in INDICATOR_THRESHOLDS:
        return {"error": f"indicator_id {indicator_id}은 카탈로그에 없음. list-indicators로 확인"}

    ind = INDICATOR_THRESHOLDS[indicator_id]
    threshold = ind["threshold"]
    cmp       = ind["cmp"]

    if cmp == "lte":
        crossed    = current_value <= threshold
        approaching = current_value <= threshold * 1.1
    elif cmp == "gte":
        crossed    = current_value >= threshold
        approaching = current_value >= threshold * 0.9
    else:
        return {"error": f"알 수 없는 comparison: {cmp}"}

    if crossed:
        status_str = "🔴 임계 돌파"
    elif approaching:
        status_str = "🟡 임계 접근 (10% 이내)"
    else:
        status_str = "🟢 정상 범위"

    return {
        "indicator_id": indicator_id,
        "name":         ind["name"],
        "threshold":    threshold,
        "unit":         ind["unit"],
        "current":      current_value,
        "comparison":   cmp,
        "crossed":      crossed,
        "approaching":  approaching,
        "status":       status_str,
    }


# ── 빈도 급증 감지 (Weak Signal Pattern 1) ────────────────────────────────────

def detect_frequency_spike(current_count: int, previous_count: int,
                            ratio_threshold: float = 2.0) -> dict:
    """결정론적 빈도 급증 감지 (Weak Signal Pattern 1).

    LLM이 '많이 늘었다'를 자연어로 판단하지 않도록 수치 기준을 고정.
    ratio_threshold=2.0 → 2배 이상이면 spike.
    """
    if previous_count < 0 or current_count < 0:
        return {"error": "음수 카운트 불가"}

    if previous_count == 0:
        ratio      = None
        pct_change = None
        is_spike   = current_count > 0
    else:
        ratio      = round(current_count / previous_count, 2)
        pct_change = round((current_count - previous_count) / previous_count * 100, 1)
        is_spike   = ratio >= ratio_threshold

    return {
        "current":         current_count,
        "previous":        previous_count,
        "ratio":           ratio,
        "pct_change":      pct_change,
        "ratio_threshold": ratio_threshold,
        "is_spike":        is_spike,
        "status":          "🔴 Weak Signal — 빈도 급증" if is_spike else "🟢 정상 범위",
    }


# ── 도메인 분포 분석 ──────────────────────────────────────────────────────────

def analyze_domain_frequency(records: list, template: str = "UNDP") -> dict:
    """records 목록에서 도메인별 빈도 계산. 완전 결정론."""
    domain_key = "classification" if template.upper() == "UNDP" else "domain"
    counts: Counter = Counter()
    for rec in records:
        domains = rec.get(domain_key, [])
        if isinstance(domains, str):
            domains = [domains]
        for d in domains:
            counts[d.strip()] += 1

    total = len(records)
    return {
        "template":           template.upper(),
        "total_records":      total,
        "domain_distribution": {
            d: {
                "count": c,
                "pct":   round(c / total * 100, 1) if total > 0 else 0,
            }
            for d, c in counts.most_common()
        },
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

def _print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    # --- validate-date ---
    if cmd == "validate-date":
        if len(args) < 2:
            _print({"error": "사용법: validate-date YYYY-MM-DD"})
            sys.exit(1)
        ok, msg = validate_date(args[1])
        _print({"valid": ok, "message": msg, "input": args[1]})

    # --- field-number ---
    elif cmd == "field-number":
        if len(args) < 3:
            _print({"error": "사용법: field-number KOC|UNDP <field_name>"})
            sys.exit(1)
        tmpl, fname = args[1], args[2].lower()
        num = field_number(tmpl, fname)
        if num is not None:
            note = None
            if tmpl.upper() == "KOC" and fname == "scanner":
                note = "KOC field 10은 Date/Scanner 통합 필드"
            result = {"template": tmpl.upper(), "field": fname, "number": num}
            if note:
                result["note"] = note
            _print(result)
        else:
            valid_names = list(KOC_FIELD_MAP if tmpl.upper() == "KOC" else UNDP_FIELD_MAP)
            if tmpl.upper() == "KOC":
                valid_names += list(KOC_FIELD_ALIASES.keys())
            _print({"error": f"'{fname}'은 {tmpl.upper()} 템플릿에 없음",
                    "valid_fields": sorted(valid_names)})

    # --- generate-id ---
    elif cmd == "generate-id":
        if len(args) < 3:
            _print({"error": "사용법: generate-id YYYY-MM-DD <sequence_int>"})
            sys.exit(1)
        try:
            rid = generate_record_id(args[1], int(args[2]))
            _print({"record_id": rid})
        except (ValueError, IndexError) as e:
            _print({"error": str(e)})

    # --- check-threshold ---
    elif cmd == "check-threshold":
        if len(args) < 3:
            _print({"error": "사용법: check-threshold <indicator_id_int> <current_value_float>"})
            sys.exit(1)
        try:
            result = check_indicator_threshold(int(args[1]), float(args[2]))
            _print(result)
        except ValueError as e:
            _print({"error": str(e)})

    # --- validate-domain ---
    elif cmd == "validate-domain":
        if len(args) < 3:
            _print({"error": "사용법: validate-domain KOC|UNDP <domain1> [domain2 ...]"})
            sys.exit(1)
        tmpl   = args[1]
        domains = args[2:]
        if tmpl.upper() == "KOC":
            ok, invalid = validate_koc_domains(domains)
            valid_list  = KOC_DOMAINS_ORDERED
        else:
            ok, invalid = validate_undp_classification(domains)
            valid_list  = UNDP_DOMAINS_ORDERED
        _print({
            "template":        tmpl.upper(),
            "input_domains":   domains,
            "valid":           ok,
            "invalid_domains": invalid,
            "approved_list":   valid_list,
        })

    # --- spike-detect ---
    elif cmd == "spike-detect":
        if len(args) < 3:
            _print({"error": "사용법: spike-detect <current_int> <previous_int> [ratio_threshold=2.0]"})
            sys.exit(1)
        threshold = float(args[3]) if len(args) >= 4 else 2.0
        try:
            result = detect_frequency_spike(int(args[1]), int(args[2]), threshold)
            _print(result)
        except ValueError as e:
            _print({"error": str(e)})

    # --- list-fields ---
    elif cmd == "list-fields":
        if len(args) < 2:
            _print({"error": "사용법: list-fields KOC|UNDP"})
            sys.exit(1)
        tmpl = args[1].upper()
        if tmpl == "KOC":
            fmap = KOC_FIELD_MAP
            note = "KOC field 10 = Date/Scanner 통합. 'scanner'도 field 10 조회 가능 (field-number KOC scanner)"
        elif tmpl == "UNDP":
            fmap = UNDP_FIELD_MAP
            note = None
        else:
            _print({"error": "KOC 또는 UNDP 중 하나"})
            sys.exit(1)
        result = {
            "template":     tmpl,
            "total_fields": KOC_TOTAL_FIELDS if tmpl == "KOC" else UNDP_TOTAL_FIELDS,
            "fields":       {str(v): k for k, v in sorted(fmap.items(), key=lambda x: x[1])},
        }
        if note:
            result["note"] = note
        _print(result)

    # --- list-domains ---
    elif cmd == "list-domains":
        if len(args) < 2:
            _print({"error": "사용법: list-domains KOC|UNDP"})
            sys.exit(1)
        tmpl = args[1].upper()
        if tmpl == "KOC":
            _print({
                "template": "KOC",
                "total_domains": len(KOC_DOMAINS_ORDERED),
                "domains": KOC_DOMAINS_ORDERED,
                "note": "Gordon-Glenn Section II 원전 순서 (TEEPS)"
            })
        elif tmpl == "UNDP":
            _print({
                "template": "UNDP",
                "total_domains": len(UNDP_DOMAINS_ORDERED),
                "domains": UNDP_DOMAINS_ORDERED,
                "note": "9 Gordon-Glenn 원전 + 1 박사님 추가 (Spirituality) — 원전 정규 순서 보존"
            })
        else:
            _print({"error": "KOC 또는 UNDP 중 하나"})

    # --- cross-map ---
    elif cmd == "cross-map":
        _print(cross_template_field_map())

    # --- list-indicators ---
    elif cmd == "list-indicators":
        _print({
            "count": len(INDICATOR_THRESHOLDS),
            "indicators": {
                str(k): {"name": v["name"], "threshold": v["threshold"],
                          "unit": v["unit"], "comparison": v["cmp"]}
                for k, v in sorted(INDICATOR_THRESHOLDS.items())
            },
        })

    # --- validate-completeness ---
    elif cmd == "validate-completeness":
        if len(args) < 2:
            _print({"error": "사용법: validate-completeness KOC|UNDP (stdin에서 JSON record 읽기)\n"
                             "예: echo '{\"domain\":\"Technological\",\"source\":\"Reuters\",\"date\":\"2026-05-09\"}' | "
                             "python3 validate_record.py validate-completeness KOC"})
            sys.exit(1)
        try:
            record_json = sys.stdin.read().strip()
            if not record_json:
                _print({"error": "stdin에서 JSON record를 읽지 못함"})
                sys.exit(1)
            record = json.loads(record_json)
            if not isinstance(record, dict):
                _print({"error": "JSON은 dict(object)여야 함"})
                sys.exit(1)
            result = field_completeness(record, args[1])
            _print(result)
        except json.JSONDecodeError as e:
            _print({"error": f"JSON 파싱 실패: {e}"})
            sys.exit(1)

    # --- analyze-domain-freq ---
    elif cmd == "analyze-domain-freq":
        if len(args) < 2:
            _print({"error": "사용법: analyze-domain-freq KOC|UNDP (stdin에서 JSON records array 읽기)\n"
                             "예: echo '[{\"classification\":\"Energy\"},{\"classification\":\"Science and Technology\"}]' | "
                             "python3 validate_record.py analyze-domain-freq UNDP"})
            sys.exit(1)
        try:
            records_json = sys.stdin.read().strip()
            if not records_json:
                _print({"error": "stdin에서 JSON records array를 읽지 못함"})
                sys.exit(1)
            records = json.loads(records_json)
            if not isinstance(records, list):
                _print({"error": "JSON은 array여야 함"})
                sys.exit(1)
            result = analyze_domain_frequency(records, args[1])
            _print(result)
        except json.JSONDecodeError as e:
            _print({"error": f"JSON 파싱 실패: {e}"})
            sys.exit(1)

    else:
        print(f"알 수 없는 명령: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
