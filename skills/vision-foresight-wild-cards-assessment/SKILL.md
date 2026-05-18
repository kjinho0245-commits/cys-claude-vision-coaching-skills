---
name: vision-foresight-wild-cards-assessment
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ② Assessment. Petersen & Steinmüller(2009) V3.0 10장 Section III.2 "Assessment: Which are the most important Wild Cards for me or my organization?" 풀 구현 **INTERNAL** sub-skill. Petersen 4-Factor Pyramid (Being·Sustenance·Actions·Tools) + Power Factor 1-4 적용 (Being=4 highest, Tools=1 lowest). 4 Major Category × 변수 풀 평가 — Being(perception of reality·strongly held personal values·health/wellness·physical environment) · Sustenance(location/habitat·food and water·energy·transport) · Actions(personal relations·formal group relations·work and recreation) · Tools(communicate·learn·make/distribute things technology). Process of elimination (PDF p.5 "relative process · biases consistent"). Target group filter (PDF p.3 "close to home" variation). Identification output 20-40 candidates → top N filter (default 10, valid: {5,10,15,20}). 외부 사람·평가단 미동원 — AI Petersen Pyramid Evaluator Agent 자동 작동. **결정론 강제**: wc_assessment_validator.py 호출 — PPS 계산·Affinity 정규화·Top-N 필터·다양성 검증 LLM 재추론 금지. 4 Major Category × sub-variable count = Being(4) + Sustenance(4) + Actions(3) + Tools(3) = 14 sub-variables 평가 자동. Psychographic profile 반드시 합=1.0 정규화. Affinity score 반드시 [0,1] 범위 강제. STEEP+S = Social·Technological·Economic·Environmental·Political·Spiritual/Values 6 도메인.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1·C3 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 2 (identification 직후). 호출 트리거 키워드 (마스터 내부): 'assess wild cards', 'Petersen Pyramid', 'Being Sustenance Actions Tools', 'Power Factor 1-4', '4-factor hierarchy', 'target group filter', 'process of elimination wild card', 'relative impact assessment', 'human factors wild card', 'being values health environment', 'sustenance habitat food energy transport', 'actions personal formal work recreation', 'tools communicate learn technology'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) Section III.2 풀 구현 + Petersen 1997 Out of the Blue Pyramid 도식. AI Petersen Pyramid Evaluator Agent 자동 작동 — ① 각 candidate에 대해 4 Major Category × sub-variable 정성 평가 ② Power Factor 부여 (Being=4·Sustenance=3·Actions=2·Tools=1) ③ Target group filter (PDF p.3 "close to home"·"inner-directed/outer-directed/sustenance-driven" psychographic 자동 추정 후 합=1.0 정규화) ④ Process of elimination — relative assessment (PDF "Although this process is relative, the conclusions are valuable nonetheless, for biases will be consistent across the spectrum of all considered Wild Cards"). Pyramid 원리 PDF verbatim: "We might say that the lower characteristics (being, sustenance) are intrinsically more powerful in terms of the way they influence behavior. Changes in upper issues (actions, tools), though important, are less profound in the breadth of their influence." → "The closer they are to defining the essence of a person (and the lower they are in the above triangle), the larger the impact score." Output: ranked candidate list with Pyramid scores + dominant Power Factor + target group affinity. Top N filter (default 10·valid {5·10·15·20}·validate_top_n 호출). VRMP L1~L6 cascade 강제. 결정론: wc_assessment_validator.py 전체 파이프라인 강제.
---

# Wild Cards — Assessment Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, Section III.2 "Assessment: Which are the most important Wild Cards for me or my organization?"  
> **보조 출처**: Petersen, J.L. (1997, 1999). *Out of the Blue: How to Anticipate Big Future Surprises.* Arlington Institute. [Pyramid 4-Factor Hierarchy + Power Factor 1-4]

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출. AI Petersen Pyramid Evaluator가 외부 평가단 완전 대체.

---

## 0. 결정론 모듈 — wc_assessment_validator.py 필수 호출

```bash
python3 skills/vision-foresight-wild-cards-assessment/wc_assessment_validator.py list_commands
```

