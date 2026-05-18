---
name: vision-foresight-scenarios-importance-uncertainty-ranking
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 3번째 sub-skill. Glenn J.C. & TFG (2009) *Futures Research Methodology V3.0* 19장 Section III Schwartz Step 3 풀 구현. **Importance × Uncertainty Ranker AI Agent** — Schwartz P. (1991) *The Art of the Long View* pp. 226-234 Seven Step Process Step 3 verbatim: *"rank the driving forces and trends by importance and uncertainty"*. 핵심 도구 — 2×2 matrix (Importance axis × Uncertainty axis) → 4 quadrant 분류: ① **High Importance + High Uncertainty = Critical Drivers** (scenario axes 후보, Step 4 logics 선택 input) ② **High Importance + Low Uncertainty = Predetermined Elements** (모든 scenario에 공통, Wack 1985 / van der Heijden 1996) ③ **Low Importance + High Uncertainty = Noise** (제외) ④ **Low Importance + Low Uncertainty = Background**. Top-2 Critical Drivers가 4-quadrant scenarios의 axes로 권장 (Schoemaker 1995). **결정론 도구** — `iu_ranker.py` (이 폴더 내) — verbatim·Likert anchor·quadrant 임계값(3.5)·median/mean/std 집계·Top-2 정렬 규칙·입력 schema 검증·ASCII 2×2 matrix 렌더링을 LLM이 자연어로 재추론하지 않도록 차단. **DEFAULT**: 6-12 driving forces × 6-8 persona scoring → JSON 입력 → `python3 iu_ranker.py rank input.json output.md` 1회 호출로 § Importance-Uncertainty Matrix 완성.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 세 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Schwartz Step 3 풀 구현. **Importance-Uncertainty Ranker Agent** 6-Step pipeline (결정론 환원): ① 입력 § Driving Forces (6-12 curated) — `python3 iu_ranker.py validate_input input.json` 강제 검증 → ② 각 driving force × AI Agent 6-8 persona scoring — Importance score 1-5 Likert (anchor: `iu_ranker.py likert_scale`) + Uncertainty score 1-5 Likert → ③ aggregate scores: `statistics.median` + `statistics.mean` + `statistics.pstdev` (`iu_ranker.py rank` 자동 호출) → ④ 4 quadrant 분류 — 임계값 정확히 3.5 (1-5 Likert 중점 3.0 위) — `classify_quadrant(importance, uncertainty)`: HH=CRITICAL, HL=PREDETERMINED, LH=NOISE, LL=BACKGROUND → ⑤ Top-2 Critical Drivers 결정론 정렬 규칙: combined_score(I×U) desc → sum_score(I+U) desc → consensus_sigma asc → id asc → ⑥ § Importance-Uncertainty Matrix markdown 출력 + 다음 sub-skill `vision-foresight-scenarios-scenario-logics-selection` 전달. 출력 양식 — scoring table + 2×2 ASCII matrix + Top-2 axes + Predetermined list + Determinism Audit fingerprint.
disable-model-invocation: true
---

# Scenarios — Importance × Uncertainty Ranking Sub-skill (INTERNAL)

> **1차 출처**: Glenn J.C. & TFG (2009). "Scenarios." In *Futures Research Methodology V3.0*, Ch.19. The Millennium Project. Section III Schwartz Step 3.
> **2차 출처**: Schwartz P. (1991). *The Art of the Long View*. Doubleday/Currency. pp. 226-234.
> **보조 출처**: Schoemaker P.J.H. (1995). "Scenario Planning: A Tool for Strategic Thinking." *Sloan Management Review* 36(2):25-40. / Wack P. (1985). "Scenarios: Uncharted Waters Ahead." *HBR* Sep-Oct:73-89. / van der Heijden K. (1996). *Scenarios: The Art of Strategic Conversation*. Wiley.

> **결정론 도구**: `iu_ranker.py` (이 폴더 내)
> PDF verbatim·Likert anchor·quadrant 임계값·집계 통계·정렬 규칙·입력 schema·ASCII matrix 렌더링을
> LLM이 자연어로 재추론하지 않도록 차단.
>
> ```bash
> python3 iu_ranker.py validate   # ALL_PASS: true 필수 (실행 전 항상 확인)
> ```

**LLM은 아래 항목을 자연어로 재추론하지 않는다 — 반드시 Python 호출 결과 사용:**

| 항목 | 호출 |
|---|---|
| PDF verbatim 인용 | `python3 iu_ranker.py verbatim KEY` |
| 전체 verbatim 목록 | `python3 iu_ranker.py verbatim_all` |
| Likert 1-5 anchor 정의 | `python3 iu_ranker.py likert_scale` |
| 4 quadrant 분류 임계값 | `python3 iu_ranker.py quadrant_thresholds` |
| 단일 cell 분류 | `python3 iu_ranker.py classify I U` |
| 입력 schema 검증 | `python3 iu_ranker.py validate_input input.json` |
| 풀 ranking + 출력 | `python3 iu_ranker.py rank input.json output.md` |

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **3번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 입력 인터페이스 (§ Driving Forces)

