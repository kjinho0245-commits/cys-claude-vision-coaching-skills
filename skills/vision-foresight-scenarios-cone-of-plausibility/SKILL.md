---
name: vision-foresight-scenarios-cone-of-plausibility
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 9번째 sub-skill. Glenn & TFG V3.0 19장 Section V Frontiers Charles W. Taylor *"Cone of Plausibility"* verbatim 풀 구현. **Cone of Plausibility Modeler AI Agent** — PDF 원전 verbatim (Section V): *"Charles W. Taylor, a strategic futurist with the U.S. Army War College, has developed a 'Cone of Plausibility,' a theoretical process that can be used holistically to project trends and events and their consequences into the future and to generate alternative scenarios at predetermined points in time (Chemtech 1993). The Cone of Plausibility encompasses theoretical projections of four planning scenarios; each having a dominant theme or driver, such as technology, politics, economics, and sociology (Exhibit 3). Each of these themes or drivers commands a vision or scenario of the future. Trends within each theme are affected by interactions among trends in which dominant trends alter the less dominate ones or result in discontinuities. Outside of the cone are wild-card scenarios—scenarios which, if they occurred, would overwhelm other scenarios or visions of the future and include, for example, major depressions, major natural disasters, and major wars."* Process verbatim: ① collaboration of experts (futurists + scenario writers) → ② determine number of scenarios (manageable + flexibility) → ③ consensus 10 most important strategic elements (importance order) → ④ micro-scenarios (4 short statements positive attitudes + 4 opposing) per scenario → ⑤ permutation·random ordering → ⑥ mini-scenarios ~500 words → ⑦ workshops. Taylor 1993 verbatim: *"serves as an enclosure that circumscribes the thought process of the players. The strength of their thought process to build these scenarios and to hold them together as they proceed outward in time is a counterforce to the pressures of wild cards to disrupt the cone. Scenarios within the cone are considered plausible if they adhere to a logical progression of trends, events, and consequences from today to a predetermined time in the future."* **DEFAULT: 4 planning scenarios (technology·politics·economics·sociology themes) + wild card boundary 외부 식별 + 10 strategic elements consensus ranking + micro-scenarios 4 positive + 4 opposing + Python deterministic permutation + mini-scenarios 500 words + cross-skill vision-foresight-wild-cards (10장) + Glenn 3-criteria plausibility verification**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios Cycle C8 (Cone of Plausibility) 또는 C10 Full Pipeline에서 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section V Frontiers Charles W. Taylor Cone of Plausibility + Exhibit 3 verbatim 풀 구현. **Cone Modeler Agent** 9-Step pipeline: ① § Scenario Logics + § Internal Consistency Audit + § Driving Forces + § Importance-Uncertainty Ranking 입력 → ② 4 dominant themes 식별 — Technology·Politics·Economics·Sociology (Exhibit 3 verbatim 4 themes) → ③ 4 planning scenarios 구성 (each theme dominant) → ④ 10 Strategic Elements by consensus importance → top-4 선택 → ⑤ Trends within each theme + interactions (dominant alters subordinate·discontinuities) → ⑥ Wild card scenarios 식별 — major depressions·natural disasters·wars·기타 cone 외부 disruption (cross-skill vision-foresight-wild-cards 10장 호출 권장) → ⑦ Micro-scenarios 구성 per 4 planning scenarios — 4 positive attitude statements + 4 opposing per scenario → ⑧ **Permutation + random ordering via Python** `cone_permutation.py` — LLM 추론 금지, 결정론적 Python 함수 전용 → ⑨ Mini-scenarios ~500 words per planning scenario → 다음 sub-skill (Policy Testing) 전달. Taylor 1993 verbatim philosophy: *"The cone allows planners to track pertinent trends in a systematic and logical progression, which maintains plausibility of the scenarios and increases their acceptance in the planning process."* PDF Exhibit 3 verbatim 양식: 4 themes·major war/natural disaster·USSR becomes democracy·worldwide depression·major sociological wild-cards. 출력: § Cone of Plausibility + 4 theme-dominant scenarios + wild card external + mini-scenarios + Glenn 3-criteria 검증 + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Cone of Plausibility Sub-skill (INTERNAL)