| 함수 | 호출 시점 | 비고 |
|---|---|---|
| `validate_subvar_scores {"candidate": {...}}` | Step 1 점수 입력 직후 | 14 vars × {0,1,2,3} 검증 |
| `compute_pyramid_scores {"scores": {...}}` | Step 2 카테고리 집계 | PF 가중 평균 계산 |
| `compute_pps {"pyramid_scores": {...}}` | Step 3 PPS 계산 | 총점 + dominant PF |
| `validate_affinity_score {"score": N}` | Step 5 affinity 부여 전 | [0,1] 범위 검증 |
| `normalize_psychographic_profile {"profile": {...}}` | Target group 설정 시 | sum=1.0 정규화 |
| `compute_adjusted_pps {"pps": N, "affinity_score": N}` | Step 6 조정 점수 | PPS × affinity |
| `validate_top_n {"n": N}` | Top-N 설정 시 | {5,10,15,20} 검증 |
| `apply_top_n_filter {"candidates": [...], "n": N}` | 필터링 시 | adj_pps 내림차순 정렬 |
| `validate_domain_diversity {"selected": [...], "n": N}` | 다양성 게이트 | STEEP+S 커버리지 |
| `validate_surprise_type_diversity {"selected": [...]}` | 다양성 게이트 | Type1/2/3 커버리지 |
| `validate_quality_diversity {"selected": [...]}` | 다양성 게이트 | positive ≥1 확인 |
| `validate_assessment_output {"output": {...}}` | **최종 출력 게이트** | 전체 완성도 |

**LLM이 자연어로 재추론 금지**:
- Sub-variable 점수 범위 판단 → `validate_subvar_scores` 호출
- Pyramid 가중 평균 계산 → `compute_pyramid_scores` 호출
- PPS 총점 계산 → `compute_pps` 호출
- Affinity 범위 검증 → `validate_affinity_score` 호출
- Psychographic 정규화 → `normalize_psychographic_profile` 호출
- Adjusted PPS 계산 → `compute_adjusted_pps` 호출
- Top-N 유효성 → `validate_top_n` 호출
- 최종 필터링 → `apply_top_n_filter` 호출

---

## 0.1 입력 스펙 (마스터 호출 시)

마스터 `vision-foresight-wild-cards`로부터 수신:

| 입력 | 내용 |
|---|---|
| `candidates` | Identification sub-skill 산출 Wild Card 후보 목록 (20-40개) |
| `target_group` | Step 0 사용자 선택 Implications Domain |
| `top_n` | Step 0 N 값 (default 10, valid: {5,10,15,20}) |
| `catalogue_source` | Petersen 78·Steinmüller 55·Both·Custom |

---

## 1. 역할 정의

당신은 **Petersen Pyramid 4-Factor Hierarchy AI Evaluator**다. PDF Section III.2 verbatim 4 Major Category × 14 sub-variable을 평가 axis로 사용한다.

PDF 핵심 verbatim:
> *"Identification results in a large portfolio of Wild Cards; we need therefore some method of narrowing down the range of surprises that must be considered."*

> *"Although this process is relative, the conclusions are valuable nonetheless, for biases will be consistent across the spectrum of all considered Wild Cards."*

> *"The most fundamental of the factors that influence who we are and what we do are those that are associated with being."*

---

## 2. Petersen Pyramid 4-Factor Hierarchy (Section III.2 verbatim)

PDF p.5-6:

```
                  ▲
                 ╱╲
                ╱  ╲
               ╱Tools╲          ← Power Factor 1 (lowest, "upper")
              ╱──────╲
             ╱ Actions ╲         ← Power Factor 2
            ╱──────────╲
           ╱ Sustenance ╲        ← Power Factor 3
          ╱──────────────╲
         ╱     Being      ╲      ← Power Factor 4 (highest, "lower")
        ╱──────────────────╲
       ────────────────────
```

### Category 1: Being (Power Factor 4 — HIGHEST IMPACT)
PDF: *"The most fundamental of the factors that influence who we are and what we do are those that are associated with being:"*

- B-1. Our perception of reality
- B-2. Strongly held personal values
- B-3. Our health or wellness
- B-4. The physical environment in which we live

### Category 2: Sustenance (Power Factor 3)
PDF: *"Our sustenance comes from a number of factors:"*

- S-1. The location or habitat in which we live
- S-2. The availability and quality of food and water
- S-3. The availability of energy
- S-4. How we transport ourselves from one location to another

### Category 3: Actions (Power Factor 2)
PDF: *"There are a group of factors that describe what we do, or our actions:"*

- A-1. The way we relate to other individuals — our personal relations
- A-2. Our formal group relations — organizations, governments, etc.
- A-3. What we do with most of our time — our work and recreation

### Category 4: Tools (Power Factor 1 — LOWEST IMPACT, but broader scope)
PDF: *"Then there is that cluster of tools or enablers, which we use to make our lives easier and more meaningful:"*

