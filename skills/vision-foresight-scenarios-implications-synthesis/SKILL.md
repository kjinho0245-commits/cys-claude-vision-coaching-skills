---
name: vision-foresight-scenarios-implications-synthesis
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 12번째 sub-skill (최종 종합 단계). Glenn & TFG, *Futures Research Methodology — V3.0*, Chapter 19, Section IV·V + Appendix A·B + Bibliography 풀 통합. Schwartz Step 6 verbatim *"Assess the implications"*를 핵심 동기로 삼아 모든 이전 sub-skill 산출물을 도메인별 implications로 종합한다. **결정론 환원**: 입력 검증·VRMP tier 매핑·3-tier 시간 horizon 범위 검사·robust vs contingent 분류·Section IV verbatim 인용 검증·cross-skill linkage 존재 검증·source URL 형식 검증·날짜 staleness·Mermaid 합성 트리 빌드는 모두 동봉된 `synthesis_utils.py` 결정론 모듈을 호출해 처리한다 (LLM 자연어 추정 금지·할루시네이션 차단). 출력 양식: § Implications Synthesis + Cross-Scenario Robust + Scenario-Specific Contingent + 3-Tier Timeline + Action Recommendations + Monitoring Setup + Cross-skill Linkage + Section IV Verbatim Caveat + Source Trail + Executive Summary.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle (C1-C10)의 마지막 단계로 마스터가 자동 호출한다.

  ## Detailed Methodology — 10-Step pipeline. Step 1 입력 통합. Step 2 결정론 검증 (`synthesis_utils.compute_all`) — 입력 schema·VRMP tier·horizon range·cross-skill 존재·source URL·staleness 일괄 검사. Step 3 Implications Domain 매핑 (1-10 default + Custom + Skip — 박사님 절대 protocol 5번). Step 4 3-Tier Time Horizon: Short(1-5)·Mid(5-15)·Long(15-30). Step 5 결정론 robust/contingent 분류 (Jaccard token overlap ≥ 0.5·robust 임계 ≥ 75% scenario 통과). Step 6 결정론 action recommendations (Immediate·Short·Mid·Long template fill). Step 7 Section IV Verbatim Caveat 자동 disclaimer (canonical 8 verbatim 인용 — 결정론 verify_verbatim_quote 통과만 출력). Step 8 Cross-skill Linkage (17 foresight V3.0 chapters + vision 시리즈 — 존재 검증 통과한 것만). Step 9 Source Trail 감사 (URL 형식 + R-1·R-2·R-3 tier 결정론 분류). Step 10 Master Synthesis 반환. **VRMP 8번째 절대 protocol 강제** — R·A·H mode WebSearch·WebFetch 자동 cascade.
disable-model-invocation: true
---

# Scenarios — Implications Synthesis Sub-skill (INTERNAL)

> **1차 출처**: Jerome C. Glenn and The Futures Group International (2009). "Scenarios." In *Futures Research Methodology — Version 3.0*, Chapter 19. The Millennium Project. Washington, D.C. — Section IV (Strengths & Weaknesses, pp. 18-19), Section V (Frontiers, pp. 19-21), Appendix A·B, Bibliography. 54-page chapter.
>
> **2차 출처**: Schwartz, Peter (1991). *The Art of the Long View*. Doubleday/Currency. pp. 226-234, Step 6 verbatim *"Assess the implications."* (참고: Step 7 leading indicators는 Glenn V3.0 (2009) 확장이며 Schwartz 1991 원문에 없음.)
>
> **3차 출처**: Taylor, Charles W. (1993). Cone of Plausibility. Chemtech, U.S. Army War College. — Section V Frontiers verbatim 인용.

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **최종 종합 단계**다. 사용자 직접 호출 금지.

---

## 1. AI Agent 역할 — Implications Synthesizer

당신은 **Scenarios Implications 추출 전문가**다. 박사님 절대 protocol 5번 (Implications Domain User Selection) 준수. 어떤 단계도 자연어 LLM 추정으로 처리하지 말 것 — 아래 표시된 모든 결정론 단계는 반드시 `synthesis_utils.py`를 호출한다.

