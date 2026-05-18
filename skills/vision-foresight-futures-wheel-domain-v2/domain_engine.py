#!/usr/bin/env python3
"""
Domain V2 Engine — deterministic validation and balance audit.
Source: Glenn J.C. (2009). Futures Wheel. FRM V3.0, Chapter 06, §VI "Version 2" + Figure 6.

All arithmetic, validation, and scoring is deterministic — no LLM inference.

CLI usage:
    python3 domain_engine.py validate_frame < frame.json
    python3 domain_engine.py check_domain_coverage < coverage.json
    python3 domain_engine.py compute_balance_audit < audit.json
    python3 domain_engine.py classify_linkage < linkage.json
    python3 domain_engine.py generate_impact_id < id_request.json
    python3 domain_engine.py validate_input < input.json
"""

import json
import sys
import math
from typing import List, Dict, Optional, Any, Tuple


# ─────────────────────────────────────────────
# PREDEFINED DOMAIN FRAMES
# ─────────────────────────────────────────────

DOMAIN_FRAMES = {
    'Glenn V2 8 sector': {
        'sectors': ['Political', 'Cultural', 'Environmental', 'Psychological',
                    'Technological', 'Educational', 'Public Welfare', 'Economic'],
        'source': 'Glenn (2009) V3.0 §VI Figure 6 — African Economic Integration',
        'count': 8,
    },
    'STEEPS': {
        'sectors': ['Social', 'Technological', 'Economic', 'Environmental', 'Political', 'Spiritual'],
        'source': '박사님 미래학 프레임 (Social·Tech·Eco·Env·Political·Spiritual)',
        'count': 6,
    },
    'STEEP': {
        'sectors': ['Social', 'Technological', 'Economic', 'Environmental', 'Political'],
        'source': 'Aguilar F.J. (1967). Scanning the Business Environment. Macmillan.',
        'count': 5,
    },
    'PESTLE': {
        'sectors': ['Political', 'Economic', 'Social', 'Technological', 'Legal', 'Environmental'],
        'source': '경영전략 프레임 (PEST 확장형)',
        'count': 6,
    },
    'STEEPV': {
        'sectors': ['Social', 'Technological', 'Economic', 'Environmental', 'Political', 'Values'],
        'source': 'Coates J.F. — STEEP + Values dimension',
        'count': 6,
    },
    'Voros 4 Layers': {
        'sectors': ['Empirical', 'Interpretive', 'Normative', 'Formative'],
        'source': 'Voros J. (2003). A generic foresight process framework. Foresight, 5(3).',
        'count': 4,
    },
    'Bell 9 dimensions': {
        'sectors': ['Social', 'Cultural', 'Psychological', 'Biological', 'Economic',
                    'Technological', 'Environmental', 'Political', 'Spiritual'],
        'source': (
            'Bell W. (1997). Foundations of Futures Studies Vol.1. Transaction Publishers. '
            'NOTE: Bell\'s 9-dimension classification is a scholarly interpretation of his '
            'futures studies framework — not a verbatim "9 dimensions" list from Bell (1997). '
            'Use with caution; verify against source before citing as Bell-originating.'
        ),
        'count': 9,
        'citation_caution': True,  # Flag potential hallucination risk
    },
    'Inayatullah 6 Pillars': {
        'sectors': ['Litany', 'Systemic', 'Worldview', 'Mythology', 'Empowerment', 'Emergence'],
        'source': 'Inayatullah S. (2008). Six pillars: futures thinking for transforming. Foresight, 10(1).',
        'count': 6,
    },
    'STEEP-AI': {
        'sectors': ['Social', 'Technological', 'Economic', 'Environmental', 'Political', 'AI-Specific'],
        'source': 'AI 강조 STEEP 변형 — AI-Specific = AI 거버넌스·윤리·안전·제어',
        'count': 6,
    },
}

