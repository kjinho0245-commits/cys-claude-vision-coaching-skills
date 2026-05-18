---
name: vision-foresight-scenarios-narrative-writing
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 7번째 sub-skill. Glenn & TFG V3.0 19장 Section II + III Schwartz Step 5 + Appendix A·B verbatim 풀 구현. **Narrative Writer AI Agent** — Schwartz Step 5 verbatim: *"fill out the scenarios"*. PDF Section II 핵심 verbatim: *"A scenario is a story with plausible cause and effect links that connects a future condition with the present, while illustrating key decisions, events, and consequences throughout the narrative."* + *"sufficiently vivid so that one can clearly see and comprehend the problems, challenges, and opportunities that such an environment would present"*. TFG Development verbatim: *"Prepare descriptions. Now, given the quantitative forecasts of the measures based on the probabilistic description of the impacting events, many chains of causality become apparent, and cohesive narratives describing the future histories can be prepared."* Section II 추가: *"future history—that is, the evolution from present conditions to one of several futures... lay out the causal chain of decisions and circumstances that lead from the present"*. **Exploratory vs Normative vs Mixed** branch — Exploratory (events/trends evolve based on alternative assumptions) / Normative (desirable future emerges from present via backcasting) / Mixed (both types within same set). PDF Appendix A "Environmental Backlash" + Appendix B "S&T Develops a Mind of Its Own" verbatim full scenario 양식 reference. **DEFAULT: Per-scenario narrative 3000-5000 words + future history (present→future causal chain) + key decisions·events·consequences embedded + Appendix A·B 양식 풍부한 detail + Exploratory or Normative branch**. 결정론적 validate_narrative.py 호출 강제.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 일곱 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section II + III Schwartz Step 5 + TFG Development "Prepare descriptions" + Appendix A·B 풀 구현. **Narrative Writer Agent** 9-Step pipeline: ① 입력 형식 검증 + edge case 처리 → ② Per-scenario narrative architecture (word count 강제: opening 300-500·setup 600-1000·middle 1500-2500·climax 300-500·resolution 300-500 words) → ③ Future history 양식 강제 — *"evolution from present conditions"* (Section II verbatim), 미래 기점 과거 시제 → ④ Exploratory vs Normative vs Mixed branch — 마스터 Step 0 type input 활용 + Normative 백캐스팅 5단계 방법론 → ⑤ Plausible cause-effect links 강제 — 모든 event·decision·consequence가 explicit causal connector로 연결 → ⑥ 정량 projection 통합 — § Projections 수치를 서사에 임베딩, qualitative cycle 시 qualitative 서술자 사용 → ⑦ Appendix A·B verbatim 양식 적용 — GLEEM Plan style(acronym+full name+numbered elements)·TEF/BTS/CyberNow/ISTO style·풍부한 detail → ⑧ Surprise 요소 강제 (Section IV verbatim 하드 게이트 — surprise_count=0이면 Interest 최대 2) → ⑨ "Filling in the Blanks" 옵션 (Millennium Project verbatim) + validate_narrative.py 결정론 검증. 출력: § N Scenario Narratives (3000-5000 words each) + future history + plausible cause-effect chain + Appendix A·B 양식 풍부함 + surprises + 메타데이터 블록 + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Narrative Writing Sub-skill (INTERNAL)

> **출처**: Glenn & TFG V3.0 19장 Section II + III Schwartz Step 5 + TFG Development + Appendix A·B verbatim.

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **7번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 입력 형식 명세 + Edge Case 처리

### 0.1 필수 입력

| 입력 | 소스 sub-skill | 필수 여부 |
|---|---|---|
| § Scenario Logics | vision-foresight-scenarios-scenario-logics-selection | **필수** |
| § Projections per Scenario | vision-foresight-scenarios-projection-engine | 조건부 (TIA-integrated 시 필수; qualitative 시 생략 가능) |
| Cycle Type (C1-C10) | vision-foresight-scenarios 마스터 Step 0 | **필수** |
| Scenario Type | vision-foresight-scenarios 마스터 Step 0 | **필수** |
| Time Horizon (T₀, T_final year) | vision-foresight-scenarios 마스터 Step 0 | **필수** |
| Focal Issue | vision-foresight-scenarios-focal-issue-definition | **필수** |
| Driving Forces (axes) | vision-foresight-scenarios-importance-uncertainty-ranking | **필수** |
| Controversial Items | vision-foresight-scenarios-driving-forces-identification | 권장 (있으면 반드시 포함) |

### 0.2 Edge Case 처리

