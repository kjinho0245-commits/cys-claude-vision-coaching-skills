"""Deterministic age/education filter for candidate jobs.

Hard rules (mirror SKILL.md §나이·학력 우선 필터링 규칙):
- ✓ 적합 (pass): age in [min_age, max_age] AND user_education_rank >= min_education_rank
- △ 약간 미달 (borderline): age within ±5 of bound OR education exactly 1 rank below
- ✗ 미달 (fail): otherwise — excluded from final slot
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .catalog import education_rank, get_age_category, jobs_in_type, normalize_education

AGE_TOLERANCE = 5


def classify_fit(
    job: Dict,
    age: Optional[int],
    education: Optional[str],
) -> Tuple[str, str]:
    """Return (verdict, explanation) where verdict ∈ {pass, borderline, fail}."""

    if age is None and education is None:
        return ("unknown", "나이·학력 미확인 — 실제 적합도는 개인 상황에 따라 다름")

    min_edu = job.get("min_education")
    edu_gap = None
    if education is not None and min_edu is not None:
        user_rank = education_rank(education)
        req_rank = education_rank(min_edu)
        edu_gap = user_rank - req_rank
    age_status = "unknown"
    if age is not None:
        if job["min_age"] <= age <= job["max_age"]:
            age_status = "in_range"
        elif (
            (job["min_age"] - AGE_TOLERANCE) <= age < job["min_age"]
            or job["max_age"] < age <= (job["max_age"] + AGE_TOLERANCE)
        ):
            age_status = "borderline"
        else:
            age_status = "out"

    # strict_education = true: any negative edu_gap is FAIL (no borderline tolerance)
    is_strict = bool(job.get("strict_education"))

    # Pure FAIL: education clearly below
    if edu_gap is not None:
        if is_strict and edu_gap < 0:
            return ("fail", f"학력 미달 — 전문자격 직업({job.get('ko')})은 정확한 학력 필요 ({education} → {min_edu})")
        if edu_gap <= -2:
            return ("fail", f"학력 미달 ({education} → 필요 {min_edu})")
    # Out of age range with no borderline allowance
    if age_status == "out":
        return ("fail", f"나이 범위 초과 (권장 {job['min_age']}~{job['max_age']})")

    # Borderline conditions
    if edu_gap is not None and edu_gap == -1:
        return ("borderline", f"학력 1단계 부족 — 보완 경로 필요 ({education} → {min_edu})")
    if age_status == "borderline":
        return ("borderline", f"나이 권장 범위 ±{AGE_TOLERANCE}년 — 추가 검토 권장")

    # All clear
    return ("pass", "나이·학력 적합")


def filter_jobs_for_user(
    type_key: str,
    age: Optional[int],
    education: Optional[str],
    include_faith_jobs: bool = False,
) -> List[Dict]:
    """Return list of jobs with verdict tagged. Sorts pass > borderline > fail."""
    edu_norm = normalize_education(education) if education else None
    candidates = jobs_in_type(type_key)
    results = []
    for job in candidates:
        if job.get("requires_faith_disclosure") and not include_faith_jobs:
            continue
        verdict, reason = classify_fit(job, age, edu_norm)
        out = dict(job)
        out["_verdict"] = verdict
        out["_verdict_reason"] = reason
        results.append(out)
    order = {"pass": 0, "borderline": 1, "unknown": 2, "fail": 3}
    results.sort(key=lambda j: order[j["_verdict"]])
    return results


def _make_unfilled_slot(index: int, type_key: str, reason: str) -> Dict:
    """Placeholder slot used when no eligible job remains. SKILL.md rule:
    '5개 미만으로 출력하지 않는다' + '현재 직접 적합 직업 부족 — 이유: [구체 사유]'.
    Verdict='unfilled' so the LLM and validator can clearly mark this case.
    """
    return {
        "id": f"__unfilled_{type_key}_{index}__",
        "ko": "현재 직접 적합 직업 부족 (자료 기반)",
        "en": "No directly-fitting career in catalog (data-based)",
        "min_education": None,
        "min_age": None,
        "max_age": None,
        "rationale_keys": [],
        "_verdict": "unfilled",
        "_verdict_reason": reason,
        "_is_placeholder": True,
    }


def _is_aspirational_candidate(
    job: Dict,
    age: Optional[int],
    education: Optional[str],
    type_key: str,
) -> bool:
    """G7 #18: aspirational 후보 판정. fail 직업 중 *교육·연령 충족 시 진입 가능*한 것만 추출.

    조건:
    - 카테고리가 future/high_pay (지망 의미 있는 카테고리). retirement는 *은퇴 후* 의미라 aspirational 부적합.
    - 학력 gap이 -3 이하면 제외 (석사·박사 미보유 + 중졸 같은 극단 케이스 — 너무 멀어서 지망 의미 약함)
    - 나이가 *최소 나이보다 작은* 경우는 OK (성장하면 진입 가능). 나이 초과는 부적합 (지망 의미 없음).
    - strict_education + edu_gap<0인 직업 (전문자격 — 의사·변호사 등)은 OK — 명백한 지망 대상
    """
    if type_key in ("retirement",):
        return False
    min_edu = job.get("min_education")
    if education is not None and min_edu is not None:
        user_rank = education_rank(education)
        req_rank = education_rank(min_edu)
        edu_gap = user_rank - req_rank
        # G7 #26: 학력 gap 임계 age 기반 동적 조정 — 초등(age<15)은 -5까지 허용 (지망 의미 강함).
        # 청소년(15~18)은 -4. 성인 19+는 -3 (학력 갭이 너무 멀면 지망 무의미).
        if age is not None and age < 15:
            edu_threshold = -5
        elif age is not None and age < 19:
            edu_threshold = -4
        else:
            edu_threshold = -3
        if edu_gap < edu_threshold:
            return False
    if age is not None and "max_age" in job and job["max_age"] is not None:
        # 나이 초과 (이미 max_age 넘었으면 지망 무의미)
        if age > job["max_age"]:
            return False
    return True


def _to_aspirational_slot(job: Dict, age: Optional[int], education: Optional[str]) -> Dict:
    """G7 #18: fail 직업을 aspirational 슬롯으로 변환. 메타에 진입 조건 명시."""
    aspirational_job = dict(job)
    aspirational_job["_is_aspirational"] = True
    aspirational_job["_is_placeholder"] = False
    aspirational_job["_target_min_age"] = job.get("min_age")
    aspirational_job["_target_min_education"] = job.get("min_education")
    aspirational_job["_aspirational_note"] = (
        f"지망 직업 — 현재 조건(나이={age}, 학력={education})에는 미달하나, "
        f"필요 학력({job.get('min_education')}) + 진입 가능 나이({job.get('min_age')}~{job.get('max_age')}) "
        f"충족 시 진입 가능. 박사님 책 사양: 청소년·전환기 사용자에게 *목표 직업*으로 안내."
    )
    return aspirational_job