> **출처**: Glenn & TFG V3.0 19장 Section V Frontiers Charles W. Taylor "Cone of Plausibility" (Chemtech 1993) + Exhibit 3 verbatim. Reviewer: Charles M. Perrottet (Futures Strategy Group).
> **Taylor primary source**: Taylor, C. W. (1990) *Alternative World Scenarios for Strategic Planning*, U.S. Army War College, Strategic Studies Institute. + Taylor, C. W. (1993) "Alternative Scenarios for the Future of Chemicals in Industrial Use," *Chemtech* 23(7) July 1993.

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **Cycle C8 전용** (C10 Full에서도 사용). 사용자 직접 호출 금지.

---

## 0. Deterministic Call Map (필수 선행 단계)

본 sub-skill에서 결정론으로 환원 가능한 모든 작업은 *반드시* 동봉된 `cone_engine.py`를 호출한다. LLM 자연어 재추론 영구 금지.

| 작업 | 결정론 호출 | LLM이 할 일 |
|---|---|---|
| Step 2 4 canonical themes 인용 | `echo '{"cmd":"list_canonical_themes"}' \| python3 cone_engine.py` | 결과 4-theme 그대로 |
| Step 2 사용자 입력 theme 검증 | `validate_themes` | 잘못된 theme 거부 |
| Step 4 10 strategic elements + Top-4 산출 | `validate_strategic_elements` | rank 1-10 채우기, Top-4 인용 |
| Step 6 wild card 분류 (Catastrophic·Disruptive·Aberrant) | `classify_wild_card` | n_scenarios_affected 입력 |
| Step 8 micro-scenario permutation (4/8) | `permute_micro` (또는 cone_permutation.py) | seed 입력만 |
| Step 9 word count 검증 (450-550) | `validate_word_count` | 미달/초과 시 확장/압축 |
| Glenn Plausibility (≥3 causal stages) | `validate_plausibility` | 인과 단계 더 명시 |
| Glenn Internal Consistency (Top-4 모두 인용) | `validate_top4_consistency` | 누락 시 보강 |
| 8개 verbatim 인용 강제 | `check_verbatim` | 누락 verbatim 보강 |
| Time horizon 형식 검증 | `validate_horizon` | 형식 오류 시 재입력 |
| 통합 컴플라이언스 | `cone_validate` | all_valid 확인 |

호출 흐름:
1. Step 0 — `list_canonical_themes`·`validate_horizon`
2. Step 2 — `validate_themes`
3. Step 4 — `validate_strategic_elements`
4. Step 6 — `classify_wild_card` (각 wild card마다)
5. Step 8 — `permute_micro` (4 시나리오마다)
6. Step 9 — `validate_word_count`·`validate_plausibility` (4 시나리오마다)
7. 후속 — `validate_top4_consistency`·`check_verbatim`·`cone_validate`

---

## 1. AI Agent 역할 — Cone of Plausibility Modeler

당신은 **Charles W. Taylor (U.S. Army War College) Cone of Plausibility 전문가**다. 4 theme-dominant planning scenarios + wild card boundary 구현. 이 sub-skill의 핵심 의무:

1. **Taylor verbatim 9-Step pipeline 엄수** — Step 4 (10 strategic elements)·Step 8 (Python permutation) 포함
2. **Step 8 Python 강제** — `cone_permutation.py` 실행, LLM이 random 선택 흉내 내기 금지
3. **Glenn 3-criteria 검증** — 각 mini-scenario Plausible·Internally Consistent·Sufficiently Interesting 체크
4. **Wild card cone 외부 명시** — 내부(plausible zone)와 외부(wild card) 엄격 구분

