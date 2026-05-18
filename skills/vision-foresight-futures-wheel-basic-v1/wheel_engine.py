#!/usr/bin/env python3
"""
Futures Wheel Basic V1 Engine — deterministic computations.
Source: Glenn J.C. (2009). Futures Wheel. In J.C. Glenn & T.J. Gordon (Eds.),
  Futures Research Methodology V3.0, Chapter 06, §III.A.
  Wagschal P. (cited in Glenn 2009 §III.A): unanimity rule.
  박사님 2026-05-11 6차 강화: SRS (Sewongjima Reversal Score).

All arithmetic, validation, and scoring in this module is deterministic.
No LLM inference. Called by vision-foresight-futures-wheel-basic-v1 SKILL.md.

CLI usage:
    python3 wheel_engine.py validate < input.json
    python3 wheel_engine.py websearch_count < ring_info.json
    python3 wheel_engine.py check_sign_reversal < impacts.json
    python3 wheel_engine.py compute_srs < lineages.json
    python3 wheel_engine.py validate_ring_counts < wheel_data.json
    python3 wheel_engine.py build_ring_table < wheel_data.json
    python3 wheel_engine.py check_coer < coer_data.json
"""

import json
import sys
from typing import List, Dict, Optional, Any, Tuple


# ─────────────────────────────────────────────
# CONSTANTS (from Glenn 2009 §III.A + 박사님 강화)
# ─────────────────────────────────────────────

RING_NAMES = {
    1: 'Primary',
    2: 'Secondary',
    3: 'Tertiary',
    4: 'Quaternary',
    5: 'Quinary',
    6: 'Senary',
}

RING_TIME_FRAMES = {
    1: 'T+1~5y',
    2: 'T+5~10y',
    3: 'T+10~20y',
    4: 'T+15~25y',   # Quaternary — 세옹지마 1차 반전
    5: 'T+20~30y',   # Quinary   — 세옹지마 2차 반전
    6: 'T+25~50y',   # Senary    — 세옹지마 3차 반전·문명 단위
}

RING_COUNT_RULES = {
    # ring_num: (min_per_parent, max_per_parent)
    1: (5, 10),   # Primary: 5~10 from Center
    2: (2, 3),    # Secondary: 2~3 per Primary
    3: (1, 2),    # Tertiary: 1~2 per Secondary
    4: (1, 2),    # Quaternary: 1~2 per Tertiary
    5: (1, 2),    # Quinary: 1~2 per Quaternary
    6: (1, 2),    # Senary: 1~2 per Quinary
}

DEFAULT_DEPTH = 6   # 박사님 2026-05-11 강화: 6차 default

VALID_EVALUATION_MODES = ('fast', 'wagschal')
VALID_SIGNS = ('+', '-', 'neutral')

# WebSearch minimum counts per ring
# Phase 2 (Primary): ≥3
# Phase 4 (Secondary): ≥N (N = primary_count)
# Phase 5 (Tertiary): ≥M (M = secondary_count)
# Phase 6 (Quaternary): ≥3
# Phase 7 (Quinary): ≥3
# Phase 8 (Senary): ≥2
WEBSEARCH_BASE = {1: 3, 2: 'parent_count', 3: 'parent_count', 4: 3, 5: 3, 6: 2}

# SRS thresholds (Sewongjima Reversal Score)
SRS_EXCELLENT = 1.5   # avg reversals per lineage ≥ 1.5 → 우수
SRS_MINIMUM = 1.0     # avg reversals per lineage < 1.0 → REVISIONS_REQUIRED

# Sign reversal requirements per ring
SIGN_REVERSAL_MIN_FRACTION = {4: 0.5, 5: 0.5, 6: 0.5}  # ≥50% for rings 4,5,6

# CoER: Chain of Evidence Reasoning — 3-step structure
COER_STEPS = ('R-1 (Base Fact)', 'R-2 (Intermediate)', 'H (Hypothesis/Leap)')
COER_STEP_COUNT = 3


# ─────────────────────────────────────────────
# INPUT VALIDATION
# ─────────────────────────────────────────────