VALID_FRAME_NAMES = list(DOMAIN_FRAMES.keys()) + ['Free-form', 'Custom', 'Skip']

# Balance audit thresholds
BALANCE_VARIANCE_LOW = 0.3      # CV ≤ 0.3 → low variance (good balance)
BALANCE_VARIANCE_MEDIUM = 0.6   # CV 0.3~0.6 → medium
BALANCE_VARIANCE_HIGH = 0.6     # CV > 0.6 → high (bias risk)

CROSS_INTRA_FORMULA = 'cross_count / total_linkages'  # fraction [0, 1]
CROSS_INTRA_TARGET = 0.5  # cross/(cross+intra) ≥ 0.5 = good

# Impact ID format: {ring_abbrev}-{domain_abbrev}-{seq}
RING_ABBREV = {1: 'P', 2: 'S', 3: 'T', 4: 'Q', 5: 'Qn', 6: 'Sn'}
DOMAIN_ABBREV = {
    'Political': 'Pol', 'Cultural': 'Cul', 'Environmental': 'Env',
    'Psychological': 'Psy', 'Technological': 'Tec', 'Educational': 'Edu',
    'Public Welfare': 'PW', 'Economic': 'Eco',
    'Social': 'Soc', 'Spiritual': 'Spr', 'Legal': 'Leg', 'Values': 'Val',
    'Biological': 'Bio', 'Litany': 'Lit', 'Systemic': 'Sys', 'Worldview': 'WV',
    'Mythology': 'Myt', 'Empowerment': 'Emp', 'Emergence': 'Eme',
    'AI-Specific': 'AI', 'Empirical': 'Emp2', 'Interpretive': 'Int',
    'Normative': 'Nor', 'Formative': 'For',
}


# ─────────────────────────────────────────────
# INPUT VALIDATION
# ─────────────────────────────────────────────

def validate_input(data: Dict) -> Dict:
    """
    Validate master input for domain-v2 sub-skill.
    """
    errors = []
    warnings = []

    center_issue = data.get('center_issue', {})
    if not center_issue or not isinstance(center_issue, dict):
        errors.append("'center_issue' is required (dict with what/when/where/who).")
    else:
        for field in ('what', 'when', 'where', 'who'):
            if not str(center_issue.get(field, '')).strip():
                errors.append(f"'center_issue.{field}' is required.")

    depth_target = data.get('depth_target', 6)
    if not isinstance(depth_target, int) or depth_target < 1:
        errors.append(f"depth_target={depth_target} must be positive integer. Default: 6.")
    elif depth_target < 3:
        errors.append(
            f"depth_target={depth_target} < 3: V2 requires at least Primary+Secondary+Tertiary "
            f"for meaningful domain bucketing. Minimum: 3."
        )
    elif depth_target < 6:
        warnings.append(
            f"depth_target={depth_target} < 6: 박사님 강화 protocol은 6차 default. "
            f"V2에서도 6차 권장."
        )

    cross_ratio = data.get('cross_domain_target_ratio', 0.5)
    if not isinstance(cross_ratio, (int, float)) or not (0.0 <= cross_ratio <= 1.0):
        errors.append(
            f"cross_domain_target_ratio={cross_ratio} must be in [0, 1]. "
            f"Formula: cross_count / total_linkages. Default: 0.5."
        )

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'depth_target': depth_target if isinstance(depth_target, int) else 6,
    }


# ─────────────────────────────────────────────
# DOMAIN FRAME VALIDATION
# ─────────────────────────────────────────────

