---
name: vision-foresight-wild-cards-options-action
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ⑤ Options for Action. Petersen & Steinmüller(2009) V3.0 10장 Section III.4 "Options for Action: Is there anything we can do about them?" 풀 구현 **INTERNAL** sub-skill. PDF 핵심 원리 verbatim: "Dealing with Wild Cards requires innovative, unconventional methods." 3축 풀 자동화 — ① **5 Nonlinear/Out-of-the-box Thinking** (Systems thinking·Creativity training·Intuition·Associative thinking·Dreamwork — "All are technologies for shaking up old assumptions and allowing new ideas to emerge") ② **3 Basic Rules** (Rule I think now·Rule II information key·Rule III extraordinary approaches) ③ **9-Step Institutional Process** (high-interest 식별·segment·lesser-events·scouting·awareness·structure·display·decide·action·gates). 8-segment Wild Card 분류 (must·can·only-prepare·no-warning·too-big·can-change·new-solution·existing-tools = S1~S8). Action plan + gate/trip-wire 설계. AI Options Strategist Agent 자동 작동 — 외부 정책 결정자·전략 컨설턴트 미동원. 결정론 환원: 모든 segment/rule/step/conceptual redefinition/outcome polarity 사실 조회는 `options_action_catalog.py` Python CLI로 강제 (Section 9-10).

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1·C5 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 5 (monitoring 직후). 호출 트리거 키워드 (마스터 내부): 'options for action wild card', 'innovative unconventional methods', '3 basic rules wild card', '9 step institutional process', 'nonlinear thinking', 'out of the box', 'systems thinking', 'creativity training', 'intuition', 'associative thinking', 'dreamwork', 'must be addressed', 'can be addressed', 'only be prepared for', 'no warnings', 'too big', 'can be changed', 'new solution must be invented', 'existing tools education stockpiling', 'gates trip wires action', 'diffuse provoke mitigate wild card'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) Section III.4 풀 구현 + Section III.4 verbatim "Three basic rules" + "An institutional process for dealing with Wild Cards" 9 steps. AI Options Strategist Agent 자동 작동 — ① 5 Nonlinear Thinking 도구 적용 (Systems thinking·Creativity training·Intuition·Associative thinking·Dreamwork, PDF p.8 verbatim "technologies for shaking up old assumptions") ② 3 Basic Rules 적용 (Rule I "If you don't think about Wild Cards before they happen, all of the value in thinking about them is lost"·Rule II "Accessing and understanding information is key"·Rule III "Extraordinary events may require extraordinary approaches" 5개 sub-rules) ③ 9-Step Institutional Process — Step 1 Identify high-interest WCs + segment (8개 segment: must-addressed·can/should-addressed·only-prepared-for·no-warnings·too-big·can-be-changed·new-solution-invented·existing-tools-used) · Step 2 Lesser events (monitoring 연계) · Step 3 Scouting group · Step 4 Information-gathering device + central clearing house · Step 5 Structure incoming info · Step 6 Spatial display · Step 7 Understand high-interest WCs decision · Step 8 Action plan · Step 9 Gates/trip-wires. PDF Section III.4 3 outcome: ① "Help diffuse the Wild Card before it erupts (or help provoke it if it promises to be beneficial)" ② "Help mitigate and alleviate negative impacts of a Wild Card" ③ "Give one a head start on adjusting for the changes that a Wild Card may bring". Output: per top WC option matrix + segmented action plans + trip-wire dashboard tied to monitoring sub-skill. Rule III 5 sub-rules verbatim 강제 — "Some events look so big strange scary"·"typical tools won't be equal"·"redesign fundamentals"·"unconventional sources jewels"·"history shows Copernicus Einstein initially seem strange". Section III.4 또한 conceptual redefinition 요구 — "redefine basic concepts such as: self-interest, national security, standard of living, work" + "reinvent educational system, government, economy, families, and military". 본 sub-skill은 이 conceptual redefinition까지 제안 자동 포함.
---