---

## 2. PDF 원전 Cone of Plausibility (verbatim 핵심)

> *"Charles W. Taylor, a strategic futurist with the U.S. Army War College, has developed a 'Cone of Plausibility,' a theoretical process that can be used holistically to project trends and events and their consequences into the future and to generate alternative scenarios at predetermined points in time (Chemtech 1993)."*

> *"The Cone of Plausibility encompasses theoretical projections of four planning scenarios; each having a dominant theme or driver, such as technology, politics, economics, and sociology (Exhibit 3). Each of these themes or drivers commands a vision or scenario of the future. Trends within each theme are affected by interactions among trends in which dominant trends alter the less dominate ones or result in discontinuities."*

> *"Outside of the cone are wild-card scenarios—scenarios which, if they occurred, would overwhelm other scenarios or visions of the future and include, for example, major depressions, major natural disasters, and major wars."*

> *"The process begins with a collaboration of experts internal to the organization—futurists and scenario writers. These players first determine the number of scenarios, with the number sufficient to allow considerable flexibility, yet manageable. The next step is to determine, by consensus, the ten most important strategic elements that influence their planning subject matter. These strategic elements are listed in order of their importance to the subject matter. This information is then used to create micro-scenarios comprised of the first four ranked elements. These micro-scenarios are four short statements that reflect positive attitudes of the elements and four that reflect opposing attitudes. Through a process of permutation and sorting of the eight statements, the order of the four final statements is established at random. In the workshop that follows, experts create their visions of the future for each scenario, expanding micro-scenarios to mini-scenarios of about 500 words."*

> *"Taylor: 'serves as an enclosure that circumscribes the thought process of the players. The strength of their thought process to build these scenarios and to hold them together as they proceed outward in time is a counterforce to the pressures of wild cards to disrupt the cone. Scenarios within the cone are considered plausible if they adhere to a logical progression of trends, events, and consequences from today to a predetermined time in the future' (Taylor 1993)."*

---

## 3. 9-Step Cone Pipeline

### Step 1 — Input (필수 입력)

이전 sub-skill 출력에서 다음을 수신한다:

- **§ Scenario Logics** (existing 4-5 worlds from § scenario-logics-selection)
- **§ Internal Consistency Audit** (from § internal-consistency-check)
- **§ Driving Forces** (from § driving-forces-identification) — 전략 요소 소스
- **§ Importance-Uncertainty Ranking** (from § importance-uncertainty-ranking) — 10대 요소 순위 소스
- **Time horizon** (박사님 설정값)

입력 부재 시: "§ Driving Forces 및 § Importance-Uncertainty Ranking이 없습니다. vision-foresight-scenarios C8 또는 C10 pipeline을 통해 호출하거나, 해당 입력을 직접 제공해 주세요."

---

### Step 2 — 4 Dominant Themes (Exhibit 3 verbatim)

Taylor Exhibit 3 verbatim 4개 themes:

- **Technological**
- **Political**
- **Economic**
- **Sociological**

박사님 컨텍스트별 추가 가능 (verbatim 4 themes + 추가):
- **Spiritual** (목회·신학 도메인)
- **Environmental** (지속가능성 도메인)

추가 theme은 5번째 시나리오(E)로 처리. DEFAULT는 Exhibit 3 verbatim 4개.

---

### Step 3 — 4 Planning Scenarios (Each Theme Dominant)

```
Scenario A: Technology-dominant  (Tech trends 주도)
Scenario B: Politics-dominant    (Political trends 주도)
Scenario C: Economics-dominant   (Economic trends 주도)
Scenario D: Sociology-dominant   (Social trends 주도)
```

**§ Scenario Logics와의 관계**:
- C8 cycle: 위 4개가 기존 worlds를 대체 (Taylor 4-theme 구조 우선)
- C10 Full Pipeline: 기존 worlds를 위 4개 theme으로 재분류·통합
- 기존 worlds가 theme에 자연스럽게 매핑되면 해당 world의 narrative를 시작점으로 활용