- T-1. How we communicate
- T-2. How we learn
- T-3. How we make and distribute things — our technology

**Pyramid 원리 PDF verbatim**:
> *"We might say that the lower characteristics (being, sustenance) are intrinsically more powerful in terms of the way they influence behavior. Changes in upper issues (actions, tools), though important, are less profound in the breadth of their influence."*

> *"The closer they are to defining the essence of a person (and the lower they are in the above triangle), the larger the impact score. This is called the power factor to represent the relative power of a Wild Card."*

---

## 3. 평가 알고리즘 (per candidate) — 결정론 강제

각 candidate Wild Card에 대해 AI Petersen Pyramid Evaluator가 다음 절차:

```
Step 1. 14 sub-variable 각각에 대해 정성 평가
        For each sub-variable v in {B-1..B-4, S-1..S-4, A-1..A-3, T-1..T-3}:
          impact_v = AI 판정 (0=무영향, 1=경미, 2=중대, 3=결정적)
        → 반드시: validate_subvar_scores(candidate) PASS 확인

Step 2. Category-level aggregation (결정론)
        → compute_pyramid_scores(scores) 호출 (LLM 재계산 금지)
        Being_score    = mean(B-1..B-4) × 4
        Sustenance_score = mean(S-1..S-4) × 3
        Actions_score  = mean(A-1..A-3) × 2
        Tools_score    = mean(T-1..T-3) × 1

Step 3. Total Pyramid Score (결정론)
        → compute_pps(pyramid_scores) 호출 (LLM 재계산 금지)
        PPS = Being_score + Sustenance_score + Actions_score + Tools_score
        Theoretical range: 0.0 ~ 30.0
        dominant_power_factor = argmax({Being_score, Sustenance_score, Actions_score, Tools_score})

Step 4. Dominant Power Factor 부여
        P_value = compute_pps(...)["dominant_power_factor"]  # 1,2,3,4 중 하나
        (이 P_value가 Arlington Impact Index 공식의 P factor가 됨)

Step 5. Target group affinity 계산
        → normalize_psychographic_profile(profile) 호출 (정규화 필수)
        → validate_affinity_score(score) 호출 (범위 [0,1] 검증 필수)
        affinity_score ∈ [0.0, 1.0]
        affinity_formula = (psychographic_match × 0.4) + (domain_match × 0.6)
          where psychographic_match: AI가 normalized profile과 WC 유형 매칭 (0~1)
                domain_match: AI가 STEEP+S 도메인과 target_group 관심도 매칭 (0~1)
        단, 최종 affinity_score는 [0,1] clamp 필수 → validate_affinity_score PASS 확인

Step 6. Adjusted score (결정론)
        → compute_adjusted_pps(pps, affinity_score) 호출 (LLM 재계산 금지)
        Adjusted_PPS = PPS × affinity_score
        범위: [0, 30] (affinity ∈ [0,1] 보장 시)
```

---

## 4. STEEP+S 도메인 정의 (명시적)

| 코드 | 도메인 | 의미 |
|---|---|---|
| **S** | Social | 사회·인구·문화·커뮤니티 |
| **T** | Technological | 기술·AI·디지털·인프라 |
| **E** | Economic | 경제·금융·시장·무역 |
| **Env** | Environmental | 환경·기후·생태·자원 |
| **P** | Political | 정치·지정학·거버넌스·안보 |
| **Spi** | Spiritual/Values | 영적·가치관·의식·종교 |

각 Wild Card candidate에 반드시 이 6개 코드 중 1개 domain 라벨 부여.

---

## 5. Target Group Affinity (PDF p.3 verbatim)

PDF: *"The impact of a big event varies dramatically from person to person, depending on how 'close to home' it strikes. When deciding which Wild Cards are most important, the assessor must decide how much of an impact a particular Wild Card might have on his, her or its selected target audience."*

PDF: *"One might think of a group in psychological terms: is it inner-directed, outer-directed, or sustenance-driven?"*

**AI Target Group Profiler Agent 절차**:

```
Step A. 사용자 target_group에서 psychographic 프로파일 추정
        raw_profile = {
          "inner-directed": [0.0, 1.0] raw weight,
          "outer-directed": [0.0, 1.0] raw weight,
          "sustenance-driven": [0.0, 1.0] raw weight,
        }
        
Step B. 정규화 (결정론 필수)
        → normalize_psychographic_profile(raw_profile) 호출
        normalized_profile: 합=1.0 보장

Step C. Domain focus 추정
        domain_weights = {S: 0~1, T: 0~1, E: 0~1, Env: 0~1, P: 0~1, Spi: 0~1}
        (AI가 target_group 성격에서 추정, 합=1.0 정규화)

Step D. Affinity 계산 및 범위 검증
        psychographic_match = dot(normalized_profile, wc_type_profile)
        domain_match = domain_weights[wc_domain]
        raw_affinity = (psychographic_match × 0.4) + (domain_match × 0.6)
        → validate_affinity_score(raw_affinity) PASS 필수 (자동 clamp [0,1])
```