def validate_frame(data: Dict) -> Dict:
    """
    Validate the domains_frame configuration.
    Source: Glenn (2009) §VI — "a predetermined set of areas or domains"
    """
    errors = []
    warnings = []

    frame_name = data.get('name', 'Glenn V2 8 sector')
    custom_sectors = data.get('sectors', [])
    min_per_sector = data.get('min_impacts_per_sector', 1)
    target_per_sector = data.get('target_impacts_per_sector', '2~3')

    # Resolve sectors
    if frame_name == 'Free-form':
        warnings.append("'Free-form' selected: V2 domain-bucketing disabled, falls back to V1.")
        return {'valid': True, 'errors': [], 'warnings': warnings,
                'fallback_to_v1': True, 'sectors': []}

    if frame_name == 'Skip':
        warnings.append("'Skip' selected: master will auto-infer domain frame.")
        return {'valid': True, 'errors': [], 'warnings': warnings,
                'auto_infer': True, 'sectors': []}

    if frame_name == 'Custom':
        if not custom_sectors:
            errors.append("'Custom' frame requires 'sectors' list to be provided.")
        elif len(custom_sectors) < 3:
            errors.append(
                f"Custom frame needs ≥3 sectors (got {len(custom_sectors)}). "
                f"Glenn: 'should be as broad as manageably possible'."
            )
        sectors = custom_sectors
        source = 'Custom user-defined frame'
        citation_caution = False
    elif frame_name in DOMAIN_FRAMES:
        frame_def = DOMAIN_FRAMES[frame_name]
        sectors = custom_sectors if custom_sectors else frame_def['sectors']
        source = frame_def['source']
        citation_caution = frame_def.get('citation_caution', False)
        if citation_caution:
            warnings.append(
                f"Frame '{frame_name}' has citation_caution=True: "
                f"the sector list is a scholarly interpretation, not verbatim from the source. "
                f"Verify against: {source}"
            )
    else:
        errors.append(
            f"frame_name='{frame_name}' not recognized. "
            f"Valid options: {VALID_FRAME_NAMES}"
        )
        sectors = []
        source = ''
        citation_caution = False

    if not isinstance(min_per_sector, int) or min_per_sector < 1:
        errors.append(
            f"min_impacts_per_sector={min_per_sector} must be int ≥ 1. "
            f"Glenn: 'impacts be considered for a predetermined set of areas'."
        )

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'frame_name': frame_name,
        'sectors': sectors,
        'sector_count': len(sectors),
        'min_impacts_per_sector': min_per_sector,
        'target_impacts_per_sector': target_per_sector,
        'source': source if not errors else '',
    }


# ─────────────────────────────────────────────
# DOMAIN COVERAGE CHECK
# ─────────────────────────────────────────────

def check_domain_coverage(data: Dict) -> Dict:
    """
    Check that every required domain has ≥ min_impacts_per_sector impacts.
    Glenn (2009) §VI: "added the requirement that impacts be considered for
    a predetermined set of areas or domains." — ALL domains must be covered.

    Input: {sectors: [...], per_domain_count: {domain: count}, min_per_sector: 1}
    """
    sectors = data.get('sectors', [])
    counts = data.get('per_domain_count', {})
    min_per = int(data.get('min_per_sector', 1))

    if not sectors:
        return {'error': "'sectors' list is required."}

    missing = []
    below_min = []
    coverage = {}

    for sector in sectors:
        count = counts.get(sector, 0)
        coverage[sector] = count
        if count == 0:
            missing.append(sector)
        elif count < min_per:
            below_min.append({'sector': sector, 'count': count, 'required': min_per})

    all_covered = len(missing) == 0 and len(below_min) == 0

    return {
        'all_covered': all_covered,
        'sectors_required': sectors,
        'sector_count': len(sectors),
        'coverage': coverage,
        'missing_sectors': missing,
        'below_minimum': below_min,
        'min_per_sector': min_per,
        'total_impacts': sum(counts.get(s, 0) for s in sectors),
        'errors': (
            [f"Missing sectors: {missing}"] if missing else []
        ) + (
            [f"Below minimum: {[b['sector'] for b in below_min]}"] if below_min else []
        ),
        'source': 'Glenn (2009) §VI — "impacts be considered for a predetermined set of areas"',
    }