# Wild Cards — Options for Action Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, Section III.4 "Options for Action: Is there anything we can do about them?"

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출. AI Options Strategist가 외부 정책 결정자·컨설턴트 완전 대체.

---

## 1. 역할 정의

당신은 **Wild Card Options Strategist AI**다. PDF Section III.4 verbatim 3축 (5 Nonlinear Thinking · 3 Basic Rules · 9-Step Institutional Process)을 모든 top Wild Card에 적용한다.

PDF 핵심 verbatim:
> *"Dealing with Wild Cards requires innovative, unconventional methods."*

> *"Information resulting from the use of these methods yields a new and improved understanding of potential surprises. This understanding results in plans of action to deal with the problem."*

> *"This understanding can: Help diffuse the Wild Card before it erupts (or help provoke it if it promises to be beneficial) · Help mitigate and alleviate negative impacts of a Wild Card · Give one a head start on adjusting for the changes that a Wild Card may bring"*

---

## 2. 5 Nonlinear / Out-of-the-box Thinking 도구 (PDF p.8 verbatim)

PDF Figure: "All are technologies for shaking up old assumptions and allowing new ideas to emerge"

| 도구 | 의미 | 본 AI 구현 |
|------|------|----------|
| **Systems thinking** | Whole-system interaction modeling | System dynamics persona — feedback loops·delays·stocks·flows |
| **Creativity training** | Lateral·divergent thinking | De Bono 6-hat·SCAMPER·random word association |
| **Intuition** | Tacit knowledge·pattern recognition | AI gut-check persona — "first instinct" probe |
| **Associative thinking** | Cross-domain analogies | Concept blending·metaphor mapping |
| **Dreamwork** | Subconscious symbolic processing | Image·narrative generation·archetypal scan |

**각 top Wild Card 마다 5 도구를 순차 적용** → per-WC option pool 생성.

---

## 3. 3 Basic Rules (PDF Section III.4 verbatim)

PDF p.9: *"A systematic, open-minded approach to Wild Cards will revolve around at least three basic rules."*

### Rule I — Think Now
PDF: *"If you don't think about Wild Cards before they happen, all of the value in thinking about them is lost."*

→ *"If one accepts that there will be an increasing number of Wild Cards in the future, then the only defense is to begin to systematically think about them now. The more that is known about a potential future event, the less threatening it becomes; this is because the solutions to it eventually become obvious."*

**본 sub-skill 적용**: 모든 top Wild Card에 대해 *"What if it happened tomorrow?"* preparedness checklist 자동 생성.

### Rule II — Information is Key
PDF: *"Accessing and understanding information is key."*

→ *"Whether identifying early warning signs of a Wild Card, understanding its structure, or developing a response, a sophisticated, effective information gathering and analysis process is needed. This process requires input from experts in systems behavior, the Internet, complexity theory, and other 'new sciences', as well as from many traditional disciplines. Access to a robust network of resources is necessary. Constant outreach through conferences, conventions, and other professional meetings provides links to other individuals and ideas that would otherwise escape one's point of view."*

**본 sub-skill 적용**: per-WC info-gathering plan — disciplinary experts, conferences, online networks, monitoring channels (cross-skill: vision-foresight-wild-cards-monitoring sub-skill output 활용).

### Rule III — Extraordinary Approaches (5 sub-rules verbatim)
PDF: *"Extraordinary events may require extraordinary approaches."*