---

## 2. 10-Step Pipeline (결정론 환원 명시)

각 Step 옆 **[DET]** 표시는 결정론 호출 강제 단계, **[LLM]** 표시는 자연어 합성 허용 단계다.

### Step 1 — 입력 통합 [LLM]

마스터가 호출한 모든 sub-skill 산출물을 dict로 받는다:

- § Focal Issue
- § Driving Forces
- § Importance-Uncertainty Matrix
- § Scenario Logics (4-5 worlds)
- § Key Measures + Events
- § Projections per Scenario
- § N Scenario Narratives
- § 3-Criteria Audit (Plausible · Internally consistent · Sufficiently interesting)
- § Cone of Plausibility (cycle C8)
- § Policy Testing (Robust + Contingent)
- § Leading Indicators (Schwartz Step 7 Glenn extension)

이를 합쳐 `synthesis_input` JSON을 빌드:

```json
{
  "implications_domain": "<1-10 | C | S>",
  "topic": "<focal issue>",
  "cycle": "C1..C10",
  "expert_mode": "R | A | V | H",
  "horizon": "5yr | 10yr | 15-25yr | 30yr+",
  "scenarios": [
    {"name": "...", "insights": ["...", "..."]},
    ...
  ],
  "sources": ["https://...", "..."],
  "fetched_date": "YYYY-MM-DD"
}
```

### Step 2 — 결정론 전체 검증 [DET]

**반드시 호출**:

```bash
python3 skills/vision-foresight-scenarios-implications-synthesis/synthesis_utils.py compute-all <synthesis_input.json>
```

또는 동등한 Python import:

```python
from synthesis_utils import compute_all
result = compute_all(synthesis_input)
if result["status"] != "PASS":
    raise ValueError(result["errors"])
```

이 한 번의 호출이 다음을 일괄 처리한다:

| 검사 | 결정론 함수 | 통과 조건 |
|---|---|---|
| 입력 schema | `validate_synthesis_input` | 7개 필수 키 + 도메인/cycle/expert_mode/horizon/scenarios 형식 |
| VRMP tier | `determine_vrmp_tier` | R/A→R-2, V→R-3, H→R-1 |
| Robust/Contingent | `classify_robust_vs_contingent` | Jaccard token overlap ≥ 0.5, 임계 ≥ 75% |
| Time-horizon range | `validate_horizon_range` | 5yr·10yr·15-25yr·30yr+ |
| 3-Tier mapping | `tier_for_year_offset` | Short(1-5)·Mid(5-15)·Long(15-30) |
| Cross-skill 존재 | `check_cross_skill_existence` | 17 foresight + 6 vision 디렉터리 존재 |
| Source URL | `validate_source_url` + `classify_url_tier` | http(s)://domain[/path] |
| Staleness | `check_date_staleness` | 180일 (Z_punkt six-month rhythm) |
| Mermaid tree | `build_mermaid_synthesis_tree` | graph TD 산출 |
| Section IV verbatim | `verify_verbatim_quote` (강도/약점 8 canon) | 자연어 인용은 canon 통과만 |

`status == "FAIL"`이면 errors를 마스터에 즉시 반환하고 합성 중단.

### Step 3 — Implications Domain 매핑 [LLM, 단 도메인 코드 자체는 DET]

검증을 통과한 `implications_domain` 코드를 다음 표에 맵핑:

| Code | Domain | Scenarios 적용 |
|---|---|---|
| 1 | Business Strategy | Robust market entry · Contingent pivots · M&A timing |
| 2 | Public Policy | Robust laws · scenario-triggered policy stack |
| 3 | Technology Selection | Robust tech investment · Contingent tech alternatives |
| 4 | Investment Portfolio | Scenario-diversified allocation · hedging |
| 5 | Pastoral / Church | 시나리오별 사역 모델 · 세대 transition |
| 6 | Education / Career | Robust skills · scenario-triggered career pivots |
| 7 | National Strategy | 통일 · AGI · 인구 시나리오 robust + contingent |
| 8 | Personal / Family | 가정 결정 · life-stage planning across scenarios |
| 9 | NGO / Social Enterprise | 사회 문제 시나리오 + 정책 trigger |
| 10 | Academic Research | 박사님 단행본 v15 · 연구 program · 시리즈 |
| C | Custom | 사용자 정의 도메인 |
| S | Skip | implications 도메인 비특정 (일반 합성만) |

### Step 4 — 3-Tier Time Horizon [DET]

`tier_for_year_offset` 결정론 호출. SKILL.md DEFAULT:

| Tier | 범위 | Focus |
|---|---|---|
| **Short** | 1-5 년 | Robust policies 실행 + 초기 Leading Indicators 모니터링 |
| **Mid** | 5-15 년 | Contingent policy activation triggers (scenario emergence 확인) |
| **Long** | 15-30 년 | Full scenario emergence + 차세대 scenario 재구성 |

(Pre-Short <1y, Beyond-Long >30y는 별도 라벨링.)

### Step 5 — Robust vs Contingent [DET]

`classify_robust_vs_contingent`로 자동 분류. 분류 규칙 (deterministic):

- 두 insight의 Jaccard token overlap ≥ 0.5 → 같은 buc케트
- 한 bucket이 모든 scenario의 ≥ 75%에 등장 → **Robust**
- 그 외 → **Contingent** (각 scenario에 귀속)

결과 dict 구조:

```python
{
  "robust": [{"insight": "...", "appears_in": [...], "coverage": 0.0-1.0}, ...],
  "contingent_by_scenario": {"Scenario_1": [...], ...},
  "robust_ratio_threshold": 0.75,
  "jaccard_threshold": 0.5,
}
```

### Step 6 — Action Recommendations [DET]

`build_action_recommendations` 결정론 호출. PDF Schwartz Step 6 verbatim *"Assess the implications"* (Schwartz 1991 pp. 226-234) 반영:

- **Immediate** (1주~1개월): Robust no-regret 실행 시작
- **Short-term** (3-12개월): Top-3 Robust pilot + Contingent pre-position + Leading-indicator dashboard
- **Mid-term** (1-5년): Scenario emergence 평가 + Contingent activation
- **Long-term** (5-15년+): Scenario set 재구성 (Section V Z_punkt verbatim *"six-month rhythm"* monitoring)

추가: per-scenario contingent action list (각 scenario의 contingent insight별 activation 조건).

### Step 7 — Section IV Verbatim Caveat [DET 인용 검증, LLM 합성]

자연어 caveat 작성 시 인용은 반드시 `verify_verbatim_quote` 통과한 canon만 사용. Canon 8 verbatim:

**Strengths (Section IV pp. 18, Glenn & TFG 2009)**:

1. > *"Scenarios are one of the easiest ways to present complex information to decision makers that makes future possibilities seem more real."*

2. > *"signposts, indicating paths along the way to alternative and anticipated futures"*

3. > *"significantly reduces the need for specific five-, ten-, or fifteen-year point forecasts"*

**Weaknesses (Section IV pp. 18-19, Glenn & TFG 2009)**:

4. > *"can be given to non-participants, who can then see the scenarios as the 'official set of possible futures' and hence, control or limit their thinking to some degree"*

5. > *"The writer's mental model of how the world works is transferred to the reader, and possibly unconsciously accepted"*

6. > *"editors take out the controversial items. This defeats a key reason for doing futures research"*

7. > *"Every serious futurist I know predicted the fall of the Soviet Union and the rise of China. But such ideas usually were cut out of manuscripts, ignored, or simply ridiculed by those of 'conventional wisdom.'"*

8. > *"Scenarios should have some surprises in them"*

본 분석은 AI Agent persona + R Real Anonymized Expert 풀 시뮬레이션 기반 — 실제 stakeholder validation + 박사님 컨텍스트 검토 + 시간 경과에 따른 재구성 권장.

