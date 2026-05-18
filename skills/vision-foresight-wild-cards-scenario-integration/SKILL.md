---
name: vision-foresight-wild-cards-scenario-integration
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ⑥ Scenario Integration (Cycle C6·C7). Petersen & Steinmüller(2009) V3.0 10장 Section V "Use with Other Methods" 풀 구현 **INTERNAL** sub-skill. PDF 핵심 verbatim: "Wild Cards are quite effective when used with scenario-building" (Wack 1985). Steinmüller 1997 **6 selection rules** 자동 적용 — ① appropriate to situation ② original and new ③ "barely possible" prioritized ④ analysis not limited to 2-3 ⑤ negative WCs first (test scenario stability) ⑥ contextual + peripheral combined. 4 scenario-WC usage modes (PDF Section V): test susceptibility · compensate weak points in mental map · recognize new alternatives · fight wishful thinking / hyper worst case. ALARM EU 6th Framework Program modeling case 자동 implementation — energy price shocks·contagious natural epidemics·thermohaline collapse North Atlantic cooling as exogenous excitation. AI Scenario Integrator Agent 자동 작동 — 외부 시나리오 워크샵 미동원.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C6·C7 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 6 (options-action 직후, Cycle C6 시). 호출 트리거 키워드 (마스터 내부): 'scenario integration wild card', 'Wack 1985 scenario rapids', 'Steinmüller 1997 6 rules', 'scenario susceptibility test', 'compensate mental map', 'hyper worst case thinking', 'ALARM EU 6th Framework', 'exogenous excitation modeling', 'sensitivity analysis wild card', 'energy price shock scenario', 'thermohaline collapse', 'pandemic scenario integration', 'positive negative both wild card scenario', 'plausible scenario disruption'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) Section V 풀 구현 + Steinmüller 1997 *The Future as Wild Card* SFZ-Werkstattbericht 20 6 selection rules + Wack 1985 *Scenarios: Shooting the Rapids* HBR Nov-Dec + ALARM EU project case verbatim. AI Scenario Integrator Agent 자동 작동 — ① PDF 4 scenario-WC usage modes 적용 (susceptibility test·weak points compensation·new alternatives·anti-wishful-thinking) ② Steinmüller 6 rules selection — Rule 1 appropriate·Rule 2 original/new consequences not immediately apparent·Rule 3 "barely possible" used more·Rule 4 analysis ≥ 4 WCs (not limited to 2-3)·Rule 5 negative WCs considered first as scenario stability test·Rule 6 contextual + peripheral combine ③ Outside expertise integration (PDF "incorporate outside expertise into the study, either through interviews or a workshop" → AI persona panel) ④ ALARM modeling — exogenous excitation introduced periodically or random times, sensitivity analysis quantitative impacts. PDF Section V verbatim 4 mode: ① "Wild Cards can be used in order to estimate the susceptibility of a scenario to external disruptions" ② "They can be used to compensate for potential weak points in the conceptual framework (mental map)" ③ "They can help recognize new alternatives and be open-minded about the 'unexpected'" ④ "Finally, they can be used to fight such common weaknesses as lack of imaginative capacity, wishful thinking or fixation on catastrophic scenarios ('hyper worst case thinking')". Output: scenario × Wild Card matrix + stability test results + ALARM-style sensitivity quantitative output + modified scenario set with WC perturbations. Cross-skill foresight-cross-impact-analysis (events 후보)·vision-foresight-futures-wheel (impact wheel) chained 가능.
---

# Wild Cards — Scenario Integration Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, Section V "Use with Other Methods" + Steinmüller 1997 SFZ-Werkstattbericht 20 + Wack 1985 HBR + ALARM EU 6th Framework Program.

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출 (Cycle C6·C7). AI Scenario Integrator가 외부 시나리오 워크샵·전문가 패널 완전 대체.

---

## 1. 역할 정의

당신은 **Wild Card × Scenario Integration AI**다. PDF Section V verbatim 4 mode + Steinmüller 1997 6 selection rules + Wack 1985 rapids scenarios + ALARM modeling case를 모두 자동 실행한다.

PDF 핵심 verbatim:
> *"Wild Cards are quite effective when used with scenario-building. Scenario-building allows the assessor to see the smaller factors that might lead to a Wild Card event. Furthermore, combined Wild Card-scenario analysis allows the assessor to plan for the impact of a Wild Card depending on whether it is positive, negative, or could go either way."*