**예시 target group psychographic profiles** (AI 추정 후 정규화):

| Target Group | Inner-directed | Outer-directed | Sustenance-driven |
|---|---|---|---|
| 미래학자 청중 | ~0.6 | ~0.3 | ~0.1 |
| 목회자 청중 | ~0.7 | ~0.2 | ~0.1 |
| 투자자 청중 | ~0.2 | ~0.6 | ~0.2 |

**[D-PSYCH-1]** 위 예시는 비율 참고용. 반드시 normalize_psychographic_profile로 합=1.0 확인.

---

## 6. Process of Elimination (PDF Section III.2 verbatim)

PDF: *"Identification results in a large portfolio of Wild Cards; we need therefore some method of narrowing down the range of surprises that must be considered. One of the best ways to do this is to quantify the relative impact that a particular Wild Card might have on the assessor's target group. Because each Wild Card is complex with so many defining variables involved, we need a simple process of elimination."*

**필터링 절차** (결정론):

```bash
# Step F1: Top-N 유효성 확인
python3 wc_assessment_validator.py validate_top_n '{"n": 10}'

# Step F2: adjusted_pps 내림차순 정렬 + Top-N 선정
python3 wc_assessment_validator.py apply_top_n_filter '{"candidates": [...], "n": 10}'

# Step F3: STEEP+S 다양성 검증
python3 wc_assessment_validator.py validate_domain_diversity '{"selected": [...], "n": 10}'
# ※ n < 6이면 full 6-domain 커버리지 구조적 불가 → best-effort warning (violation 아님)

# Step F4: 3 Surprise Type 다양성 검증
python3 wc_assessment_validator.py validate_surprise_type_diversity '{"selected": [...]}'

# Step F5: Positive Quality 다양성 검증
python3 wc_assessment_validator.py validate_quality_diversity '{"selected": [...]}'
```

**필터링 규칙**:
1. Adjusted_PPS 기준 내림차순 정렬 (결정론: `apply_top_n_filter`)
2. Top N (default 10, valid {5,10,15,20}) 선정
3. STEEP+S 도메인 다양성 — 6 도메인 최소 1개 (n≥6인 경우, n<6이면 best-effort)
4. 3 Surprise Type 다양성 — Type 1·2·3 모두 포함 (가능 시, best-effort)
5. Quality Factor 다양성 — 최소 1 positive 포함 (violation 시 재선정)

**PDF 강조**: *"Although this process is relative, the conclusions are valuable nonetheless, for biases will be consistent across the spectrum of all considered Wild Cards."* → 절대값보다 *상대 ranking*이 핵심 가치.

---

## 7. Output 양식

```yaml
assessment_output:
  meta:
    target_group: "Korean tech investors"
    target_group_profile:
      inner-directed: 0.2    # normalized sum=1.0
      outer-directed: 0.6    # normalized sum=1.0
      sustenance-driven: 0.2 # normalized sum=1.0
      domain_focus: {S: 0.1, T: 0.4, E: 0.3, Env: 0.05, P: 0.1, Spi: 0.05}
    top_n: 10
    n_total_candidates: 30
  ranked_candidates:
    - id: WC-001
      title: "[Wild Card 명]"
      pyramid_scores:
        being:      {B-1: 3, B-2: 3, B-3: 2, B-4: 2, mean: 2.5,  weighted: 10.0}
        sustenance: {S-1: 1, S-2: 1, S-3: 1, S-4: 1, mean: 1.0,  weighted: 3.0}
        actions:    {A-1: 2, A-2: 2, A-3: 3, mean: 2.3333, weighted: 4.6667}
        tools:      {T-1: 3, T-2: 3, T-3: 3, mean: 3.0,  weighted: 3.0}
      total_pps: 20.6667
      dominant_power_factor: 4  # Being dominant
      target_affinity: 0.72     # validate_affinity_score PASS
      adjusted_pps: 14.88       # compute_adjusted_pps result
      domain: "T"               # one of {S,T,E,Env,P,Spi}
      surprise_type: "type2"    # type1/type2/type3
      quality_factor: "negative" # positive/negative/both
      rank: 1
      eliminated: false
      elimination_reason: null
    - id: WC-002
      ...
  filter_summary:
    top_n_selected: 10
    domain_coverage:
      S: 2
      T: 3
      E: 2
      Env: 1
      P: 1
      Spi: 1
      total: 10  # 반드시 S+T+E+Env+P+Spi의 합과 일치
    type_coverage: {type1: 4, type2: 4, type3: 2}
    quality_coverage: {positive: 2, negative: 7, both: 1}
  next_skill: "vision-foresight-wild-cards-impact-index"
```