```
§ Scenario Logics 부재:
  → 즉시 오류: "§ Scenario Logics 없음 — narrative 작성 불가. 마스터에 에스컬레이션."

§ Projections 부재 (TIA-integrated cycle 선택 시):
  → 경고 후 qualitative 서술로 대체.
  → "§ Projections 없음 — qualitative 서술자 사용 ('크게 증가', '약 두 배' 등). 
     수치 근거 없음 명시. 가능하면 upstream에 재요청."
  → 수치 직접 fabrication 금지.

§ Projections 부재 (qualitative cycle: C2·C3·C5·C7):
  → 정상 처리. qualitative 서술자만 사용.

시나리오 수 < 3: 경고 후 진행.
시나리오 수 4-5: 정상 (TFG 권장).
시나리오 수 > 5: 경고 후 진행.
시나리오 수 = 0: 즉시 오류.

Focal Issue 부재: 즉시 오류.
T₀ 또는 T_final 부재: T₀ = 현재 연도, T_final = T₀ + 15 로 DEFAULT 적용 후 경고.
```

### 0.3 데이터 무결성 원칙

**서사 내 모든 수치·사실 주장은 upstream sub-skill 출력 (§ Projections, § Scenario Logics)에서 도출해야 한다. LLM이 수치를 자체 생성(fabrication)하는 것은 금지다.**

- 수치 있는 경우: "By [year], [measure]가 [value]에 달했다 (2026 기준 [baseline]에서 증가)" 형식으로 임베딩.
- 수치 없는 경우 (qualitative): "크게 증가했다", "약 두 배 수준에 달했다" 등 qualitative 서술자만 사용.

---

## 1. AI Agent 역할 — Narrative Writer

당신은 **Scenarios Narrative 작가**다. Schwartz Step 5 *"fill out the scenarios"* + Appendix A·B verbatim 양식으로 plausible cause-effect future history 작성.

---

## 2. PDF 원전 (verbatim)

> *"A scenario is a story with plausible cause and effect links that connects a future condition with the present, while illustrating key decisions, events, and consequences throughout the narrative."*

> *"sufficiently vivid so that one can clearly see and comprehend the problems, challenges, and opportunities that such an environment would present"*

> *"future history—that is, the evolution from present conditions to one of several futures... lay out the causal chain of decisions and circumstances that lead from the present"*

> *"Prepare descriptions. Now, given the quantitative forecasts of the measures based on the probabilistic description of the impacting events, many chains of causality become apparent, and cohesive narratives describing the future histories can be prepared."*

### Section IV verbatim 강제

> *"scenarios should have some surprises in them – even in surprise-free or business-as-usual scenarios, because the rate of change is accelerating"*

### Appendix A·B Examples Reference

- **Appendix A**: Environmental Backlash 2020 — Indian Ocean nuclear catastrophe·GLEEM Plan 13 elements·ExxonMobil lawsuit·biofuels·hydrogen·INSOLSAT space solar·seawater agriculture·stem cell meat
- **Appendix B**: S&T Develops a Mind of Its Own 2025 — TEF (Tele-Everywhere-Feedback)·CyberNow·BTS (Brain Trans-science Service)·ISTO·collective human-machine intelligence

---

## 3. 9-Step Narrative Writing Pipeline

### Step 1 — Input

- § Scenario Logics (4-5 worlds with names + axes)
- § Projections per Scenario (quantitative trajectories) — 조건부 (§0.2 참조)
- Cycle type (C1-C10), Scenario Type (Exploratory/Normative/Mixed)
- Time Horizon: T₀ baseline year, T_final target year
- Focal Issue, Driving Forces, Controversial Items

### Step 2 — Per-Scenario Narrative Architecture

각 시나리오의 서사 구조와 **단어 수 범위**:

```
For each scenario s (total: 3000-5000 words):

  [Opening] (≈10% / 300-500 words):
    T₀ snapshot — Current state of focal issue domain
    Key driving forces at their T₀ baseline values
    Sense of uncertainty and possibility

  [Setup] (≈20% / 600-1000 words):
    Triggering events·driver activations (early time period)
    Why THIS scenario path diverges from others
    First decision points

  [Middle] (≈50% / 1500-2500 words):
    Causal chain·decisions·consequences (year-by-year time markers)
    Each year: at least 1 named event + causal link to next
    Key measures evolving per § Projections (or qualitative)
    Named institutions, programs, actors, policies

  [Climax] (≈10% / 300-500 words):
    Pivotal moment / tipping point — the decisive turn
    The moment that made this scenario's world irreversible

  [Resolution] (≈10% / 300-500 words):
    T_final full picture — what the world looks like now
    State of key driving forces at T_final
    Strategic landscape for decision makers
```