# ─────────────────────────────────────────────
# BALANCE AUDIT
# ─────────────────────────────────────────────

def compute_balance_audit(data: Dict) -> Dict:
    """
    Compute domain balance audit: variance classification + bias detection.
    Source: Section 5 Phase 5 of SKILL.md.

    Variance metric: Coefficient of Variation (CV = std_dev / mean)
      - CV ≤ 0.30 → "low" (well-balanced)
      - 0.30 < CV ≤ 0.60 → "medium"
      - CV > 0.60 → "high" (bias risk)

    Input: {per_domain_count: {domain: count}, sectors: [...]}
    """
    per_domain = data.get('per_domain_count', {})
    sectors = data.get('sectors', list(per_domain.keys()))

    if not per_domain or not sectors:
        return {'error': "per_domain_count and sectors are required."}

    counts = [per_domain.get(s, 0) for s in sectors]
    n = len(counts)
    if n == 0:
        return {'error': "No sectors to audit."}

    mean_count = sum(counts) / n
    if mean_count == 0:
        return {
            'mean': 0.0, 'std_dev': 0.0, 'cv': 0.0,
            'variance_level': 'low',
            'error': 'All domain counts are 0. No impacts generated yet.',
        }

    variance = sum((c - mean_count) ** 2 for c in counts) / n
    std_dev = math.sqrt(variance)
    cv = std_dev / mean_count

    if cv <= BALANCE_VARIANCE_LOW:
        variance_level = 'low'
    elif cv <= BALANCE_VARIANCE_MEDIUM:
        variance_level = 'medium'
    else:
        variance_level = 'high'

    # Bias alerts: domains significantly above mean
    max_count = max(counts) if counts else 0
    bias_alerts = []
    rebalance_actions = []
    for sector in sectors:
        c = per_domain.get(sector, 0)
        if mean_count > 0 and c > mean_count * 1.5 and c == max_count:
            bias_alerts.append(
                f"'{sector}' has {c} impacts (>{mean_count*1.5:.1f}x mean). "
                f"Analyst bias toward {sector} domain detected — rebalance required."
            )
        if c < mean_count * 0.5:
            rebalance_actions.append(
                f"Boost '{sector}' (count={c}, mean={mean_count:.1f}): add more {sector} impacts."
            )

    return {
        'mean': round(mean_count, 4),
        'std_dev': round(std_dev, 4),
        'cv': round(cv, 4),
        'cv_formula': 'std_dev / mean (Coefficient of Variation)',
        'variance_level': variance_level,
        'thresholds': {
            'low': f"CV ≤ {BALANCE_VARIANCE_LOW}",
            'medium': f"CV {BALANCE_VARIANCE_LOW}~{BALANCE_VARIANCE_MEDIUM}",
            'high': f"CV > {BALANCE_VARIANCE_MEDIUM}",
        },
        'per_domain': {s: per_domain.get(s, 0) for s in sectors},
        'bias_alerts': bias_alerts,
        'rebalance_actions': rebalance_actions,
        'rebalance_needed': variance_level == 'high',
        'source': 'Section 5 Phase 5 Domain Balance Audit + CV formula',
    }


# ─────────────────────────────────────────────
# CROSS/INTRA LINKAGE
# ─────────────────────────────────────────────

