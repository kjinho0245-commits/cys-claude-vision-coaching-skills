#!/usr/bin/env python3
"""
iu_ranker.py — Importance × Uncertainty Ranking 결정론 엔진
출처: Glenn J.C. & TFG (2009). "Scenarios." In Futures Research Methodology V3.0,
      Ch.19. The Millennium Project. Section III Schwartz Step 3 (Schwartz GBN).
      Schwartz P. (1991). The Art of the Long View: Planning for the Future in an
      Uncertain World. Doubleday/Currency. (pp. 226-234 Seven Step Process).
      Schoemaker P.J.H. (1995). "Scenario Planning: A Tool for Strategic Thinking."
      Sloan Management Review, Winter 1995, pp. 25-40 (Importance × Uncertainty 격자).

결정론 환원 대상:
  - PDF verbatim 인용 (Schwartz Step 3·Schoemaker 격자 정의)
  - 1-5 Likert 척도 정의 (Importance·Uncertainty 각 anchor)
  - persona 점수 aggregation (median·mean·std)
  - 4-quadrant 분류 임계값
  - Top-2 Critical Drivers 자동 식별 (정렬 규칙 명시)
  - 2×2 ASCII matrix 시각화 (deterministic)
  - 입력 검증 (driving force 수 6-12, persona 수 6-8, score 범위)
  - 출력 markdown 양식 빌더

Usage:
  python3 iu_ranker.py validate                         — 자체 검증 (ALL_PASS)
  python3 iu_ranker.py verbatim KEY                     — PDF verbatim 인용
  python3 iu_ranker.py verbatim_all                     — 전체 verbatim 출력
  python3 iu_ranker.py likert_scale                     — 1-5 anchor 정의
  python3 iu_ranker.py quadrant_thresholds              — 분류 임계값
  python3 iu_ranker.py classify IMPORTANCE UNCERTAINTY  — 단일 cell 분류
  python3 iu_ranker.py rank INPUT.json [OUTPUT.md]      — 풀 ranking 수행
  python3 iu_ranker.py validate_input INPUT.json        — 입력 schema 검증
  python3 iu_ranker.py audit_output OUTPUT.md           — 생성 markdown 헤더 검증
  python3 iu_ranker.py demo                             — 데모 출력
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

# ════════════════════════════════════════════════════════════════════════════
# PRIMARY SOURCES
# ════════════════════════════════════════════════════════════════════════════

PRIMARY_SOURCE = (
    "Glenn J.C. & TFG (2009). 'Scenarios.' In Glenn, J.C. (Ed.), "
    "Futures Research Methodology V3.0, Ch.19. The Millennium Project. "
    "Section III Schwartz Step 3."
)

SCHWARTZ_1991 = (
    "Schwartz P. (1991). The Art of the Long View: Planning for the Future in an "
    "Uncertain World. Doubleday/Currency. (Seven Step Process pp. 226-234)."
)

SCHOEMAKER_1995 = (
    "Schoemaker P.J.H. (1995). 'Scenario Planning: A Tool for Strategic Thinking.' "
    "Sloan Management Review, 36(2), pp. 25-40. (Importance × Uncertainty 격자 — "
    "Step 3 verbatim: 'identify basic trends and key uncertainties')."
)

WACK_1985 = (
    "Wack P. (1985). 'Scenarios: Uncharted Waters Ahead.' Harvard Business Review, "
    "Sep-Oct 1985, pp. 73-89. (Predetermined elements vs Critical uncertainties — "
    "Shell origin)."
)

VAN_DER_HEIJDEN_1996 = (
    "van der Heijden K. (1996). Scenarios: The Art of Strategic Conversation. "
    "John Wiley & Sons. (GBN canonical 2x2 matrix method)."
)

# ════════════════════════════════════════════════════════════════════════════
# PDF VERBATIM QUOTES (외부 출처와 1:1 대조 가능한 인용)
# ════════════════════════════════════════════════════════════════════════════

PDF_VERBATIM = {
    "schwartz_step3": (
        "rank the driving forces and trends by importance and uncertainty"
    ),
    "schwartz_seven_steps": (
        "These steps include: identify the focal issue or decision; identify "
        "the key forces and trends in the environment; rank the driving forces "
        "and trends by importance and uncertainty; select the scenario logics; "
        "fill out the scenarios; assess the implications; and select the "
        "leading indicators and signposts for monitoring purposes."
    ),
    "predetermined_elements": (
        "Predetermined elements are factors that affect scenarios but whose "
        "future state is virtually certain; they appear in every scenario."
    ),
    "critical_uncertainties": (
        "Critical uncertainties are factors high in importance and high in "
        "uncertainty; these become the axes of the scenario logics."
    ),
    "schoemaker_step3": (
        "identify basic trends and key uncertainties"
    ),
    "wack_pre_uncertain": (
        "the predetermined elements and the critical uncertainties"
    ),
}

VERBATIM_ATTRIBUTION = {
    "schwartz_step3": SCHWARTZ_1991 + " — Step 3 verbatim.",
    "schwartz_seven_steps": SCHWARTZ_1991 + " — Seven Step Process.",
    "predetermined_elements": (
        WACK_1985 + " + " + VAN_DER_HEIJDEN_1996 + " — standard GBN definition."
    ),
    "critical_uncertainties": (
        SCHWARTZ_1991 + " + " + VAN_DER_HEIJDEN_1996 + " — standard GBN definition."
    ),
    "schoemaker_step3": SCHOEMAKER_1995 + " — Schoemaker Step 3 of 10.",
    "wack_pre_uncertain": WACK_1985 + " — Shell origin terminology.",
}

# ════════════════════════════════════════════════════════════════════════════
# LIKERT SCALE — 1-5 anchors (Schoemaker 1995 + GBN convention)
# ════════════════════════════════════════════════════════════════════════════

LIKERT_IMPORTANCE = {
    1: "trivial — no meaningful effect on focal issue",
    2: "minor — small marginal effect",
    3: "moderate — noticeable but bounded effect",
    4: "major — substantially shapes focal issue outcome",
    5: "critical — changes everything about focal issue",
}

LIKERT_UNCERTAINTY = {
    1: "highly predictable — direction & magnitude known (predetermined)",
    2: "mostly predictable — small variance in outcome",
    3: "moderately uncertain — known range, unknown trajectory",
    4: "highly uncertain — outcome could swing widely",
    5: "wildly unpredictable — true uncertainty, multiple opposing futures",
}

LIKERT_MIN = 1
LIKERT_MAX = 5

# ════════════════════════════════════════════════════════════════════════════
# QUADRANT CLASSIFICATION — 결정론 임계값
# ════════════════════════════════════════════════════════════════════════════
#
# 임계값 근거:
#   1-5 Likert 척도의 중점은 3.0이다. "High"는 중점보다 명확히 위에 있을 때
#   (>= 3.5), "Low"는 중점 이하 (< 3.5)일 때로 정의한다. 정수 점수만 들어올
#   경우 사실상 1·2·3 = Low, 4·5 = High로 작동한다. 이는 Schoemaker (1995)와
#   van der Heijden (1996)이 사용한 사실상의 GBN convention과 일치한다.
#
# 분류 규칙:
#   Top-Right    = Importance >= 3.5 AND Uncertainty >= 3.5 → CRITICAL DRIVERS
#   Top-Left     = Importance >= 3.5 AND Uncertainty <  3.5 → PREDETERMINED
#   Bottom-Right = Importance <  3.5 AND Uncertainty >= 3.5 → NOISE
#   Bottom-Left  = Importance <  3.5 AND Uncertainty <  3.5 → BACKGROUND
# ════════════════════════════════════════════════════════════════════════════

QUADRANT_THRESHOLD = 3.5

QUADRANTS = {
    "CRITICAL":      "High Importance + High Uncertainty → scenario axes 후보",
    "PREDETERMINED": "High Importance + Low Uncertainty → 모든 scenario 공통 반영",
    "NOISE":         "Low Importance + High Uncertainty → 제외 (omit·too unpredict)",
    "BACKGROUND":    "Low Importance + Low Uncertainty → omit·context only",
}

QUADRANT_LABEL = {
    "CRITICAL":      "CRITICAL ★",
    "PREDETERMINED": "Predetermined",
    "NOISE":         "Noise",
    "BACKGROUND":    "Background",
}


def classify_quadrant(importance: float, uncertainty: float) -> str:
    """결정론 분류 — 임계값 정확히 3.5."""
    hi_imp = importance >= QUADRANT_THRESHOLD
    hi_unc = uncertainty >= QUADRANT_THRESHOLD
    if hi_imp and hi_unc:
        return "CRITICAL"
    if hi_imp and not hi_unc:
        return "PREDETERMINED"
    if not hi_imp and hi_unc:
        return "NOISE"
    return "BACKGROUND"


# ════════════════════════════════════════════════════════════════════════════
# 입력 schema 검증
# ════════════════════════════════════════════════════════════════════════════

FORCE_COUNT_MIN = 6
FORCE_COUNT_MAX = 12
PERSONA_COUNT_MIN = 6
PERSONA_COUNT_MAX = 8


def validate_input(data: dict) -> dict:
    """입력 JSON schema 검증. PASS/FAIL + errors 반환."""
    errors: list[str] = []

    if not isinstance(data, dict):
        return {"pass": False, "errors": ["root must be object"]}

    forces = data.get("driving_forces")
    if not isinstance(forces, list):
        errors.append("'driving_forces' field missing or not list")
        return {"pass": False, "errors": errors}

    n = len(forces)
    if not (FORCE_COUNT_MIN <= n <= FORCE_COUNT_MAX):
        errors.append(
            f"driving_forces count {n} out of range "
            f"[{FORCE_COUNT_MIN}-{FORCE_COUNT_MAX}]"
        )

    seen_ids: set[str] = set()
    for i, df in enumerate(forces):
        path = f"driving_forces[{i}]"
        if not isinstance(df, dict):
            errors.append(f"{path} not object")
            continue
        for key in ("id", "name", "scores"):
            if key not in df:
                errors.append(f"{path} missing field '{key}'")
        df_id = df.get("id", "")
        if not isinstance(df_id, str) or not df_id:
            errors.append(f"{path}.id must be non-empty string")
        elif df_id in seen_ids:
            errors.append(f"{path}.id duplicate '{df_id}'")
        else:
            seen_ids.add(df_id)

        scores = df.get("scores", [])
        if not isinstance(scores, list):
            errors.append(f"{path}.scores must be list")
            continue
        m = len(scores)
        if not (PERSONA_COUNT_MIN <= m <= PERSONA_COUNT_MAX):
            errors.append(
                f"{path}.scores count {m} out of range "
                f"[{PERSONA_COUNT_MIN}-{PERSONA_COUNT_MAX}]"
            )
        for j, s in enumerate(scores):
            spath = f"{path}.scores[{j}]"
            if not isinstance(s, dict):
                errors.append(f"{spath} not object")
                continue
            for key in ("persona", "importance", "uncertainty"):
                if key not in s:
                    errors.append(f"{spath} missing field '{key}'")
            for axis in ("importance", "uncertainty"):
                v = s.get(axis)
                if not isinstance(v, (int, float)):
                    errors.append(f"{spath}.{axis} must be number")
                    continue
                if not (LIKERT_MIN <= v <= LIKERT_MAX):
                    errors.append(
                        f"{spath}.{axis}={v} out of Likert range "
                        f"[{LIKERT_MIN}-{LIKERT_MAX}]"
                    )

    return {"pass": len(errors) == 0, "errors": errors}


# ════════════════════════════════════════════════════════════════════════════
# AGGREGATION — median·mean·std (결정론 statistics.median)
# ════════════════════════════════════════════════════════════════════════════


def aggregate_scores(scores: list[dict]) -> dict:
    """persona 점수 리스트 → median·mean·std for Importance·Uncertainty."""
    imp = [float(s["importance"]) for s in scores]
    unc = [float(s["uncertainty"]) for s in scores]
    return {
        "n_personas": len(scores),
        "importance_median": statistics.median(imp),
        "importance_mean":   round(statistics.mean(imp), 3),
        "importance_std":    round(statistics.pstdev(imp), 3) if len(imp) > 1 else 0.0,
        "uncertainty_median": statistics.median(unc),
        "uncertainty_mean":   round(statistics.mean(unc), 3),
        "uncertainty_std":    round(statistics.pstdev(unc), 3) if len(unc) > 1 else 0.0,
    }


# ════════════════════════════════════════════════════════════════════════════
# RANKING — Top-2 Critical Drivers 결정론 선정
# ════════════════════════════════════════════════════════════════════════════


def rank_forces(forces: list[dict]) -> list[dict]:
    """각 force에 aggregate + quadrant + combined_score 추가."""
    enriched = []
    for df in forces:
        agg = aggregate_scores(df["scores"])
        imp = agg["importance_median"]
        unc = agg["uncertainty_median"]
        consensus = round((agg["importance_std"] + agg["uncertainty_std"]) / 2, 3)
        enriched.append({
            "id": df["id"],
            "name": df["name"],
            "endpoints_low":  df.get("endpoints_low", ""),
            "endpoints_high": df.get("endpoints_high", ""),
            **agg,
            "quadrant": classify_quadrant(imp, unc),
            "combined_score": round(imp * unc, 3),
            "sum_score": round(imp + unc, 3),
            "consensus_sigma": consensus,
        })
    return enriched


def select_top2_critical(enriched: list[dict]) -> list[dict]:
    """Critical 사분면 force만 추려 Top-2 선정.
    정렬 규칙(결정론·재현 가능):
      1) combined_score (importance_median × uncertainty_median) 내림차순
      2) sum_score 내림차순
      3) consensus_sigma 오름차순 (합의 강할수록 우선)
      4) id 사전순 오름차순
    """
    crit = [df for df in enriched if df["quadrant"] == "CRITICAL"]
    crit.sort(key=lambda d: (
        -d["combined_score"],
        -d["sum_score"],
        d["consensus_sigma"],
        d["id"],
    ))
    return crit[:2]


def list_predetermined(enriched: list[dict]) -> list[dict]:
    return [df for df in enriched if df["quadrant"] == "PREDETERMINED"]


# ════════════════════════════════════════════════════════════════════════════
# ASCII 2×2 MATRIX (deterministic 5×5 grid 점 배치)
# ════════════════════════════════════════════════════════════════════════════


def render_2x2_matrix(enriched: list[dict]) -> str:
    """5×5 grid에 force ID 배치. 동일 cell 다중일 경우 '+N' suffix.
    경계 매핑: importance_median 반올림(round-half-even Python 기본)으로
    정수 row 결정. round(3.5)=4 (banker's rounding), round(2.5)=2.
    """
    grid: dict[tuple[int, int], list[str]] = {}
    overflow: list[str] = []
    for df in enriched:
        imp_r = int(round(df["importance_median"]))
        unc_r = int(round(df["uncertainty_median"]))
        imp_r = max(1, min(5, imp_r))
        unc_r = max(1, min(5, unc_r))
        grid.setdefault((imp_r, unc_r), []).append(df["id"])

    lines = ["```", "Importance ▲"]
    for imp in range(5, 0, -1):
        row_cells = []
        for unc in range(1, 6):
            ids = grid.get((imp, unc), [])
            if not ids:
                cell = " · "
            elif len(ids) == 1:
                cell = ids[0]
            else:
                cell = ids[0] + f"+{len(ids) - 1}"  # 동일 cell 다중 표기
                if len(ids) > 1:
                    overflow.append(
                        f"  cell ({imp},{unc}): " + ", ".join(ids)
                    )
            row_cells.append(cell.center(8))
        lines.append(f"       {imp} │{''.join(row_cells)}")
    lines.append("         └" + "────────" * 5 + "─► Uncertainty")
    lines.append("           " + "".join(str(u).center(8) for u in range(1, 6)))
    lines.append("```")
    if overflow:
        lines.append("")
        lines.append("(동일 cell 다중 force 상세 — '+N' marker 풀이)")
        for o in overflow:
            lines.append(o)
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════════════
# MARKDOWN OUTPUT BUILDER
# ════════════════════════════════════════════════════════════════════════════


def build_markdown(
    enriched: list[dict],
    top2: list[dict],
    predetermined: list[dict],
    meta: dict | None = None,
) -> str:
    n_total = len(enriched)
    n_crit = sum(1 for d in enriched if d["quadrant"] == "CRITICAL")
    n_pre  = sum(1 for d in enriched if d["quadrant"] == "PREDETERMINED")
    n_noise = sum(1 for d in enriched if d["quadrant"] == "NOISE")
    n_back  = sum(1 for d in enriched if d["quadrant"] == "BACKGROUND")

    out = []
    out.append("### § Importance-Uncertainty Matrix "
               "(vision-foresight-scenarios-importance-uncertainty-ranking)")
    out.append("")
    out.append(f"**Total Driving Forces Ranked**: {n_total}")
    if top2:
        ids = ", ".join(d["id"] for d in top2)
        out.append(f"**Top-2 Critical Drivers (Recommended Axes)**: {ids}")
    else:
        out.append("**Top-2 Critical Drivers (Recommended Axes)**: NONE — "
                   "no force met CRITICAL threshold; re-evaluate scoring.")
    if predetermined:
        ids = ", ".join(d["id"] for d in predetermined)
        out.append(f"**Predetermined Elements (Common to All Scenarios)**: {ids}")
    else:
        out.append("**Predetermined Elements (Common to All Scenarios)**: none")
    out.append("")
    out.append(f"**Quadrant Distribution**: CRITICAL={n_crit} · "
               f"PREDETERMINED={n_pre} · NOISE={n_noise} · BACKGROUND={n_back}")
    out.append(f"**Quadrant Threshold**: median ≥ {QUADRANT_THRESHOLD} = High; "
               f"< {QUADRANT_THRESHOLD} = Low (1-5 Likert midpoint 3.0 기준)")
    out.append("")
    out.append("---")
    out.append("")
    out.append("#### Scoring Table")
    out.append("")
    out.append("| ID | Driving Force | Importance (med·mean·σ) | "
               "Uncertainty (med·mean·σ) | Combined | Quadrant |")
    out.append("|---|---|---|---|---|---|")
    # 표 정렬: Critical 먼저, combined_score 내림차순, id 오름차순
    quad_order = {"CRITICAL": 0, "PREDETERMINED": 1, "NOISE": 2, "BACKGROUND": 3}
    sorted_forces = sorted(
        enriched,
        key=lambda d: (quad_order[d["quadrant"]], -d["combined_score"], d["id"]),
    )
    for df in sorted_forces:
        label = QUADRANT_LABEL[df["quadrant"]]
        out.append(
            f"| {df['id']} | {df['name']} | "
            f"{df['importance_median']:.1f} · {df['importance_mean']:.2f} · "
            f"{df['importance_std']:.2f} | "
            f"{df['uncertainty_median']:.1f} · {df['uncertainty_mean']:.2f} · "
            f"{df['uncertainty_std']:.2f} | "
            f"{df['combined_score']:.2f} | {label} |"
        )
    out.append("")
    out.append("#### 2×2 Matrix Visualization (medians, integer-rounded cells)")
    out.append("")
    out.append(render_2x2_matrix(enriched))
    out.append("")
    out.append("#### Top-2 Critical Drivers (Scenario Axes Recommendation)")
    out.append("")
    if top2:
        for rank, df in enumerate(top2, start=1):
            low = df["endpoints_low"] or "[low end]"
            high = df["endpoints_high"] or "[high end]"
            out.append(
                f"{rank}. **{df['id']}: {df['name']}** — "
                f"Importance {df['importance_median']:.1f}, "
                f"Uncertainty {df['uncertainty_median']:.1f}, "
                f"Combined {df['combined_score']:.2f}"
            )
            out.append(f"   - Endpoints: {low}  ↔  {high}")
    else:
        out.append("(없음 — Critical 사분면에 도달한 force가 없습니다. "
                   "scoring 재검토 또는 driving forces 재식별 권장)")
    out.append("")
    out.append("#### Predetermined Elements (반드시 모든 scenario에 반영)")
    out.append("")
    if predetermined:
        for df in predetermined:
            high = df["endpoints_high"] or "[expected trajectory]"
            out.append(f"- **{df['id']}: {df['name']}** — anchored at: {high}")
    else:
        out.append("- (해당 없음 — high-importance·low-uncertainty force가 없습니다.)")
    out.append("")
    out.append("---")
    out.append("")
    out.append("#### 다음 sub-skill 전달")
    out.append("")
    out.append("→ vision-foresight-scenarios-scenario-logics-selection")
    out.append("  (Top-2 Critical Drivers axes 권장)")
    out.append("")
    out.append("---")
    out.append("")
    out.append("##### Determinism Audit")
    out.append("")
    out.append(f"- Aggregation: `statistics.median` / `statistics.mean` / "
               f"`statistics.pstdev` (Python {sys.version_info.major}."
               f"{sys.version_info.minor})")
    out.append(f"- Quadrant threshold: {QUADRANT_THRESHOLD} (midpoint of 1-5 Likert)")
    out.append("- Top-2 sort key: "
               "(combined_score desc, sum_score desc, consensus_sigma asc, id asc)")
    out.append("- All scores produced via `iu_ranker.py rank` — no LLM arithmetic.")
    if meta:
        out.append(f"- Input metadata: {json.dumps(meta, ensure_ascii=False)}")

    return "\n".join(out)


# ════════════════════════════════════════════════════════════════════════════
# CLI ENTRYPOINTS
# ════════════════════════════════════════════════════════════════════════════


def cmd_validate() -> int:
    """자체 검증: 상수 무결성·예제 입력 처리."""
    checks: list[tuple[str, bool, str]] = []

    # 1. Likert 범위 길이
    checks.append((
        "likert_importance_5levels",
        len(LIKERT_IMPORTANCE) == 5 and set(LIKERT_IMPORTANCE) == {1, 2, 3, 4, 5},
        "Importance Likert must have exactly anchors 1-5",
    ))
    checks.append((
        "likert_uncertainty_5levels",
        len(LIKERT_UNCERTAINTY) == 5 and set(LIKERT_UNCERTAINTY) == {1, 2, 3, 4, 5},
        "Uncertainty Likert must have exactly anchors 1-5",
    ))

    # 2. Quadrant 정의 4개
    checks.append((
        "quadrant_count_4",
        len(QUADRANTS) == 4,
        "Must have exactly 4 quadrants",
    ))

    # 3. classify_quadrant 4 모서리
    cases = [
        ((5, 5), "CRITICAL"),
        ((5, 1), "PREDETERMINED"),
        ((1, 5), "NOISE"),
        ((1, 1), "BACKGROUND"),
        ((3.5, 3.5), "CRITICAL"),
        ((3.4, 3.4), "BACKGROUND"),
        ((3.5, 3.4), "PREDETERMINED"),
        ((3.4, 3.5), "NOISE"),
    ]
    for (i, u), expect in cases:
        got = classify_quadrant(i, u)
        checks.append((
            f"classify({i},{u})=={expect}",
            got == expect,
            f"got {got}",
        ))

    # 4. aggregate_scores 정확성
    sample_scores = [
        {"persona": "P1", "importance": 5, "uncertainty": 4},
        {"persona": "P2", "importance": 4, "uncertainty": 5},
        {"persona": "P3", "importance": 5, "uncertainty": 4},
        {"persona": "P4", "importance": 4, "uncertainty": 5},
        {"persona": "P5", "importance": 5, "uncertainty": 4},
        {"persona": "P6", "importance": 4, "uncertainty": 5},
    ]
    agg = aggregate_scores(sample_scores)
    checks.append((
        "median_importance",
        agg["importance_median"] == 4.5,
        f"got {agg['importance_median']}",
    ))
    checks.append((
        "median_uncertainty",
        agg["uncertainty_median"] == 4.5,
        f"got {agg['uncertainty_median']}",
    ))

    # 5. validate_input 양성/음성
    good = {
        "driving_forces": [
            {"id": f"DF{i:02d}", "name": f"force{i}", "scores": [
                {"persona": f"P{k}", "importance": 3, "uncertainty": 3}
                for k in range(6)
            ]}
            for i in range(1, 7)
        ]
    }
    res = validate_input(good)
    checks.append((
        "validate_input_good_passes",
        res["pass"] is True,
        f"errors={res['errors']}",
    ))

    bad = {"driving_forces": [{"id": "DF01", "name": "x", "scores": []}]}
    res = validate_input(bad)
    checks.append((
        "validate_input_bad_fails",
        res["pass"] is False,
        "should fail",
    ))

    # 6. Top-2 selection deterministic
    enriched_sample = rank_forces([
        {"id": "DF01", "name": "a",
         "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 5}
                    for k in range(6)]},
        {"id": "DF02", "name": "b",
         "scores": [{"persona": f"P{k}", "importance": 4, "uncertainty": 5}
                    for k in range(6)]},
        {"id": "DF03", "name": "c",
         "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 4}
                    for k in range(6)]},
        {"id": "DF04", "name": "d",
         "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 2}
                    for k in range(6)]},
        {"id": "DF05", "name": "e",
         "scores": [{"persona": f"P{k}", "importance": 1, "uncertainty": 1}
                    for k in range(6)]},
        {"id": "DF06", "name": "f",
         "scores": [{"persona": f"P{k}", "importance": 1, "uncertainty": 5}
                    for k in range(6)]},
    ])
    top2 = select_top2_critical(enriched_sample)
    checks.append((
        "top2_count",
        len(top2) == 2,
        f"got {len(top2)}",
    ))
    checks.append((
        "top2_first_is_DF01",
        top2[0]["id"] == "DF01",
        f"got {top2[0]['id']}",
    ))
    # DF02 (4×5=20) and DF03 (5×4=20) tie on combined_score; tie-break by sum_score
    # both have sum 9, then by consensus_sigma (both 0), then by id → DF02
    checks.append((
        "top2_second_tiebreak_DF02",
        top2[1]["id"] == "DF02",
        f"got {top2[1]['id']}",
    ))

    # 7. PDF verbatim keys non-empty
    for key, txt in PDF_VERBATIM.items():
        checks.append((
            f"verbatim:{key}",
            bool(txt) and len(txt) > 10,
            "verbatim must be substantive string",
        ))
        checks.append((
            f"attribution:{key}",
            key in VERBATIM_ATTRIBUTION and bool(VERBATIM_ATTRIBUTION[key]),
            "every verbatim must have attribution",
        ))

    all_pass = all(ok for _, ok, _ in checks)
    print(json.dumps({
        "ALL_PASS": all_pass,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }, ensure_ascii=False, indent=2))
    return 0 if all_pass else 1


def cmd_verbatim(key: str) -> int:
    if key not in PDF_VERBATIM:
        print(json.dumps({
            "error": f"unknown verbatim key '{key}'",
            "available": sorted(PDF_VERBATIM.keys()),
        }, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({
        "key": key,
        "verbatim": PDF_VERBATIM[key],
        "attribution": VERBATIM_ATTRIBUTION[key],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_verbatim_all() -> int:
    print(json.dumps({
        "primary_source": PRIMARY_SOURCE,
        "verbatim": {k: {
            "quote": v,
            "attribution": VERBATIM_ATTRIBUTION[k],
        } for k, v in PDF_VERBATIM.items()},
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_likert_scale() -> int:
    print(json.dumps({
        "importance": LIKERT_IMPORTANCE,
        "uncertainty": LIKERT_UNCERTAINTY,
        "min": LIKERT_MIN,
        "max": LIKERT_MAX,
        "source": SCHOEMAKER_1995,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_quadrant_thresholds() -> int:
    print(json.dumps({
        "threshold": QUADRANT_THRESHOLD,
        "rule": (f"value >= {QUADRANT_THRESHOLD} → High; "
                 f"value < {QUADRANT_THRESHOLD} → Low"),
        "quadrants": QUADRANTS,
        "label_map": QUADRANT_LABEL,
        "source": (VAN_DER_HEIJDEN_1996 + " + " + SCHOEMAKER_1995 +
                   " — standard GBN 2x2 method"),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_classify(imp: str, unc: str) -> int:
    i = float(imp)
    u = float(unc)
    if not (LIKERT_MIN <= i <= LIKERT_MAX) or not (LIKERT_MIN <= u <= LIKERT_MAX):
        print(json.dumps({
            "error": f"values must be in [{LIKERT_MIN}, {LIKERT_MAX}]",
        }))
        return 1
    q = classify_quadrant(i, u)
    print(json.dumps({
        "importance": i,
        "uncertainty": u,
        "quadrant": q,
        "label": QUADRANT_LABEL[q],
        "meaning": QUADRANTS[q],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_validate_input(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    res = validate_input(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["pass"] else 1


def cmd_rank(input_path: str, output_path: str | None) -> int:
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    vr = validate_input(data)
    if not vr["pass"]:
        print(json.dumps({
            "error": "input validation failed",
            "errors": vr["errors"],
        }, ensure_ascii=False, indent=2))
        return 1
    enriched = rank_forces(data["driving_forces"])
    top2 = select_top2_critical(enriched)
    pre = list_predetermined(enriched)
    meta = data.get("meta")
    md = build_markdown(enriched, top2, pre, meta)
    if output_path:
        Path(output_path).write_text(md, encoding="utf-8")
        print(json.dumps({
            "wrote": output_path,
            "top2": [d["id"] for d in top2],
            "predetermined": [d["id"] for d in pre],
            "quadrant_counts": {
                q: sum(1 for d in enriched if d["quadrant"] == q)
                for q in ("CRITICAL", "PREDETERMINED", "NOISE", "BACKGROUND")
            },
        }, ensure_ascii=False, indent=2))
    else:
        print(md)
    return 0


REQUIRED_HEADERS = [
    "### § Importance-Uncertainty Matrix",
    "**Total Driving Forces Ranked**:",
    "**Top-2 Critical Drivers (Recommended Axes)**:",
    "**Predetermined Elements (Common to All Scenarios)**:",
    "**Quadrant Distribution**:",
    "**Quadrant Threshold**:",
    "#### Scoring Table",
    "#### 2×2 Matrix Visualization",
    "#### Top-2 Critical Drivers (Scenario Axes Recommendation)",
    "#### Predetermined Elements",
    "#### 다음 sub-skill 전달",
    "→ vision-foresight-scenarios-scenario-logics-selection",
    "##### Determinism Audit",
]


def cmd_audit_output(path: str) -> int:
    """생성된 markdown이 모든 필수 섹션을 포함하는지 검증."""
    text = Path(path).read_text(encoding="utf-8")
    missing = [h for h in REQUIRED_HEADERS if h not in text]
    res = {
        "pass": len(missing) == 0,
        "missing_headers": missing,
        "file": path,
        "size_bytes": len(text.encode("utf-8")),
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["pass"] else 1


def cmd_demo() -> int:
    """데모 입력 → ranking 결과 출력."""
    demo_input = {
        "meta": {"focal_issue": "한국 EV 배터리 2030 시나리오"},
        "driving_forces": [
            {"id": "DF01", "name": "중국 배터리 가격 경쟁력",
             "endpoints_low": "급격한 가격 하락", "endpoints_high": "가격 정상화",
             "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 5}
                        for k in range(6)]},
            {"id": "DF02", "name": "전고체전지 상용화 시점",
             "endpoints_low": "2028 조기 상용화", "endpoints_high": "2035 이후 지연",
             "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 4}
                        for k in range(6)]},
            {"id": "DF03", "name": "원자재(리튬·니켈) 수급",
             "endpoints_low": "안정", "endpoints_high": "위기",
             "scores": [{"persona": f"P{k}", "importance": 4, "uncertainty": 4}
                        for k in range(6)]},
            {"id": "DF04", "name": "글로벌 EV 침투율",
             "endpoints_low": "둔화", "endpoints_high": "가속",
             "scores": [{"persona": f"P{k}", "importance": 5, "uncertainty": 2}
                        for k in range(6)]},
            {"id": "DF05", "name": "미국 IRA 보조금 지속",
             "endpoints_low": "축소", "endpoints_high": "유지",
             "scores": [{"persona": f"P{k}", "importance": 4, "uncertainty": 5}
                        for k in range(6)]},
            {"id": "DF06", "name": "EU 탄소국경세 강도",
             "endpoints_low": "완화", "endpoints_high": "강화",
             "scores": [{"persona": f"P{k}", "importance": 2, "uncertainty": 2}
                        for k in range(6)]},
        ]
    }
    enriched = rank_forces(demo_input["driving_forces"])
    top2 = select_top2_critical(enriched)
    pre = list_predetermined(enriched)
    print(build_markdown(enriched, top2, pre, demo_input["meta"]))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "validate":
        return cmd_validate()
    if cmd == "verbatim" and len(argv) >= 3:
        return cmd_verbatim(argv[2])
    if cmd == "verbatim_all":
        return cmd_verbatim_all()
    if cmd == "likert_scale":
        return cmd_likert_scale()
    if cmd == "quadrant_thresholds":
        return cmd_quadrant_thresholds()
    if cmd == "classify" and len(argv) >= 4:
        return cmd_classify(argv[2], argv[3])
    if cmd == "validate_input" and len(argv) >= 3:
        return cmd_validate_input(argv[2])
    if cmd == "rank" and len(argv) >= 3:
        out = argv[3] if len(argv) >= 4 else None
        return cmd_rank(argv[2], out)
    if cmd == "audit_output" and len(argv) >= 3:
        return cmd_audit_output(argv[2])
    if cmd == "demo":
        return cmd_demo()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
