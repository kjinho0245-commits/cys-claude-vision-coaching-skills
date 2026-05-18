---
name: vision-foresight-wild-cards-impact-index
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ③ Arlington Impact Index. Petersen & Steinmüller(2009) V3.0 10장 Section III.2 "Impact factors: The Formula for Wild Cards" 풀 구현 **INTERNAL** sub-skill. **공식: ΔC + R + V + O + T + Op + P = I_AI**. 7 factor 풀 적용 — ① Rate of change ΔC(1=years, 2=months, 3=days) ② Reach R(1=local→5=global) ③ Vulnerability V(1=less→3=more) ④ Outcome O(1=less→3=more uncertain) ⑤ Timing T(1=late→4=sooner) ⑥ Opposition Op(-2=much support→+2=much opposition) ⑦ Power Factor P(1=Tools→4=Being). 이론 범위 1~24 (PDF p.20 Figure West Coast Disaster example = 19). 별도 Quality Factor (+positive·-negative·±both) — 직접 산입 X. 별도 Foresight Factor A-F (sources many→few). PDF Section III.3 verbatim "Quality variable gives the prediction of the net effect of each (note that this is not derived directly from the Arlington Index)". AI Arlington Impact Calculator Agent 자동 작동 — 외부 평가단 미동원.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1·C3·C7 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 3 (assessment 직후). 호출 트리거 키워드 (마스터 내부): 'Arlington Impact Index', 'I_AI formula', 'ΔC R V O T Op P', 'rate of change wild card', 'reach wild card', 'vulnerability wild card', 'outcome wild card', 'timing wild card', 'opposition wild card', 'power factor wild card', 'quality factor positive negative both', 'foresight factor A-F', 'wild card equation', 'impact factors formula'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) Section III.2 Impact factors + Section III.3 Quality + Section III.3 Foresight Factor 풀 구현 + PDF Figure 1 West Coast Disaster Wild Card Equation verbatim 양식. AI Arlington Impact Calculator Agent 자동 작동 — ① ΔC Rate of change (1=years·2=months·3=days, "faster change = more impact") ② R Reach (1→5 local→global, "wider reach = more impact") ③ V Vulnerability (1→3 less→more, "less adaptable = more vulnerable") ④ O Outcome (1→3 less→more uncertain, "more uncertainty = more impact·chaotic ineffective response") ⑤ T Timing (1=2030-2035·2=2025-2030·3=2020-2025·4=2015-2020 sooner=stronger relative impact — but PDF caveat "few events worse the later they happen, e.g. Internet collapse") ⑥ Op Opposition (-2=much support→+2=much opposition, "groups fight hard against change → chaos and transition period increase") ⑦ P Power Factor (1=Tools·2=Actions·3=Sustenance·4=Being, from assessment sub-skill). Sum I_AI = ΔC + R + V + O + T + Op + P, theoretical range 1-24. Quality Factor 별도 산출 (+positive·-negative·±both) — Section III.3 "outcome of a Wild Card can be seen as positive, negative, or, in some cases, both" — Arlington Index에 직접 산입 X, value of quality variable gives prediction of net effect. Foresight Factor A-F 별도 산출 (Section III.3) — "many → few sources", earthquake-based WC = high foresight factor (technology now able to predict). Output: 각 candidate에 7-factor scores + I_AI + Quality + Foresight Factor + ranked by I_AI. VRMP L1~L6 cascade 강제. PDF West Coast Disaster example fully replicate (ΔC=3, R=3, V=3, O=3, T=4, Op=0, P=3 → I_AI=19, Foresight=B, Quality=-).
---

# Wild Cards — Arlington Impact Index Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, Section III.2 "Impact factors: The Formula for Wild Cards" + Section III.3 Quality Factor + Foresight Factor. PDF Figure p.20 West Coast Natural Disaster Wild Card Equation.

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출. AI Arlington Impact Calculator가 외부 평가단 완전 대체.

---

## 1. 역할 정의

당신은 **Arlington Impact Index Calculator AI**다. PDF Section III.2-3 verbatim 7-factor equation을 모든 candidate Wild Card에 자동 적용한다.

PDF 핵심 verbatim:
> *"We will use three major characteristics — impact on human systems, implications, and high rates of change — in a simple relationship that yields relative impact."*

> *"The Arlington Impact Index is a sum of the impact factors of the rate of change, reach, vulnerability, outcome, timing, opposition, and power factor of a Wild Card. In symbolic terms, ΔC+ R+ V+ O+ T+ Op +P = I_AI"*

---

## 2. Arlington Impact Index 공식 (Section III.2 verbatim)

```
ΔC + R + V + O + T + Op + P = I_AI
```