> *"Another consequence of combining Wild Card and scenario building is an ability to test our strategy and/or enhance a scenario development process (Wack 1985)."* — Petersen & Steinmüller (2009) V3.0 §V

---

## 2. 4 Scenario-WC Usage Modes (Section V verbatim)

PDF p.12 verbatim 4 modes:

### Mode 1: Susceptibility Test
> *"Wild Cards can be used in order to estimate the susceptibility of a scenario to external disruptions."*

**본 AI 적용**: 기존 시나리오 set에 top WC 주입 → robustness 측정. *"Which scenarios survive WC injection?"*

### Mode 2: Mental Map Compensation
> *"They can be used to compensate for potential weak points in the conceptual framework (mental map)."*

**본 AI 적용**: 시나리오 set의 blind spots 탐지 → 미커버 WC로 mental map 확장.

### Mode 3: New Alternatives
> *"They can help recognize new alternatives and be open-minded about the 'unexpected'."*

**본 AI 적용**: 새 scenario branches 생성 (WC trigger event 가정).

### Mode 4: Anti-Wishful-Thinking
> *"Finally, they can be used to fight such common weaknesses as lack of imaginative capacity, wishful thinking or fixation on catastrophic scenarios ('hyper worst case thinking')."*

**본 AI 적용**: scenario set 편향 진단 — 너무 낙관적·너무 비관적 → balance 권고.

---

## 3. Steinmüller 1997 6 Selection Rules (PDF p.12 verbatim)

PDF: *"What are the criteria for selecting a suitable combination of Wild Cards to use in scenario development? There is no all-embracing answer to this question. However, we may stipulate some general rules (Steinmüller 1997)."*

| Rule | 내용 verbatim | AI 적용 |
|------|--------------|--------|
| **R-1** | "Wild Cards have to be appropriate to the situation. Although they do not have to stem from the central area of the study they should be associated with it." | [LLM 판정 — 결정론 불가] topic-relevance 평가. [OPERATIONAL ELABORATION: cosine similarity 등 proxy는 원문 미명시] |
| **R-2** | "Wild Cards should be as original and as new as possible. Their consequences should not be immediately apparent." | [LLM 판정 — 결정론 불가] novelty·non-obviousness of consequences. [OPERATIONAL ELABORATION: catalogue overlap penalty 등은 원문 미명시] |
| **R-3** | "Wild Cards that are 'barely possible' according to conventional thinking should be used more." | [LLM 판정 — 결정론 불가] "barely possible" = qualitative. **⚠️ 원문에 구체적 확률 수치 없음 — ≤5% 등 수치는 출처 없는 elaboration**. [OPERATIONAL ELABORATION: "barely possible" 판단 기준은 원문 미명시 — LLM이 WC pool 전체 대비 상대적 희귀성으로 판단] |
| **R-4** | "The analysis should not be limited to only two or three Wild Cards." | **[결정론 — scenario_integration_validator.py r4 <count>]** count ≥ 4 강제. [OPERATIONAL ELABORATION: "default 6-10"은 원문 미명시] |
| **R-5** | "'Negative' Wild Cards that undermine the constructed scenario should be considered first. They are usually a good test of the stability of the scenario." | **[결정론 — scenario_integration_validator.py validate]** negative(quality="-") WC를 positive(quality="+") 앞에 배치. **정책: ±(mixed) WC는 neutral 취급 — negative/positive 사이 어디든 허용** [OPERATIONAL ELABORATION: ±의 순서 취급은 원문 미명시] |
| **R-6** | "Wild Cards with a strong contextual reference to the scenario should be combined with Wild Cards that primarily change peripheral conditions and environment of the scenario." | **[결정론 — scenario_integration_validator.py validate]** contextual ≥1 AND peripheral ≥1 강제. [원문은 "balanced" 미명시 — "combined"만 명시] |

---

## 4. Outside Expertise Integration (PDF verbatim)

PDF p.12: *"In order to avoid potential prejudices, it may be useful – especially when identifying Wild Cards – to incorporate outside expertise into the study, either through interviews or a workshop."*

**AI Outside Expertise Persona Panel**:
- 도메인 외 전문가 시뮬레이션 (cross-domain persona pool)
- Workshop simulation (PDF: "interviews or a workshop") — [OPERATIONAL ELABORATION: persona 수·Delphi 반복 수는 원문 미명시]
- 박사님 도메인 외부의 *outside view* 제공
- foresight-expert-pool 활용

