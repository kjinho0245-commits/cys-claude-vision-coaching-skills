#!/usr/bin/env python3
"""
Deep Reasoning Engine — deterministic validation and scoring.
Source: 박사님 2026-05-11 강화 명령 — 6차 강제·차수별 검색 강제·출처 명시 강제.
Glenn J.C. (2009). Futures Wheel. FRM V3.0, Chapter 06, §III.A + §IV.

Implements deterministic components of 5 protocols:
  MDE — Minimum Depth Enforcement
  PRRG — Per-Ring Research Gate (6 Gates)
  CoER — Chain-of-Evidence Reasoning validation
  CCP — Citation Completeness Protocol (regex-based hallucination detection)
  SRS — Sewongjima Reversal Score

All arithmetic/regex/validation is deterministic — no LLM inference.
Called by SKILL.md at each gate decision point.

CLI usage:
    python3 reasoning_engine.py validate_gate < gate_request.json
    python3 reasoning_engine.py compute_srs < lineages.json
    python3 reasoning_engine.py check_sign_reversal < impacts.json
    python3 reasoning_engine.py check_coer < coer_entry.json
    python3 reasoning_engine.py check_ccp < text_data.json
    python3 reasoning_engine.py check_mde < mde_request.json
    python3 reasoning_engine.py gate_websearch_needed < gate_info.json
    python3 reasoning_engine.py validate_ring_quality < ring_data.json
    python3 reasoning_engine.py generate_source_trail < gate_logs.json
    python3 reasoning_engine.py check_excessive_reversal < srs_data.json
"""

import json
import re
import sys
from typing import List, Dict, Optional, Any, Tuple


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

VALID_GATES = ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')
GATE_RING_MAP = {
    'P1': ('Primary', 1),
    'P2': ('Secondary', 2),
    'P3': ('Tertiary', 3),
    'P4': ('Quaternary', 4),
    'P5': ('Quinary', 5),
    'P6': ('Senary', 6),
}
GATE_NAMES_FULL = {
    'P1': 'Gate_P1_Pre',
    'P2': 'Gate_P2_Pre',
    'P3': 'Gate_P3_Pre',
    'P4': 'Gate_P4_Pre',
    'P5': 'Gate_P5_Pre',
    'P6': 'Gate_P6_Pre',
}

# WebSearch minimums per gate
# P1: ≥3; P2: ≥N(primary count, min 5); P3: ≥M(secondary count, min 5); P4~P5: ≥3; P6: ≥2
GATE_WEBSEARCH_FIXED = {'P1': 3, 'P4': 3, 'P5': 3, 'P6': 2}
GATE_WEBSEARCH_PARENT_BASED = {'P2', 'P3'}  # min = max(5, parent_count)
GATE_PARENT_MIN = 5  # minimum even if parent_count < 5

# SRS thresholds (Section 2.5 — 4 levels)
SRS_EXCELLENT = 2.0   # avg ≥ 2.0
SRS_GOOD = 1.5        # avg 1.5~2.0
SRS_ACCEPTABLE = 1.0  # avg 1.0~1.5
SRS_INSUFFICIENT = 0.0  # avg < 1.0
SRS_EXCESSIVE = 3.5   # avg > 3.5 → wishful thinking warning

# Sign reversal requirements
SIGN_REVERSAL_GATES = {'P4': 0.5, 'P5': 0.5, 'P6': 0.5}  # ≥50% fraction
VALID_SIGNS = ('+', '-', '🟢', '🔴', '🟡', 'positive', 'negative', 'neutral')
POSITIVE_SIGNS = ('+', '🟢', 'positive')
NEGATIVE_SIGNS = ('-', '🔴', 'negative')
NEUTRAL_SIGNS = ('🟡', 'neutral')

# MDE constants
MDE_DEFAULT_DEPTH = 6
MDE_MIN_EXPLICIT_DEPTH = 3  # user can explicitly set ≥3
MDE_EXCEPTION_KEYWORDS = [
    '간단히', '빠르게', '대충', 'quick wheel', 'summary only',
    'brief', '간단', '빨리', '짧게'
]

# CoER structure requirements
COER_REQUIRED_STEPS = ('R1_text', 'R2_text', 'H_text')
COER_STEP_LABELS = {
    'R1_text': 'R-1 (Base Fact)',
    'R2_text': 'R-2 (Intermediate Inference)',
    'H_text': 'H (Leap to Impact)',
}
COER_CITATION_REQUIRED = ('R1_citation',)