def validate_input(data: Dict) -> Dict:
    """
    Validate master input for vision-foresight-futures-wheel-basic-v1.
    Returns: {valid, errors, warnings, normalized}
    """
    errors = []
    warnings = []

    # center_issue: required
    ci = data.get('center_issue', {})
    if not ci or not isinstance(ci, dict):
        errors.append("'center_issue' must be a dict with {what, when, where, who}.")
    else:
        for field in ('what', 'when', 'where', 'who'):
            if not ci.get(field, '').strip():
                errors.append(f"'center_issue.{field}' is required and must not be empty.")

    # depth_target: [1, 6], default 6
    depth = data.get('depth_target', DEFAULT_DEPTH)
    if not isinstance(depth, int) or not (1 <= depth <= 6):
        errors.append(
            f"'depth_target'={depth} must be integer in [1, 6]. "
            f"Default is {DEFAULT_DEPTH} (박사님 6차 강화 명령)."
        )
    if depth != DEFAULT_DEPTH and not errors:
        warnings.append(
            f"depth_target={depth} overrides default {DEFAULT_DEPTH}. "
            f"박사님 2026-05-11 강화: 6차 기본값. 의도적 변경인지 확인."
        )

    # primary_count_target: [5, 10]
    pct = data.get('primary_count_target', 7)
    if not isinstance(pct, int) or not (5 <= pct <= 10):
        errors.append(
            f"'primary_count_target'={pct} must be integer in [5, 10]. "
            f"Glenn (2009) §III.A: 'the leader draws short wheel-like spokes' — typically 5-10."
        )

    # secondary_per_primary: [2, 3]
    spp = data.get('secondary_per_primary', 2)
    if not isinstance(spp, int) or not (2 <= spp <= 3):
        errors.append(
            f"'secondary_per_primary'={spp} must be integer in [2, 3]. "
            f"Glenn (2009): 'two or three short spokes out from each of the ovals'."
        )

    # tertiary_per_secondary: [1, 2]
    tps = data.get('tertiary_per_secondary', 1)
    if not isinstance(tps, int) or not (1 <= tps <= 2):
        errors.append(
            f"'tertiary_per_secondary'={tps} must be integer in [1, 2]."
        )

    # evaluation_mode
    em = data.get('evaluation_mode', 'fast')
    if em not in VALID_EVALUATION_MODES:
        errors.append(
            f"'evaluation_mode'='{em}' invalid. Must be one of: {VALID_EVALUATION_MODES}. "
            f"'fast'=list quickly then evaluate; "
            f"'wagschal'=unanimity rule before entering (Glenn 2009 §III.A)."
        )

    normalized = {
        'center_issue': ci,
        'depth_target': depth if isinstance(depth, int) else DEFAULT_DEPTH,
        'primary_count_target': pct if isinstance(pct, int) else 7,
        'secondary_per_primary': spp if isinstance(spp, int) else 2,
        'tertiary_per_secondary': tps if isinstance(tps, int) else 1,
        'evaluation_mode': em if em in VALID_EVALUATION_MODES else 'fast',
        'expert_pool_cast': data.get('expert_pool_cast', []),
        'domains_frame': data.get('domains_frame', 'free-form'),
    }

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'normalized': normalized,
    }


# ─────────────────────────────────────────────
# WEBSEARCH COUNT CALCULATION
# ─────────────────────────────────────────────

def compute_websearch_needed(ring_num: int, parent_count: int) -> Dict:
    """
    Compute minimum WebSearch count required before processing each ring's Gate.
    Glenn (2009) + 박사님 강화:
      Ring 1 (Primary): WebSearch ≥3
      Ring 2 (Secondary): WebSearch ≥N (N=primary count)
      Ring 3 (Tertiary): WebSearch ≥M (M=secondary count)
      Ring 4 (Quaternary): WebSearch ≥3
      Ring 5 (Quinary): WebSearch ≥3
      Ring 6 (Senary): WebSearch ≥2
    """
    if ring_num not in RING_NAMES:
        return {'error': f"ring_num={ring_num} invalid. Must be 1-6."}

    rule = WEBSEARCH_BASE.get(ring_num, 3)
    if rule == 'parent_count':
        min_count = max(3, parent_count)  # at least 3, or parent count
    else:
        min_count = rule

    return {
        'ring_num': ring_num,
        'ring_name': RING_NAMES[ring_num],
        'parent_count': parent_count,
        'min_websearch': min_count,
        'formula': (
            f"≥{parent_count} (=parent_count={parent_count})"
            if WEBSEARCH_BASE.get(ring_num) == 'parent_count'
            else f"≥{min_count} (fixed for ring {ring_num})"
        ),
    }


# ─────────────────────────────────────────────
# SIGN REVERSAL CHECK (Phases 6, 7, 8)
# ─────────────────────────────────────────────