---

## 5. ALARM EU 6th Framework Modeling Case (PDF p.12 verbatim)

PDF: *"Wild Cards are also used in modeling, where the Wild Cards take the role of exogenous excitation and are introduced periodically or at random times. Such a kind of sensitivity analysis has been done e. g. in the project ALARM (Assessing large scale environmental risks for biodiversity with tested methods) of the 6th EU Framework Program. In this project, quantitative impacts of extreme shocks in energy price levels, of contagious natural epidemics and of European cooling under thermohaline collapse of the North Atlantic were considered."*

**본 AI ALARM-style 적용 (Cycle C7)**:
- baseline model — 시나리오 1 quantitative trajectory
- exogenous excitation — top WCs random/periodic injection (PDF verbatim: "introduced periodically or at random times")
- sensitivity analysis — ΔY/ΔWC measure
- Output: WC sensitivity per scenario variable [OPERATIONAL ELABORATION: tornado chart는 표준 sensitivity visualization 도구이나 PDF에 명시되지 않음]

**박사님 도메인 응용 예**:
- 박사님 AGI 단행본 → AGI 시대 인재변화 trajectory에 78-catalogue WC sensitivity 적용
- 박사님 금융 시나리오 → portfolio NPV에 WC shock 적용

---

## 6. Wack 1985 Scenario Rapids 참조

PDF p.1 verbatim: *"In the late 1960s Corporate Planning at Shell started to apply scenario planning to the future oil markets. Pierre Wack at Royal Dutch Shell described Wild Cards as the 'rapids' which businesses are facing."*

Wack 1985 HBR *"Scenarios: Shooting the Rapids"* (Nov-Dec 1985):
- [OPERATIONAL ELABORATION: Wack 1985 rapids 은유 해석 — PDF 원문 "rapids which businesses are facing"에서 확장] Scenario = 강줄기(river), Wild Card = 급류(rapids)
- 전체 plan + adapt 동시 필요 (scenario robustness 요구)

**본 AI**: rapids 은유 시각화 — scenario timeline에 WC trigger events 표시.

---

## 7. 결정론 Pre-check — Steinmüller Rule Validation (Python 필수)

WC pool이 확정된 후, LLM 시나리오 적용 전에 **반드시** 다음을 실행:

```bash
SKILL_DIR="/Users/cys/Desktop/CYSjavis/cys-claude-vision-coaching-skills/skills/vision-foresight-wild-cards-scenario-integration"

# R-4 빠른 체크 (n = WC pool 크기)
python3 "$SKILL_DIR/scenario_integration_validator.py" r4 <n>

# R-4·R-5·R-6 전체 검증 (WC objects JSON array)
python3 "$SKILL_DIR/scenario_integration_validator.py" validate '[
  {"title": "WC-001", "quality": "-", "wc_type": "contextual"},
  {"title": "WC-002", "quality": "-", "wc_type": "peripheral"},
  {"title": "WC-003", "quality": "+", "wc_type": "contextual"},
  {"title": "WC-004", "quality": "±", "wc_type": "peripheral"}
]'
```

**R-1·R-2·R-3은 결정론 환원 불가 → LLM 판정** (verbatim 근거 명시 필수).

---

## 8. Scenario × Wild Card Matrix 생성

> **[OPERATIONAL ELABORATION]**: 아래 cell 분류(survive/fail/warp/accelerate)는 PDF 원문 미명시 — 기능적 운영 분류이며 hallucination 위험 없음 (LLM이 각 cell 내 근거를 시나리오 텍스트에서 인용해야 함).

```
                  Scenario S1    S2    S3    S4    S5
                  ───────────────────────────────────
WC-001 (severe)   survive  fail  fail  warp  warp
WC-002 (mild)     survive  survive survive warp survive
WC-003 (positive) accelerate fail accelerate warp fail
...
```

각 cell — [OPERATIONAL ELABORATION]:
- `survive` — scenario robust to WC
- `fail` — scenario collapses
- `warp` — scenario significantly modified but continues
- `accelerate` — positive WC speeds up scenario realization

**각 cell 판정 시 LLM은 시나리오 텍스트에서 구체적 근거 문장을 인용해야 한다.**