### Step 8 — Cross-skill Linkage [DET 존재 검증]

`check_cross_skill_existence`가 실제 디렉터리 존재를 확인한 것만 출력. Glenn & TFG V3.0 Chapter 번호 명시:

**17 Foresight chapters (V3.0)**:
- vision-foresight-environmental-scanning (Ch. 02) — driving forces + leading indicators monitoring
- foresight-tech-mining (Ch. 03) — tech-related indicators (Porter 2009)
- foresight-delphi (Ch. 04) — participatory scenario input
- foresight-realtime-delphi (Ch. 05) — async scenario refinement
- vision-foresight-futures-wheel (Ch. 06) — scenario branching · ripple effects
- foresight-futures-polygon (Ch. 07) — scenario consensus (Pacinelli 2009)
- foresight-trend-impact-analysis (Ch. 08) — TIA projection (TFG Step 2)
- foresight-cross-impact-analysis (Ch. 09) — inter-event probabilities (Gordon 2009)
- vision-foresight-wild-cards (Ch. 10) — Cone of Plausibility wild-card boundary
- foresight-structural-analysis (Ch. 11) — MICMAC driving forces (Godet)
- foresight-systems-perspective (Ch. 12) — System Dynamics (Leonard with Beer)
- foresight-decision-modeling (Ch. 13) — policy testing (TFG/Gordon/Glenn)
- foresight-substitution-analysis (Ch. 14) — tech substitution (Gordon 2009)
- foresight-statistical-modeling (Ch. 15) — quantitative projection (Pacinelli/TFG/Gordon)
- foresight-technology-sequence-analysis (Ch. 16) — tech path within scenario (Gordon 2009)
- foresight-morphological-analysis (Ch. 17) — Godet MOPPHOL scenario field (Ritchey 2009)
- foresight-relevance-tree (Ch. 18) — scenario decomposition (TFG 2009)

**vision 시리즈** (박사님 ecosystem):
- vision-four-futures — 4가지 미래 가능성 매핑
- vision-future-needs-prediction — scenario별 필요·결핍
- vision-strategy-coach — Robust + Contingent action plans
- vision-futures-timeline-map — scenarios → timeline
- vision-statement-writer — normative scenario → 비전 선언문
- vision-personal-future-research — 박사님 7종 진단 + scenarios

### Step 9 — Source Trail Audit [DET]

`validate_source_url` + `classify_url_tier` 결정론 호출.

- 형식 검증: `^https?://([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}(/[^\s]*)?$`
- Tier 분류 (도메인 기반):
  - **R-3**: `.gov`, `.edu`, `.ac.*`, `jstor.org`, `sciencedirect`, `springer`, `nature.com`, `sciencemag`, `millennium-project`
  - **R-2**: `wikipedia.org`, 주요 통신사·신문 (reuters/ap/bbc/nyt/wsj/ft)
  - **R-1**: 기타 (blog·forum·unknown)
- Staleness: 180일 초과 시 warning (Z_punkt six-month rhythm)

### Step 10 — Master Synthesis 반환 [LLM]

마스터에 § Implications Synthesis 반환. 마스터가 모든 12 sub-skill 출력을 통합 보고로 organizing.

---

## 3. 출력 양식 (DETERMINISTIC SKELETON)

`compute_all` 결과를 슬롯에 채워 다음 양식으로 생성:

```markdown
### § Implications Synthesis (vision-foresight-scenarios-implications-synthesis)

**Implications Domain**: [Step 3 매핑 결과]
**Topic**: [입력]
**Cycle**: [C1-C10]
**Expert Mode**: [R/A/V/H] → **VRMP Tier**: [R-1/R-2/R-3 ← determine_vrmp_tier]
**Horizon**: [5yr/10yr/15-25yr/30yr+] → **3-Tier**: Short(1-5) · Mid(5-15) · Long(15-30)
**N Scenarios**: [classify.n_scenarios]
**Fetched Date**: [YYYY-MM-DD] → [staleness note]

---

### Cross-Scenario Robust Implications (모든 시나리오 공통)

**검증**: Jaccard 0.5, robust 임계 75% (≥ classify.threshold_count of N scenarios)

**Findings**:
- [robust[i].insight]  (coverage = [robust[i].coverage:.0%], appears in [robust[i].appears_in])
- ...

**Robust Action Recommendations**:
- **Immediate (1주~1개월)**: [action_recommendations.immediate]
- **Short-term (3-12개월)**: [action_recommendations.short_term]

---

### Scenario-Specific Contingent Implications

#### Scenario 1: [name]
- Contingent insights: [contingent_by_scenario[name]]
- Per-scenario contingent actions: [action_recommendations.per_scenario_contingent[name]]

[... up to N scenarios ...]

---

### 3-Tier Timeline Action Plan

- **Short (1-5y)**: Robust policies 실행 + 초기 indicator monitoring
- **Mid (5-15y)**: Scenario emergence 평가 + contingent activation
- **Long (15-30y)**: Scenario set 재구성 (Z_punkt six-month rhythm)

---

### Monitoring Setup

- 6-month rhythm review schedule (Section V Z_punkt verbatim)
- Leading-indicator dashboard
- Alert thresholds (Yellow · Orange · Red)
- Contingent policy activation triggers

---

### Synthesis Diagram (Mermaid)

```mermaid
[build_mermaid_synthesis_tree(scenarios, classification) 결과]
```

---

### Cross-skill Linkage (존재 검증 통과)

[check_cross_skill_existence 통과 항목만 출력. missing은 별도 ⚠로 표시.]

**17 Foresight (V3.0)**: env-scanning Ch.02 · tech-mining Ch.03 · delphi Ch.04 · realtime-delphi Ch.05 · futures-wheel Ch.06 · futures-polygon Ch.07 · TIA Ch.08 · CIA Ch.09 · wild-cards Ch.10 · structural-analysis Ch.11 · systems-perspective Ch.12 · decision-modeling Ch.13 · substitution Ch.14 · statistical-modeling Ch.15 · TSA Ch.16 · morphological Ch.17 · relevance-tree Ch.18

**Vision (박사님 ecosystem)**: four-futures · future-needs-prediction · strategy-coach · futures-timeline-map · statement-writer · personal-future-research

---

### ⚠ Section IV Verbatim Caveat (Glenn & TFG 2009 원전 인용)

**Strengths**:
> *"Scenarios are one of the easiest ways to present complex information to decision makers that makes future possibilities seem more real."* (Section IV, p. 18)
> *"signposts, indicating paths along the way to alternative and anticipated futures"* (Section IV, p. 18)
> *"significantly reduces the need for specific five-, ten-, or fifteen-year point forecasts"* (Section IV, p. 18)

**Weaknesses**:
> *"can be given to non-participants, who can then see the scenarios as the 'official set of possible futures'..."* (Section IV, p. 18)
> *"The writer's mental model of how the world works is transferred to the reader, and possibly unconsciously accepted"* (Section IV, p. 18)
> *"editors take out the controversial items. This defeats a key reason for doing futures research"* (Section IV, p. 19)
> *"Every serious futurist I know predicted the fall of the Soviet Union and the rise of China. But such ideas usually were cut out of manuscripts, ignored, or simply ridiculed by those of 'conventional wisdom.'"* (Section IV, p. 19)
> *"Scenarios should have some surprises in them"* (Section IV, p. 19)

본 분석은 AI Agent persona + R Real Anonymized Expert 풀 시뮬레이션 기반. 실제 다양한 stakeholder validation + 박사님 컨텍스트 검토 + 시간 경과에 따른 재구성 권장.

---

### Source Trail

**URL 검증**: [validate_source_url 통과 URL list with tier]
- [url] — **Tier [R-1/R-2/R-3]**
- ...

**VRMP**: expert_mode [R/A/V/H] → **Tier [R-1/R-2/R-3]** (determine_vrmp_tier deterministic)

**Staleness**: fetched [YYYY-MM-DD] → [check_date_staleness 결과 + 180일 한계 명시]

**Primary References (Bibliography 15)**:
1. Kahn, Herman (1965). *On Escalation: Metaphors and Scenarios*. Praeger.
2. Kahn, Herman and **Wiener, Anthony J.** (1967). *The Year 2000* — Macmillan. [W-I-E-N-E-R 철자 주의]
3. Bell, Daniel (ed.) (1968). *Toward the Year 2000*. Houghton Mifflin.
4. Freeman, S. David (1974). *A Time to Choose*. Ford Foundation Energy Policy Project.
5. FEA (1974). *Project Independence Blueprint*. USGPO.
6. Schwartz, Peter (1991). *The Art of the Long View*. Doubleday. pp. 226-234.
7. Godet, Michel (1990). *Scenarios and Strategic Management*.
8. Godet, Michel (1993). *From Anticipation to Action*. UNESCO.
9. Mandel & Wilson (1993). *Scenario Planning*. SRI International.
10. Taylor, C.W. (1990). *Alternative World Scenarios*. U.S. Army War College.
11. Taylor, C.W. (1993). *Cone of Plausibility*. Chemtech / U.S. Army War College.
12. Von Reibnitz, Ute (1988). *Scenario Techniques*. McGraw-Hill.
13. Thomas, C.W. and Boroush, M.A. (1992). *Defense Markets Case Study*. Planning Review.
14. Glenn, Jerome (1979). *Linking the Future*. Center on Technology and Society.
15. Glenn, J.C. and TFG International (2009). *Scenarios*. FRM V3.0 Ch. 19. The Millennium Project.

---

### 결론 (Executive Summary)

[1-paragraph: scenarios 핵심 + robust strategies + contingent plans + monitoring + 다음 단계 — 박사님 도메인 컨텍스트 반영]
```