**주의**: "2026" 하드코딩 금지 — 실제 T₀ 연도를 사용할 것. 박사님이 다른 focal issue year를 지정할 수 있다.

### Step 3 — Future History Format (verbatim 강제)

```
REQUIRED opening format (choose one):
  "It is now [T_final]. The world experienced..."
  "By [T_final], [scenario name] world had emerged when..."
  "As of [T_final], looking back at the [N] years since [T₀]..."

FORBIDDEN: Forward-predicting present-tense narrative.
  ✗ "In 2032, X will happen..."
  ✗ "By 2035, we expect..."
  ✓ "In 2032, X happened because..."
  ✓ "By 2035, it had become clear that..."

각 narrative는 T_final 기점에서 BACK을 바라본다. NOT predicting forward.
```

### Step 4 — Exploratory vs Normative vs Mixed Branch

```
Exploratory (DEFAULT):
  Events/trends evolve based on alternative driver combinations
  Multiple paths equally valid — no moral preference
  Narrative: "This is what happened in THIS path"
  각 scenario: different axis endpoint combination

Normative:
  Preferred/desirable end state given at T_final
  Backcasting 5단계 방법론:
    1. Open: Describe T_final desired state in vivid detail
    2. T_final-5: "This was possible because [prior period]..."
    3. T_final-10: "That period was enabled by [earlier]..."
    4. Repeat backward until T₀
    5. Causal chain reads: T₀ decisions → T₀+5 conditions → ... → T_final
  "How did we get here?" — every step backward must be causally justified
  박사님 vision-* skill 양식 연계 가능

Mixed (C1/C9/C10에서 주로 사용):
  Set 내 일부 scenarios = Exploratory (다양한 path)
  Set 내 1 scenario = Normative (aspirational/preferred end state)
  통상: 3 Exploratory + 1 Normative (aspirational 시나리오)
  각 시나리오 헤더에 "[Exploratory]" 또는 "[Normative]" 태그 명시
```

### Step 5 — Plausible Cause-Effect Links 강제

```
For every event/decision/consequence:
  Q: What caused this?
  Q: What does this cause?
  Q: Is the link plausible (rational route)?

필수 causal connector 문구 (최소 이 중 하나를 매 전환마다 사용):
  "Because X happened, Y followed"
  "This decision led to Z"
  "The combination of A + B produced C"
  "As a direct consequence of..."
  "This triggered a cascade: first..., then..., finally..."
  "Precisely because..., [country/actor] chose..."

모든 link explicit:
  ✗ "In 2033, the economy collapsed." (assertion — no causal link)
  ✓ "Because the 2031 AGI incident eroded investor confidence, and because
     no regulatory framework had been adopted, capital flight accelerated
     through 2032-33, producing the economic contraction that followed."
```

### Step 6 — Quantitative Projection 통합

```
TIA-integrated cycles (§ Projections per Scenario 있는 경우):
  For each key measure M:
    Find M's trajectory for scenario s from § Projections (median ± CI)
    Embed at appropriate time marker in narrative

  Format:
    "By [year], [measure M]가 [value] (±[CI])에 달했다
     — [T₀] 기준 [baseline]에서 [증가/감소]한 수치다."

  예시:
    "By 2032, renewable energy had reached 47% (±3%) of the national grid,
     up from the 2026 baseline of 22%, driven by the GREEM Initiative's
     accelerated deployment mandate."

Qualitative cycles (§ Projections 없는 경우):
  수치 fabrication 금지. 사용 가능한 서술자:
    "크게 증가했다 / roughly doubled / grew substantially /
     declined sharply / remained relatively stable despite..."
  Controversial or uncertain trends는 conditional language 사용:
    "If projections held, X would have reached near-double digits..."
```

### Step 7 — Appendix A·B 양식 풍부함

각 narrative에 포함:

**필수 (hard requirement):**
- **≥1 named fictional institution/program/plan** (GLEEM Plan 양식):
  - 형식: `[ACRONYM] ([Full Name]) — [scope] [elements count]`
  - 예시 GLEEM 양식: `"GREEM Plan (Global-Regional Energy-Environment Marshall Plan)" with 11 action items`
  - 예시 Appendix B 양식: `"TEF (Tele-Everywhere-Feedback)"` — TEF는 전지구적 실시간 사회 감지 통신 시스템 (TFG V3.0 Ch.19 Appendix B)
  - Appendix B 추가 사례: `BTS (Brain Trans-science Service)` — 신경과학 기반 인지 증강 서비스; `CyberNow` — 실시간 사이버-물리 통합 플랫폼; `ISTO` — 집단 인간-기계 지능 거버넌스 기구
  - 이들은 **스타일 참조**다. 각 시나리오 고유 context에 맞는 새 fictional entity를 창조할 것.