# G7 #20: 다중지능·에니어그램 → rationale_keys cross-matching 사전
# 박사님 책 사양: 다중지능 강점이 rationale_keys에 매칭되는 직업이 사용자에게 더 정합.
_MI_RATIONALE_TAGS = {
    "논리수학지능": ["analytical", "logical", "research", "data", "math", "science", "engineering", "stem"],
    "언어지능": ["verbal", "writing", "communication", "teaching", "language", "literature"],
    "공간지능": ["spatial", "visual", "design", "architecture", "art"],
    "음악지능": ["music", "audio", "rhythm"],
    "신체운동지능": ["physical", "kinesthetic", "athletic", "manual", "hands_on"],
    "인간친화지능": ["interpersonal", "social", "people", "relationship", "service", "teaching"],
    "자기성찰지능": ["introspective", "reflection", "self_aware", "philosophy"],
    "자연친화지능": ["nature", "environment", "biology", "ecology"],
    "실존지능": ["existential", "philosophy", "spirituality", "ethics", "meaning"],
}

# 에니어그램 1~9 → 직업 rationale_keys 매핑 (Holland·Riso-Hudson 표준)
_ENNEAGRAM_RATIONALE_TAGS = {
    "1": ["principled", "perfectionist", "quality", "ethics", "reform"],
    "2": ["caring", "helpful", "service", "people"],
    "3": ["achievement", "success", "performance", "ambitious"],
    "4": ["creative", "artistic", "individualistic", "expression"],
    "5": ["analytical", "research", "knowledge", "introspective", "expert", "investigator"],
    "6": ["loyal", "responsible", "security", "team"],
    "7": ["enthusiastic", "versatile", "adventurous", "innovation"],
    "8": ["leadership", "challenge", "decisive", "powerful"],
    "9": ["mediation", "peace", "harmony", "support"],
}


def _cross_match_score(
    job: Dict,
    mi_top: Optional[List[str]] = None,
    enneagram_type: Optional[str] = None,
) -> float:
    """G7 #20: 직업의 rationale_keys와 다중지능 top·에니어그램 매칭 점수 계산 (0~10).

    다중지능 1위 매칭 = 5점, 2위 = 3점, 3위 = 1점 가중치.
    에니어그램 주 유형 매칭 = 2점.
    """
    score = 0.0
    job_tags = set(job.get("rationale_keys") or [])
    if not job_tags:
        return 0.0
    if mi_top:
        weights = [5.0, 3.0, 1.0]
        for i, mi_name in enumerate(mi_top[:3]):
            tags = _MI_RATIONALE_TAGS.get(mi_name, [])
            if any(t in job_tags for t in tags):
                score += weights[i]
    if enneagram_type:
        en_tags = _ENNEAGRAM_RATIONALE_TAGS.get(str(enneagram_type), [])
        if any(t in job_tags for t in en_tags):
            score += 2.0
    return score