# CCP — Vague attribution patterns (regex)
CCP_VAGUE_PATTERNS = [
    r'(전문가\s*의견)',
    r'(많은\s*연구에\s*따르면)',
    r'(보고서에\s*의하면)',
    r'(여러\s*미래학자들이\s*지적)',
    r'(통념상)',
    r'(일반적으로\s*알려진)',
    r'(연구에\s*따르면)',
    r'(전문가들은)',
    r'(studies\s+show)',
    r'(experts\s+say)',
    r'(many\s+researchers)',
    r'(widely\s+believed)',
]

# CCP — Fabricated source patterns (requires URL or verifiable info)
CCP_FABRICATED_PATTERNS = [
    r'study\s+by\s+\w+\s+University(?!\s*,\s*https?://)',
    r'research\s+from\s+\w+\s+Institute(?!\s*,\s*https?://)',
    r'report\s+from\s+\w+\s+(?:Foundation|Center)(?!\s*,\s*https?://)',
    r'according\s+to\s+(?:a|the)\s+\w+\s+(?:paper|article|study)(?!\s*,\s*https?://)',
]

# CCP — Unsourced specific numbers (should have R-1 citation)
CCP_UNSOURCED_NUMBER_PATTERNS = [
    r'\d+%(?:\s+(?:increase|decrease|reduction|growth|decline))?(?!\s*\[)',
    r'약\s*\d+\s*개(?!\s*\[)',
    r'T\+\d+y?(?:\s*~\s*T\+\d+y?)?(?!\s*\[)',
    r'\d{1,3}(?:,\d{3})*\s*(?:billion|million|trillion|명|개|건)(?!\s*\[)',
]

# Ring time ranges for quality gate
RING_TIME_YEARS = {
    1: (1, 5),
    2: (5, 10),
    3: (10, 20),
    4: (15, 25),
    5: (20, 30),
    6: (25, 50),
}


# ─────────────────────────────────────────────
# GATE REQUEST VALIDATION
# ─────────────────────────────────────────────

def validate_gate_request(data: Dict) -> Dict:
    """
    Validate caller's gate request (from basic-v1, domain-v2, etc.).
    Checks gate_id, prior state consistency, and required fields.
    """
    errors = []
    warnings = []

    gate_raw = data.get('gate_requested', '')
    # Normalize: accept 'Gate_P4_Pre', 'P4_Pre', 'P4'
    gate_id = gate_raw.replace('Gate_', '').replace('_Pre', '').upper()
    if gate_id not in VALID_GATES:
        errors.append(
            f"gate_requested='{gate_raw}' invalid. "
            f"Must be one of: {[GATE_NAMES_FULL[g] for g in VALID_GATES]}."
        )
        return {'valid': False, 'errors': errors, 'warnings': warnings}

    ring_name, ring_num = GATE_RING_MAP[gate_id]

    # Prior state consistency check
    prior = data.get('prior_state', {})
    completed = prior.get('ring_already_completed', [])
    upcoming = prior.get('upcoming_ring', '')

    # Gates P2~P6 require prior rings to be completed
    if ring_num >= 2:
        required_prior = [GATE_RING_MAP[f'P{i}'][0] for i in range(1, ring_num)]
        for rp in required_prior:
            if rp not in completed:
                errors.append(
                    f"Gate {gate_id} requires {rp} to be completed first. "
                    f"ring_already_completed={completed}."
                )

    # Caller field required
    if not data.get('caller_skill', '').strip():
        errors.append("'caller_skill' is required (e.g., 'vision-foresight-futures-wheel-basic-v1').")

    # blocking flag
    if not data.get('blocking', False):
        warnings.append(
            "blocking=false — gate response will be advisory, not mandatory. "
            "박사님 강화: blocking=true 권장."
        )

    normalized_gate = GATE_NAMES_FULL[gate_id]

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'gate_id': gate_id,
        'gate_name': normalized_gate,
        'ring_name': ring_name,
        'ring_num': ring_num,
    }


# ─────────────────────────────────────────────
# WEBSEARCH COUNT (PRRG)
# ─────────────────────────────────────────────