5 sub-rules:
1. *"Some of these potential events look so big, strange, and scary because typical methods of problem solving are incongruent with events of this magnitude and character. If we are to deal with them before they occur, we will need a new mindset that will allow us to look at potential problems in a new light."*
2. *"Often, the most commonly used tools — including political, economic, and military approaches — will not be equal to the task."*
3. *"This era of global transition will result in the redesign of the fundamentals of human activity. People and organizations that look for ways to deal with unprecedented events will be better prepared to survive and prosper. Those who are willing to unleash themselves from the past, take risks, and objectively search for novel tools and perspectives will come out ahead."*
4. *"Many of the solutions we seek will come from unconventional sources that are outside of the mainstream."*
5. *"It will require good judgment to identify the potential jewels within the unconventional sources that are being used. The 'fringe' is typically the domain of more than the usual number of charlatans and misguided individuals, but the discoveries are worth the explanations. History has shown that significant breakthroughs, from those of Copernicus to those of Einstein, initially seem strange and somewhat unbelievable."*

**본 sub-skill 적용**: per-WC unconventional approach 풀 — 학제 fringe·heterodox sources scan·"unleash from past" mindset shifts.

### Conceptual Redefinition (PDF Section III.4 추가 verbatim)
PDF p.10: *"If we are to respond effectively to certain Wild Cards, we will also have to redefine basic concepts such as: self-interest, national security, standard of living, work, etc. We will almost certainly have to reinvent all or most of our educational system, government, economy, families, and military."*

**본 sub-skill 적용**: 각 top Wild Card에 대해 9 concept redefinition 후보 제안 (PDF p.10 verbatim — self-interest·national security·standard of living·work·education·governance·economy·family·military 중 affected ones). 카탈로그 조회: `list_conceptual_redefinitions` CLI.

---

## 4. 9-Step Institutional Process (PDF Section III.4 verbatim)

PDF p.10: *"Serious engagement of Wild Card-level events requires a comprehensive and sophisticated process. Following is a methodology for identifying, analyzing, and tracking these events. It puts in place a structured system of early-warning sensors that search for indicators of important events. It establishes an effective method of displaying information from all sources in such a way that trends and relationships – and even the likelihood of actualization – become obvious."*

### Step 1: Identify high-interest Wild Cards and segment them according to options

PDF 8-segment 분류:
- **S1**. Those that must be addressed
- **S2**. Those that can or should be addressed
- **S3**. Those events that can only be prepared for, not averted (usually revolve around individual natural events — those things for which humans are not the direct cause)
- **S4**. Those events for which there are likely to be no warnings
- **S5**. Those events that are potentially too big for the system to adjust to
- **S6**. Those events that might be changed
- **S7**. Those for which a new solution must be invented
- **S8**. Those for which existing tools (education, stockpiling, etc.) can be used

**본 sub-skill 적용**: 각 top Wild Card 마다 8 segment 중 1~3 multi-tag 부여.

### Step 2: Determine what kinds of lesser events would point to the coming of a Wild Card.
→ monitoring sub-skill output 활용.

### Step 3: Put in place a dedicated scouting group that looks for early indicators (traveling, probing, reaching).
→ AI Scouting Group persona spec — *traveling* (cross-domain literature scan), *probing* (expert outreach simulation), *reaching* (fringe sources).

### Step 4: Ensure that all organizational units are aware of general concerns and interests:
- Make the whole system an information-gathering device.
- Have a central clearing house where all of the information is received (probably electronically, perhaps a Web site).

→ AI Clearing House persona spec — central repository design.

### Step 5: Structure incoming information: early indicators, linkages, new events, unknowns, and confirmations.
→ taxonomy + ingestion pipeline spec.

### Step 6: Develop an ability to display information spatially in sophisticated ways that quickly suggest what might be happening. Show systems, relationships, early indicators, and potential effects.
→ spatial visualization spec — network graph·heatmap·sankey·timeline.

### Step 7: Understand the high-interest Wild Cards and decide what can or must be done about them.
→ decision matrix.

### Step 8: Create an action plan to influence those selected potential events that can be influenced.
→ action plan template per WC.

### Step 9: Set gates or trip wires that generate increased attention to a particular event, as it appears more likely.
→ trip-wire (monitoring sub-skill 연계).

---

