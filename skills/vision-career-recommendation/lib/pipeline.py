"""End-to-end deterministic pipeline.

Inputs (UserProfile) → Filtered candidates → 20-slot plan → Dedup → Validation.

LLM only consumes the structured plan to write rationales + 1000+ char coaching.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

from .catalog import TYPE_KEYS, normalize_education, get_age_category
from .dedup import assert_no_duplicates, resolve_duplicates
from .filter_jobs import select_top5
from .language import detect_language


@dataclass
class UserProfile:
    age: Optional[int] = None
    education: Optional[str] = None  # raw or normalized
    mbti: Optional[str] = None
    enneagram: Optional[str] = None
    riasec: Optional[str] = None
    multiple_intel: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    current_job: Optional[str] = None
    location: Optional[str] = None
    faith_disclosed: bool = False
    raw_input: str = ""


def build_plan(profile: UserProfile) -> Dict:
    edu_norm = normalize_education(profile.education) if profile.education else None
    age_cat = get_age_category(profile.age) if profile.age is not None else None

    # G7 #20: 다중지능·에니어그램 cross-match weighting을 select_top5에 전달
    mi_top = profile.multiple_intel[:3] if profile.multiple_intel else None
    plan = {}
    for t in TYPE_KEYS:
        plan[t] = select_top5(
            type_key=t,
            age=profile.age,
            education=edu_norm,
            include_faith_jobs=profile.faith_disclosed,
            mi_top=mi_top,
            enneagram_type=profile.enneagram,
        )

    plan = resolve_duplicates(
        plan,
        age=profile.age,
        education=edu_norm,
        include_faith_jobs=profile.faith_disclosed,
    )

    dup_issues = assert_no_duplicates(plan)
    meta = {
        "language": detect_language(profile.raw_input or ""),
        "age_category": age_cat,
        "education_normalized": edu_norm,
        "faith_disclosed": profile.faith_disclosed,
        "dup_issues_after_resolve": dup_issues,
        "input_categories": _summarize_input(profile),
    }
    return {"plan": plan, "meta": meta}


def _summarize_input(profile: UserProfile) -> Dict:
    return {
        "mbti": profile.mbti,
        "enneagram": profile.enneagram,
        "riasec": profile.riasec,
        "multiple_intel": profile.multiple_intel,
        "values": profile.values,
        "interests": profile.interests,
        "current_job": profile.current_job,
        "location": profile.location,
    }


CLI_HELP = """vision-career-recommendation 결정론 파이프라인

UserProfile JSON을 입력받아 4유형 × 5슬롯 = 20개 직업 추천 plan을 산출.

사용:
  python3 scripts/run_pipeline.py <profile.json>     # 파일 입력
  python3 scripts/run_pipeline.py -                  # stdin 입력
  python3 scripts/run_pipeline.py --stdin            # stdin 입력 (동등)
  cat profile.json | python3 scripts/run_pipeline.py # stdin 파이프
  python3 scripts/run_pipeline.py --help             # 본 도움말

UserProfile 스키마 (모두 선택, 빠지면 null/기본값):
  age (int)              : 만 나이 — 최우선 필터
  education (str)        : 중졸이하/고졸/전문대/대졸/석사/박사
  mbti (str)             : 4글자 (예: INFJ)
  enneagram (str)        : Type 1~9
  riasec (str)           : 트라이코드 (예: IRS)
  multiple_intel (list)  : 상위 3개 지능 이름
  values (list)          : 가치 단어 5~10개
  interests (list)       : 관심 분야 자유 기술
  current_job (str)      : 진로 전환자에 필수
  location (str)         : "한국"/"해외"
  faith_disclosed (bool) : true면 Type 3 종교 봉사 직업 활성화
  raw_input (str)        : 원본 사용자 텍스트 (언어 감지용)

출력: {"plan": {...}, "meta": {...}} JSON.
"""


def cli_main(argv: List[str]) -> int:
    """CLI entry: read JSON profile from stdin or first arg, print plan as JSON.

    #16: argparse 도입 — --help·-h 지원·인자 의미 명시.
    """
    # 도움말 분기 (argparse 풀세팅 대신 경량 분기 — JSON 파이프 호환 우선)
    if len(argv) > 1 and argv[1] in {"-h", "--help", "help"}:
        sys.stdout.write(CLI_HELP)
        return 0

    if len(argv) > 1 and argv[1] not in {"-", "--stdin"}:
        try:
            with open(argv[1], "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            sys.stderr.write(f"ERROR: File not found: {argv[1]}\n")
            sys.stderr.write("Use --help for usage. Use '-' or '--stdin' to read from stdin.\n")
            return 2
        except json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: Invalid JSON in {argv[1]}: {e}\n")
            return 2
    else:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: Invalid JSON from stdin: {e}\n")
            return 2

    prof = UserProfile(
        age=data.get("age"),
        education=data.get("education"),
        mbti=data.get("mbti"),
        enneagram=data.get("enneagram"),
        riasec=data.get("riasec"),
        multiple_intel=data.get("multiple_intel", []),
        values=data.get("values", []),
        interests=data.get("interests", []),
        current_job=data.get("current_job"),
        location=data.get("location"),
        faith_disclosed=bool(data.get("faith_disclosed", False)),
        raw_input=data.get("raw_input", ""),
    )
    result = build_plan(prof)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(cli_main(sys.argv))