**수신 형식** (vision-foresight-scenarios Step 2 → Importance-Uncertainty Ranking):

```json
{
  "meta": {"focal_issue": "[focal issue statement]",
           "decision_horizon": "[year]",
           "domain": "[domain]"},
  "driving_forces": [
    {
      "id": "DF01",
      "name": "[driving force name]",
      "endpoints_low":  "[axis low end description]",
      "endpoints_high": "[axis high end description]",
      "scores": [
        {"persona": "P1 Industry Insider",     "importance": 5, "uncertainty": 4},
        {"persona": "P2 Scenario Specialist",  "importance": 4, "uncertainty": 5},
        {"persona": "P3 Policy Analyst",       "importance": 5, "uncertainty": 4},
        {"persona": "P4 Tech Expert",          "importance": 4, "uncertainty": 5},
        {"persona": "P5 Sociologist",          "importance": 5, "uncertainty": 4},
        {"persona": "P6 Economist",            "importance": 4, "uncertainty": 5}
      ]
    }
  ]
}
```

**Schema 제약** (`iu_ranker.py validate_input`이 강제):
- driving_forces 수: 6-12 (Coates winnowing 범위와 일치)
- 각 driving force의 scores 수: 6-8 persona (Driving Forces Identifier 8-persona pool 부분집합)
- importance / uncertainty 각: integer or float, 1.0-5.0 (Likert 범위 위반 자동 FAIL)
- id는 고유 (중복 자동 FAIL)
- 필수 필드: id, name, scores (각 score는 persona, importance, uncertainty)

---

## 1. AI Agent 역할 — Importance × Uncertainty Ranker

당신은 **Scenarios Importance × Uncertainty Ranking 전문가**다. Schwartz Step 3 verbatim 양식으로 driving forces를 2×2 matrix에 배치하고 Top-2 Critical Drivers를 식별한다.

```bash
python3 iu_ranker.py verbatim schwartz_step3
# → "rank the driving forces and trends by importance and uncertainty"
#   Schwartz P. (1991). The Art of the Long View — Step 3 verbatim.
```

당신의 역할은 LLM 자연어 평가가 아니라:
1. 6-8 persona 시점에서 각 driving force에 1-5 Likert 점수를 부여하는 **점수 결정자**
2. 점수 결과를 `iu_ranker.py rank`에 넘기는 **deterministic engine 호출자**
3. 출력 markdown을 § Importance-Uncertainty Matrix로 전달하는 **메시지 전달자**

집계·분류·정렬·시각화는 모두 `iu_ranker.py`가 수행한다.

---

## 2. PDF 원전 (verbatim — 1:1 외부 출처 대조)

다음 verbatim은 모두 `iu_ranker.py verbatim KEY`로 조회한다.

```bash
python3 iu_ranker.py verbatim schwartz_step3
```
> *"rank the driving forces and trends by importance and uncertainty"*
> — Schwartz P. (1991), *The Art of the Long View*, Doubleday/Currency, pp. 226-234. Step 3 verbatim.

```bash
python3 iu_ranker.py verbatim schwartz_seven_steps
```
> *"These steps include: identify the focal issue or decision; identify the key forces and trends in the environment; rank the driving forces and trends by importance and uncertainty; select the scenario logics; fill out the scenarios; assess the implications; and select the leading indicators and signposts for monitoring purposes."*
> — Schwartz 1991, Seven Step Process.

```bash
python3 iu_ranker.py verbatim wack_pre_uncertain
```
> *"the predetermined elements and the critical uncertainties"*
> — Wack P. (1985), "Scenarios: Uncharted Waters Ahead," *HBR* Sep-Oct 1985, pp. 73-89. Shell origin terminology.

```bash
python3 iu_ranker.py verbatim schoemaker_step3
```
> *"identify basic trends and key uncertainties"*
> — Schoemaker P.J.H. (1995), *Sloan Management Review* 36(2):25-40. Step 3 of 10.

```bash
python3 iu_ranker.py verbatim predetermined_elements
```
> Wack 1985 + van der Heijden 1996 — Predetermined elements는 모든 scenario에 공통 반영.

```bash
python3 iu_ranker.py verbatim critical_uncertainties
```
> Schwartz 1991 + van der Heijden 1996 — Critical uncertainties는 scenario axes가 된다.

---

## 3. Likert 1-5 Anchor 정의 (자연어 재추론 금지)

```bash
python3 iu_ranker.py likert_scale
```