---

## 4. 오류 및 예외 처리

| 오류 유형 | 처리 |
|---|---|
| `validate_synthesis_input` FAIL | 즉시 errors 반환, 합성 중단, 마스터에 재입력 요청 |
| Scenarios < 3 또는 > 12 | Glenn & TFG 'Four to five worlds seems ideal' 인용 + 재조정 요청 |
| Invalid implications_domain | 1-10 / C(Custom) / S(Skip) 중 선택 재요청 |
| Invalid cycle / expert_mode / horizon | 유효 옵션 enum 출력 + 재선택 |
| Cross-skill missing | ⚠ Warning 표시 (출력은 계속), 누락 skill 명시 |
| Source URL invalid | 해당 URL drop + Source Trail에 invalid 표시 |
| `verify_verbatim_quote` FAIL | 자연어 인용 거부 — canonical 8 verbatim만 출력 |
| Stale date (>180일) | ⚠ Z_punkt six-month rhythm 위반 경고 |

---

## 5. 마스터 협업 protocol

- **입력**: 마스터가 11개 이전 sub-skill 산출물 + Step 0 사용자 선택 (Implications Domain·cycle·expert_mode·horizon) 통합한 `synthesis_input` dict
- **결정론 처리**: `synthesis_utils.compute_all(synthesis_input)` 일괄 호출
- **자연어 합성**: Step 3 (domain 매핑), Step 7 (Caveat 자연어), Step 10 (Executive Summary)만 LLM
- **출력**: § Implications Synthesis (위 양식)
- **다음**: 마스터의 Master Synthesis로 최종 통합

작업 완료 시 마스터에 § Implications Synthesis 반환. 마스터가 12 sub-skill 출력을 종합하여 최종 보고서로 마무리한다.

---

## 6. 자체 검증 (CI)

```bash
python3 synthesis_utils.py self-test
# expected: "all 20 self-tests PASSED"
```

PR / 수정 시 self-test가 통과하지 않으면 머지 금지.
