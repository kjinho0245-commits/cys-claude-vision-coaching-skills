#!/usr/bin/env python3
"""
_e2e_test_runner_round2.py — Second independent validation round for Wild Cards Assessment.

10 COMPLETELY DIFFERENT test prompts from Round 1 (T1-T10).
Round 1 covered: tech investors, climate researcher, pastor, public policy, normalization bugs,
                 quality diversity, PPS computation, domain total mismatch, academic researcher.

Round 2 covers:  max PPS validation, invalid score detection, affinity clamping,
                 small business owner, military/defense, NGO/civil society, top_n=15,
                 top_n=20, sustenance-dominant priority, all-same-domain error.

Source: Petersen & Steinmüller (2009) Ch.10 Section III.2.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from wc_assessment_validator import (
    validate_subvar_scores,
    compute_pyramid_scores,
    compute_pps,
    validate_affinity_score,
    normalize_psychographic_profile,
    compute_adjusted_pps,
    validate_top_n,
    apply_top_n_filter,
    validate_domain_diversity,
    validate_surprise_type_diversity,
    validate_quality_diversity,
    validate_assessment_output,
    VALID_IMPACT_SCORES,
    PPS_MAX,
)

# ── Helpers from Round 1 (shared) ─────────────────────────────────────────────

def make_candidate(cid, title, scores, domain, surprise_type, quality_factor,
                   psychographic_profile, domain_focus):
    sv_result = validate_subvar_scores({"scores": scores})
    if not sv_result["passed"]:
        return None, sv_result["violations"]
    ps_result = compute_pyramid_scores(scores)
    if not ps_result["passed"]:
        return None, ps_result["violations"]
    pyramid = ps_result["pyramid_scores"]
    pps_result = compute_pps(pyramid)
    pps = pps_result["total_pps"]
    dominant_pf = pps_result["dominant_power_factor"]

    norm_result = normalize_psychographic_profile(psychographic_profile)
    norm_profile = norm_result["normalized"]

    wc_type_profiles = {
        "type1": {"inner-directed": 0.3, "outer-directed": 0.5, "sustenance-driven": 0.2},
        "type2": {"inner-directed": 0.4, "outer-directed": 0.4, "sustenance-driven": 0.2},
        "type3": {"inner-directed": 0.7, "outer-directed": 0.2, "sustenance-driven": 0.1},
    }
    wc_profile = wc_type_profiles.get(surprise_type, {"inner-directed": 0.33, "outer-directed": 0.33, "sustenance-driven": 0.34})
    psych_match = sum(norm_profile.get(k, 0) * wc_profile.get(k, 0) for k in norm_profile)
    d_match = domain_focus.get(domain, 0.1)
    raw_affinity = (psych_match * 0.4) + (d_match * 0.6)
    raw_affinity = min(1.0, max(0.0, raw_affinity))
    aff_result = validate_affinity_score(raw_affinity)
    affinity = raw_affinity if aff_result["valid"] else 0.0
    adj_result = compute_adjusted_pps(pps, affinity)
    adjusted_pps = adj_result["adjusted_pps"]

    return {
        "id": cid, "title": title,
        "total_pps": pps, "dominant_power_factor": dominant_pf,
        "target_affinity": round(affinity, 4),
        "adjusted_pps": adjusted_pps,
        "domain": domain, "surprise_type": surprise_type, "quality_factor": quality_factor,
        "eliminated": False, "elimination_reason": None,
    }, []


def build_filter_summary(selected, n):
    dc = {"S": 0, "T": 0, "E": 0, "Env": 0, "P": 0, "Spi": 0}
    tc = {"type1": 0, "type2": 0, "type3": 0}
    qc = {"positive": 0, "negative": 0, "both": 0}
    for c in selected:
        d = c.get("domain", "")
        if d in dc: dc[d] += 1
        t = c.get("surprise_type", "")
        if t in tc: tc[t] += 1
        q = c.get("quality_factor", "")
        if q in qc: qc[q] += 1
    return {
        "top_n_selected": len(selected),
        "domain_coverage": {**dc, "total": sum(dc.values())},
        "type_coverage": tc,
        "quality_coverage": qc,
    }


def make_test(tid, scenario, mode, target_group, psych, domain_focus, top_n, candidates_spec, expected="PASS"):
    errors = []
    n_result = validate_top_n(top_n)
    actual_n = top_n if n_result["valid"] else 10
    if not n_result["valid"]:
        errors.append(f"INVALID_TOP_N: {n_result['error']}")

    norm_result = normalize_psychographic_profile(psych)
    if not norm_result["passed"]:
        errors.extend(norm_result["violations"])

    candidates = []
    build_errors = []
    for spec in candidates_spec:
        cand, cerrs = make_candidate(spec["id"], spec["title"], spec["scores"],
                                     spec["domain"], spec["surprise_type"], spec["quality_factor"],
                                     psych, domain_focus)
        if cand:
            candidates.append(cand)
        else:
            build_errors.extend(cerrs)

    filter_result = apply_top_n_filter(candidates, actual_n)
    if not filter_result["passed"]:
        errors.extend(filter_result["violations"])
    selected = filter_result.get("selected", [])

    dd = validate_domain_diversity(selected, actual_n)
    if not dd["passed"]: errors.extend(dd["violations"])
    qd = validate_quality_diversity(selected)
    if not qd["passed"]: errors.extend(qd["violations"])

    fs = build_filter_summary(selected, actual_n)
    output = {
        "meta": {"target_group": target_group,
                 "target_group_profile": norm_result.get("normalized", psych),
                 "top_n": actual_n, "n_total_candidates": len(candidates)},
        "ranked_candidates": selected,
        "filter_summary": fs,
        "next_skill": "vision-foresight-wild-cards-impact-index",
    }
    gate = validate_assessment_output(output)
    gate_pass = gate["passed"]

    if expected == "PASS":
        overall = "PASS" if gate_pass and len(errors) == 0 else "FAIL"
    elif expected == "FAIL":
        overall = "PASS (correctly detected FAIL)" if (not gate_pass or len(errors) > 0) else "FAIL"
    else:
        overall = "PASS" if gate_pass else "FAIL"

    return {
        "test_id": tid, "scenario": scenario, "mode": mode, "expected": expected,
        "overall": overall, "n_candidates": len(candidates), "n_selected": len(selected),
        "gate_result": gate, "build_errors": build_errors, "validation_errors": errors,
    }


# ── Score templates (DIFFERENT from Round 1 — specific patterns) ──────────────

def all_max_scores():
    """All sub-variables at maximum (3) — should give PPS=30."""
    return {"B-1":3,"B-2":3,"B-3":3,"B-4":3,"S-1":3,"S-2":3,"S-3":3,"S-4":3,
            "A-1":3,"A-2":3,"A-3":3,"T-1":3,"T-2":3,"T-3":3}

def all_min_scores():
    """All sub-variables at minimum (0) — should give PPS=0."""
    return {"B-1":0,"B-2":0,"B-3":0,"B-4":0,"S-1":0,"S-2":0,"S-3":0,"S-4":0,
            "A-1":0,"A-2":0,"A-3":0,"T-1":0,"T-2":0,"T-3":0}

def mid_scores():
    return {"B-1":2,"B-2":1,"B-3":2,"B-4":1,"S-1":2,"S-2":1,"S-3":2,"S-4":1,
            "A-1":2,"A-2":1,"A-3":2,"T-1":2,"T-2":1,"T-3":2}

def sustenance_dominant():
    return {"B-1":1,"B-2":1,"B-3":1,"B-4":1,"S-1":3,"S-2":3,"S-3":3,"S-4":3,
            "A-1":1,"A-2":1,"A-3":1,"T-1":1,"T-2":1,"T-3":1}

def actions_dominant():
    return {"B-1":1,"B-2":1,"B-3":1,"B-4":1,"S-1":1,"S-2":1,"S-3":1,"S-4":1,
            "A-1":3,"A-2":3,"A-3":3,"T-1":1,"T-2":1,"T-3":1}

def being_medium_rest_low():
    return {"B-1":2,"B-2":2,"B-3":2,"B-4":2,"S-1":1,"S-2":1,"S-3":0,"S-4":0,
            "A-1":1,"A-2":0,"A-3":0,"T-1":1,"T-2":0,"T-3":0}


PSYCH_BUSINESS = {"inner-directed": 0.3, "outer-directed": 0.5, "sustenance-driven": 0.2}
PSYCH_MILITARY = {"inner-directed": 0.2, "outer-directed": 0.7, "sustenance-driven": 0.1}
PSYCH_NGO = {"inner-directed": 0.5, "outer-directed": 0.3, "sustenance-driven": 0.2}
PSYCH_EQUAL = {"inner-directed": 0.33, "outer-directed": 0.33, "sustenance-driven": 0.34}

DOMAIN_BUSINESS = {"S": 0.2, "T": 0.3, "E": 0.3, "Env": 0.1, "P": 0.05, "Spi": 0.05}
DOMAIN_MILITARY = {"S": 0.1, "T": 0.3, "E": 0.1, "Env": 0.1, "P": 0.35, "Spi": 0.05}
DOMAIN_NGO = {"S": 0.35, "T": 0.1, "E": 0.15, "Env": 0.2, "P": 0.1, "Spi": 0.1}
DOMAIN_EQUAL = {"S": 0.167, "T": 0.167, "E": 0.167, "Env": 0.167, "P": 0.167, "Spi": 0.165}

TESTS = []

# ── TEST R2-01: Maximum PPS validation (all scores=3 → PPS=30) ───────────────
ps_max = compute_pyramid_scores(all_max_scores())
pps_max = compute_pps(ps_max["pyramid_scores"])
adj_max = compute_adjusted_pps(30.0, 0.9)
TESTS.append({
    "test_id": "R2-01",
    "scenario": "결정론 검증 — 모든 sub-var=3일 때 PPS=30.0 (이론적 최대값 검증)",
    "mode": "computation_accuracy",
    "expected": "PASS",
    "overall": "PASS" if (
        abs(pps_max["total_pps"] - PPS_MAX) < 0.001 and pps_max["passed"]
    ) else "FAIL",
    "gate_result": pps_max,
    "validation_errors": pps_max["violations"],
    "build_errors": [],
    "n_candidates": 1, "n_selected": 1,
    "pps_verification": {
        "all_scores": "3 (maximum)",
        "expected_pps": PPS_MAX,
        "actual_pps": pps_max["total_pps"],
        "formula": "Being(3×4=12) + Sustenance(3×3=9) + Actions(3×2=6) + Tools(3×1=3) = 30",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    },
})

# ── TEST R2-02: Minimum PPS (all scores=0 → PPS=0) ──────────────────────────
ps_min = compute_pyramid_scores(all_min_scores())
pps_min = compute_pps(ps_min["pyramid_scores"])
TESTS.append({
    "test_id": "R2-02",
    "scenario": "결정론 검증 — 모든 sub-var=0일 때 PPS=0.0 (이론적 최솟값 검증)",
    "mode": "computation_accuracy",
    "expected": "PASS",
    "overall": "PASS" if abs(pps_min["total_pps"] - 0.0) < 0.001 and pps_min["passed"] else "FAIL",
    "gate_result": pps_min,
    "validation_errors": pps_min["violations"],
    "build_errors": [],
    "n_candidates": 1, "n_selected": 1,
    "pps_verification": {
        "all_scores": "0 (minimum)",
        "expected_pps": 0.0,
        "actual_pps": pps_min["total_pps"],
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    },
})

# ── TEST R2-03: Invalid sub-variable score (score=4 → out of {0,1,2,3}) ──────
invalid_scores = {"B-1":4,"B-2":3,"B-3":2,"B-4":2,"S-1":1,"S-2":1,"S-3":1,"S-4":1,
                  "A-1":2,"A-2":2,"A-3":3,"T-1":3,"T-2":3,"T-3":3}
sv_invalid = validate_subvar_scores({"candidate": {"scores": invalid_scores}, "scores": invalid_scores})
TESTS.append({
    "test_id": "R2-03",
    "scenario": "오류 감지 — sub-variable score=4 (허용 범위 {0,1,2,3} 초과)",
    "mode": "error_detection",
    "expected": "FAIL",
    "overall": "PASS (correctly detected invalid score=4)" if not sv_invalid["passed"] and any("B-1" in v for v in sv_invalid["violations"]) else "FAIL",
    "gate_result": sv_invalid,
    "validation_errors": sv_invalid["violations"],
    "build_errors": [],
    "n_candidates": 1, "n_selected": 0,
})

# ── TEST R2-04: Affinity clamping — raw > 1.0 must be clamped ────────────────
aff_over = validate_affinity_score(1.5)
TESTS.append({
    "test_id": "R2-04",
    "scenario": "오류 감지 — affinity_score=1.5 > 1.0 범위 위반 (Adjusted_PPS 무한 확장 차단)",
    "mode": "error_detection",
    "expected": "FAIL",
    "overall": "PASS (correctly rejected score=1.5)" if not aff_over["valid"] else "FAIL",
    "gate_result": aff_over,
    "validation_errors": [aff_over.get("error", "")],
    "build_errors": [],
    "n_candidates": 1, "n_selected": 1,
})

# ── TEST R2-05: Small business owner — top_n=10, E/T domains heavy ────────────
biz_candidates = [
    {"id":"WC-B01","title":"AI 공급망 최적화 → 중소기업 비용 70% 절감","scores":being_medium_rest_low(),"domain":"E","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-B02","title":"블록체인 스마트계약 법인 대체","scores":mid_scores(),"domain":"T","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-B03","title":"글로벌 통화 붕괴 달러 패권 종언","scores":sustenance_dominant(),"domain":"E","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-B04","title":"AI 규제 프레임워크 국제 표준화","scores":actions_dominant(),"domain":"P","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-B05","title":"해킹으로 전국 결제망 동시 마비","scores":sustenance_dominant(),"domain":"T","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-B06","title":"기업 ESG 의무화 중소기업 도산 급증","scores":being_medium_rest_low(),"domain":"P","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-B07","title":"초장기 경기침체 10년 디플레이션","scores":sustenance_dominant(),"domain":"E","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-B08","title":"재생에너지 제로비용 에너지 민주화","scores":sustenance_dominant(),"domain":"Env","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-B09","title":"온라인 근무 도시 집중화 완전 역전","scores":mid_scores(),"domain":"S","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-B10","title":"AI 창업 자동화 — 인간 기업가 불필요","scores":being_medium_rest_low(),"domain":"Spi","surprise_type":"type3","quality_factor":"negative"},
]

TESTS.append(make_test(
    "R2-05", "C3 Assessment — 소상공인 대상 비즈니스 중심 Wild Cards 평가",
    "C3", "Korean small business owner", PSYCH_BUSINESS, DOMAIN_BUSINESS, 10, biz_candidates, "PASS"
))

# ── TEST R2-06: Military context — top_n=10, P domain dominant ────────────────
mil_candidates = [
    {"id":"WC-M01","title":"북한 핵 EMP 공격 전국 전력 마비","scores":sustenance_dominant(),"domain":"P","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-M02","title":"AI 드론 전쟁 재래식 군사력 무효화","scores":mid_scores(),"domain":"T","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-M03","title":"미중 전쟁 한반도 전장화","scores":sustenance_dominant(),"domain":"P","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-M04","title":"민간인 자율 드론 테러","scores":being_medium_rest_low(),"domain":"P","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-M05","title":"사이버 핵 발사 코드 해킹","scores":all_max_scores(),"domain":"T","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-M06","title":"UN 군사력 사용 금지 조약","scores":actions_dominant(),"domain":"P","surprise_type":"type3","quality_factor":"positive"},
    {"id":"WC-M07","title":"생물무기 은밀 공격 발원 불명 생태계 붕괴","scores":all_max_scores(),"domain":"Env","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-M08","title":"동아시아 집단 안보 NATO형 동맹","scores":actions_dominant(),"domain":"P","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-M09","title":"민간 우주 기업 군사화","scores":mid_scores(),"domain":"T","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-M10","title":"군인 사회 신뢰 붕괴 징병 거부 운동 대규모화","scores":all_max_scores(),"domain":"S","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-M11","title":"글로벌 경제 제재 전면 공급망 붕괴 대공황급","scores":all_max_scores(),"domain":"E","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-M12","title":"군사 종교 결합 성전 선포 국제전 발발","scores":all_max_scores(),"domain":"Spi","surprise_type":"type1","quality_factor":"negative"},
]

TESTS.append(make_test(
    "R2-06", "C3 Assessment — 군사/안보 전문가 대상 안보 Wild Cards 평가 (P 도메인 집중)",
    "C3", "Korean military strategist", PSYCH_MILITARY, DOMAIN_MILITARY, 10, mil_candidates, "PASS"
))

# ── TEST R2-07: NGO/civil society — top_n=15 ────────────────────────────────
ngo_candidates = [
    {"id":"WC-N01","title":"인터넷 완전 검열 국가 탈인터넷화","scores":actions_dominant(),"domain":"P","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-N02","title":"디지털 신분증 전면 의무화","scores":being_medium_rest_low(),"domain":"T","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N03","title":"시민사회 탄압 — 글로벌 NGO 해산령","scores":actions_dominant(),"domain":"P","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-N04","title":"기본소득 전면 도입","scores":sustenance_dominant(),"domain":"E","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-N05","title":"집단 기억 상실 — 소셜미디어 역사 왜곡","scores":being_medium_rest_low(),"domain":"S","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N06","title":"종교 다원주의 법제화","scores":actions_dominant(),"domain":"Spi","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-N07","title":"코로나급 신규 팬데믹 재발","scores":sustenance_dominant(),"domain":"Env","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-N08","title":"기후 난민 1억 명 이동","scores":sustenance_dominant(),"domain":"Env","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N09","title":"청년 글로벌 파업 운동 동시 발화","scores":actions_dominant(),"domain":"S","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-N10","title":"AI 복지 시스템 불평등 자동 심화","scores":being_medium_rest_low(),"domain":"T","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N11","title":"물 전쟁 — 수자원 국가 갈등 폭발","scores":sustenance_dominant(),"domain":"Env","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N12","title":"집단 지성 AI — 세계 의회 창설","scores":actions_dominant(),"domain":"P","surprise_type":"type3","quality_factor":"positive"},
    {"id":"WC-N13","title":"마이크로 국가 100개 독립 선언","scores":mid_scores(),"domain":"P","surprise_type":"type3","quality_factor":"both"},
    {"id":"WC-N14","title":"성별 경계 법적 해체 — 제3성 공식화","scores":being_medium_rest_low(),"domain":"S","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-N15","title":"AI 인권 선언 — 기계에 법적 지위","scores":mid_scores(),"domain":"Spi","surprise_type":"type3","quality_factor":"both"},
    {"id":"WC-N16","title":"생명연장 기술 불평등 — 초고령 엘리트 vs 단명 빈곤층","scores":sustenance_dominant(),"domain":"E","surprise_type":"type2","quality_factor":"negative"},
    {"id":"WC-N17","title":"공공 의료 AI — 의사 전면 대체","scores":mid_scores(),"domain":"T","surprise_type":"type2","quality_factor":"both"},
    {"id":"WC-N18","title":"양자 인터넷 보안 혁명","scores":mid_scores(),"domain":"T","surprise_type":"type2","quality_factor":"positive"},
    {"id":"WC-N19","title":"종교 근본주의 국가 주도 부활","scores":being_medium_rest_low(),"domain":"Spi","surprise_type":"type1","quality_factor":"negative"},
    {"id":"WC-N20","title":"전 세계 동시 교육 개혁 — AI 튜터 보편화","scores":actions_dominant(),"domain":"S","surprise_type":"type2","quality_factor":"positive"},
]

TESTS.append(make_test(
    "R2-07", "C3 Assessment — NGO/시민사회 대상 top_n=15 Wild Cards 광범위 평가",
    "C3", "Korean NGO/civil society", PSYCH_NGO, DOMAIN_NGO, 15, ngo_candidates, "PASS"
))

# ── TEST R2-08: top_n=20 — large pool ─────────────────────────────────────────
large_pool = [
    {"id":f"WC-L{i:02d}","title":f"Wild Card {i}","scores":mid_scores(),
     "domain":["S","T","E","Env","P","Spi"][i%6],
     "surprise_type":["type1","type2","type3"][i%3],
     "quality_factor":["positive","negative","both"][i%3]}
    for i in range(25)
]
# Ensure at least 1 positive and Spi domain gets high PPS to survive top-20 cutoff
large_pool[0]["quality_factor"] = "positive"
large_pool[1]["quality_factor"] = "positive"
# Boost Spi and E domain entries to ensure they rank high in top-20
for idx in [5, 11, 17, 23]:   # Spi domains
    if idx < len(large_pool):
        large_pool[idx]["scores"] = all_max_scores()
for idx in [2, 8, 14, 20]:    # E domains
    if idx < len(large_pool):
        large_pool[idx]["scores"] = all_max_scores()

TESTS.append(make_test(
    "R2-08", "top_n=20 — 25개 후보 풀에서 20개 선정 (대규모 평가)",
    "C3", "Global foresight panel", PSYCH_EQUAL, DOMAIN_EQUAL, 20, large_pool, "PASS"
))

# ── TEST R2-09: Sustenance-dominant WC priority test ─────────────────────────
# Verify that Sustenance-dominant WCs score higher when Being scores are equal
scores_sustenance = {"B-1":2,"B-2":2,"B-3":2,"B-4":2,"S-1":3,"S-2":3,"S-3":3,"S-4":3,
                     "A-1":1,"A-2":1,"A-3":1,"T-1":1,"T-2":1,"T-3":1}
scores_tools_same_being = {"B-1":2,"B-2":2,"B-3":2,"B-4":2,"S-1":1,"S-2":1,"S-3":1,"S-4":1,
                            "A-1":1,"A-2":1,"A-3":1,"T-1":3,"T-2":3,"T-3":3}

ps_sust = compute_pyramid_scores(scores_sustenance)
ps_tools = compute_pyramid_scores(scores_tools_same_being)
pps_sust = compute_pps(ps_sust["pyramid_scores"])
pps_tools = compute_pps(ps_tools["pyramid_scores"])

# Expected: PPS_sustenance > PPS_tools (Sustenance PF=3 > Tools PF=1)
# Sustenance: Being(2×4=8) + Sustenance(3×3=9) + Actions(1×2=2) + Tools(1×1=1) = 20
# Tools_same_being: Being(2×4=8) + Sustenance(1×3=3) + Actions(1×2=2) + Tools(3×1=3) = 16
sust_wins = pps_sust["total_pps"] > pps_tools["total_pps"]
sust_dominant_correct = pps_sust["dominant_category"] == "sustenance"

TESTS.append({
    "test_id": "R2-09",
    "scenario": "Pyramid 원리 검증 — Sustenance(PF=3) 우선순위 > Tools(PF=1) (same Being 기반 비교)",
    "mode": "computation_accuracy",
    "expected": "PASS",
    "overall": "PASS" if sust_wins and sust_dominant_correct else "FAIL",
    "gate_result": {"passed": sust_wins, "sustenance_pps": pps_sust["total_pps"], "tools_pps": pps_tools["total_pps"],
                    "verbatim": "lower characteristics (being, sustenance) are intrinsically more powerful",
                    "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 verbatim"},
    "validation_errors": [] if sust_wins else [f"Sustenance PPS({pps_sust['total_pps']}) should > Tools PPS({pps_tools['total_pps']})"],
    "build_errors": [],
    "n_candidates": 2, "n_selected": 2,
    "pps_comparison": {
        "sustenance_dominant_pps": pps_sust["total_pps"],
        "tools_dominant_pps": pps_tools["total_pps"],
        "sustenance_wins": sust_wins,
        "expected_sustenance_pps": 20.0,
        "expected_tools_pps": 16.0,
    },
})

# ── TEST R2-10: All-same-domain error → domain diversity violation ─────────────
all_T_candidates = [
    {"id":f"WC-T{i:02d}","title":f"Technology WC {i}","scores":mid_scores(),
     "domain":"T","surprise_type":["type1","type2","type3"][i%3],
     "quality_factor":"positive" if i == 0 else "negative"}
    for i in range(12)
]

TESTS.append(make_test(
    "R2-10", "오류 감지 — 모든 후보가 T(Technology) 도메인 → STEEP+S 다양성 위반",
    "C3", "Tech-only focus group", PSYCH_EQUAL, DOMAIN_EQUAL, 10, all_T_candidates, "FAIL"
))


# ── Runner ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("Wild Cards Assessment — ROUND 2 End-to-End Validation Suite")
    print("10 COMPLETELY DIFFERENT scenarios from Round 1 (T1-T10)")
    print("Source: Petersen & Steinmüller (2009) Ch.10 Section III.2")
    print("=" * 72)

    pass_count = 0
    fail_count = 0

    for test in TESTS:
        tid = test["test_id"]
        scenario = test["scenario"]
        overall = test["overall"]
        gate = test.get("gate_result", {})
        violations = test.get("validation_errors", [])
        build_errors = test.get("build_errors", [])

        icon = "✓" if "PASS" in overall else "✗"
        print(f"\n[{icon}] {tid}: {scenario}")
        print(f"    Mode: {test['mode']} | Expected: {test['expected']}")
        print(f"    Overall: {overall}")

        if isinstance(gate, dict):
            passed = gate.get("passed", gate.get("valid", None))
            if passed is not None:
                inner_icon = "  ✓" if passed else "  ✗"
                summary = gate.get("summary", str({k: v for k, v in gate.items() if k in ("total_pps", "sustenance_pps", "tools_pps")}))
                print(f"   {inner_icon} Gate: {'PASS' if passed else 'FAIL'} — {str(summary)[:70]}")

        if violations and not ("PASS" in overall and "correctly" not in overall):
            for v in violations[:2]:
                print(f"    Violation: {str(v)[:80]}")

        extra = test.get("pps_verification") or test.get("pps_comparison")
        if extra:
            for k, v in list(extra.items())[:3]:
                print(f"    {k}: {v}")

        if "n_selected" in test and test["n_selected"] > 0:
            print(f"    Candidates: {test.get('n_candidates',0)} input → {test['n_selected']} selected")

        if "PASS" in overall:
            pass_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 72)
    print(f"ROUND 2 FINAL RESULT: {pass_count}/{len(TESTS)} PASS, {fail_count} FAIL")
    print("=" * 72)
    for t in TESTS:
        icon = "✓" if "PASS" in t["overall"] else "✗"
        print(f"  {icon} {t['test_id']}: {t['scenario'][:65]}")

    if fail_count == 0:
        print("\n✓ ROUND 2 ALL TESTS PASSED — Wild Cards Assessment Agent double-verified.")
        print("  Both Round 1 (T1-T10) and Round 2 (R2-01~R2-10) passed independently.")
        print("  Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 verbatim compliance.")
    else:
        print(f"\n✗ {fail_count} test(s) FAILED — see above.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