def gate_websearch_needed(data: Dict) -> Dict:
    """
    Compute minimum WebSearch count for a given Gate.
    P1: ≥3; P2,P3: ≥max(5, parent_count); P4,P5: ≥3; P6: ≥2
    SCBE mode: if caller == 'categorical-binary-expansion', use 6 (one per STEEPS category).
    """
    gate_raw = data.get('gate_id', '')
    gate_id = gate_raw.replace('Gate_', '').replace('_Pre', '').upper()
    if gate_id not in VALID_GATES:
        return {'error': f"gate_id='{gate_raw}' invalid. Use P1~P6."}

    parent_count = int(data.get('parent_count', 0))
    caller = data.get('caller_skill', '')
    scbe_mode = (caller == 'categorical-binary-expansion')

    if scbe_mode:
        # SCBE batching: 6 queries per gate (one per STEEPS category)
        min_count = 6
        formula = "SCBE mode: 6 queries (1 per STEEPS category)"
    elif gate_id in GATE_WEBSEARCH_PARENT_BASED:
        min_count = max(GATE_PARENT_MIN, parent_count)
        formula = f"max({GATE_PARENT_MIN}, parent_count={parent_count}) = {min_count}"
    else:
        min_count = GATE_WEBSEARCH_FIXED[gate_id]
        formula = f"fixed ≥{min_count} for {gate_id}"

    return {
        'gate_id': gate_id,
        'gate_name': GATE_NAMES_FULL[gate_id],
        'parent_count': parent_count,
        'min_websearch': min_count,
        'formula': formula,
        'scbe_mode': scbe_mode,
        'source': '박사님 2026-05-11 강화: PRRG 6 Gates WebSearch requirements',
    }


# ─────────────────────────────────────────────
# SIGN NORMALIZATION
# ─────────────────────────────────────────────

def normalize_sign(sign: str) -> str:
    """Normalize sign to '+', '-', or 'neutral'."""
    s = str(sign).strip()
    if s in POSITIVE_SIGNS:
        return '+'
    elif s in NEGATIVE_SIGNS:
        return '-'
    else:
        return 'neutral'


# ─────────────────────────────────────────────
# SIGN REVERSAL CHECK (PRRG Gates P4, P5, P6)
# ─────────────────────────────────────────────

def check_sign_reversal(data: Dict) -> Dict:
    """
    Check ≥50% sign reversal requirement for Quaternary/Quinary/Senary rings.
    Source: 박사님 강화 명령: "Quaternary의 50% 이상이 직전 Tertiary와 *반대 부호*여야 함"

    Fail condition: sign_reversal_fraction < 0.5 (NOT just sign_reversal_count==0).
    The SKILL.md Section 2.2 fail_condition 'sign_reversal_count == 0' is INCORRECT —
    the correct threshold is fraction < 0.5 per Section 2.2 description text.

    Input: {impacts: [{id, sign, parent_sign, ring_num}], gate_id}
    """
    impacts = data.get('impacts', [])
    gate_id = data.get('gate_id', '').replace('Gate_', '').replace('_Pre', '').upper()

    if not impacts:
        return {'passed': False, 'error': 'No impacts provided.'}

    if gate_id not in SIGN_REVERSAL_GATES:
        return {
            'gate_id': gate_id,
            'note': f"Sign reversal not required for Gate {gate_id}. Required only for P4, P5, P6.",
            'passed': True,
        }

    required_fraction = SIGN_REVERSAL_GATES[gate_id]

    # Normalize signs and filter evaluable
    evaluable = []
    for imp in impacts:
        s = normalize_sign(imp.get('sign', 'neutral'))
        ps = normalize_sign(imp.get('parent_sign', 'neutral'))
        if s in ('+', '-') and ps in ('+', '-'):
            evaluable.append({
                'id': imp.get('id', '?'),
                'sign': s,
                'parent_sign': ps,
                'reversed': s != ps,
            })

    if not evaluable:
        return {
            'gate_id': gate_id,
            'total_evaluable': 0,
            'passed': False,
            'error': (
                'No evaluable impacts (all signs neutral or missing). '
                'Assign + or - to impacts before gate check.'
            ),
        }

    total = len(evaluable)
    reversals = sum(1 for e in evaluable if e['reversed'])
    fraction = reversals / total
    passed = fraction >= required_fraction

    return {
        'gate_id': gate_id,
        'gate_name': GATE_NAMES_FULL.get(gate_id, gate_id),
        'ring_name': GATE_RING_MAP[gate_id][0] if gate_id in GATE_RING_MAP else gate_id,
        'total_evaluable': total,
        'reversals': reversals,
        'fraction': round(fraction, 4),
        'fraction_pct': f"{fraction*100:.1f}%",
        'required_fraction': required_fraction,
        'required_fraction_pct': f"{required_fraction*100:.0f}%",
        'passed': passed,
        'status': 'PASSED' if passed else 'BLOCKED — sign reversal fraction < 50%',
        'fail_note': (
            None if passed else
            "CORRECT FAIL CONDITION: fraction < 0.5 (NOT sign_reversal_count==0 per SKILL.md Section 2.2 description)"
        ),
        'details': evaluable,
        'source': '박사님 2026-05-11 강화: SIGN REVERSAL ≥50% 강제',
    }