**Importance** (1-5):
1. trivial — no meaningful effect on focal issue
2. minor — small marginal effect
3. moderate — noticeable but bounded effect
4. major — substantially shapes focal issue outcome
5. critical — changes everything about focal issue

**Uncertainty** (1-5):
1. highly predictable — direction & magnitude known (predetermined)
2. mostly predictable — small variance in outcome
3. moderately uncertain — known range, unknown trajectory
4. highly uncertain — outcome could swing widely
5. wildly unpredictable — true uncertainty, multiple opposing futures

출처: Schoemaker 1995, GBN convention. 모든 persona 점수는 이 anchor에 맞춰 부여.

---

## 4. Quadrant 분류 임계값 (결정론)

```bash
python3 iu_ranker.py quadrant_thresholds
```

**임계값**: median ≥ **3.5** = High; median < 3.5 = Low.
**근거**: 1-5 Likert 중점은 3.0. High는 중점보다 명확히 위(≥ 3.5), Low는 중점 이하(< 3.5)로 정의한다. 정수 점수만 들어올 경우 사실상 1·2·3 = Low, 4·5 = High. van der Heijden (1996)과 Schoemaker (1995) GBN convention과 일치.

**4 Quadrants**:
- **CRITICAL** (High Imp + High Unc): scenario axes 후보 — Schwartz "critical uncertainties"
- **PREDETERMINED** (High Imp + Low Unc): 모든 scenario 공통 반영 — Wack/van der Heijden
- **NOISE** (Low Imp + High Unc): 제외 (omit·too unpredictable)
- **BACKGROUND** (Low Imp + Low Unc): omit·context only

`classify_quadrant(I, U)` cell-by-cell 분류는 위 임계값을 엄격히 사용.

---

## 5. 6-Step I-U Ranking Pipeline (결정론 환원)

### Step 1 — 입력 § Driving Forces 수신 + 검증

```bash
python3 iu_ranker.py validate_input driving_forces.json
# {"pass": true, "errors": []}    ← FAIL이면 Step 2 진행 금지
```

검증 실패 시 입력 폴더에 반려: 누락 필드, 범위 초과, 중복 ID, persona/force 수 위반은 모두 PASS=false로 차단.

### Step 2 — AI Agent 6-8 Persona Scoring

각 driving force에 대해 (Driving Forces Identifier 8-persona pool에서 6-8명 선정):

- P1 Industry Insider, P2 Scenario Specialist, P3 Policy Analyst, P4 Tech Expert,
- P5 Sociologist, P6 Economist, P7 Environmental Scientist, P8 Devil's Advocate

각 persona가 Importance·Uncertainty 점수(1-5 Likert) 부여 → JSON에 기록.

**점수 부여 원칙**:
- focal issue 영향력이 평가 기준 (Importance)
- 미래 방향 예측 불가능 정도가 평가 기준 (Uncertainty)
- LLM이 직접 계산·평균·중앙값을 산출하지 않는다 — 단일 persona 점수만 부여

### Step 3 — Aggregate Scores (Python statistics 강제)

```bash
python3 iu_ranker.py rank driving_forces.json /dev/stdout
```

`rank_forces`가 자동으로:
- `statistics.median(importance_scores)` → importance_median
- `statistics.mean(...)` → importance_mean
- `statistics.pstdev(...)` → importance_std
- (Uncertainty 동일)
- combined_score = median(I) × median(U)
- sum_score = median(I) + median(U)
- consensus_sigma = (importance_std + uncertainty_std) / 2

### Step 4 — 4 Quadrant 분류

각 force에 `classify_quadrant(importance_median, uncertainty_median)` 자동 적용.

### Step 5 — Top-2 Critical Drivers 결정론 선정

`select_top2_critical()` 정렬 키:
1. combined_score 내림차순
2. sum_score 내림차순 (combined 동률 시)
3. consensus_sigma 오름차순 (합의 강할수록 우선)
4. id 사전순 (모두 동률 시)

이 4단계 tie-break으로 어떤 입력이든 단일 deterministic Top-2 선정.

### Step 6 — § Importance-Uncertainty Matrix 출력 + 다음 sub-skill 전달

```bash
python3 iu_ranker.py rank driving_forces.json iu_matrix.md
# {"wrote": "iu_matrix.md",
#  "top2": ["DF01", "DF02"],
#  "predetermined": ["DF04"],
#  "quadrant_counts": {"CRITICAL": 4, "PREDETERMINED": 1, "NOISE": 0, "BACKGROUND": 1}}
```

→ `vision-foresight-scenarios-scenario-logics-selection`

---

## 6. 출력 양식 (§ Importance-Uncertainty Matrix)

`iu_ranker.py rank`가 직접 생성. 아래는 출력 골격이며 LLM은 양식을 수정·재구성하지 않는다.