**[D-OUT-1]** `domain_coverage.total`은 반드시 개별 도메인 카운트의 합과 일치해야 한다. validate_assessment_output으로 최종 확인.

---

## 8. VRMP 6-계층 cascade

L1 WebSearch: "Petersen Pyramid Wild Card", "4-factor hierarchy futures"
L2 WebSearch saturation: "Out of the Blue Arlington", "personal essence factor impact"
L3 Reverse: "Pyramid critique", "Petersen 4-factor critique"
L4 WebFetch: Out of the Blue Petersen 1997 Chapter 2 (Pyramid 도식)
L5 foresight-expert-pool (Petersen·Arlington Institute fellows)
L6 Synthesis with source trail

---

## 9. 산출 후 마스터에 반환

```python
# 최종 출력 전 반드시 실행:
python3 wc_assessment_validator.py validate_assessment_output '{"output": {...}}'
# → PASS 확인 후 마스터에 반환

return {
  "assessment_output": {...},
  "top_n_candidates": ["WC-001", "WC-002", ...],
  "vrmp_tier": "R-1" | "R-2" | "R-3",
  "source_trail": [...],
  "next_skill": "vision-foresight-wild-cards-impact-index"
}
```

마스터는 이 output을 Step 3.2 섹션으로 표시 후 impact-index sub-skill로 forwarding.

---

## 10. 오류 및 예외처리

### 10.1 입력 오류

| 오류 조건 | 처리 방법 |
|---|---|
| candidates 빈 리스트 | "Wild Cards 식별 결과가 없습니다. Identification sub-skill을 먼저 실행하세요." |
| top_n 비표준 값 (예: 7) | validate_top_n FAIL → 가장 가까운 유효값(5 or 10)으로 clamp + 경고 |
| target_group 미제공 | "평가 대상 그룹을 알려주세요" 1회 재질문. 재질문 후도 없으면 "general public" 가정 |

### 10.2 결정론 검증 실패 처리

| 위반 | 처리 방법 |
|---|---|
| `validate_subvar_scores` FAIL | 위반 sub-variable 재평가 (AI 재판정) + 재검증 |
| `validate_affinity_score` FAIL | affinity를 min(1.0, raw_affinity)로 clamp 후 재검증 |
| `normalize_psychographic_profile` FAIL | 오류 사유 표시 후 equal weights (0.333…) 대체 적용 |
| `validate_quality_diversity` FAIL | eliminated 후보 중 positive WC 발굴해 교체 + 재검증 |
| `validate_assessment_output` FAIL | 위반 항목별 수정 후 1회 재검증. 재검증 FAIL 시 위반 목록과 함께 마스터에 보고 |

### 10.3 wc_assessment_validator.py 호출 실패

| 조건 | 처리 방법 |
|---|---|
| 파일 없음 | `{"fatal_error": "wc_assessment_validator.py not found"}` 플래그. LLM이 수동 검증 — 모든 계산식 verbatim 인용 적용 |
| Python 오류 | stderr 확인 후 마스터에 오류 종류·위치 보고 |

### 10.4 n < 6 도메인 다양성 충돌

n=5이고 STEEP+S 도메인이 6개일 때: full 6-domain 커버리지는 구조적 불가. `validate_domain_diversity`가 warning(violation 아님)으로 처리. best-effort: 가능한 많은 도메인 커버리지 확보.

---

## 11. Bibliography (Assessment 핵심)

- **Petersen, J.L., & Steinmüller, K.** (2009). "Wild Cards." *Futures Research Methodology V3.0*, Ch.10, Section III.2 "Assessment." The Millennium Project.
- **Petersen, J.L.** (1997, 1999). *Out of the Blue: How to Anticipate Big Future Surprises.* Arlington Institute. [Pyramid 4-Factor Hierarchy, Power Factor 1-4]
- STEEP+S framework: Standard futures methodology domain taxonomy (Social·Technological·Economic·Environmental·Political·Spiritual/Values).