# ─────────────────────────────────────────────
# SRS — SEWONGJIMA REVERSAL SCORE
# ─────────────────────────────────────────────

def compute_srs(data: Dict) -> Dict:
    """
    Compute SRS (Sewongjima Reversal Score).
    Source: Section 2.5 of SKILL.md (4-level thresholds).

    🟡 (neutral) signs are NOT counted as reversals.
    SRS per lineage = count of consecutive sign changes (only between + and -).

    Thresholds (4-level, from Section 2.5):
      excellent:   avg ≥ 2.0
      good:        avg 1.5~2.0
      acceptable:  avg 1.0~1.5
      insufficient: avg < 1.0 → REVISIONS_REQUIRED

    Excessive guard: avg > 3.5 → wishful thinking warning.

    Input: {lineages: [{id, signs: ['+','-',...], path_labels: [...]}]}
    """
    lineages = data.get('lineages', [])
    if not lineages:
        return {
            'avg_srs': 0.0, 'status': 'REVISIONS_REQUIRED',
            'error': 'No lineages provided.',
        }

    scores = []
    details = []
    skipped = []

    for lin in lineages:
        lin_id = lin.get('id', 'unknown')
        signs_raw = lin.get('signs', [])
        labels = lin.get('path_labels', signs_raw)

        # Normalize signs
        signs = [normalize_sign(s) for s in signs_raw]

        # Only evaluate consecutive pairs where both are + or -
        pairs = [(signs[i], signs[i+1]) for i in range(len(signs)-1)
                 if signs[i] in ('+', '-') and signs[i+1] in ('+', '-')]

        if len(pairs) < 1:
            skipped.append(lin_id)
            continue

        reversals = sum(1 for a, b in pairs if a != b)
        scores.append(reversals)
        details.append({
            'lineage_id': lin_id,
            'signs': signs,
            'path_labels': labels,
            'transitions_evaluated': len(pairs),
            'reversals': reversals,
            'srs': reversals,
        })

    if not scores:
        return {
            'avg_srs': 0.0,
            'status': 'REVISIONS_REQUIRED',
            'lineage_count': 0,
            'error': 'No lineages with evaluable sign transitions.',
        }

    avg_srs = round(sum(scores) / len(scores), 4)

    # Determine status (4-level)
    if avg_srs >= SRS_EXCELLENT:
        status = 'EXCELLENT'
        status_note = f"avg_SRS={avg_srs} ≥ {SRS_EXCELLENT} — rich 세옹지마 effect"
    elif avg_srs >= SRS_GOOD:
        status = 'GOOD'
        status_note = f"avg_SRS={avg_srs} in [{SRS_GOOD}, {SRS_EXCELLENT})"
    elif avg_srs >= SRS_ACCEPTABLE:
        status = 'ACCEPTABLE'
        status_note = f"avg_SRS={avg_srs} in [{SRS_ACCEPTABLE}, {SRS_GOOD})"
    else:
        status = 'REVISIONS_REQUIRED'
        status_note = f"avg_SRS={avg_srs} < {SRS_ACCEPTABLE} — 직선적 단정, Phase 6/7/8 재작업"

    # Excessive reversal guard
    excessive_warning = None
    if avg_srs > SRS_EXCESSIVE:
        excessive_warning = (
            f"avg_SRS={avg_srs} > {SRS_EXCESSIVE}: wishful thinking / dramatic narrative 의심. "
            "Plausibility 재검증 권장."
        )

    return {
        'avg_srs': avg_srs,
        'status': status,
        'status_note': status_note,
        'lineage_count': len(scores),
        'skipped_lineages': skipped,
        'excessive_reversal_warning': excessive_warning,
        'thresholds': {
            'excellent': f"avg_SRS ≥ {SRS_EXCELLENT}",
            'good': f"avg_SRS [{SRS_GOOD}, {SRS_EXCELLENT})",
            'acceptable': f"avg_SRS [{SRS_ACCEPTABLE}, {SRS_GOOD})",
            'revisions_required': f"avg_SRS < {SRS_ACCEPTABLE}",
            'excessive_guard': f"avg_SRS > {SRS_EXCESSIVE} → plausibility check",
        },
        'details': details,
        'source': '박사님 2026-05-11 강화: SRS (Sewongjima Reversal Score), Section 2.5',
    }


# ─────────────────────────────────────────────
# COER VALIDATION
# ─────────────────────────────────────────────