def classify_linkage(data: Dict) -> Dict:
    """
    Classify each linkage as cross-domain or intra-domain.
    Formula: cross_fraction = cross_count / (cross_count + intra_count)
    Target: cross_fraction ≥ cross_domain_target_ratio (default 0.5)

    Input: {linkages: [{from_domain, to_domain}], target_ratio: 0.5}
    """
    linkages = data.get('linkages', [])
    target_ratio = float(data.get('target_ratio', CROSS_INTRA_TARGET))

    if not linkages:
        return {'error': 'No linkages provided.', 'cross_count': 0, 'intra_count': 0}

    classified = []
    cross_count = 0
    intra_count = 0

    for link in linkages:
        from_d = str(link.get('from_domain', '')).strip()
        to_d = str(link.get('to_domain', '')).strip()
        is_cross = from_d.lower() != to_d.lower()
        link_type = 'cross' if is_cross else 'intra'
        if is_cross:
            cross_count += 1
        else:
            intra_count += 1
        classified.append({
            'from_domain': from_d,
            'to_domain': to_d,
            'linkage_type': link_type,
            'primary_id': link.get('primary_id', '?'),
            'secondary_id': link.get('secondary_id', '?'),
        })

    total = cross_count + intra_count
    cross_fraction = cross_count / total if total > 0 else 0.0

    return {
        'cross_count': cross_count,
        'intra_count': intra_count,
        'total_linkages': total,
        'cross_fraction': round(cross_fraction, 4),
        'cross_fraction_pct': f"{cross_fraction*100:.1f}%",
        'cross_fraction_formula': 'cross_count / (cross_count + intra_count)',
        'target_ratio': target_ratio,
        'target_met': cross_fraction >= target_ratio,
        'status': (
            f"GOOD — cross-domain fraction {cross_fraction*100:.1f}% ≥ target {target_ratio*100:.0f}%"
            if cross_fraction >= target_ratio else
            f"BELOW TARGET — {cross_fraction*100:.1f}% < {target_ratio*100:.0f}% — add more cross-domain impacts"
        ),
        'classified': classified,
        'source': 'Section 5 Phase 5 + Section 6.3 Cross-Domain Linkage Table',
    }


# ─────────────────────────────────────────────
# IMPACT ID GENERATION
# ─────────────────────────────────────────────

def generate_impact_id(data: Dict) -> Dict:
    """
    Generate deterministic impact ID.
    Format: {ring_abbrev}-{domain_abbrev}-{seq}
    Cross-domain secondary: {ring_abbrev}-{source_abbrev}{target_abbrev}-{seq}

    Input: {ring_num, domain, sequence, source_domain (optional for cross-domain)}
    """
    ring_num = int(data.get('ring_num', 1))
    domain = str(data.get('domain', ''))
    source_domain = str(data.get('source_domain', ''))
    sequence = int(data.get('sequence', 1))

    if ring_num not in RING_ABBREV:
        return {'error': f"ring_num={ring_num} invalid. Must be 1-6."}

    ring_a = RING_ABBREV[ring_num]
    domain_a = DOMAIN_ABBREV.get(domain, domain[:3].capitalize())

    if source_domain and source_domain != domain:
        # Cross-domain: primary from source_domain, secondary in domain
        source_a = DOMAIN_ABBREV.get(source_domain, source_domain[:3].capitalize())
        impact_id = f"{ring_a}-{source_a}{domain_a}-{sequence}"
        note = f"Cross-domain: {source_domain} → {domain}"
    else:
        impact_id = f"{ring_a}-{domain_a}-{sequence}"
        note = f"Intra-domain: {domain}"

    return {
        'impact_id': impact_id,
        'ring_num': ring_num,
        'ring_abbrev': ring_a,
        'domain': domain,
        'domain_abbrev': domain_a,
        'sequence': sequence,
        'note': note,
    }


# ─────────────────────────────────────────────
# CLI DISPATCH
# ─────────────────────────────────────────────

COMMANDS = {
    'validate_input': lambda d: validate_input(d),
    'validate_frame': lambda d: validate_frame(d),
    'check_domain_coverage': lambda d: check_domain_coverage(d),
    'compute_balance_audit': lambda d: compute_balance_audit(d),
    'classify_linkage': lambda d: classify_linkage(d),
    'generate_impact_id': lambda d: generate_impact_id(d),
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        valid = ', '.join(COMMANDS.keys())
        print(json.dumps({'error': f'Usage: python3 domain_engine.py <command> < input.json. Commands: {valid}'}),
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