def check_sign_reversal(impacts: List[Dict]) -> Dict:
    """
    Check ≥50% sign reversal requirement for Quaternary/Quinary/Senary rings.
    박사님 강화: rings 4, 5, 6 must have ≥50% opposite-sign children.

    Each impact: {id, sign ('+'/'-'/'neutral'), parent_id, parent_sign, ring_num}
    A "reversal" = child sign differs from parent sign (excluding 'neutral').

    Returns: {ring_num, total, reversals, fraction, passed, details}
    """
    if not impacts:
        return {
            'total': 0, 'reversals': 0, 'fraction': 0.0,
            'passed': False, 'error': 'No impacts provided.',
        }

    ring_nums = {imp.get('ring_num') for imp in impacts}
    if len(ring_nums) > 1:
        return {'error': 'All impacts must be from the same ring for sign reversal check.'}

    ring_num = next(iter(ring_nums))
    if ring_num not in SIGN_REVERSAL_MIN_FRACTION:
        return {
            'ring_num': ring_num,
            'note': f"Sign reversal requirement not applicable to ring {ring_num} (only rings 4,5,6).",
            'passed': True,
        }

    required_fraction = SIGN_REVERSAL_MIN_FRACTION[ring_num]
    evaluable = [imp for imp in impacts
                 if imp.get('sign') in ('+', '-') and imp.get('parent_sign') in ('+', '-')]
    total_evaluable = len(evaluable)

    if total_evaluable == 0:
        return {
            'ring_num': ring_num,
            'ring_name': RING_NAMES[ring_num],
            'total_evaluable': 0,
            'reversals': 0,
            'fraction': 0.0,
            'required_fraction': required_fraction,
            'passed': False,
            'error': (
                'No evaluable impacts (all signs are neutral or missing). '
                'Assign + or - signs to impacts before checking reversal.'
            ),
        }

    reversals = sum(
        1 for imp in evaluable if imp['sign'] != imp['parent_sign']
    )
    fraction = reversals / total_evaluable
    passed = fraction >= required_fraction

    details = []
    for imp in evaluable:
        reversed_ = imp['sign'] != imp['parent_sign']
        details.append({
            'id': imp.get('id'),
            'sign': imp['sign'],
            'parent_id': imp.get('parent_id'),
            'parent_sign': imp['parent_sign'],
            'reversed': reversed_,
        })

    return {
        'ring_num': ring_num,
        'ring_name': RING_NAMES[ring_num],
        'total_evaluable': total_evaluable,
        'reversals': reversals,
        'fraction': round(fraction, 4),
        'fraction_pct': f"{fraction*100:.1f}%",
        'required_fraction': required_fraction,
        'required_fraction_pct': f"{required_fraction*100:.0f}%",
        'passed': passed,
        'status': 'PASS' if passed else 'FAIL — sign reversal < 50%, Gate BLOCKED',
        'details': details,
        'source': 'Glenn (2009) §III.A + 박사님 2026-05-11 강화: SIGN REVERSAL ≥50% 강제',
    }


# ─────────────────────────────────────────────
# SRS — SEWONGJIMA REVERSAL SCORE
# ─────────────────────────────────────────────