def check_coer(data: Dict) -> Dict:
    """
    Validate CoER (Chain-of-Evidence Reasoning) structure.
    Source: Section 2.3 of SKILL.md.

    Required structure per impact:
      R1_text + R1_citation (mandatory)
      R2_text
      H_text + disclosure (H step must disclose assumptions)

    Rejection criteria:
      - Missing R1/R2/H text
      - Missing R1 citation
      - Missing H disclosure
      - All steps are H-tagged (no base fact)
    """
    impacts = data.get('impacts', data.get('coer_entries', [data]))
    if not isinstance(impacts, list):
        impacts = [impacts]

    errors = []
    details = []

    for imp in impacts:
        imp_id = imp.get('id', imp.get('impact_id', 'unknown'))
        imp_errors = []

        r1 = str(imp.get('R1_text', '')).strip()
        r1_cite = str(imp.get('R1_citation', '')).strip()
        r2 = str(imp.get('R2_text', '')).strip()
        h = str(imp.get('H_text', '')).strip()
        h_disclosure = str(imp.get('H_disclosure', imp.get('disclosure', ''))).strip()

        if not r1:
            imp_errors.append("R-1 (Base Fact) text missing")
        if not r1_cite:
            imp_errors.append("R-1 citation missing — [저자/기관, 연도, URL] mandatory (CCP)")
        if not r2:
            imp_errors.append("R-2 (Intermediate Inference) missing")
        if not h:
            imp_errors.append("H (Leap to Impact) text missing")
        if h and not h_disclosure:
            imp_errors.append("H step disclosure missing — 본 step의 가정 명시 필수 (Section 2.3)")

        details.append({
            'id': imp_id,
            'label': imp.get('label', imp.get('claim', '')),
            'coer_complete': len(imp_errors) == 0,
            'errors': imp_errors,
        })
        errors.extend([f"'{imp_id}': {e}" for e in imp_errors])

    return {
        'valid': len(errors) == 0,
        'total_impacts': len(impacts),
        'complete_count': sum(1 for d in details if d['coer_complete']),
        'errors': errors,
        'details': details,
        'coer_definition': {
            'R1': 'Base Fact — verifiable, must have citation',
            'R2': 'Intermediate Inference — logical bridge',
            'H': 'Hypothesis/Leap — final impact, must disclose assumptions',
        },
        'source': 'Section 2.3 CoER Protocol',
    }


# ─────────────────────────────────────────────
# CCP — CITATION COMPLETENESS PROTOCOL
# ─────────────────────────────────────────────

def check_ccp(data: Dict) -> Dict:
    """
    Check text for CCP violations (Section 2.4).
    Detects:
      1. Vague attribution patterns (auto-reject)
      2. Fabricated source patterns (hallucination guard)
      3. Unsourced specific numbers (flag for R-1 requirement)

    Input: {text: str} or {impacts: [{id, text}]}
    """
    text_items = []
    if 'text' in data:
        text_items = [{'id': 'input', 'text': data['text']}]
    elif 'impacts' in data:
        text_items = [{'id': imp.get('id', str(i)), 'text': str(imp.get('text', ''))}
                      for i, imp in enumerate(data['impacts'])]
    else:
        return {'error': "Input must have 'text' or 'impacts' field."}

    all_violations = []
    details = []

    for item in text_items:
        item_id = item['id']
        text = item['text']
        violations = []

        # 1. Vague attribution
        for pattern in CCP_VAGUE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                violations.append({
                    'type': 'vague_attribution',
                    'matched': m if isinstance(m, str) else ' '.join(m),
                    'action': '자동 삭제 + 구체 citation 재요청',
                    'severity': 'REJECT',
                })

        # 2. Fabricated source patterns
        for pattern in CCP_FABRICATED_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                violations.append({
                    'type': 'fabricated_source_pattern',
                    'matched': m if isinstance(m, str) else ' '.join(m),
                    'action': 'hallucination guard 발동, 자동 삭제',
                    'severity': 'REJECT',
                })

        # 3. Unsourced specific numbers
        for pattern in CCP_UNSOURCED_NUMBER_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                violations.append({
                    'type': 'unsourced_specific_number',
                    'matched': m if isinstance(m, str) else ' '.join(m),
                    'action': 'R-1 출처 보강 또는 "추정" tag 강제',
                    'severity': 'FLAG',
                })

        details.append({
            'id': item_id,
            'violation_count': len(violations),
            'violations': violations,
            'ccp_clean': len(violations) == 0,
        })
        all_violations.extend(violations)

    reject_count = sum(1 for v in all_violations if v['severity'] == 'REJECT')
    flag_count = sum(1 for v in all_violations if v['severity'] == 'FLAG')

    return {
        'valid': reject_count == 0,
        'total_violations': len(all_violations),
        'reject_count': reject_count,
        'flag_count': flag_count,
        'details': details,
        'source': 'Section 2.4 CCP — Citation Completeness Protocol',
    }