---

### Step 4 — 10 Strategic Elements (Taylor verbatim 핵심 단계)

Taylor verbatim: *"determine, by consensus, the ten most important strategic elements that influence their planning subject matter. These strategic elements are listed in order of their importance to the subject matter."*

**소스**: § Driving Forces + § Importance-Uncertainty Ranking (Step 1 입력에서)

**처리**:
1. § Driving Forces 목록에서 모든 strategic elements 추출
2. § Importance-Uncertainty Ranking 기준으로 중요도 순 정렬
3. Top-10 선택 (합의 원칙 — AI Futurist Agent + Scenario Writer Agent 합의 시뮬레이션)
4. **Top-4 식별** (micro-scenario 생성에 사용)

**출력 형식**:

| 순위 | Strategic Element | 출처 도메인 | 중요도 근거 |
|------|------------------|-------------|-------------|
| 1 | [element] | [domain] | [rationale] |
| 2 | [element] | [domain] | [rationale] |
| ... | ... | ... | ... |
| 10 | [element] | [domain] | [rationale] |

**Top-4** (micro-scenario용): 순위 1~4

---

### Step 5 — Trends within Each Theme + Interactions

Taylor verbatim: *"Trends within each theme are affected by interactions among trends in which dominant trends alter the less dominate ones or result in discontinuities."*

각 4개 theme마다:

```
Theme: [Technology / Politics / Economics / Sociology]

Trends (이 theme 내 주요 트렌드):
  - Dominant trend: [설명]
  - Subordinate trends: [목록]

Interactions:
  - [Dominant trend] → alters → [Subordinate trend]: [메커니즘]
  - [Dominant trend] → results in discontinuity: [불연속점]

Discontinuities flagged:
  - [설명]
```

---

### Step 6 — Wild Card Scenarios (Cone 외부 식별)

Taylor verbatim: *"Outside of the cone are wild-card scenarios—scenarios which, if they occurred, would overwhelm other scenarios or visions of the future."*

PDF Exhibit 3 verbatim 예시:
- Worldwide depression (major)
- Major natural disaster
- Major war
- USSR becomes a democracy (역사적 예시 → 박사님 컨텍스트: 한반도 통일 등)
- Other catastrophic/aberrant events

**Wild Card 분류 (3 tier)**:

| 분류 | 정의 | PDF 예시 |
|------|------|---------|
| **Catastrophic** | 모든 시나리오 무력화 | Major war, worldwide depression |
| **Disruptive** | 2개 이상 시나리오 방향 전환 | Major natural disaster |
| **Aberrant** | 1개 시나리오 무효화 | Anomalous one-off event |

**Cross-skill 연계**: → `vision-foresight-wild-cards` (10장) 호출 권장 (심층 wild card 분석)

---

### Step 7 — Micro-Scenarios (8 Statements per Planning Scenario)

Taylor verbatim: *"micro-scenarios comprised of the first four ranked elements. These micro-scenarios are four short statements that reflect positive attitudes of the elements and four that reflect opposing attitudes."*

각 4개 planning scenario마다:

**입력**: Top-4 Strategic Elements (Step 4 결과)

**생성**: 8개 statements (4 positive + 4 opposing)

Statement 형식:
```
[Element name] — [긍정/부정 태도 서술]. [해당 theme 관점에서의 함의]
```

예시 (Scenario A — Technology 컨텍스트):
```
Positive statements:
  T+1: AI integration — Productivity multiplies across sectors, enabling unprecedented efficiency.
  T+2: Digital infrastructure — Universal access creates new economic and social equity.
  T+3: Innovation cycles — Rapid iteration accelerates solutions to major challenges.
  T+4: Tech governance — Regulatory frameworks successfully manage AI risks.

Opposing statements:
  T-1: AI integration — Displacement of labor creates structural unemployment crises.
  T-2: Digital infrastructure — Surveillance state capabilities expand unchecked.
  T-3: Innovation cycles — Pace of change outstrips adaptive capacity of institutions.
  T-4: Tech governance — Regulatory fragmentation enables regulatory arbitrage.
```