```markdown
### § Importance-Uncertainty Matrix (vision-foresight-scenarios-importance-uncertainty-ranking)

**Total Driving Forces Ranked**: [N]
**Top-2 Critical Drivers (Recommended Axes)**: [DF_a, DF_b]
**Predetermined Elements (Common to All Scenarios)**: [DF_c, ...]

**Quadrant Distribution**: CRITICAL=[x] · PREDETERMINED=[y] · NOISE=[z] · BACKGROUND=[w]
**Quadrant Threshold**: median ≥ 3.5 = High; < 3.5 = Low (1-5 Likert midpoint 3.0 기준)

---

#### Scoring Table

| ID | Driving Force | Importance (med·mean·σ) | Uncertainty (med·mean·σ) | Combined | Quadrant |
|---|---|---|---|---|---|
| DF01 | ... | 5.0 · 5.00 · 0.00 | 5.0 · 5.00 · 0.00 | 25.00 | CRITICAL ★ |
| ... |

#### 2×2 Matrix Visualization (medians, integer-rounded cells)

```
Importance ▲
       5 │  ·     ·     ·    DF02  DF01
       4 │  ...
         └───────────────────────────────► Uncertainty
             1     2     3     4     5
```

#### Top-2 Critical Drivers (Scenario Axes Recommendation)

1. **DF01: [name]** — Importance 5.0, Uncertainty 5.0, Combined 25.00
   - Endpoints: [low]  ↔  [high]
2. **DF02: [name]** — ...

#### Predetermined Elements (반드시 모든 scenario에 반영)

- **DF04: [name]** — anchored at: [expected trajectory]

---

#### 다음 sub-skill 전달

→ vision-foresight-scenarios-scenario-logics-selection
  (Top-2 Critical Drivers axes 권장)

---

##### Determinism Audit

- Aggregation: statistics.median / mean / pstdev (Python <ver>)
- Quadrant threshold: 3.5 (midpoint of 1-5 Likert)
- Top-2 sort key: (combined_score desc, sum_score desc, consensus_sigma asc, id asc)
- All scores produced via iu_ranker.py rank — no LLM arithmetic.
```

---

## 7. 오류 및 예외 처리

| 상황 | 결정론 동작 |
|---|---|
| `driving_forces` 수 6 미만 또는 12 초과 | `validate_input` PASS=false, 명시적 에러 메시지 |
| persona 수 6 미만 또는 8 초과 | PASS=false |
| importance/uncertainty 1-5 범위 위반 | PASS=false ("out of Likert range") |
| id 중복 | PASS=false |
| 필수 필드 누락 (id·name·scores·persona·importance·uncertainty) | PASS=false |
| Critical 사분면 force 0개 | Top-2 = NONE; 출력에 "scoring 재검토" 권고 |
| Critical 사분면 force 1개 | Top-2 list 길이 1; 정상 출력 (scenario logics가 1-axis 처리) |
| Critical force 3개 이상 | Top-2만 추천; 출력에 나머지도 표시 (분석가가 3-axis 또는 morphological 선택) |
| Critical 사분면 동률 (combined_score 동률) | 4단계 tie-break으로 deterministic 선정 (sum → sigma → id) |
| 입력 JSON 파일 없음 / 파싱 실패 | Python `json.JSONDecodeError` 전파 — 호출자가 인지 |
| 단일 persona만 입력 (n=1) | `pstdev`=0.0으로 계산, 정상 작동 (단 검증에서 persona 수 제약 위반 시 PASS=false) |

LLM은 위 어떤 사례도 자연어로 임의 처리하지 않는다 — 모든 분기는 `iu_ranker.py` 내부 결정론 분기.

---

## 8. 마스터 협업 protocol

- **입력**: § Driving Forces (JSON, Driving Forces Identifier sub-skill 결과)
- **처리**:
  1. `python3 iu_ranker.py validate_input input.json` → PASS 확인
  2. `python3 iu_ranker.py rank input.json output.md` → § Importance-Uncertainty Matrix 생성
- **출력**: § Importance-Uncertainty Matrix (markdown)
- **다음 단계**: `vision-foresight-scenarios-scenario-logics-selection` (Top-2 axes 입력)

작업 완료 시 마스터에 § Importance-Uncertainty Matrix 반환 + Determinism Audit fingerprint 포함.

---

## 9. 자체 점검 체크리스트 (sub-skill 종료 직전)

- [ ] `python3 iu_ranker.py validate` ALL_PASS=true
- [ ] 입력 schema `validate_input` PASS=true
- [ ] 출력에 § Importance-Uncertainty Matrix 헤더 정확히 포함
- [ ] Top-2 / Predetermined / Quadrant Distribution 모두 명시
- [ ] 2×2 ASCII matrix 정확히 5×5 grid
- [ ] Determinism Audit fingerprint 출력 포함
- [ ] 다음 sub-skill (`scenario-logics-selection`) 명시