# ─────────────────────────────────────────────
# MDE — MINIMUM DEPTH ENFORCEMENT
# ─────────────────────────────────────────────

def check_mde(data: Dict) -> Dict:
    """
    Validate depth_target against MDE protocol (Section 2.1).
    Returns whether depth is acceptable and any adjustments needed.

    MDE rules:
      - Default: depth = 6
      - Exception: user explicitly says "간단히/빠르게/대충/Quick wheel/summary only"
        → minimum depth = 3 (explicit specification)
      - User specifies "N차까지": N ≥ 3 allowed, N < 3 rejected
      - depth_target < 6 without exception: advisory warning
      - depth_target > 6: allowed (higher-order, 7+)
    """
    depth_target = data.get('depth_target', MDE_DEFAULT_DEPTH)
    user_input = str(data.get('user_input', '')).lower()
    user_depth_explicit = data.get('user_depth_explicit', False)

    errors = []
    warnings = []

    # Check for exception keywords
    has_exception = any(kw.lower() in user_input for kw in MDE_EXCEPTION_KEYWORDS)

    if not isinstance(depth_target, int):
        errors.append(f"depth_target must be an integer, got: {depth_target!r}")
        return {'valid': False, 'errors': errors}

    # Minimum depth enforcement
    if depth_target < 3:
        errors.append(
            f"depth_target={depth_target} < 3 is rejected. "
            f"MDE minimum: 3 (only with user exception keywords). "
            f"Default: {MDE_DEFAULT_DEPTH}."
        )
    elif depth_target < MDE_DEFAULT_DEPTH:
        if has_exception:
            warnings.append(
                f"depth_target={depth_target} accepted (exception keyword detected: "
                f"{[kw for kw in MDE_EXCEPTION_KEYWORDS if kw.lower() in user_input]}). "
                f"박사님 강화: 6차 default를 {depth_target}차로 조정."
            )
        else:
            warnings.append(
                f"depth_target={depth_target} < {MDE_DEFAULT_DEPTH}. "
                f"박사님 강화 protocol에 따라 6차 default. "
                f"명시적으로 줄이시려면 '간단히'/'빠르게' 등 명시 필요."
            )

    return {
        'valid': len(errors) == 0,
        'depth_target': depth_target,
        'effective_depth': depth_target if len(errors) == 0 else MDE_DEFAULT_DEPTH,
        'exception_active': has_exception,
        'exception_keywords_detected': [kw for kw in MDE_EXCEPTION_KEYWORDS if kw.lower() in user_input],
        'default_depth': MDE_DEFAULT_DEPTH,
        'errors': errors,
        'warnings': warnings,
        'source': 'Section 2.1 MDE Protocol',
    }


# ─────────────────────────────────────────────
# RING QUALITY VALIDATION (MDE Per-Ring Gate)
# ─────────────────────────────────────────────