**8개 statements를 JSON으로 준비** → Step 8 Python 호출

---

### Step 8 — Permutation + Random Ordering (결정론적 Python 전용)

Taylor verbatim: *"Through a process of permutation and sorting of the eight statements, the order of the four final statements is established at random."*

**⚠️ 이 단계는 LLM 추론 금지. Python `cone_permutation.py`만 사용.**

**실행 방법**:

```bash
# 방법 1: stdin JSON
echo '[
  "T+1 statement", "T+2 statement", "T+3 statement", "T+4 statement",
  "T-1 statement", "T-2 statement", "T-3 statement", "T-4 statement"
]' | python3 cone_permutation.py --scenario "Scenario A"

# 방법 2: pipe-separated
python3 cone_permutation.py \
  --statements "T+1|T+2|T+3|T+4|T-1|T-2|T-3|T-4" \
  --scenario "Scenario A"

# 재현 가능한 결과 (seed 고정)
python3 cone_permutation.py --scenario "Scenario A" --seed 42
```

**출력 (JSON)**:
```json
{
  "scenario": "Scenario A",
  "seed_used": 42,
  "input_count": 8,
  "selected_micro_scenario": [
    "T+2 statement",
    "T+1 statement",
    "T-2 statement",
    "T+3 statement"
  ]
}
```

**오류 조건**:
- 8개가 아닐 경우 → ValueError 발생, LLM이 임의 선택 금지
- Python 실행 불가 환경 → 반드시 사용자에게 알리고, 수동 random.sample 코드 제공

각 4개 시나리오에 대해 Step 7 → Step 8 반복 실행.

---

### Step 9 — Mini-Scenarios ~500 Words

Taylor verbatim: *"In the workshop that follows, experts create their visions of the future for each scenario, expanding micro-scenarios to mini-scenarios of about 500 words."*

**입력**: Step 8 결과 micro-scenario (4 selected statements)

**AI Agent 역할**: Workshop 전문가 패널 시뮬레이션 (Senior Futurist + Scenario Writer)

각 4개 planning scenario마다:
1. 4개 selected statements를 서사의 뼈대로 사용
2. ~500 words 확장 (허구 사실 금지 — 실제 트렌드·연구·역사적 사례 기반)
3. "오늘 → T년" 인과 진행 명시
4. Wild card 위협이 narrative 경계를 어떻게 압박하는지 언급
5. Plausibility 유지 (cone 내부 논리 일관성)

**워드 카운트 검증**: mini-scenario는 450~550 words 범위 내. 미달 시 확장, 초과 시 압축.

---

## 4. 출력 양식

출력은 다음 구조를 반드시 따른다. 각 섹션을 순서대로 완성한다.

---

### 출력 구조

**헤더**:

    ### § Cone of Plausibility (vision-foresight-scenarios-cone-of-plausibility)

    **출처**: Charles W. Taylor, U.S. Army War College, "Cone of Plausibility"
             (Chemtech 1993), in Glenn & TFG V3.0 19장 Section V Frontiers.
    **Themes**: Technology · Politics · Economics · Sociology
    **Planning Scenarios (within cone)**: 4
    **Wild Cards (outside cone)**: [N개]
    **Time Horizon**: [T years]

---