def compute_srs(lineages: List[Dict]) -> Dict:
    """
    Compute SRS (Sewongjima Reversal Score) for all lineages.
    박사님 2026-05-11 강화 정의:
      A lineage = ordered list of signs from Center → P → S → T → Q → Qn → Sn
      e.g. ['+', '-', '+', '-', '+', '-', '+']  (7 nodes, 6 transitions)
      reversal_count = number of consecutive sign changes (excluding 'neutral')
      SRS_lineage = reversal_count  (raw count, not normalized)
      avg_SRS = mean(SRS_lineage for all lineages with ≥2 evaluable signs)

    Thresholds:
      avg_SRS ≥ 1.5 → EXCELLENT (rich 세옹지마 effect)
      avg_SRS 1.0~1.49 → ACCEPTABLE
      avg_SRS < 1.0 → REVISIONS_REQUIRED (insufficient reversal depth)

    Each lineage: {id, signs: ['+', '-', '+', ...], path_labels: [...]}
    Signs must match path length. 'neutral' signs are skipped in reversal counting.
    """
    if not lineages:
        return {
            'avg_srs': 0.0, 'status': 'REVISIONS_REQUIRED',
            'error': 'No lineages provided.',
        }

    lineage_scores = []
    details = []
    skipped = []

    for lin in lineages:
        lin_id = lin.get('id', 'unknown')
        signs = lin.get('signs', [])
        labels = lin.get('path_labels', signs)

        # Filter out neutral signs for counting
        evaluable = [(signs[i], signs[i+1]) for i in range(len(signs)-1)
                     if signs[i] in ('+', '-') and signs[i+1] in ('+', '-')]

        if len(evaluable) < 1:
            skipped.append(lin_id)
            continue

        reversals = sum(1 for a, b in evaluable if a != b)
        lineage_scores.append(reversals)
        details.append({
            'lineage_id': lin_id,
            'signs': signs,
            'path_labels': labels,
            'transitions_evaluated': len(evaluable),
            'reversals': reversals,
            'srs': reversals,
        })

    if not lineage_scores:
        return {
            'avg_srs': 0.0,
            'status': 'REVISIONS_REQUIRED',
            'lineage_count': 0,
            'error': 'No lineages had evaluable sign transitions.',
        }

    avg_srs = round(sum(lineage_scores) / len(lineage_scores), 4)

    if avg_srs >= SRS_EXCELLENT:
        status = 'EXCELLENT'
    elif avg_srs >= SRS_MINIMUM:
        status = 'ACCEPTABLE'
    else:
        status = 'REVISIONS_REQUIRED'

    return {
        'avg_srs': avg_srs,
        'status': status,
        'status_detail': (
            f"avg_SRS={avg_srs:.4f} "
            f"({'≥'+str(SRS_EXCELLENT)+' EXCELLENT' if avg_srs>=SRS_EXCELLENT else '≥'+str(SRS_MINIMUM)+' ACCEPTABLE' if avg_srs>=SRS_MINIMUM else '<'+str(SRS_MINIMUM)+' REVISIONS_REQUIRED'})"
        ),
        'lineage_count': len(lineage_scores),
        'skipped_lineages': skipped,
        'thresholds': {
            'excellent': f"avg_SRS ≥ {SRS_EXCELLENT}",
            'acceptable': f"avg_SRS ≥ {SRS_MINIMUM}",
            'revisions_required': f"avg_SRS < {SRS_MINIMUM}",
        },
        'details': details,
        'source': '박사님 2026-05-11 강화: SRS (Sewongjima Reversal Score)',
    }


# ─────────────────────────────────────────────
# RING COUNT VALIDATION
# ─────────────────────────────────────────────

def validate_ring_counts(wheel_data: Dict) -> Dict:
    """
    Validate that each ring meets count requirements per Glenn (2009) §III.A.
    wheel_data: {
      ring_1: [{id, parent_id, label, sign}, ...],
      ring_2: [...], ..., ring_6: [...]
    }
    """
    errors = []
    warnings = []
    results = {}

    depth_target = wheel_data.get('depth_target', DEFAULT_DEPTH)
    rings = {}
    for i in range(1, 7):
        key = f'ring_{i}'
        rings[i] = wheel_data.get(key, [])

    center_id = wheel_data.get('center_id', 'Center')

    for ring_num in range(1, depth_target + 1):
        impacts = rings[ring_num]
        min_per_parent, max_per_parent = RING_COUNT_RULES[ring_num]

        if ring_num == 1:
            # Primary: parent is Center
            n = len(impacts)
            passed = min_per_parent <= n <= max_per_parent
            results[str(ring_num)] = {
                'ring_name': RING_NAMES[ring_num],
                'total': n,
                'parent': center_id,
                'parent_count': 1,
                'required_per_parent': f"{min_per_parent}~{max_per_parent}",
                'passed': passed,
            }
            if not passed:
                errors.append(
                    f"Ring 1 (Primary): {n} impacts found, "
                    f"need {min_per_parent}~{max_per_parent}. "
                    f"Glenn (2009): 'the leader draws short wheel-like spokes' (5~10)."
                )
        else:
            # For rings 2+: validate per parent
            parent_ring = rings[ring_num - 1]
            parent_ids = {p['id'] for p in parent_ring}
            per_parent = {}
            for imp in impacts:
                pid = imp.get('parent_id')
                per_parent.setdefault(pid, []).append(imp)

            # Check each parent has correct number of children
            ring_errors = []
            for pid in parent_ids:
                children = per_parent.get(pid, [])
                n_children = len(children)
                if not (min_per_parent <= n_children <= max_per_parent):
                    ring_errors.append(
                        f"Parent '{pid}' has {n_children} children in ring {ring_num} "
                        f"(need {min_per_parent}~{max_per_parent})"
                    )

            results[str(ring_num)] = {
                'ring_name': RING_NAMES[ring_num],
                'total': len(impacts),
                'parent_count': len(parent_ids),
                'required_per_parent': f"{min_per_parent}~{max_per_parent}",
                'per_parent_errors': ring_errors,
                'passed': len(ring_errors) == 0,
            }
            errors.extend(ring_errors)

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'ring_results': results,
        'depth_target': depth_target,
    }


# ─────────────────────────────────────────────
# RING TABLE BUILDER
# ─────────────────────────────────────────────