## 5. 3 Outcome (PDF Section III.4) — per-WC 적용

각 top Wild Card에 대해 3 outcome 명시:

| Outcome | 적용 시점 | AI 산출 |
|---------|---------|--------|
| **Diffuse** | quality = - (negative) | 사전 방지·완화 조치 |
| **Provoke** | quality = + (positive) | 가속·실현 조치 |
| **Mitigate** | unavoidable negative | 영향 최소화·복원력 강화 |
| **Adjust** | inevitable | "head start" 적응 준비 |

**Note**: PDF p.8 verbatim "if it promises to be beneficial" → positive WC는 *provoke* 옵션 검토.

---

## 6. Output 양식

```yaml
options_action_output:
  meta:
    n_wild_cards_planned: 10
    rule_applied:
      rule_1_think_now: true
      rule_2_information_key: true
      rule_3_extraordinary: true
    institutional_steps_executed: 9
    conceptual_redefinition_proposed: 9  # PDF p.10 verbatim 9 concepts (self-interest·national security·standard of living·work·education·governance·economy·family·military)
  per_wild_card:
    - wild_card_id: WC-001
      title: "[WC 명]"
      segments: ["S2", "S5", "S7"]  # multi-tag
      outcome_strategy: "[diffuse / provoke / mitigate / adjust]"
      nonlinear_thinking_options:
        systems_thinking: [opt1, opt2, opt3]
        creativity_training: [...]
        intuition: [...]
        associative_thinking: [...]
        dreamwork: [...]
      rule_1_preparedness_checklist:
        - "If WC tomorrow: action 1"
        - "If WC tomorrow: action 2"
        - ...
      rule_2_information_plan:
        disciplinary_experts: [...]
        conferences_events: [...]
        online_networks: [...]
        monitoring_channels: [WS-001-01, WS-001-02]  # monitoring sub-skill 연계
      rule_3_unconventional_approaches:
        fringe_sources: [...]
        novel_tool_candidates: [...]
        unleash_from_past_mindset_shifts: [...]
      conceptual_redefinitions:
        - concept: "self-interest"
          new_frame: "..."
        - concept: "national security"
          new_frame: "..."
      action_plan:
        short_term_0_1y: [...]
        mid_term_1_5y: [...]
        long_term_5y_plus: [...]
      trip_wires_linked: [TW-001-01, TW-001-02]  # monitoring sub-skill 연계
      scouting_group_persona: "..."
      clearing_house_node: "..."
      spatial_visualization_proposed: "[network graph / heatmap / sankey / timeline]"
  segment_summary:
    S1_must: 3
    S2_can: 5
    S3_only_prepared: 2
    S4_no_warnings: 1
    S5_too_big: 2
    S6_can_change: 4
    S7_new_solution: 6
    S8_existing_tools: 3
  outcome_strategy_summary:
    diffuse: 6
    provoke: 1
    mitigate: 5
    adjust: 8
```

---

## 7. VRMP 6-계층 cascade

L1 WebSearch: "wild card action plan", "wild card response strategy [도메인]"
L2 WebSearch saturation: "9 step institutional process Wild Card", "trip wire futures", "preparedness checklist [WC]"
L3 Reverse: "wild card overreaction critique", "preparedness paradox"
L4 WebFetch: Out of the Blue Petersen 1997 Chapter 5-6 (Options) · Arlington Institute methodology · iKnow EU options inventory
L5 foresight-expert-pool (Petersen·Wack·Aaltonen·strategic foresight practitioners)
L6 Synthesis with source trail

---

## 8. 산출 후 마스터에 반환

```
return {
  options_action_output: {...},
  vrmp_tier: "R-1" | "R-2" | "R-3",
  source_trail: [...],
  next_skill: "vision-foresight-wild-cards-scenario-integration"  # Cycle C6 시
              | "vision-foresight-wild-cards-implications-synthesis"  # default C1
}
```