**Cone 형태 시각화** (indented 텍스트 — 중첩 코드블록 금지):

    TODAY                                              T YEARS
      │
      │    ╔══ WILD CARDS (cone 외부) ══════════════╗
      │    ║  • [wild card 1]                        ║
      │    ║  • [wild card 2]                        ║
      │    ╠════════════════════════════════════════╣
      ●────╣  Scenario A: Technology-dominant        ╠────→
      │    ╣  Scenario B: Politics-dominant          ╠────→
      │    ╣  Scenario C: Economics-dominant         ╠────→
      │    ╣  Scenario D: Sociology-dominant         ╠────→
      │    ╠════════════════════════════════════════╣
      │    ║  • [wild card 3]                        ║
      │    ║  • [wild card 4]                        ║
      │    ╚══ WILD CARDS (cone 외부) ══════════════╝
      │
    [PLAUSIBLE ZONE = 논리적 트렌드 진행 · cone 내부]

---

**10 Strategic Elements (순위별)**:

    #### 10 Strategic Elements (Consensus Ranking)

    | 순위 | Strategic Element | 도메인 | 중요도 근거 |
    |------|------------------|--------|-------------|
    | 1    | [element]        | [T/P/E/S] | [근거] |
    | 2    | [element]        | ...    | ...     |
    | ...  | ...              | ...    | ...     |
    | 10   | [element]        | ...    | ...     |

    **Top-4** (micro-scenario 생성용): [1위], [2위], [3위], [4위]

---

**각 Planning Scenario (4개 반복 구조)**:

    #### Scenario [A/B/C/D] — [Theme]-Dominant

    **Dominant Theme**: [Technology / Politics / Economics / Sociology]
    **Key Trends (within theme)**:
    - Dominant: [트렌드 설명]
    - Subordinate: [트렌드 목록]

    **Trend Interactions**:
    - [Dominant] → alters → [Subordinate]: [메커니즘]
    - Discontinuity: [불연속점]

    **Micro-scenario (Python permutation — Step 8 결과)**:

    Python call:
      `echo '[...8 statements JSON...]' | python3 cone_permutation.py --scenario "Scenario [A]"`

    Input (8 statements):
    - [T+1] [positive statement 1]
    - [T+2] [positive statement 2]
    - [T+3] [positive statement 3]
    - [T+4] [positive statement 4]
    - [T-1] [opposing statement 1]
    - [T-2] [opposing statement 2]
    - [T-3] [opposing statement 3]
    - [T-4] [opposing statement 4]

    Selected micro-scenario (random 4 from Python output):
    1. [statement]
    2. [statement]
    3. [statement]
    4. [statement]

    **Mini-scenario (~500 words)**:

    [500-word narrative — 인과 진행 오늘→T년, 트렌드 상호작용, wild card 압박 언급]

    **Word count**: [N] words

    **Plausibility Verification (Taylor 1993)**:
    - [ ] 논리적 인과 진행 (오늘 → T년): ✓/✗
    - [ ] Dominant trend이 subordinate trend 변화: ✓/✗
    - [ ] Discontinuities 명시: ✓/✗
    - [ ] Wild card 외부 위협 언급: ✓/✗

    **Glenn 3-Criteria (TFG V3.0 verbatim)**:
    - Plausible (합리적 경로 + 인과 명시): ✓/✗
    - Internally Consistent (유사 이슈 비교 가능): ✓/✗
    - Sufficiently Interesting (전략적 대응 유발): ✓/✗

    ---

**Wild Cards (Cone 외부)**:

    #### Wild Cards (Outside Cone)

    | Wild Card Event | 분류 | Trigger 조건 | Cone 영향 |
    |----------------|------|-------------|----------|
    | [event] | Catastrophic | [트리거] | 모든 4 시나리오 무력화 |
    | [event] | Disruptive | [트리거] | 2개 이상 시나리오 방향 전환 |
    | [event] | Aberrant | [트리거] | 1개 시나리오 무효화 |

    **Cross-skill**: → `vision-foresight-wild-cards` (10장) 심층 분석

---

**다음 sub-skill 전달**:

    #### 다음 sub-skill 전달

    → vision-foresight-scenarios-policy-testing
    입력: § Cone of Plausibility (위 전체 출력)

---