def select_top5(
    type_key: str,
    age: Optional[int],
    education: Optional[str],
    include_faith_jobs: bool = False,
    preferred_ids: Optional[List[str]] = None,
    mi_top: Optional[List[str]] = None,
    enneagram_type: Optional[str] = None,
) -> Dict:
    """Select 5 jobs for this type. Always returns 5 slots.

    HARD RULE (SKILL.md §나이·학력 우선 필터링):
    - verdict='fail' jobs are NEVER inserted into a slot.
    - When eligible count < 5, slots are padded with explicit placeholder objects
      (id='__unfilled_*__') rather than silently leaking fail-verdict jobs.

    Sort priority within eligible:
      1. preferred_ids (if any)
      2. faith-disclosed user → faith retirement jobs first (within retirement type)
      3. pass > borderline > unknown
    """
    filtered = filter_jobs_for_user(type_key, age, education, include_faith_jobs)
    eligible = [j for j in filtered if j["_verdict"] in ("pass", "borderline", "unknown")]
    # G7 #17·#18·#19: aspirational 모드 — fail verdict 중 *지망 가능*한 직업 후보 추출
    # (학력 gap이 너무 크지 않거나 나이 미달만이면서 카테고리가 future/high_pay인 경우)
    aspirational = [j for j in filtered if j["_verdict"] == "fail" and _is_aspirational_candidate(j, age, education, type_key)]

    pref_set = set(preferred_ids) if preferred_ids else set()
    verdict_rank = {"pass": 0, "borderline": 1, "unknown": 2}

    def sort_key(j):
        is_pref = 0 if j["id"] in pref_set else 1
        faith_boost = 0 if (
            type_key == "retirement"
            and include_faith_jobs
            and j.get("requires_faith_disclosure")
        ) else 1
        # G7 #20: 다중지능·에니어그램 cross-match score (음수로 내림차순)
        cross_score = -_cross_match_score(j, mi_top, enneagram_type)
        return (is_pref, faith_boost, verdict_rank[j["_verdict"]], cross_score)

    eligible.sort(key=sort_key)

    # SKILL.md: faith_disclosed=True surfaces faith jobs but does NOT monopolize.
    # Reserve at least 2 of 5 retirement slots for non-faith secular volunteering
    # so users see breadth, not a faith-only lineup.
    if type_key == "retirement" and include_faith_jobs:
        faith_jobs = [j for j in eligible if j.get("requires_faith_disclosure")]
        secular_jobs = [j for j in eligible if not j.get("requires_faith_disclosure")]
        faith_quota = min(3, len(faith_jobs))
        secular_quota = 5 - faith_quota
        selected = faith_jobs[:faith_quota] + secular_jobs[:secular_quota]
    else:
        selected = eligible[:5]
    warning = None
    aspirational_count = 0
    if len(selected) < 5:
        shortfall = 5 - len(selected)
        # G7 #17·#18·#19: aspirational 슬롯으로 우선 채우고, 그래도 부족하면 placeholder로
        # 카탈로그 데이터 fabrication 없이 *지망 직업*으로 의미 있는 추천 확보.
        aspirational.sort(key=lambda j: (
            # 학력 gap 작은 순 (가까운 목표 우선)
            -(education_rank(education) - education_rank(j.get("min_education", "high"))) if education and j.get("min_education") else 0,
            # 나이 미달 작은 순 (가까운 진입 시기 우선)
            (j.get("min_age", 0) or 0) - (age or 0) if age else 0,
        ))
        added_asp = 0
        for j in aspirational:
            if added_asp >= shortfall:
                break
            selected.append(_to_aspirational_slot(j, age, education))
            added_asp += 1
        aspirational_count = added_asp
        # aspirational로도 부족하면 placeholder
        still_short = 5 - len(selected)
        if still_short > 0:
            for i in range(still_short):
                selected.append(
                    _make_unfilled_slot(
                        index=len(selected) + 1,
                        type_key=type_key,
                        reason=(
                            f"나이 {age}·학력 {education} 조건에 직접 부합하거나 지망 가능한 {type_key} "
                            "카테고리 직업이 카탈로그 내에 부족합니다. "
                            "보완 경로(추가 교육·자격증·경력)를 통해 진입 가능한 미래 옵션으로만 안내하세요."
                        ),
                    )
                )
        if aspirational_count > 0 or still_short > 0:
            real_count = sum(1 for s in selected if not s.get("_is_placeholder") and not s.get("_is_aspirational"))
            warning = (
                f"실제 적합 {real_count}/5 + 지망(aspirational) {aspirational_count}/5"
                + (f" + 미달 placeholder {still_short}/5" if still_short else "")
                + f" — 사용자 조건(나이={age}, 학력={education}). 지망 슬롯은 *목표 직업*으로 안내."
            )
    return {
        "type": type_key,
        "slots": selected,
        "warning": warning,
        "aspirational_count": aspirational_count,
    }