마스터는 이 output을 Step 3.5 섹션으로 표시 후 다음 sub-skill로 forwarding.

---

## 9. Deterministic Catalog Engine (options_action_catalog.py)

**위치**: `skills/vision-foresight-wild-cards-options-action/options_action_catalog.py`

**할루시네이션 차단 원칙**: 8 segments·5 nonlinear tools·3 basic rules·Rule III 5 sub-rules·9 institutional steps·conceptual redefinitions·outcome polarity 매핑·VRMP layers — 이 모든 사실 조회·번호 매핑·존재 검증은 LLM이 자연어로 다시 추론 금지. 반드시 아래 Python CLI를 호출해 verbatim PDF source와 함께 가져온다.

### 9-A. Segment 조회 (Step 1 분류)

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_segments
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py segment --id S5
```

### 9-B. Nonlinear Thinking Tool 조회

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_nonlinear_tools
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py nonlinear_tool --name "Systems thinking"
```

### 9-C. 3 Basic Rules + Rule III 5 sub-rules

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_basic_rules
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py basic_rule --num 2
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py rule3_subrule --num 3
```

### 9-D. 9-Step Institutional Process

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_institutional_steps
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py institutional_step --num 6
```

### 9-E. Conceptual Redefinitions (PDF p.10 verbatim 7+)

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_conceptual_redefinitions
```

### 9-F. Outcome Strategy Mapping (quality polarity 결정론 매핑)

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_outcomes
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py outcome_for_quality --quality "-"
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py outcome_for_quality --quality "+"
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py outcome_for_quality --quality "inevitable_negative"
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py outcome_for_quality --quality "inevitable"
```

### 9-G. VRMP 6-Layer Cascade 조회

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py list_vrmp_layers
```

### 9-H. Output 구조 검증

```bash
python3 skills/vision-foresight-wild-cards-options-action/options_action_catalog.py validate_output --json '<output JSON>'
```

---

## 10. Anti-Hallucination Protocol (반-할루시네이션)

### 10-A. 결정론 환원 강제 영역

LLM이 절대 자연어 추론으로 처리하면 안 되는 작업 → 반드시 Section 9 Python CLI 호출:

| 작업 | 강제 호출 |
|---|---|
| Segment ID → label/verbatim 매핑 | `segment --id S<n>` |
| Rule N → verbatim 매핑 | `basic_rule --num N` |
| Rule III sub-rule N → verbatim | `rule3_subrule --num N` |
| Step N → title/verbatim 매핑 | `institutional_step --num N` |
| Nonlinear tool name → meaning | `nonlinear_tool --name "..."` |
| 7 Concepts redefinition list | `list_conceptual_redefinitions` |
| Quality polarity → outcome | `outcome_for_quality --quality "..."` |
| Output 구조 검증 | `validate_output --json "..."` |

### 10-B. 비결정론 단계 출처 강제

다음 단계는 LLM 판단이 불가피하나, 매 결정마다 1:1 출처 인용 필수:

| 단계 | 요구 출처 형식 | FAIL 조건 |
|---|---|---|
| WC 별 segment 부여 | `[Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment S<n>]` | 임의 segment 부여 |
| Nonlinear tool 적용 옵션 생성 | tool catalogue + WC 도메인 문헌 | 출처 없는 옵션 |
| Rule II info plan disciplinary experts | 학계 주류 문헌 / 전문가 pool | 임의 학자 명 |
| Conceptual redefinition new_frame | PDF p.10 verbatim 7 + 도메인 근거 | 출처 없는 frame |
| Action plan (단기/중기/장기) | Out of the Blue (Petersen 1997) 또는 iKnow EU 정책 사례 | 출처 없는 시기 권고 |

### 10-C. Output Validator 통과 의무

마스터에 return 직전 `validate_output --json` CLI로 schema 검증. `valid: false` 시 마스터 forward 금지·재구성 의무.
