#!/usr/bin/env python3
"""
10개의 새로운 검증 프롬프트 — 이전 검증과 전혀 다른 도메인·cycle·expert mode·horizon 조합.
스킬 hardcoded 패턴 학습 우회용. 박사님 지시 조건 #4 준수.

검증 기준
---------
1) 할루시네이션 전혀 없을 것 — 모든 결정론 단계 PASS
2) 원문(Glenn & TFG V3.0 Ch.19) verbatim과 일치 — verify_verbatim_quote 통과
3) 추가 오류·미구현·약점 발견되지 않을 것 — assertion 통과
4) 이전 검증 프롬프트와 전혀 다른 입력
"""

import json
import sys
from synthesis_utils import compute_all, verify_verbatim_quote, validate_synthesis_input


TEST_PROMPTS = [
    # P1 — 한국 인구절벽 시나리오 (도메인 7 National Strategy, cycle C8 Cone of Plausibility, expert V, 30yr+)
    {
        "id": "P1",
        "description": "한국 인구절벽 2055 시나리오 — Cone of Plausibility 30년+",
        "input": {
            "implications_domain": "7",
            "topic": "한국 인구절벽과 사회구조 2055",
            "cycle": "C8",
            "expert_mode": "V",
            "horizon": "30yr+",
            "fetched_date": "2026-05-15",
            "sources": [
                "https://kostat.go.kr/portal/korea/index.action",
                "https://www.millennium-project.org/projects/",
                "https://en.wikipedia.org/wiki/Demographics_of_South_Korea",
            ],
            "scenarios": [
                {
                    "name": "급격한 축소",
                    "insights": [
                        "지방 소멸 가속화 80% 시군구",
                        "노동력 부족 GDP 위협",
                        "AI 자동화 적극 도입",
                    ],
                },
                {
                    "name": "이민 통합",
                    "insights": [
                        "외국인 인구 비중 25%",
                        "노동력 부족 GDP 위협",
                        "AI 자동화 적극 도입",
                        "다문화 정책 패러다임 전환",
                    ],
                },
                {
                    "name": "디지털 전환",
                    "insights": [
                        "원격 근무 보편화",
                        "노동력 부족 GDP 위협",
                        "AI 자동화 적극 도입",
                        "산업 구조 서비스 중심 재편",
                    ],
                },
                {
                    "name": "출산률 회복",
                    "insights": [
                        "출산장려금 GDP 5% 투입",
                        "주거 비용 안정화",
                        "AI 자동화 적극 도입",
                    ],
                },
            ],
        },
        "expectations": {
            "vrmp_tier": "R-3",
            "robust_min": 1,  # "AI 자동화 적극 도입"이 4/4
        },
    },

    # P2 — 비즈니스 전략 (도메인 1, cycle C2 Schwartz GBN, expert R, 10yr)
    {
        "id": "P2",
        "description": "K-콘텐츠 글로벌 확장 10년 시나리오 — Schwartz GBN",
        "input": {
            "implications_domain": "1",
            "topic": "K-콘텐츠 글로벌 시장 점유율 2036",
            "cycle": "C2",
            "expert_mode": "R",
            "horizon": "10yr",
            "fetched_date": "2026-05-15",
            "sources": [
                "https://www.reuters.com/lifestyle/entertainment/",
                "https://www.kocca.kr/",
            ],
            "scenarios": [
                {
                    "name": "스트리밍 패권",
                    "insights": [
                        "Netflix·Disney+ 한국 IP 독점 입찰",
                        "글로벌 시청자 확대",
                        "지식재산권 분쟁 증가",
                    ],
                },
                {
                    "name": "플랫폼 다변화",
                    "insights": [
                        "글로벌 시청자 확대",
                        "지식재산권 분쟁 증가",
                        "독립 플랫폼 부상",
                    ],
                },
                {
                    "name": "AI 콘텐츠 침투",
                    "insights": [
                        "글로벌 시청자 확대",
                        "AI 생성 콘텐츠 보편화",
                        "지식재산권 분쟁 증가",
                    ],
                },
                {
                    "name": "지역 시장 강세",
                    "insights": [
                        "글로벌 시청자 확대",
                        "동남아·인도 시장 부상",
                        "지식재산권 분쟁 증가",
                    ],
                },
            ],
        },
        "expectations": {
            "vrmp_tier": "R-2",
            "robust_min": 2,  # 글로벌 시청자 확대 + IP 분쟁
        },
    },

    # P3 — 교육 / 진로 (도메인 6, cycle C5 Von Reibnitz, expert A, 15-25yr)
    {
        "id": "P3",
        "description": "고등교육 AGI 시대 적응 시나리오 — Von Reibnitz 6-step",
        "input": {
            "implications_domain": "6",
            "topic": "한국 고등교육 시스템 AGI 적응 2046",
            "cycle": "C5",
            "expert_mode": "A",
            "horizon": "15-25yr",
            "fetched_date": "2026-05-10",
            "sources": [
                "https://www.moe.go.kr/",
                "https://www.oecd.org/education/",
            ],
            "scenarios": [
                {"name": "AGI 통합", "insights": ["커리큘럼 전면 재설계", "교수 역할 코치化", "평생교육 보편화"]},
                {"name": "대학 분화", "insights": ["연구중심·실무중심 양극화", "평생교육 보편화", "교수 역할 코치化"]},
                {"name": "마이크로 자격", "insights": ["나노 디그리 확산", "평생교육 보편화", "교수 역할 코치化"]},
                {"name": "AI 회의주의", "insights": ["전통 학위 회귀", "휴머니티 교과 강세", "평생교육 보편화"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-2", "robust_min": 1},
    },

    # P4 — 목회·교회 (도메인 5, cycle C6 Millennium Participatory, expert H, 5yr)
    {
        "id": "P4",
        "description": "한국 디아스포라 한인교회 5년 시나리오 — Millennium Participatory",
        "input": {
            "implications_domain": "5",
            "topic": "북미·유럽 한인 디아스포라 교회 5년 사역 변화",
            "cycle": "C6",
            "expert_mode": "H",
            "horizon": "5yr",
            "fetched_date": "2026-05-12",
            "sources": ["https://www.christianitytoday.com/", "https://www.barna.com/"],
            "scenarios": [
                {"name": "세대 교체", "insights": ["1.5/2세대 리더십", "온라인 예배 정착", "다언어 사역 확대"]},
                {"name": "재정 위기", "insights": ["헌금 30% 감소", "온라인 예배 정착", "교회 통폐합"]},
                {"name": "사회참여 강화", "insights": ["지역사회 봉사 확장", "온라인 예배 정착", "다언어 사역 확대"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-1", "robust_min": 1},
    },

    # P5 — 투자 포트폴리오 (도메인 4, cycle C3 Coates-Jarratt, expert V, 5yr)
    {
        "id": "P5",
        "description": "글로벌 ESG 투자 5년 시나리오 — Coates-Jarratt",
        "input": {
            "implications_domain": "4",
            "topic": "글로벌 ESG 투자 자본 흐름 2031",
            "cycle": "C3",
            "expert_mode": "V",
            "horizon": "5yr",
            "fetched_date": "2026-05-15",
            "sources": [
                "https://www.sciencedirect.com/journal/journal-of-cleaner-production",
                "https://www.bloomberg.com/markets/esg",
            ],
            "scenarios": [
                {"name": "ESG 주류화", "insights": ["연기금 ESG 의무 편입", "그린본드 시장 5배 확대", "데이터 표준 통일"]},
                {"name": "ESG 백래시", "insights": ["미국 정치 분극화", "연기금 ESG 의무 편입", "ESG 펀드 환매 증가"]},
                {"name": "기후 위기 가속", "insights": ["탄소세 글로벌 확산", "데이터 표준 통일", "연기금 ESG 의무 편입"]},
                {"name": "기술 돌파", "insights": ["수소·배터리 혁신", "데이터 표준 통일", "연기금 ESG 의무 편입"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-3", "robust_min": 1},
    },

    # P6 — Custom Domain, cycle C9 Hybrid, expert R, 15-25yr
    {
        "id": "P6",
        "description": "도시 모빌리티 Custom 도메인 — Hybrid TFG+Schwartz",
        "input": {
            "implications_domain": "Custom",
            "topic": "서울 도시 모빌리티 2045",
            "cycle": "C9",
            "expert_mode": "R",
            "horizon": "15-25yr",
            "fetched_date": "2026-05-14",
            "sources": [
                "https://www.seoul.go.kr/",
                "https://www.itf-oecd.org/",
            ],
            "scenarios": [
                {"name": "자율주행 보편화", "insights": ["AV 대중교통 통합", "도로 인프라 재설계", "택시 산업 재편"]},
                {"name": "공유 모빌리티", "insights": ["MaaS 플랫폼 통합", "AV 대중교통 통합", "주차장 축소"]},
                {"name": "지하·공중 분리", "insights": ["UAM 상용화", "AV 대중교통 통합", "도시 3차원 재설계"]},
                {"name": "근거리 자족", "insights": ["15분 도시 확산", "AV 대중교통 통합", "보행·자전거 우선"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-2", "robust_min": 1},
    },

    # P7 — Skip Domain, cycle C7 Bishop Workshop, expert R, 10yr
    {
        "id": "P7",
        "description": "Skip 도메인 — Bishop Workshop 추상 시나리오",
        "input": {
            "implications_domain": "Skip",
            "topic": "양자컴퓨팅 상용화 일반 시나리오 2036",
            "cycle": "C7",
            "expert_mode": "R",
            "horizon": "10yr",
            "fetched_date": "2026-05-14",
            "sources": ["https://www.nature.com/subjects/quantum-computing"],
            "scenarios": [
                {"name": "QC 돌파", "insights": ["오류 정정 완성", "암호 체계 재편", "신약 개발 가속"]},
                {"name": "QC 지연", "insights": ["고전 컴퓨터 우위 지속", "암호 체계 재편", "투자 거품 붕괴"]},
                {"name": "QC 양극화", "insights": ["미·중 디커플링", "암호 체계 재편", "기술 수출 통제"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-2", "robust_min": 1},
    },

    # P8 — NGO 도메인 (9), C10 Full Pipeline, expert V, 30yr+
    {
        "id": "P8",
        "description": "글로벌 식량안보 NGO 시나리오 — Full Pipeline C10",
        "input": {
            "implications_domain": "9",
            "topic": "글로벌 식량안보와 NGO 역할 2060",
            "cycle": "C10",
            "expert_mode": "V",
            "horizon": "30yr+",
            "fetched_date": "2026-05-13",
            "sources": [
                "https://www.fao.org/state-of-food-security-nutrition",
                "https://www.springer.com/journal/12571",
                "https://www.un.org/sustainabledevelopment/hunger/",
            ],
            "scenarios": [
                {"name": "기후 적응 성공", "insights": ["가뭄 저항 작물 확산", "정밀농업 글로벌 보급", "공급망 디지털화"]},
                {"name": "식량 위기", "insights": ["곡물 가격 3배 상승", "공급망 디지털화", "난민 1억 명"]},
                {"name": "단백질 전환", "insights": ["대체육 가격 경쟁력", "공급망 디지털화", "축산업 축소"]},
                {"name": "지역 자립", "insights": ["수직 농장 도시 보급", "공급망 디지털화", "수입 의존 감소"]},
                {"name": "디지털 통제", "insights": ["블록체인 농산물 추적", "공급망 디지털화", "농민 디지털 격차"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-3", "robust_min": 1},
    },

    # P9 — 개인·가정 도메인 (8), C1 TFG 3-step, expert A, 15-25yr
    {
        "id": "P9",
        "description": "박사님 가정 자녀 진로 시나리오 — TFG 3-step",
        "input": {
            "implications_domain": "8",
            "topic": "AGI 시대 자녀 진로 형성 2046",
            "cycle": "C1",
            "expert_mode": "A",
            "horizon": "15-25yr",
            "fetched_date": "2026-05-10",
            "sources": [
                "https://www.brookings.edu/topic/future-of-work/",
                "https://hbr.org/topic/subject/future-of-work",
            ],
            "scenarios": [
                {"name": "AGI 동반성장", "insights": ["인간-AI 협력 직군", "평생학습 필수", "다중 커리어 보편"]},
                {"name": "AGI 대체 가속", "insights": ["전통 직업 50% 자동화", "평생학습 필수", "기본소득 도입 논의"]},
                {"name": "AGI 규제 강화", "insights": ["AI 사용 제한", "평생학습 필수", "전통 전문직 회귀"]},
                {"name": "휴머니티 우선", "insights": ["창의·돌봄·예술 강세", "평생학습 필수", "공동체 가치 부상"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-2", "robust_min": 1},
    },

    # P10 — 학술 연구 도메인 (10), C4 Godet MOPPHOL, expert R, 15-25yr
    {
        "id": "P10",
        "description": "박사님 미래학 단행본 v15 시나리오 — Godet MOPPHOL",
        "input": {
            "implications_domain": "10",
            "topic": "한국 미래학 학문 정립과 박사님 단행본 v15",
            "cycle": "C4",
            "expert_mode": "R",
            "horizon": "15-25yr",
            "fetched_date": "2026-05-08",
            "sources": [
                "https://www.millennium-project.org/",
                "https://www.wfsf.org/",
                "https://onlinelibrary.wiley.com/journal/14685248",
            ],
            "scenarios": [
                {"name": "미래학 제도화", "insights": ["대학 학위 과정 신설", "정부 미래전략실 상설화", "전문가 풀 1000명"]},
                {"name": "미래학 분산", "insights": ["기업 컨설팅 시장 성장", "전문가 풀 1000명", "공공·민간 협업"]},
                {"name": "미래학 융합", "insights": ["AI·신경과학 융합", "전문가 풀 1000명", "방법론 자동화"]},
                {"name": "미래학 회의론", "insights": ["검증 위기", "전문가 풀 1000명", "방법론 재정립 요구"]},
            ],
        },
        "expectations": {"vrmp_tier": "R-2", "robust_min": 1},
    },
]


def run_all():
    """10개 프롬프트 모두 실행. 100% 통과 시 0 반환."""
    passed = 0
    failed = []
    for tp in TEST_PROMPTS:
        print(f"\n──── {tp['id']}: {tp['description']} ────")
        result = compute_all(tp["input"])
        if result["status"] != "PASS":
            failed.append((tp["id"], result.get("errors", [])))
            print(f"✗ FAIL: {result.get('errors')}")
            continue

        # Expectations 점검
        exp = tp.get("expectations", {})
        if "vrmp_tier" in exp:
            if result["vrmp_tier"] != exp["vrmp_tier"]:
                failed.append((tp["id"], [f"VRMP tier mismatch: expected {exp['vrmp_tier']}, got {result['vrmp_tier']}"]))
                print(f"✗ FAIL: VRMP tier {result['vrmp_tier']} ≠ {exp['vrmp_tier']}")
                continue

        if "robust_min" in exp:
            n_robust = len(result["classification"]["robust"])
            if n_robust < exp["robust_min"]:
                failed.append((tp["id"], [f"robust insights {n_robust} < {exp['robust_min']}"]))
                print(f"✗ FAIL: robust {n_robust} < {exp['robust_min']}")
                continue

        # Source URL 검증 — 모두 유효해야
        for ua in result["url_audit"]:
            if not ua.get("valid"):
                failed.append((tp["id"], [f"invalid URL: {ua}"]))
                print(f"✗ FAIL: invalid URL {ua}")
                break
        else:
            # Mermaid 산출
            assert result["mermaid_synthesis_tree"].startswith("graph TD")
            # 17 foresight 모두 존재
            cs = result["cross_skill_linkage"]
            missing_fs = [k for k, v in cs["foresight"].items() if not v["exists"]]
            if missing_fs:
                failed.append((tp["id"], [f"missing foresight skills: {missing_fs}"]))
                print(f"✗ FAIL: missing foresight: {missing_fs}")
                continue
            # Verbatim canon — 통과해야 할 strength 1개·weakness 1개 검증
            ok_strength = verify_verbatim_quote(
                "Scenarios are one of the easiest ways to present complex information to "
                "decision makers that makes future possibilities seem more real."
            )
            ok_weakness = verify_verbatim_quote(
                "editors take out the controversial items. This defeats a key reason for "
                "doing futures research"
            )
            assert ok_strength["verified"] and ok_strength["tier"] == "strength"
            assert ok_weakness["verified"] and ok_weakness["tier"] == "weakness"

            # Staleness 정상
            assert result["date_staleness"]["is_stale"] is False, \
                f"staleness on fresh fetched_date: {result['date_staleness']}"

            passed += 1
            print(
                f"✓ PASS — VRMP={result['vrmp_tier']}, "
                f"robust={len(result['classification']['robust'])}, "
                f"contingent={sum(len(v) for v in result['classification']['contingent_by_scenario'].values())}, "
                f"urls={len(result['url_audit'])}, "
                f"mermaid={len(result['mermaid_synthesis_tree'].splitlines())}lines"
            )

    print(f"\n══════════════════════════════════════════")
    print(f"RESULT: {passed}/{len(TEST_PROMPTS)} PASS")
    if failed:
        print("FAILURES:")
        for tid, errs in failed:
            print(f"  [{tid}] {errs}")
        return 1
    print("100% PASS — 모든 10개 프롬프트 결정론 검증 통과")
    return 0


if __name__ == "__main__":
    sys.exit(run_all())