**권장 포함:**
- Technology developments (specific named tech + mechanism)
- Social/cultural shifts (specific communities, behaviors, norms)
- Economic patterns (specific sectors, flows, numbers if available)
- Environmental changes (specific regions, measurements)
- Governance/political events (specific laws, treaties, elections)
- Spiritual/identity dimensions (박사님 pastoral 컨텍스트 적용 가능)
- Geographic specifics (country·region·city examples)
- Time markers (year·decade — "In 2031...", "By mid-decade...")
- Quotes·dialogue·media excerpts (option for vividness)

### Step 8 — Surprises Embedded (Section IV verbatim 강제)

**Surprise 정의**: 시나리오의 driver combination과 주류 전문가 전망으로부터 이탈하는 요소. 즉, 해당 scenario의 driving force 방향성에서 도출되는 '가장 likely한 trajectory'를 명시적으로 위반하는 사건·결과.

```
각 scenario에 최소 1 surprise element (hard gate — §9 validator 검증):
  - Technology breakthrough/failure beyond consensus forecast
  - Wild card event (외부에서 유입된 충격)
  - Counterintuitive outcome (driver가 예상치 못한 방향으로 작용)
  - Actor behavior reversal (진영/국가가 예상 반대로 행동)
  - "Conventional wisdom didn't see it coming"

유효한 surprise 예시:
  ✓ "The AGI consensus forecast was 2035, but emergence occurred in 2031
     — three years ahead, via an unexpected BCI synthesis that no team
     had published on." [주류 전망에서 이탈하는 timing reversal]
  ✓ "South Korea, not the US or China, became the de facto global
     AGI governance standard-setter." [actor behavior surprise]

유효하지 않은 surprise (거부):
  ✗ "Technology advanced rapidly." [이미 scenario의 예상 방향]
  ✗ "Geopolitical tensions continued." [당연한 트렌드 연장]

surprise_descriptions는 validate_narrative.py에 제출 → 검증.
```

### Step 9 — Filling in the Blanks (Millennium Project Verbatim — 선택적)

PDF Section V Frontiers verbatim 참조 (S&T 2025·Middle East Peace Scenarios 사례):

```
BLANK 옵션이 활성화된 경우 (마스터 또는 사용자 지정):
  드래프트 서사에 [BLANK] 마커 삽입.
  
  마커 형식:
    [BLANK: 카테고리 — 내용 설명]
  
  사용 시점:
    - 지역 전문가 지식이 필요한 수치 (예: "지역별 GDP 성장률")
    - 후속 Delphi 라운드 결과를 대기 중인 확률 수치
    - 기관 대표자가 채워야 할 조직 내부 데이터
    - 실제 발생 여부가 불확실한 wildcard 결과
  
  예시:
    "By 2033, the GREEM Plan had disbursed [BLANK: total funding amount —
     추정치 범위: $200B–$500B, Delphi 패널 입력 대기] in green energy
     transition funds across [BLANK: N participating nations — 현재 협상 중]."
  
  BLANK 목록을 appendix로 정리:
    [BLANK Registry]
    | # | 위치 | 카테고리 | 필요 입력 | 담당자 |
    |---|---|---|---|---|
    | 1 | Scenario 1, 2033 | 재정 규모 | ... | ... |

DEFAULT: BLANK 옵션 OFF.
```

> **Pipeline 완료 전환**: Steps 1-9 완료 후 → **§4 (결정론적 Validator 호출)** → §5 (출력 양식) → vision-foresight-scenarios-internal-consistency-check.

---

## 4. 결정론적 Validator 호출 (validate_narrative.py)

모든 서사 작성 완료 후, validate_narrative.py를 **반드시** 호출하여 구조적 요건을 검증한다.

### 4.1 입력 JSON 구성

LLM이 서사 작성 완료 직후 다음 JSON을 구성한다:

```json
{
  "metadata": {
    "focal_issue": "[마스터 Step 0 focal issue]",
    "t0_year": [T₀ 연도 int],
    "t_final_year": [T_final 연도 int],
    "cycle_type": "[C1-C10]",
    "scenario_type": "[Exploratory/Normative/Mixed]",
    "driving_forces": ["[DF1]", "[DF2]", "..."],
    "controversial_items": ["있으면 포함", "..."],
    "n_scenarios": [int]
  },
  "scenarios": [
    {
      "id": 1,
      "name": "[Scenario Name]",
      "word_count_self_reported": [직접 단어 수 계산 int],
      "surprise_count": [int],
      "surprise_descriptions": ["[surprise 1 설명]", "..."],
      "has_future_pov": true/false,
      "future_pov_marker": "[서사 첫 문장 또는 POV 개방 문장]",
      "sections_present": {
        "opening": true/false,
        "setup": true/false,
        "middle": true/false,
        "climax": true/false,
        "resolution": true/false
      },
      "named_decision_points_count": [int],
      "named_decision_points_list": ["[결정 1]", "..."],
      "causal_links_explicit": true/false,
      "has_real_sounding_institution": true/false,
      "filling_blanks_used": true/false
    }
  ],
  "output_checks": {
    "header_format_h3_dash": true/false,
    "metadata_block_present": true/false,
    "surprise_inventory_table_present": true/false
  }
}
```

### 4.2 Validator 실행

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SKILL_DIR/validate_narrative.py" --input /tmp/narrative_data.json
```

### 4.3 결과 처리

```
errors 존재 → 해당 시나리오 수정 후 재검증 (최대 2회)
  - WORD_COUNT_ERROR: 해당 시나리오 서사 확장
  - SURPRISE_GATE_ERROR: surprise 요소 추가
  - FUTURE_POV_ERROR: 서사 opening 재작성 (Step 3 양식 적용)
  - SECTION_ERROR: 누락 section 추가
  - CAUSAL_LINK_ERROR: 인과 연결자 문구 추가
  - FORMAT_ERROR: 출력 포맷 수정

warnings만 → 수정 권장, 진행 가능

2회 후도 errors 존재 → 마스터 에스컬레이션. FAIL 표기 후 다음 단계 진행.
```

---

## 5. 출력 양식

**중요**: 시나리오 헤더는 반드시 `### Scenario N — [Name]` (H3 + 대시) 형식을 사용한다.  
내부 일관성 검사기(vision-foresight-scenarios-internal-consistency-check) §5 입력 형식과 호환 필수.

```markdown
### § N Scenario Narratives (vision-foresight-scenarios-narrative-writing)

**N Scenarios Drafted**: [4-5]
**Type**: [Exploratory/Normative/Mixed]
**Word Count Range**: [min]-[max] per scenario (average: ~[avg])
**Validator**: validate_narrative.py [PASS/FAIL]

---

**Metadata for Internal Consistency Check**
- Focal Issue: [마스터 Step 0 focal issue]
- Time Horizon: [T₀]–[T_final] ([N] years)
- Cycle Type: [C1-C10] [cycle name]
- Scenario Type: [Exploratory/Normative/Mixed]
- Driving Forces (axes): [DF1], [DF2], ...
- Controversial Items: [있으면 목록, 없으면 "없음"]

---

### Scenario 1 — [Name]
<!-- [Exploratory/Normative] — [Axis config: A1·High, A2·Low] -->

[3000-5000 word future history with all 9-step elements]

---

### Scenario 2 — [Name]
<!-- [Exploratory/Normative] — [Axis config] -->

[3000-5000 word narrative]

---

[... up to N scenarios ...]

---

#### Surprise Elements Inventory

| Scenario | Name | Surprise Element |
|---|---|---|
| 1 | [이름] | [unexpected element — brief description] |
| 2 | [이름] | [unexpected element] |
| ... | ... | ... |

---

#### Deterministic Validator Output

```json
{
  "valid": true/false,
  "overall_pass_fail": "PASS/FAIL",
  "errors": [...],
  "warnings": [...]
}
```

→ vision-foresight-scenarios-internal-consistency-check
```

---

## 6. 마스터 협업 protocol

| 항목 | 내용 |
|---|---|
| **입력** | § Scenario Logics + § Projections per Scenario (조건부) + 마스터 메타데이터 |
| **처리** | 9-Step pipeline per scenario + validate_narrative.py 검증 |
| **출력** | § N Scenario Narratives + 메타데이터 블록 + Surprise Inventory + Validator 결과 |
| **FAIL 시** | 해당 시나리오 수정 + 재검증 (최대 2회) |
| **2회 후도 FAIL** | 마스터 에스컬레이션 + FAIL 표기 유지 후 다음 단계 진행 |
| **다음 단계** | vision-foresight-scenarios-internal-consistency-check |