def build_ring_table(wheel_data: Dict) -> Dict:
    """
    Build the markdown ring table for all 6 rings.
    Output includes all rings up to depth_target.
    """
    depth_target = wheel_data.get('depth_target', DEFAULT_DEPTH)
    rows = []
    rows.append("| 차수 | # | Impact | 시간 | 부모 oval | 부호 |")
    rows.append("|-----|---|--------|------|-----------|------|")

    for ring_num in range(1, depth_target + 1):
        key = f'ring_{ring_num}'
        impacts = wheel_data.get(key, [])
        ring_name = RING_NAMES[ring_num]
        time_frame = RING_TIME_FRAMES[ring_num]

        for imp in impacts:
            imp_id = imp.get('id', '?')
            label = imp.get('label', '?')
            parent_id = imp.get('parent_id', 'Center' if ring_num == 1 else '?')
            sign = imp.get('sign', '?')
            rows.append(f"| {ring_name} | {imp_id} | {label} | {time_frame} | {parent_id} | {sign} |")

    # Count summary
    summary = {}
    total = 0
    for ring_num in range(1, depth_target + 1):
        key = f'ring_{ring_num}'
        n = len(wheel_data.get(key, []))
        summary[RING_NAMES[ring_num].lower()] = n
        total += n

    return {
        'table_markdown': '\n'.join(rows),
        'ring_count': summary,
        'total_impacts': total,
        'depth_target': depth_target,
    }


# ─────────────────────────────────────────────
# CoER VALIDATION — Chain of Evidence Reasoning
# ─────────────────────────────────────────────

def check_coer(coer_data: List[Dict]) -> Dict:
    """
    Validate CoER (Chain of Evidence Reasoning) 3-step structure.
    Glenn (2009) §III.A + 박사님 강화: each impact must have:
      R-1: Base Fact (sourced, verifiable claim)
      R-2: Intermediate (logical bridge)
      H: Hypothesis/Leap (the impact itself)
    Plus inline citation mandatory for R-1.

    Each entry: {id, label, R1_text, R1_citation, R2_text, H_text}
    """
    if not coer_data:
        return {'valid': False, 'error': 'No CoER entries provided.', 'details': []}

    errors = []
    details = []
    for entry in coer_data:
        entry_id = entry.get('id', 'unknown')
        entry_errors = []

        r1 = entry.get('R1_text', '').strip()
        r1_cite = entry.get('R1_citation', '').strip()
        r2 = entry.get('R2_text', '').strip()
        h = entry.get('H_text', '').strip()

        if not r1:
            entry_errors.append("R-1 (Base Fact) is missing")
        if not r1_cite:
            entry_errors.append("R-1 citation is missing (inline citation [저자, 연도] mandatory)")
        if not r2:
            entry_errors.append("R-2 (Intermediate reasoning) is missing")
        if not h:
            entry_errors.append("H (Hypothesis/Impact) is missing")

        details.append({
            'id': entry_id,
            'label': entry.get('label', ''),
            'coer_complete': len(entry_errors) == 0,
            'errors': entry_errors,
        })
        errors.extend([f"'{entry_id}': {e}" for e in entry_errors])

    return {
        'valid': len(errors) == 0,
        'total_entries': len(coer_data),
        'complete_entries': sum(1 for d in details if d['coer_complete']),
        'errors': errors,
        'details': details,
        'coer_definition': {
            'source': 'Glenn (2009) §III.A + 박사님 강화',
            'steps': {
                'R-1': 'Base Fact — sourced, verifiable claim with inline citation',
                'R-2': 'Intermediate — logical bridge linking R-1 to the impact',
                'H': 'Hypothesis/Leap — the impact claim itself',
            },
        },
    }


# ─────────────────────────────────────────────
# CLI DISPATCH
# ─────────────────────────────────────────────

COMMANDS = {
    'validate': lambda d: validate_input(d),
    'websearch_count': lambda d: compute_websearch_needed(
        d.get('ring_num', 1), d.get('parent_count', 0)),
    'check_sign_reversal': lambda d: check_sign_reversal(d.get('impacts', [])),
    'compute_srs': lambda d: compute_srs(d.get('lineages', [])),
    'validate_ring_counts': lambda d: validate_ring_counts(d),
    'build_ring_table': lambda d: build_ring_table(d),
    'check_coer': lambda d: check_coer(d.get('coer_entries', [])),
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        valid_cmds = ', '.join(COMMANDS.keys())
        print(json.dumps({
            'error': f'Usage: python3 wheel_engine.py <command> < input.json. '
                     f'Commands: {valid_cmds}'
        }), file=sys.stderr)
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