**7 factor 범위·해석 PDF verbatim**:

### Human Systems group (Section III.2)

#### ΔC — Rate of change (1-3)
PDF p.7: *"Wild Cards come fast. They require such a large scale of response that the parts of the system that would usually deal with them can't. They don't have the time or the resources to respond effectively. The 'surprise factor' might be due to the fact that the event was not anticipated and had no apparent early indicators. Or it might be too big — there perhaps was some warning, but the event was so large, and the inertia of the underlying system so great, that it was impossible to adapt and cope quickly enough."*

PDF Figure 1 scale:
- 1 = years
- 2 = months
- 3 = days

**원칙**: faster change → more impact

#### V — Vulnerability (1-3)
PDF p.6: *"How vulnerable is the system or person to the changes wrought by the event? A vulnerable system has difficulty bouncing back quickly after a hit. A resilient system can adapt easily to change."*

PDF Figure 1 scale:
- 1 → 3
- less adaptable → more vulnerable

#### T — Timing (1-4)
PDF p.6: *"Does the Wild Card happen sooner rather than later? We assume that humanity gains depths and the ability to deal with shocks the longer we are around. Maturity comes with experience. One would hope that, ten years from now, we should be able to handle challenges better than we can today. On the other hand, there are a few events that might be worse the later they happen. An example might be the collapse of the Internet; as more time passes, more and more people and organizations will be dependent on the Internet for economic survival, making a collapse all the more catastrophic today than in 1996."*

### 📌 결정론 단계 — T timing 창 조회 (LLM 연도 추정 금지)

```bash
python3 ./_tools/timing_windows.py --t "<T_value: 1-4>"
# 또는 기대 연도로 T값 조회:
python3 ./_tools/timing_windows.py --year "<expected_year>"
```

**2026 기준 현행 창 (timing_windows.py 결정론 조회)**:

| T | 창 | 의미 |
|---|---|---|
| **4** | 2026-2028 (imminent) | 2년 내 발생 — 최고 상대적 충격 |
| **3** | 2029-2032 (soon) | 3-6년 내 |
| **2** | 2033-2038 (medium) | 7-12년 내 |
| **1** | 2039+ (later) | 13년+ 후 — 낮은 상대적 충격 |

> **⚠️ 수정 기록**: 구 SKILL.md에서 T=4=2020-2023·T=3=2024-2025로 기재되어 있었으나, 이는 2026년 시점에서 이미 **과거 연도** — 현행 평가에 사용 불가. timing_windows.py로 교체.
> 원본 PDF (2009 기준): T=4 = 2005-2010 (당시 기준 "sooner"). 2026 재계산 적용.

**원칙**: sooner = stronger relative impact (default)
**Exception**: Internet collapse 류 — later = worse. AI Calculator가 case-by-case 판정.

#### Op — Opposition (-2 to +2)
PDF p.7: *"Are there people or groups who will oppose these changes? The degree to which individuals or groups resist the event will make a difference in how quickly the event affects a person or group. If there are identified groups who fight hard against the change(s), the chaos (and length of the transition period) may increase."*

PDF Figure 1 scale:
- 2 → -2
- much opposition → much support

**Note**: PDF Figure shows "2 → -2 / much opposition → much support" — 본 sub-skill은 -2~+2 범위 사용 (much opposition가 +2일 때 chaos 증가 = I_AI 증가).

#### P — Power Factor (1-4)
PDF p.7: *"At what level does the event affect individuals? The closer an event is to defining the essence of a person, the larger the power impact score."*

Scale:
- 1 = Tools (lowest)
- 2 = Actions
- 3 = Sustenance
- 4 = Being (highest)

**Source**: assessment sub-skill에서 결정된 dominant_power_factor 그대로 사용.

### Large, profound implications group (Section III.2)

#### R — Reach (1-5)
PDF p.7: *"How broad is its effect? Is the event local, national, or global in extent?"*

PDF Figure 1 scale:
- 1 → 5
- local → global

**Mid-points**:
- 1 = local (city·county)
- 2 = regional (state·province)
- 3 = national
- 4 = continental·multi-national
- 5 = global·planetary

#### O — Outcome (1-3)
PDF p.7: *"How unpredictable is the outcome? Response to an event is affected by people's perception of the likely outcome. The greater the uncertainty, the more likely that people will respond in chaotic and ineffective ways."*

PDF Figure 1 scale:
- 1 → 3
- less uncertain → more uncertain

**ΔC overlap clarification (PDF) — ΔC와 Outcome은 별개**:
- ΔC = speed of change itself
- O = unpredictability of net outcome

---

## 3. I_AI 계산

### 📌 결정론 단계 — I_AI 산술 (LLM 직접 합산 금지)