## 5. Python Permutation Helper (cone_permutation.py)

본 스킬 폴더에 포함된 결정론적 헬퍼:

```
skills/vision-foresight-scenarios-cone-of-plausibility/cone_permutation.py
```

**기능**: Taylor verbatim Step 8 — 8 statements (4 positive + 4 opposing) → 4개 random 선택

**입력 검증**: 정확히 8개가 아니면 ValueError 발생 (LLM 우회 구조적 차단)

**재현성**: `--seed` 옵션으로 동일 결과 재현 가능

**환경 요구**: Python 3.8+ stdlib only (외부 패키지 없음)

**오류 발생 시 처리**:
1. Python 실행 불가 → 사용자에게 명시 보고
2. 8개 미만/초과 입력 → statements 재생성 요청
3. JSON 파싱 오류 → 입력 형식 수정

---

## 6. Plausibility + 3-Criteria 검증 (결정론 불가 영역 — 원전 증명 의무)

Step 9 mini-scenarios에 대한 검증은 결정론으로 환원 불가. 따라서 **원전 verbatim 인용 + 외부 출처 1:1 대조**로 증명한다.

### 6.1 Plausibility 기준 (Taylor 1993 verbatim)

> *"Scenarios within the cone are considered plausible if they adhere to a logical progression of trends, events, and consequences from today to a predetermined time in the future."*

검증 항목 (각 mini-scenario):
- **논리적 진행**: 오늘의 상태 → 중간 단계 → T년 결과가 인과적으로 연결되는가?
- **트렌드 상호작용**: Dominant trend이 subordinate trends를 변화시키는 메커니즘이 명시되는가?
- **불연속점**: 예상치 못한 분기점이 식별되고 설명되는가?
- **Wild card 경계**: Mini-scenario가 cone 외부 사건을 내부로 잘못 포함하지 않는가?

### 6.2 Glenn 3-Criteria (Glenn & TFG V3.0 19장 verbatim)

> *"'Good' scenarios are those that are: 1) Plausible (a rational route from here to there that make causal processes and decisions explicit); 2) Internally consistent (alternative scenarios should address similar issues so that they can be compared); and 3) Sufficiently interesting and exciting to make the future 'real' enough to elicit strategic responses."*

| 기준 | 검증 질문 | PASS 조건 |
|------|---------|----------|
| **Plausible** | 오늘→T년 인과 경로가 명시되는가? | 최소 3개 인과 단계 포함 |
| **Internally Consistent** | 4개 시나리오가 동일 이슈를 다루어 비교 가능한가? | 모든 시나리오가 Top-4 elements를 공통 참조 |
| **Sufficiently Interesting** | 전략적 대응을 유발할 만큼 생생한가? | 구체적 결정 포인트·결과·stake 포함 |

**출처 없는 판정 = 자동 FAIL**. 모든 검증은 Taylor 1993 또는 Glenn & TFG V3.0 원전 verbatim 인용 필수.

---

## 7. 마스터 협업 Protocol

**입력** (Step 1):
- § Scenario Logics (from vision-foresight-scenarios-scenario-logics-selection)
- § Internal Consistency Audit (from vision-foresight-scenarios-internal-consistency-check)
- § Driving Forces (from vision-foresight-scenarios-driving-forces-identification)
- § Importance-Uncertainty Ranking (from vision-foresight-scenarios-importance-uncertainty-ranking)

**처리**: 9-Step pipeline (Taylor + Glenn verbatim)

**결정론 단계**: Step 8 — `cone_permutation.py` Python 함수 전용

**LLM 단계**: Step 4 (strategic elements 합의), Step 5 (trend 분석), Step 6 (wild card 식별), Step 7 (8 statements 작성), Step 9 (mini-scenarios 500 words)

**출력**: § Cone of Plausibility + 4 theme scenarios + wild cards + Glenn 3-criteria 검증

**다음 단계**: → vision-foresight-scenarios-policy-testing