def validate_ring_quality(data: Dict) -> Dict:
    """
    Validate per-ring quality requirements from MDE Section 2.1 + PRRG Gate fail_conditions.
    Each ring must:
      1. Have time frame ≥5 years later than prior ring (deterministic)
      2. Have distinct domain or target group (LLM-reported boolean)
      3. Show qualitative mechanism change (LLM-reported boolean)
    Gate P3-specific:
      4. historical_analog_count ≥ 1 (Gate_P3_Pre fail_condition per Section 2.2)
    """
    ring_num = int(data.get('ring_num', 0))
    ring_time_start = data.get('ring_time_start')
    prior_ring_time_end = data.get('prior_ring_time_end')

    errors = []
    warnings = []

    RING_NAMES_MAP = {1:'Primary',2:'Secondary',3:'Tertiary',4:'Quaternary',5:'Quinary',6:'Senary'}

    if ring_num not in RING_TIME_YEARS:
        errors.append(f"ring_num={ring_num} invalid. Must be 1-6.")
        return {'valid': False, 'errors': errors}

    expected_start, expected_end = RING_TIME_YEARS[ring_num]

    # Time frame check (deterministic)
    if ring_time_start is not None and prior_ring_time_end is not None:
        gap = ring_time_start - prior_ring_time_end
        if gap < 5:
            errors.append(
                f"Ring {ring_num} time gap = {gap}y < 5y minimum. "
                f"MDE Section 2.1: '이전 차수와 시간 5년 이상 간극'"
            )

    # Gate P3 specific: historical_analog_count (Section 2.2 Gate_P3_Pre fail_condition)
    if ring_num == 3:
        historical_analog_count = data.get('historical_analog_count', None)
        if historical_analog_count is not None:
            if historical_analog_count < 1:
                errors.append(
                    f"Ring 3 (Tertiary): historical_analog_count={historical_analog_count} < 1. "
                    f"Gate_P3_Pre fail_condition: 'historical_analog_count < 1'. "
                    f"Section 2.2: 'historical analog 최소 1건' required."
                )
        else:
            warnings.append(
                "historical_analog_count not provided for Ring 3 (Tertiary). "
                "Gate_P3_Pre requires ≥1 historical analog. Pass historical_analog_count to enforce."
            )

    # Content quality checks (LLM-reported)
    domain_distinct = data.get('domain_distinct', None)
    qualitative_change = data.get('qualitative_change', None)

    if domain_distinct is False:
        errors.append(
            f"Ring {ring_num} domain NOT distinct from prior ring. "
            "MDE: '이전 차수와 domain 또는 대상 집단 명확 구별'"
        )
    if qualitative_change is False:
        errors.append(
            f"Ring {ring_num} shows only intensity increase, not qualitative mechanism change. "
            "MDE: '이전 차수와 질적 메커니즘 변화 (강도 증가 아닌 새 현상)'"
        )

    return {
        'valid': len(errors) == 0,
        'ring_num': ring_num,
        'ring_name': RING_NAMES_MAP.get(ring_num, '?'),
        'expected_time_range': f"T+{expected_start}~{expected_end}y",
        'errors': errors,
        'warnings': warnings,
        'source': 'Section 2.1 MDE per_ring_quality_gate + Section 2.2 PRRG Gate_P3_Pre',
    }


# ─────────────────────────────────────────────
# EXCESSIVE REVERSAL CHECK
# ─────────────────────────────────────────────

def check_excessive_reversal(data: Dict) -> Dict:
    """
    Check if avg_srs exceeds wishful thinking threshold (>3.5).
    Source: Section 2.5 Excessive_Reversal_Guard.
    """
    avg_srs = float(data.get('avg_srs', 0.0))
    is_excessive = avg_srs > SRS_EXCESSIVE

    return {
        'avg_srs': avg_srs,
        'excessive_threshold': SRS_EXCESSIVE,
        'is_excessive': is_excessive,
        'action': (
            f"avg_SRS={avg_srs} > {SRS_EXCESSIVE}: "
            "wishful thinking / dramatic narrative 의심. "
            "Plausibility 재검증 강제. 일부 reversals 근거 재확인."
        ) if is_excessive else None,
        'status': 'WARNING — plausibility check required' if is_excessive else 'OK',
        'source': 'Section 2.5 Excessive_Reversal_Guard',
    }


# ─────────────────────────────────────────────
# SOURCE TRAIL GENERATION
# ─────────────────────────────────────────────

def generate_source_trail(data: Dict) -> Dict:
    """
    Generate Source Trail markdown from accumulated gate logs.
    Deterministic: aggregates counts and formats markdown table.
    """
    gate_logs = data.get('gate_logs', [])
    if not gate_logs:
        return {'error': 'No gate_logs provided.', 'trail': ''}

    rows = ['| Ring | Gate | Searches | Citations | Analog | Tier |',
            '|------|------|----------|-----------|--------|------|']

    totals = {'searches': 0, 'citations': 0, 'analogs': 0}
    for log in gate_logs:
        ring = log.get('ring_name', '?')
        gate = log.get('gate_name', '?')
        searches = int(log.get('searches_executed', 0))
        citations = int(log.get('citations_collected', 0))
        analog = int(log.get('analogs_found', 0))
        tier = log.get('dominant_tier', '?')
        rows.append(f"| {ring} | {gate} | {searches} | {citations} | {analog} | {tier} |")
        totals['searches'] += searches
        totals['citations'] += citations
        totals['analogs'] += analog

    rows.append(f"| **TOTAL** | | **{totals['searches']}** | **{totals['citations']}** | **{totals['analogs']}** | |")

    srs_data = data.get('srs_report', {})
    avg_srs = srs_data.get('avg_srs', 'N/A')
    srs_status = srs_data.get('status', 'N/A')

    ccp_data = data.get('ccp_summary', {})
    hg_data = data.get('hallucination_guard', {})

    trail = f"""## 📚 Source Trail (deep-reasoning-engine 누적)

### Per-Ring Pre-Research Log
{chr(10).join(rows)}

### SRS (Sewongjima Reversal Score)
- Avg SRS: **{avg_srs}** — {srs_status}

### Hallucination Guard Activity
- Vague attribution rejected: {hg_data.get('vague_rejected', 0)}
- Fabricated source detected: {hg_data.get('fabricated_detected', 0)}
- Unsourced numbers flagged: {hg_data.get('unsourced_flagged', 0)}

### CCP Compliance
- All impacts with citation: {ccp_data.get('citation_coverage', 'N/A')}
- Reject violations: {ccp_data.get('reject_count', 0)}
"""

    return {
        'trail_markdown': trail,
        'totals': totals,
        'source': 'Section 6 Source Trail output format',
    }