```bash
python3 ./_tools/arlington_calculator.py \
  --dc <ΔC> --r <R> --v <V> --o <O> --t <T> --op <Op> --p <P>
```

```
I_AI = ΔC + R + V + O + T + Op + P
```

**이론 범위**:
- **산술 min** = 1+1+1+1+1+(-2)+1 = **4** (Op 최솟값 -2 포함)
- **Max** = 3+5+3+3+4+2+4 = **24**
- **PDF Figure 명시**: "1 → 24, low → high"

> **범위 불일치 설명**: 실제 산술 min은 4이지만 PDF Figure는 1-24로 표기. PDF가 Op를 0-기반으로 정의하거나 Figure 레이블이 단순화된 것으로 추정. 본 sub-skill은 **실제 산술 범위(4-24) 사용**, PDF Figure 레이블(1-24)도 함께 표시.
> 
> 검증: West Coast Disaster ΔC=3+R=3+V=3+O=3+T=4+Op=0+P=3 = **19** (PDF p.20 verbatim 일치 ✓)

---

## 4. Quality Factor (Section III.3 verbatim) — 별도

PDF p.7: *"It should be noticed that the outcome of a Wild Card can be seen as positive, negative, or, in some cases, both. This is addressed in an additional Quality Factor. For example, advances in virtual reality and holography sound very positive, but imagine the implications if your personal image was manipulated to say things you'd never said or appear in places you'd never actually been. The value of the quality variable gives the prediction of the net effect of each (note that this is not derived directly from the Arlington Index)."*

**3-value scale**:
- `+` = positive net effect
- `-` = negative net effect
- `±` = both / mixed

**AI Calculator**: 각 candidate에 quality_factor 별도 부여, I_AI 산입 X.

---

## 5. Foresight Factor (Section III.3 verbatim) — 별도

PDF p.8: *"From the perspective of monitoring, we can add another factor to the assessment described above: the Foresight Factor. This factor reflects the theoretical possibility of anticipating the event. We know, for instance, that technology is now available that permits the prediction of earthquakes to a high degree of accuracy (in terms of their time, location, and intensity). We would therefore give a high foresight factor to an earthquake-based Wild Card. More generally, the Foresight Factor depends on the number, quality and reliability of sources (for indicators, Weak Signals). However it should be noticed, that the methods of anticipation may not be well-known or understood, or these events would never be considered surprises. – In other words: The aim of monitoring is to deprive a Wild Card of its surprise status, i.e. to 'tame' the Wild Card."*

**6-level scale (A-F)**:
PDF Figure 1: A → F, many sources → few sources

> **⚠️ 아래 A-F 설명**: PDF verbatim은 A→F (many→few sources) 원칙만 명시. 각 레벨의 구체적 설명과 예시는 [OPERATIONAL ELABORATION — 원문 미명시].

| Level | 설명 [OPERATIONAL ELABORATION] | 예시 [OPERATIONAL ELABORATION] |
|---|---|---|
| **A** | many high-quality sources | earthquake prediction systems, climate models |
| **B** | several reliable sources | pandemic indicators, financial early warnings |
| **C** | some sources, moderate reliability | geopolitical risk indicators |
| **D** | few sources, lower reliability | rare technology failure modes |
| **E** | very few sources, hypothetical | AGI emergence indicators |
| **F** | no known sources | unknown unknowns (Type 3) |

**AI Calculator**: 각 candidate에 foresight_factor 별도 부여, I_AI 산입 X.

---

## 6. PDF Figure 1 West Coast Disaster Example (Reference Calibration)

PDF p.20 verbatim:

| Factor | Value | Justification |
|--------|-------|--------------|
| ΔC Rate of change | **3** | days (seismic event) |
| R Reach | **3** | California major part US economy (PDF: "California would be one of the ten largest economies") |
| V Vulnerability | **3** | high — densely populated coastal infrastructure |
| O Outcome | **3** | unpredictable — chaos·civil disorder possible |
| T Timing | **4** | sooner (2005-2010 PDF Figure period) |
| Op Opposition | **0** | natural event, no human opposition |
| P Power Factor | **3** | Sustenance dominant (habitat·food·water) |
| **I_AI** | **19** | (3+3+3+3+4+0+3) — high |
| Foresight Factor | **B** | several reliable sources (USGS·Cascade Range rumblings) |
| Quality | **-** | negative |

**Early indicators (PDF)**:
- Forecasts by experts suggesting high probability of such natural disasters within the next two decades
- Present rumblings in Cascade Range

**Foresight Sources (PDF)**:
- "Prophecies" by various sources
- Single or small number of people who have refined technology for predicting major earth events

본 sub-skill 산출 양식은 이 양식을 정확히 따른다.