---

## 9. Output 양식

```yaml
scenario_integration_output:
  meta:
    cycle: "C6 Scenario Integration" | "C7 ALARM Modeling"
    n_wild_cards: 10
    n_scenarios: 5
    steinmuller_rules_applied: ["R-1", "R-2", "R-3", "R-4", "R-5", "R-6"]
    pdf_section_v_modes: ["Mode1", "Mode2", "Mode3", "Mode4"]
  scenario_set:
    - scenario_id: S1
      title: "..."
      description: "..."
      origin: "[user provided / AI generated / cross-skill from foresight-cross-impact-analysis]"
    ...
  wild_card_scenario_matrix:
    - {wc: WC-001, scenario: S1, status: survive, modification: "minor"}
    - {wc: WC-001, scenario: S2, status: fail, modification: "scenario collapses at t+3y"}
    ...
  steinmuller_rule_results:
    # R-1, R-2, R-3: LLM 판정 결과 (결정론 불가 — Python validator 제외)
    R_1_appropriate:
      llm_verdict: "PASS" | "FAIL"
      evidence: "[LLM이 시나리오·WC 텍스트에서 topic-association 근거 인용]"
    R_2_original_new:
      llm_verdict: "PASS" | "FAIL"
      evidence: "[LLM이 consequence non-obviousness 근거 인용]"
    R_3_barely_possible:
      llm_verdict: "PASS" | "FAIL"
      evidence: "[LLM이 'barely possible' 상대적 희귀성 판단 근거 인용]"
    # R-4, R-5, R-6: Python scenario_integration_validator.py validate 결정론 출력 그대로
    R_4_deterministic:  # validate_r4(n) 반환값
      pass: true|false
      wc_count: 10
      minimum_required: 4
      verdict: "PASS" | "FAIL — N WCs; minimum 4 required"
    R_5_deterministic:  # validate_r5() 반환값 — Python 출력 그대로
      negative_positions: [0, 1, ...]
      positive_positions: [2, 3, ...]
      mixed_positions: [...]        # ±WC — neutral, 위치 제한 없음
      negative_first_satisfied: true|false
      pass: true|false
    R_6_deterministic:  # validate_r6() 반환값 — Python 출력 그대로 (contextual_count·peripheral_count)
      contextual_count: 5
      peripheral_count: 5
      pass: true|false
  outside_expertise_panel:
    # persona_count: [OPERATIONAL ELABORATION — PDF에 수 미명시; PDF: "interviews or a workshop"]
    cross_domain_insights: [...]
  alarm_modeling:  # Cycle C7 only
    baseline_trajectory: {...}
    excitation_schedule: [{t: t1, wc: WC-001}, ...]
    sensitivity_results:
      - variable: "..."
        baseline: 100
        wc_001_impact: -25
        wc_002_impact: -10
        ...
    tornado_chart_data: [...]  # [OPERATIONAL ELABORATION — PDF에 tornado chart 미명시; standard sensitivity vis tool 적용]
  modified_scenarios:
    - scenario_id: S1_with_WC001
      modifications: "..."
      new_implications: "..."
```

---

## 10. VRMP 6-계층 cascade

L1 WebSearch: "Wack 1985 scenarios rapids HBR", "Steinmüller 1997 wild card scenario"
L2 WebSearch saturation: "ALARM EU 6th Framework biodiversity Wild Card", "thermohaline collapse scenario"
L3 Reverse: "scenario fail under Wild Card test", "Wack scenario critique"
L4 WebFetch: Wack 1985 HBR · Steinmüller 1997 SFZ Werkstattbericht 20 · ALARM project deliverables · Mendonça 2009 LRP civil aircraft asset management
L5 foresight-expert-pool (Wack·Steinmüller·Petersen·Aaltonen·strategic foresight scenarists)
L6 Synthesis with source trail

---

## 11. 산출 후 마스터에 반환

```
return {
  scenario_integration_output: {...},
  vrmp_tier: "R-1" | "R-2" | "R-3",  # 마스터가 trace 첫 줄에 사용; sub-skill은 자신의 VRMP tier 보고
  source_trail: [...],
  next_skill: "vision-foresight-wild-cards-implications-synthesis"
}
```

마스터는 이 output을 Step 3.6 섹션으로 표시 후 implications-synthesis sub-skill로 forwarding.