# ─────────────────────────────────────────────
# CLI DISPATCH
# ─────────────────────────────────────────────

def compute_sign_reversal_directive(data: Dict) -> Dict:
    """
    Compute sign_reversal_directive for Section 4.2 gate response.
    Determines dominant sign of prior rings and states requirement for next ring.
    Source: Section 4.2 response schema, PRRG Gate P4/P5/P6.

    Input: {gate_id, prior_signs: {primary:[...], secondary:[...], tertiary:[...]}}
    """
    gate_raw = data.get('gate_id', '')
    gate_id = gate_raw.replace('Gate_', '').replace('_Pre', '').upper()
    if gate_id not in VALID_GATES:
        return {'error': f"gate_id='{gate_raw}' invalid."}

    if gate_id not in ('P4', 'P5', 'P6'):
        return {
            'gate_id': gate_id,
            'note': f"sign_reversal_directive only applies to Gates P4, P5, P6.",
            'required': False,
        }

    prior_signs = data.get('prior_signs', {})

    def dominant_sign(signs: List) -> str:
        normalized = [normalize_sign(s) for s in signs]
        pos = sum(1 for s in normalized if s == '+')
        neg = sum(1 for s in normalized if s == '-')
        if pos > neg:
            return '🟢 (+)'
        elif neg > pos:
            return '🔴 (-)'
        else:
            return '🟡 (tie)'

    ring_dominants = {}
    for ring_name, signs in prior_signs.items():
        ring_dominants[ring_name] = dominant_sign(signs)

    # Determine which ring's dominant is being reversed
    gate_to_reversed_ring = {'P4': 'tertiary', 'P5': 'quaternary', 'P6': 'quinary'}
    reversed_ring = gate_to_reversed_ring[gate_id]
    prior_dominant = ring_dominants.get(reversed_ring, '🟡 (unknown)')

    required_opposite = '🟢 (+)' if '🔴' in prior_dominant else '🔴 (-)' if '🟢' in prior_dominant else '🟡 (unknown)'
    next_ring = GATE_RING_MAP[gate_id][0]

    return {
        'gate_id': gate_id,
        'prior_sign_dominants': ring_dominants,
        'reversed_ring': reversed_ring,
        'prior_dominant_sign': prior_dominant,
        'NEXT_RING_REQUIRED': f"≥50% of {next_ring} impacts must be {required_opposite} (세옹지마 반전 강제)",
        'source': 'Section 4.2 response schema + Section 2.2 SIGN REVERSAL 강제',
    }


COMMANDS = {
    'validate_gate': lambda d: validate_gate_request(d),
    'gate_websearch_needed': lambda d: gate_websearch_needed(d),
    'check_sign_reversal': lambda d: check_sign_reversal(d),
    'compute_srs': lambda d: compute_srs(d),
    'check_coer': lambda d: check_coer(d),
    'check_ccp': lambda d: check_ccp(d),
    'check_mde': lambda d: check_mde(d),
    'validate_ring_quality': lambda d: validate_ring_quality(d),
    'check_excessive_reversal': lambda d: check_excessive_reversal(d),
    'generate_source_trail': lambda d: generate_source_trail(d),
    'sign_reversal_directive': lambda d: compute_sign_reversal_directive(d),
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        valid = ', '.join(COMMANDS.keys())
        print(json.dumps({'error': f'Usage: python3 reasoning_engine.py <command> < input.json. Commands: {valid}'}),
              file=sys.stderr)
        sys.exit(1)
    command = sys.argv[1]
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'JSON parse error: {e}'}), file=sys.stderr)
        sys.exit(1)
    try:
        result = COMMANDS[command](data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'error': f'Unexpected: {e}'}), file=sys.stderr)
        sys.exit(2)