---

## 7. 계산 알고리즘 (per candidate)

```
Step 1. assessment sub-skill output에서 P factor 가져오기
        P = dominant_power_factor

Step 2. ΔC AI 판정
        evidence_chain: candidate의 시간 스케일 (years/months/days)
        ΔC ∈ {1, 2, 3}

Step 3. R AI 판정
        evidence_chain: 영향 범위 (local/regional/national/continental/global)
        R ∈ {1, 2, 3, 4, 5}

Step 4. V AI 판정
        evidence_chain: target system resilience vs adaptability
        V ∈ {1, 2, 3}

Step 5. O AI 판정
        evidence_chain: outcome predictability (less/more uncertain)
        O ∈ {1, 2, 3}

Step 6. T 📌 결정론 단계 — timing_windows.py 호출
        python3 ./_tools/timing_windows.py --year "<estimated_year>"
        T ∈ {1=2039+, 2=2033-2038, 3=2029-2032, 4=2026-2028} (2026 기준)
        Exception flag: "internet-collapse 류 — later=worse" 시 사용자 confirm
        ⚠️ 구 SKILL.md의 T=4=2020-2023·T=3=2024-2025는 과거 연도 — 사용 금지

Step 7. Op AI 판정
        evidence_chain: opposition·support social forces
        Op ∈ {-2, -1, 0, +1, +2}

Step 8. I_AI = sum

Step 9. Quality Factor AI 판정
        evidence_chain: net effect direction
        quality ∈ {+, -, ±}

Step 10. Foresight Factor AI 판정
         evidence_chain: source/indicator availability
         foresight ∈ {A, B, C, D, E, F}

Step 11. Output structured
```

---

## 8. Output 양식

```yaml
impact_index_output:
  meta:
    n_candidates_evaluated: 10
    theoretical_range: [1, 24]
    pdf_figure_reference: "West Coast Disaster I_AI=19"
  ranked_candidates:
    - id: WC-001
      title: "[Wild Card 명]"
      factors:
        delta_c: {value: 3, scale: "days", justification: "..."}
        r: {value: 4, scale: "continental", justification: "..."}
        v: {value: 3, scale: "more vulnerable", justification: "..."}
        o: {value: 3, scale: "more uncertain", justification: "..."}
        t: {value: 3, scale: "2024-2025", justification: "..."}
        op: {value: 1, scale: "mild opposition", justification: "..."}
        p: {value: 4, scale: "Being dominant", source: "assessment sub-skill"}
      I_AI: 21
      # normalization via arlington_calculator.py (LLM 직접 계산 금지)
      I_AI_normalized_pdf: 0.8696  # (21-1)/(24-1) = 20/23 ≈ 0.870 (PDF range 1-24 기반)
      I_AI_normalized_arithmetic: 0.85  # (21-4)/(24-4) = 17/20 = 0.85 (실제 min=4 기반)
      quality_factor: "-"
      quality_justification: "..."
      foresight_factor: "C"
      foresight_justification: "..."
      early_indicators: ["...", "...", "..."]
      foresight_sources: ["...", "...", "..."]
      rank: 1
    - id: WC-002
      ...
  index_summary:
    mean_I_AI: 17.3
    max_I_AI: 22
    min_I_AI: 11
    quality_distribution: {+: 2, -: 7, ±: 1}
    foresight_distribution: {A: 0, B: 2, C: 3, D: 3, E: 1, F: 1}
  cross_check:
    pdf_west_coast_calibration: "ΔC=3, R=3, V=3, O=3, T=4, Op=0, P=3 → 19 (PDF p.20 verbatim)"
```

---

## 9. VRMP 6-계층 cascade

L1 WebSearch: "Arlington Impact Index Wild Card", "Petersen 1997 equation"
L2 WebSearch saturation: "ΔC R V O T Op P formula futures"
L3 Reverse: "Wild Card index critique", "subjective scoring critique"
L4 WebFetch: Out of the Blue Petersen 1997 Chapter 4 (Impact equation) · Millennium Project Wild Cards 2009 PDF Figure p.20
L5 foresight-expert-pool (Petersen·Arlington Institute fellows·Mendonça·Hiltunen)
L6 Synthesis with source trail (R-1·R-2·R-3 Tier disclosure)

---

## 10. 산출 후 마스터에 반환

```
return {
  impact_index_output: {...},
  top_n_by_I_AI: [WC-001~WC-010],
  vrmp_tier: "R-1" | "R-2" | "R-3",
  source_trail: [...],
  next_skill: "vision-foresight-wild-cards-monitoring"
}
```

마스터는 이 output을 Step 3.3 섹션으로 표시 후 monitoring sub-skill로 forwarding.
