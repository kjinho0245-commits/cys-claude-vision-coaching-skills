---
name: vision-foresight-futures-wheel-quality-control
description: |
  ## TLDR — Jerome C. Glenn (V3.0 06장 §IV + §III.A + endnote 4) Quality Control sub-skill + 박사님 2026-05-11 강화 명령 3종 강제. **vision-foresight-futures-wheel** 마스터 전용. **11 Audit Gate**: Gate 1-8 Glenn 원전(Wagschal·spaghetti·premature·causation·butterfly·timing·probability·strengths) + ⭐ **Gate 9 Citation Completeness** + ⭐ **Gate 10 Reasoning Chain Validity·SRS** + ⭐ **Gate 11 SCBE Compliance**. 모든 wheel 산출의 *최종 품질 게이트* — 통과 못하면 REVISIONS_REQUIRED 반환.

  ## Triggers — INTERNAL ONLY. 마스터 Cycle 2·4·6·7·8에서 호출. Cycle 8 단독 발동. 사용자가 'Wagschal Unanimity', 'rule of unanimity', '품질 점검', '검증해줘', 'intellectual spaghetti', 'plausibility 검증', 'correlation vs causation', '함정 체크', 'butterfly effect', '직선적 단정 회피', 'citation 검증', 'SRS 측정', '6차 깊이 확인' 명시 시 마스터가 본 sub-skill 발동.

  ## Detailed Methodology — Glenn (2009) §IV + §III.A + endnote 4 + 박사님 2026-05-11 두 차례 강화. **11 Audit Gate**: ① **Gate 1 Wagschal Unanimity** — *"requires a restriction on the group to prevent them from arriving at conclusions that are so speculative."* ② **Gate 2 Intellectual Spaghetti** — *"messy 'intellectual spaghetti' that makes the implications more difficult to see clearly."* ③ **Gate 3 Premature Judgment Guard** — *"One must guard against making dangerously premature judgments."* ④ **Gate 4 Correlation/Causation** — Hume·de Jouvenel 철학, edge classification. ⑤ **Gate 5 Butterfly Effect** — chaos attractor 인식. ⑥ **Gate 6 Timing Distinction**. ⑦ **Gate 7 Probability Comparison**. ⑧ **Gate 8 Strengths Self-Affirmation** — 5 strengths per Glenn §IV 자가 검증 (extension 1건 별도 표시). ⭐ ⑨ **Gate 9 Citation Completeness (NEW — 박사님 2026-05-11)** — 모든 impact inline citation 100%, vague attribution 0, fabricated source 0, specific number R-1 의무. ⭐ ⑩ **Gate 10 Reasoning Chain Validity + SRS (NEW)** — 각 impact CoER(Chain of Evidence Reasoning) 3-step chain 검증 + SRS 계산(avg ≥1.5 강제, 4차·5차·6차 sign reversal 강제) + 6차 깊이 도달 검증 (MDE compliance). SRS = Sewongjima Reversal Score (박사님 proprietary metric; 세옹지마·塞翁之馬 고사에서 명명, 표준 학술 용어 아님). ⭐ ⑪ **Gate 11 SCBE Compliance (NEW — 박사님 2026-05-11 2차 강화)** — Cycle 9 SCBE 모드에서만 활성화; 다른 cycle 자동 SKIP (auto-PASS). 균일 2-fan-out 검증(모든 노드 정확히 2 children) + 카테고리 균형 ±0 강제 + 총 노드 수 검증(STEEPS 6 6차 = 379) + Anchored+Tagged 모델 검증 + 3LDP 출력 양식 검증. AI Agents 11인: Wagschal Critic · Spaghetti Auditor · Premature Judgment Guard · Causation Sleuth · Butterfly Detector · Timing Auditor · Probability Auditor · Strengths Self-Auditor · Citation Validator · Reasoning Chain & SRS Auditor · ⭐ SCBE Compliance Auditor (NEW). Final Gate Keeper가 11 Gate 통합 PASS/REVISIONS_REQUIRED/FAIL 판정 + quality_score 결정론 계산(§10.4).
disable-model-invocation: true
---

# Sub-skill: Quality Control (Wagschal + Pitfall)

> **출처**: Glenn (2009) V3.0 06장 §IV "Strengths and Weaknesses" + §III.A "rule of unanimity" + endnote 4 (correlation/causation philosophy)
> **상위 마스터**: `vision-foresight-futures-wheel`
> **호출 권한**: 마스터 orchestration 전용 (disable-model-invocation: true)

## 1. PDF 원전 정의

### 1.1 Wagschal Unanimity Rule (§III.A)

> *"Alternatively, the impacts of an event or trend can be processed more slowly and deliberately by accepting criticism prior to entering anything on the wheel. In this approach, the group discusses the plausibility of every impact. If an impact is judged plausible by all, then it is entered; otherwise, not. Peter Wagschal refers to this as the 'rule of unanimity.' He argues that making sure everyone agrees is one way of ensuring that the impacts are reasonable: 'The Futures Wheel process leads rapidly to unexpected consequences and, thus, requires a restriction on the group to prevent them from arriving at conclusions that are so speculative as to be of little worth in assessing alternative futures.'"*

### 1.2 Intellectual Spaghetti (§IV)

> *"If one is not disciplined in using the Futures Wheel, one can end up with some messy 'intellectual spaghetti' that makes the implications of the trend or event more difficult to see clearly. The use of primary, secondary, etc. rings is one way to help prevent the problem; another is the use of the single, double, triple, etc., lines to organize the linkages among the impacts as in Figure 4."*

### 1.3 Premature Judgment + Butterfly Effect (§IV)

> *"One mistake is to see the possible impacts or consequences as truly representing what will happen. One might be tempted into believing that a single triggering fact is sufficient to generate an avalanche of impacts. Although such events do occur (such as attractors in chaos theory, which give rise to 'butterfly effects' — how a seemingly insignificant event like a butterfly passing by can catch one's attention, changing the previously expected flow of events) the Futures Wheel can help to identify them. However, one must guard against making dangerously premature judgments."*

### 1.4 Correlation vs Causation (endnote 4)

> *"Philosophically, one cannot claim certainty of causality. One situation may appear to be caused by another situation, when in fact they may both be caused by a third situation not visible to the observer. This point in a futures context is well explained by Bertrand de Jouvenel in The Art of Conjecture. The philosopher David Hume in On Human Nature demonstrated that what we call causality is a habit of the mind formed by seeing one thing vary with another. It is the variation and correlation that we can know, but not the truth of causality. Impacts and consequences imply causality. Originally, one would do a Futures Wheel by answering the question, 'What are the necessary correlations (not in the mathematical sense) with the event or trend?' However, since the method is designed to help thinking rather than determine truth (since 'truth' does not apply to the future anyway), the normal use of the method today asks what are the likely impacts or consequences, as if we can really ascertain the causal relations. This paper reflects how the method is used in common practice and, hence, will only refer to impacts and consequences rather than correlations."*

### 1.5 Method Weaknesses (§IV)

> *"Weaknesses. Like Simulation Games, Delphis, or Syncons, the Futures Wheel is no better than the collective judgments of those involved. It can make a group or individual think they understand causal relations between the items that emerge, when it is possible that they have only identified correlations. The Futures Wheel can be too simplistic at times, blurring the distinctions on the timing of one identified impact relative to other impacts and the probability of one consequence relative to others."*

### 1.6 Method as Input, Not Truth (§IV)

> *"The output of a Futures Wheel should be used as a basis for further thinking, for more systematic exploration, and for the application of other techniques for probing the future. Put simply, the Futures Wheel is a creative tool that generates input to futures thinking."*

---

## 2. AI Agent 11인 구성 + Final Gate Keeper

| Agent | 역할 | Gate |
|-------|------|------|
| **Wagschal Critic** | 각 impact의 panel 만장일치 plausibility 점검 | Gate 1 |
| **Spaghetti Auditor** | 시각화 명료성, ring/line 구조화 점검; visual_clarity_score 결정론 계산 (§10.1) | Gate 2 |
| **Premature Judgment Guard** | avalanche 효과 의심, 단일 trigger의 단정 회피 | Gate 3 |
| **Causation Sleuth** | 인과·상관 명시적 구별, 제3 변수 의심 | Gate 4 |
| **Butterfly Detector** | chaos theory attractor·"butterfly effect" 식별 | Gate 5 |
| **Timing Auditor** | 차수별 시간 간극 일관성, blur 점검 | Gate 6 |
| **Probability Auditor** | impact 별 확률 비교 명시 점검 | Gate 7 |
| **Strengths Self-Auditor** | Glenn §IV 5 strengths 자가 검증 (extension 1건 별도 표시) | Gate 8 |
| **Citation Validator** | 모든 impact inline citation 100% 검증, vague attribution 0, fabricated source 0 | Gate 9 |
| **Reasoning Chain & SRS Auditor** | CoER 3-step chain 검증 + Python SRS 계산 (§10.2) + MDE compliance | Gate 10 |
| **SCBE Compliance Auditor** ⭐ | Cycle 9 전용 (비-C9 자동 SKIP): 균일 2-fan-out·카테고리 균형·총 노드수·3LDP 검증 (§10.3) | Gate 11 |
| **Final Gate Keeper** | 11 Gate 통합 PASS/REVISIONS_REQUIRED/FAIL 판정; quality_score 결정론 계산 (§10.4) | All |

---

## 3. 11 Audit Gate 처리 흐름

### Gate 1 — Wagschal Unanimity Rule

각 impact에 대해:

```yaml
wagschal_audit:
  impact_id: P1
  text: "AGI로 화이트칼라 자동화 50% 진행"
  
  panel_vote_simulation:
    Glenn:    plausible (5 panelists 가상)
    Bishop:   plausible
    Coates:   plausible
    Snyder:   speculative (concerns about timeline)
    Voros:    plausible
  
  unanimity: false   # Snyder가 speculative 표
  
  action:
    option_A: refine wording until unanimity
    option_B: mark with [low-unanimity] flag and lower visibility
    option_C: drop from wheel
  
  recommendation: option_A
  refined_text: "AGI로 화이트칼라 *부분* 자동화 가속 (속도 불확실)"
  re_vote: 5/5 plausible
```

만장일치 미달 시 3가지 옵션 자동 적용:
- **A. Refine**: 워딩 다듬어 재투표 (가장 일반적)
- **B. Flag**: low-unanimity tag로 보존, oval 작게 표시
- **C. Drop**: 너무 speculative하면 제거

---

### Gate 2 — Intellectual Spaghetti Audit

**visual_clarity_score 결정론 계산 공식** — LLM 재추론 금지; §10.1 `calculate_visual_clarity_score()` 호출:

| 감점 항목 | 감점 크기 |
|-----------|---------|
| ring 경계 미구별 (per violation) | −0.15 |
| single/double/triple 선 미구별 | −0.10 |
| domain 버킷 미표시 (per unlabeled) | −0.10 |
| cross-linkage 미표시 (per edge) | −0.03 |
| feedback loop 미강조 (per loop) | −0.05 |
| 최저 보장 | 0.0 (음수 방지) |

- spaghetti_risk 분류: `low` ≥ 0.75 / `medium` 0.50–0.74 / `high` < 0.50

```yaml
spaghetti_audit:
  total_nodes: 32
  total_edges: 41
  graph_density: 0.041
  
  visual_clarity_score: <§10.1 결정론 계산값>   # LLM이 직접 수치 생성 금지
  
  structure_checks:
    - rings_clearly_distinguished: ✓
    - line_types_distinguished: ✓ (single/double/triple)
    - domain_buckets_labeled: ✓ (V2 활용 시)
    - cross_linkages_explicitly_marked: ✓
    - feedback_loops_separately_highlighted: ✓
  
  spaghetti_risk: low|medium|high   # 위 기준으로 결정론 분류
  
  if_high:
    recommended_actions:
      - "사용 ring 줄이기 (3차 → 2차)"
      - "cross-linkage를 별도 diagram으로 분리"
      - "도메인 그룹화 강화"
      - "차수별 표로 분할"
```

---

### Gate 3 — Premature Judgment Guard

> **결정론 범위 명시**: Gate 3은 가정 의존성 식별과 qualitative alert 생성이 본질이므로 LLM 추론이 불가피하다. 단, alert 구조 포맷은 아래 YAML을 엄수하여 hallucination을 최소화. 수치·확률 클레임이 포함된 경우에만 Gate 9·10의 결정론 체크와 연동.

각 high-confidence impact에 대해:

```yaml
premature_guard:
  impact_id: P1
  confidence_level: 5/5  # 가장 높은 신뢰
  
  audit_questions:
    - "이 impact이 단일 triggering fact에 기반하는가?"
    - "다른 attenuating factor가 누락되지 않았는가?"
    - "역사적 analog가 실제로 같은 path를 따랐는가?"
    - "panel의 confidence가 *어떤 가정*에 기반하는지 명시되었는가?"
  
  alerts:
    - "P1은 단일 가정(AGI 2028 출현)에 강하게 의존. 가정 변경 시 hooked chain 전체 흔들림"
  
  required_disclosure:
    - "이 분석은 {가정 1, 가정 2}가 성립할 때만 유효"
    - "Confidence는 *판단*이지 *예측*이 아니다"
```

---

### Gate 4 — Correlation vs Causation Guard

```yaml
causation_audit:
  edges_total: 41
  
  edge_classification:
    direct_causation: 18   # A가 명백히 B를 일으킴
    necessary_correlation: 15  # A 없이 B 없음 — 인과 의심 가능
    contingent_correlation: 6  # A와 B가 같이 보이지만 제3 변수 의심
    unclassified: 2
  
  third_variable_alerts:
    - edge: P1 → S1a
      issue: "P1(자동화)와 S1a(임금 하락)는 모두 P0(자본 집중)에서 비롯될 가능성"
      action: "edge label에 [contingent] flag"
    
    - edge: P2 → S2a  
      issue: "P2(데이터센터 수요)와 S2a(SMR 부상)는 같은 P-X(에너지 전환 정책)의 두 결과일 수 있음"
      action: "추가 edge 'P-X → P2, P-X → S2a' 검토"
  
  philosophical_disclosure_required: true
  disclosure_text: |
    "본 wheel의 edge는 인과(causation)가 아닌 *likely impacts*를 표시한다.
    Hume·de Jouvenel 철학에 따라 인과 자체는 입증 불가하며, 우리는 
    correlation을 관찰할 뿐이다. 따라서 각 edge는 '~할 가능성이 있다'로 해석."
```

---

### Gate 5 — Butterfly Effect Awareness

```yaml
butterfly_audit:
  small_events_overlooked: []  # Brainstorm panel이 무시한 작은 사건
  
  attractor_candidates:
    - event: "한국 출산율 0.5 진입"
      potential_amplification: "임계점 통과 후 사회 시스템 재조직 trigger 가능"
      panel_attention: low  # 작아 보여서 주목 못 받았음
    
    - event: "특정 GPU export 규제 강화"
      potential_amplification: "글로벌 AI 산업 지정학 재편 가속 가능"
      panel_attention: medium
  
  recommended_addition:
    - "wheel에 'attractor' 표시 영역 추가 — 작지만 amplification 가능 후보"
    - "각 attractor 후보를 별도 시나리오 분기점으로 promote"
```

---

### Gate 6 — Timing Distinction Audit

```yaml
timing_audit:
  primary_ring_time_range:
    expected: T+1~5y
    actual_spread: T+0.5y ~ T+6y
    consistency: good
  
  secondary_ring_time_range:
    expected: T+5~10y
    actual_spread: T+3y ~ T+12y
    consistency: blurred  # ⚠️
    
    blur_examples:
      - S1a: T+3y (너무 빠름 — primary와 겹침)
      - S3c: T+12y (너무 늦음 — tertiary 영역)
    
    recommended_action: "S1a는 primary로 재분류, S3c는 tertiary로 재분류"
  
  tertiary_ring_time_range:
    expected: T+10~20y
    actual_spread: T+10y ~ T+25y
    consistency: acceptable
```

---

### Gate 7 — Probability Comparison Audit

```yaml
probability_audit:
  probability_assigned: 18/32 nodes  # ⚠️ 모든 노드에 미할당
  
  unassigned_nodes: 14
  required_action: "각 impact에 *상대* 확률 등급 부여 (very high / high / medium / low / very low)"
  
  cross_node_comparison:
    higher_probability: [P1, P2, P3]
    medium: [P4, S1a, S2a, S1b]
    lower: [P5, S3c, T1a1]
  
  visualization_directive:
    - line_thickness ∝ probability
    - dotted line for low-probability edges
```

---

### Gate 8 — Strengths Self-Affirmation

Glenn §IV Strengths 5종 자가 점검 (출처: Glenn 2009, V3.0 06장 §IV):

```yaml
strengths_self_audit:
  # --- Glenn §IV 5 core strengths ---
  - strength: "Easy and enjoyable — gets people thinking quickly"
    source: "Glenn (2009) §IV Strengths"
    check: AI Agent panel이 빠르게 활성화됨
  
  - strength: "Identify positive and negative feedback loops"
    source: "Glenn (2009) §IV Strengths"
    check: consequence-linker가 FL-1, FL-2 식별
  
  - strength: "Move from linear/hierarchical to network thinking"
    source: "Glenn (2009) §IV Strengths"
    check: cross-linkage 6 발견 — network thinking 작동
  
  - strength: "Visual map of complexity"
    source: "Glenn (2009) §IV Strengths"
    check: Mermaid + ASCII + table 3종 산출
  
  - strength: "Reveal contradictions as critical issues"
    source: "Glenn (2009) §IV Strengths"
    check: 2 contradiction을 critical issue로 promote
  
  # --- Extension (Glenn §IV 직접 인용 아님; 방법론 문헌 일반 확장) ---
  - strength: "Tie into formal systems model"
    source: "Extension — not a direct Glenn §IV citation"
    extension: true
    check: Causal Loop Diagram export 가능

all_glenn_strengths_demonstrated: true   # 5 core Glenn §IV strengths
extension_demonstrated: true              # 1 extension (별도 표시)
final_gate: PASSED
```

---

### Gate 9 — Citation Completeness ⭐ (박사님 2026-05-11 강화 명령 #3)

```yaml
citation_audit:
  total_impacts: N
  
  per_impact_checks:
    inline_citation_present:
      target: 100%      # 예외 없음 — 95% 이하 모두 FAIL
      current: <%>
    
    citation_format_valid:
      acceptable:
        - "[저자/기관, 연도]"              # 비웹 출처 최소 형식
        - "[저자, 연도, URL]"
        - "[저자, 연도, 제목, URL, page]"  # 최상위 형식
      reject: ["(전문가 의견)", "(연구에 따르면)", "(보고서)"]
    
    quantitative_claim_R1_sourced:
      check: "specific number/percentage/date에 R-1 출처 있는가"
      target: 100%
    
    fabricated_source_check:
      patterns:
        - '"study by .* University" (URL 검증 없으면)'
        - '"research from .* Institute" (URL 검증 없으면)'
        - '"according to .* paper" (URL 없으면)'
      reject_action: 자동 삭제 + flag
  
  fail_condition:
    # strictness에 따라 임계치 분기 (§7 strictness 참조)
    wagschal_or_default:
      - citation_present_rate < 100%
      - vague_attribution_count > 0
      - fabricated_source_count > 0
    balanced:
      - citation_present_rate < 95%   # 완화 임계치
      - vague_attribution_count > 0
      - fabricated_source_count > 0   # citation_rate=100%여도 독립적으로 FAIL
    fast:
      - gate_9_skipped: true          # fast 모드에서 Gate 9 비활성
  
  # NOTE: fabricated_source_count > 0 조건은 citation_present_rate와 독립.
  #       모든 impact에 citation이 있어도 fabricated source 1건이면 FAIL.
  
  on_fail: REVISIONS_REQUIRED → deep-reasoning-engine 재호출
```

---

### Gate 10 — Reasoning Chain Validity + SRS ⭐ (박사님 2026-05-11 강화 명령 #1·#2)

**CoER (Chain of Evidence Reasoning)**: 각 impact에 대해 "근거 사실(R-1) → 중간 추론(R-2) → 도출 주장(H)" 3단계로 추론 경로를 명시. LLM 자연어 재추론이 아닌 출처 체인으로 할루시네이션을 구조적으로 차단.

**SRS (Sewongjima Reversal Score)**: 박사님 proprietary metric (세옹지마·塞翁之馬 고사에서 명명; **표준 학술 용어 아님**). 각 lineage에서 consecutive sign reversal 횟수를 계산하여 "wheel이 단순 직선 증폭이 아닌 반전·순환을 충분히 반영하는가"를 측정.

**SRS Sign Notation** (전 게이트 공통):
- `🟢` = positive impact (긍정적 결과)
- `🔴` = negative impact (부정적 결과)
- `🟡` = neutral/ambiguous (중립·양가; reversal count 제외)
- Reversal = 연속된 `🟢→🔴` 또는 `🔴→🟢` 전환

**[결정론 위임]** SRS 계산 및 forced reversal 검사는 §10.2 Python 함수 `calculate_srs()` / `check_forced_reversals()` 호출. LLM이 직접 sign reversal을 카운트하지 않는다.

```yaml
reasoning_chain_audit:
  for_each_impact:
    chain_length: ≥3 steps required
    step_1_R1_present:
      check: "base fact에 R-1 출처 있는가"
    step_2_R2_present:
      check: "intermediate inference에 R-2 출처 또는 analog 있는가"
    step_3_disclosure:
      check: "leap step에 H tag + 가정 disclosure 있는가"
  
  fail_condition:
    - any impact with chain_length < 3
    - any step without R-tag
    - any leap step without H-tag disclosure

SRS_audit:
  # [결정론] §10.2 calculate_srs(sign_sequences) 호출 필수 — LLM 직접 계산 금지
  lineage_format: "Center→Primary→Secondary→Tertiary→Quaternary→Quinary→Senary"
  sign_sequences: [<각 lineage의 sign 리스트>]
  
  per_lineage_minimum: ≥1 reversal
  global_avg_target: ≥1.5
  
  forced_reversal_checks:
    # [결정론] §10.2 check_forced_reversals(sign_sequences, depth=6) 호출
    T_to_Q (1차 강제 반전 — Tertiary→Quaternary):
      rule: "≥50% lineages에서 Quaternary sign이 Tertiary와 반대"
    Q_to_Qn (2차 강제 반전 — Quaternary→Quinary):
      rule: "≥50% lineages에서 Quinary sign이 Quaternary와 반대"
    Qn_to_Sn (3차 강제 반전 — Quinary→Senary):
      rule: "≥50% lineages에서 Senary sign이 Quinary와 반대"
  
  srs_gate_outcome_mapping:
    PASS:    "global_avg ≥ 1.5 AND all forced_reversal_checks PASS"
    PARTIAL: "1.0 ≤ global_avg < 1.5 AND no forced_reversal FAIL → Gate 10 = PARTIAL"
    REJECT:  "global_avg < 1.0 OR any forced_reversal_check FAIL → Gate 10 = FAIL"
  
  fail_condition:
    - global_avg < 1.0 → 직선적 단정 → REJECT (Gate 10 FAIL)
    - any forced_reversal_check 미달 → 세옹지마 효과 미달성 → REJECT (Gate 10 FAIL)
    # PARTIAL zone (1.0 ≤ avg < 1.5): Gate 10 status = PARTIAL; quality_score에서 0.5 × 0.12 반영

MDE_compliance (Minimum Depth Enforcement):
  depth_target: 6
  exceptions:
    - condition: "사용자가 '간단히'/'빠르게'/'대충' 명시"
      min_depth_allowed: 3
    - condition: "마스터가 명시적으로 중간 깊이 지정"
      min_depth_allowed: 4 or 5 (마스터 지정값 따름)
  
  fail_condition:
    - depth_reached < 6 (예외 없이) → REVISIONS_REQUIRED

on_fail:
  action: REVISIONS_REQUIRED
  caller_directive: "basic-v1 Phase 6·7·8 진행 + deep-reasoning-engine Gate_P4·P5·P6_Pre 재호출"
```

---

### Gate 11 — SCBE Compliance ⭐ (박사님 2026-05-11 2차 강화)

**활성화 조건**: Cycle 9 (C9) SCBE 모드 전용.
**비-C9 동작**: 자동 SKIP → gates_passed에 11 추가 (감점 없음; quality_score 에서 SKIP = 1.0 처리).

**[결정론 위임]** 총 노드 수 계산 및 fan-out 검증은 §10.3 Python 함수 `validate_node_count()` / `check_fanout_uniformity()` 호출.

```yaml
SCBE_compliance_audit:
  activation_condition: "cycle == 'C9'"
  on_skip_condition: "cycle != 'C9'"
  on_skip_action: "Gate 11 → auto-PASS (SKIP); gates_passed += [11]; gates_skipped += [11]"
  
  uniform_fanout_check:
    rule: "Senary leaf를 제외한 모든 노드는 정확히 2 children"
    target: 100%
    measurement:
      # §10.3 check_fanout_uniformity(tree) 호출
      total_non_leaf_nodes: N
      nodes_with_exactly_2_children: M
      compliance_rate: M / N
    fail_threshold: <100%
  
  category_balance_check:
    rule: "각 ring에서 STEEPS 카테고리별 노드 수 ±0 균등"
    expected_per_ring (STEEPS 6 frame):
      Primary:    1 per category (총 6)
      Secondary:  2 per category (총 12)
      Tertiary:   4 per category (총 24)
      Quaternary: 8 per category (총 48)
      Quinary:   16 per category (총 96)
      Senary:    32 per category (총 192)
    measurement:
      per_ring_variance: σ_max - σ_min
      target: 0 (perfect balance)
  
  total_node_count_check:
    # §10.3 validate_node_count("STEEPS",6,2) → expected 379
    # 검산: 1 + 6 + 12 + 24 + 48 + 96 + 192 = 379
    STEEPS_6_expected: 379
    # §10.3 validate_node_count("V2",6,2) → expected 505
    # 검산: 1 + 8 + 16 + 32 + 64 + 128 + 256 = 505
    V2_8_expected: 505
    tolerance: ±0
  
  anchored_tagged_model_check:
    rule_1: "모든 노드에 primary_tag 존재 (STEEPS 카테고리 중 하나)"
    rule_2: "secondary_tags는 옵션, 0~3개 허용"
    rule_3: "자손은 부모의 primary_tag 기본 계승; deviation은 명시적 disclosure 필수"
    measurement:
      nodes_with_primary_tag: <%>
      inheritance_compliance: <%>
  
  3LDP_output_check:
    layer_1_present: "Executive Summary (≤1 page) 생성"
    layer_2_present: "Categorical Tree (collapsible mermaid) 6 또는 8 카테고리 모두"
    layer_3_present: "Full Node Catalog (모든 379 또는 505 노드)"
  
  fail_conditions:
    - uniform_fanout < 100%
    - category_balance variance > 0
    - total_node_count != expected
    - primary_tag 누락 노드 존재
    - layer 1/2/3 누락
  
  on_fail: REVISIONS_REQUIRED → categorical-binary-expansion 재호출
```

---

## 4. 18 Pitfall Checklist (Glenn §IV + endnotes 종합)

| # | Pitfall | Audit Gate |
|---|---------|-----------|
| 1 | Treating impacts as actual predictions | Gate 3 |
| 2 | Single-fact avalanche assumption | Gate 3 |
| 3 | Correlation/causation confusion | Gate 4 |
| 4 | Intellectual spaghetti (over-complex) | Gate 2 |
| 5 | Missed feedback loops | Gate 8 (strengths) |
| 6 | Time blurring between rings | Gate 6 |
| 7 | No probability comparison | Gate 7 |
| 8 | Speculative impacts entered without unanimity | Gate 1 |
| 9 | One-domain dominance (bias) | (delegated to domain-v2 audit) |
| 10 | Cross-linkage missed | (delegated to consequence-linker) |
| 11 | Contradictions overlooked rather than promoted | (delegated to consequence-linker) |
| 12 | Butterfly/attractor candidates ignored | Gate 5 |
| 13 | Output mistaken as truth (not "creative tool") | Gate 3 |
| 14 | Premature judgment from confident-looking ring | Gate 3 |
| 15 | No follow-up systematic exploration plan | Gate 8 |
| 16 | Sourcing tier tags (R-1/R-2/R-3/H) missing from claims | Gate 9·10 (**sourcing/신뢰도 tier — 확률 tier 아님**) |
| 17 | PDF citation missing from creative claims | Gate 9 |
| 18 | Decision-maker action layer missing | (마스터 layer) |

---

## 5. Final Gate Keeper Report

**quality_score 계산 공식** (결정론; LLM 재추론 금지):

| Gate | 가중치 | PASS | PARTIAL | SKIP | FAIL |
|------|--------|------|---------|------|------|
| 1–8 각 | 0.08 | 1.0 | 0.5 | 1.0 | 0.0 |
| 9, 10 각 | 0.12 | 1.0 | 0.5 | 1.0 | 0.0 |
| 11 | 0.08 | 1.0 | 0.5 | 1.0 | 0.0 |

- **가중치 합계**: 8×0.08 + 2×0.12 + 1×0.08 = **0.96** (의도적으로 1.0이 아님)
- **정규화**: `score = Σ(weight_i × status_score_i) / Σ(weight_i)` → 항상 0.0~1.0 보장
- 실제 계산은 §10.4 `calculate_quality_score(gate_results)` 호출

```markdown
## 🛡️ Quality Control Final Report

### Audit Summary
- Gate 1  Wagschal Unanimity:          ✓ PASSED (5/5 impacts revoted)
- Gate 2  Intellectual Spaghetti:      ✓ PASSED (clarity score <§10.1 값>)
- Gate 3  Premature Judgment:          ⚠️ PARTIAL (P1 가정 의존성 disclosed)
- Gate 4  Correlation/Causation:       ✓ PASSED (3 edges reclassified)
- Gate 5  Butterfly Effect:            ✓ PASSED (2 attractor candidates noted)
- Gate 6  Timing Distinction:          ✓ PASSED (S1a·S3c 재분류)
- Gate 7  Probability Comparison:      ✓ PASSED (모든 노드 등급 부여)
- Gate 8  Strengths Self-Audit:        ✓ PASSED (5/5 Glenn §IV strengths demonstrated)
- Gate 9  Citation Completeness:       ✓ PASSED (citation_rate 100%, vague 0, fabricated 0)
- Gate 10 Reasoning Chain + SRS:       ✓ PASSED (CoER chains ≥3, SRS avg <§10.2 값> ≥ 1.5, depth 6)
- Gate 11 SCBE Compliance:             — SKIPPED (non-C9 cycle; auto-PASS)

### Required Disclosures
1. "본 wheel은 *creative tool*이며 truth statement 아님"
2. "edges는 likely impacts (Hume 철학에 따라 인과 자체 입증 불가)"
3. "P1 가정 변경 시 hooked chain 흔들림"
4. "[Attractor] tagged 항목은 작아 보여도 amplification 가능"

### 의사결정자 책임
"본 분석은 추가 systematic exploration의 *입력*입니다. 의사결정 시
TIA·Cross-Impact·Scenario·CLA 등 다른 method와 *반드시* 결합하십시오."

### 마스터로의 반환
status: PASSED
quality_score: <§10.4 calculate_quality_score(gate_results) 반환값>
required_revisions: 0
recommended_next: scenario-forecast for divergence nodes
```

---

## 6. PDF 인용 fragment

> *"The Futures Wheel process leads rapidly to unexpected consequences and, thus, requires a restriction on the group to prevent them from arriving at conclusions that are so speculative as to be of little worth."* (Wagschal in §III.A)

> *"If one is not disciplined in using the Futures Wheel, one can end up with some messy 'intellectual spaghetti'."* (§IV)

> *"One must guard against making dangerously premature judgments."* (§IV)

> *"It can make a group or individual think they understand causal relations between the items that emerge, when it is possible that they have only identified correlations."* (§IV)

> *"The output of a Futures Wheel should be used as a basis for further thinking, for more systematic exploration, and for the application of other techniques for probing the future. Put simply, the Futures Wheel is a creative tool that generates input to futures thinking."* (§IV)

---

## 7. 마스터 입력 인터페이스

```yaml
sub_skill: vision-foresight-futures-wheel-quality-control
inputs:
  prior_wheel_output: { full wheel from basic-v1 or domain-v2 or others }
  consequence_linker_output: { feedback_loops, contradictions }  # 옵션
  enabled_gates: [1,2,3,4,5,6,7,8,9,10,11]   # 일부만 실행 가능
  strictness:
    wagschal:  "Gate 1 만장일치 엄격 + Gate 9·10 100% 기준 + Gate 11 full (C9 시)"
    balanced:  "Gate 1 majority 허용 + Gate 9 95% 기준 + Gate 10 SRS avg ≥1.2 허용"
    fast:      "Gate 1·9·10·11 비활성, Gate 2~8만 적용 (속도 우선)"
  cycle: "C1~C9"   # Gate 11은 C9에서만 활성; 나머지 자동 SKIP

outputs:
  - wagschal_audit_per_impact
  - spaghetti_score              # §10.1 결정론 계산값
  - premature_judgment_alerts
  - causation_reclassifications
  - butterfly_attractors_noted
  - timing_corrections
  - probability_assignments
  - strengths_self_audit
  - citation_audit_report        # Gate 9
  - reasoning_chain_audit_report # Gate 10
  - SRS_audit_report             # Gate 10 §10.2 결정론 계산값
  - MDE_compliance_report        # Gate 10
  - SCBE_compliance_report       # Gate 11 (C9 전용; 비-C9 SKIP)
  - final_gate_keeper_report
  - required_disclosures
  - quality_score                # §10.4 결정론 계산값
  - pdf_citations
```

---

## 8. 호출 후 마스터로 반환

```yaml
sub_skill_output:
  status: PASSED|REVISIONS_REQUIRED|FAILED
  quality_score: <0~1; §10.4 calculate_quality_score(gate_results) 반환값>
  gates_passed: [1,2,3,4,5,6,7,8,9,10,11]
  gates_failed: []
  gates_skipped: []   # 예: [11] — non-C9에서 SKIP (auto-PASS로 처리)
  required_revisions: [...]
  required_disclosures: [...]
  pdf_citations: [...]
```

마스터는 status=REVISIONS_REQUIRED 시 해당 sub-skill 재호출하여 revise.

---

## 9. references/

| 파일 | 용도 |
|------|------|
| `references/wagschal_unanimity_rule.md` | Wagschal 1981 원전 정식화 |
| `references/intellectual_spaghetti_audit.md` | 시각 명료성 알고리즘 |
| `references/correlation_causation_philosophy.md` | Hume·de Jouvenel 원전 + 미래학 적용 |
| `references/butterfly_attractor_detection.md` | chaos theory attractor 식별 |
| `references/18_pitfall_checklist.md` | 18 pitfall 상세 점검 가이드 |
| `references/probability_tier_taxonomy.md` | R-1/R-2/R-3/H tier + 5-grade probability |
| `references/citation_completeness_audit.md` | Gate 9: citation 양식·R-1 의무·fabrication 탐지 기준 |
| `references/reasoning_chain_SRS_audit.md` | Gate 10: CoER 3-step 정의 + SRS 계산법 + MDE 기준 |
| `references/SCBE_compliance_audit.md` | Gate 11: SCBE 모드 검증 기준 (C9 전용) |

---

## 10. Python 결정론 함수 (Deterministic Utilities)

LLM이 자연어로 재추론하면 할루시네이션이 발생할 수 있는 수치 계산을 결정론적 Python으로 분리한다.
마스터 orchestrator는 아래 코드를 `_qc_utils.py`로 저장 후 `python3 _qc_utils.py` 또는 `import`로 호출한다.

```python
#!/usr/bin/env python3
"""
Quality Control Deterministic Utilities
출처: vision-foresight-futures-wheel-quality-control SKILL.md §10
LLM 자연어 재추론 금지 — 이 함수들만 사용.
"""
from __future__ import annotations


# ─── §10.1  Gate 2  Visual Clarity Score ──────────────────────────────────────

def calculate_visual_clarity_score(
    rings_unclear: int = 0,
    no_line_types: bool = False,
    unlabeled_domains: int = 0,
    unmarked_crosslinks: int = 0,
    feedback_unlabeled: int = 0,
) -> float:
    """결정론적 visual clarity score (0.0~1.0). LLM 재추론 금지."""
    score = 1.0
    score -= rings_unclear * 0.15
    if no_line_types:
        score -= 0.10
    score -= unlabeled_domains * 0.10
    score -= unmarked_crosslinks * 0.03
    score -= feedback_unlabeled * 0.05
    return round(max(0.0, score), 4)


def classify_spaghetti_risk(score: float) -> str:
    """low(≥0.75) / medium(0.50–0.74) / high(<0.50) 결정론 분류."""
    if score >= 0.75:
        return "low"
    elif score >= 0.50:
        return "medium"
    return "high"


# ─── §10.2  Gate 10  SRS (Sewongjima Reversal Score) ─────────────────────────
# SRS = 박사님 proprietary metric; 표준 학술 용어 아님.
# Sign convention: "🟢" positive, "🔴" negative, "🟡" neutral (count 제외).

def calculate_srs(sign_sequences: list[list[str]]) -> dict:
    """
    sign_sequences: 각 lineage의 sign 리스트.
      예: [["🟢","🔴","🟢","🔴","🟡","🔴"], ...]
    🟡 는 reversal count에서 제외.
    반환: {per_lineage, global_avg, per_lineage_min_pass, global_avg_pass,
            fail_condition_met, status}
    """
    def _reversals(seq: list[str]) -> int:
        count, prev = 0, None
        for s in seq:
            if s == "🟡":
                continue
            if prev is not None and s != prev:
                count += 1
            prev = s
        return count

    per_lineage = [_reversals(seq) for seq in sign_sequences]
    n = len(per_lineage)
    global_avg = round(sum(per_lineage) / n, 4) if n > 0 else 0.0
    per_lineage_min_pass = all(r >= 1 for r in per_lineage)
    global_avg_pass = global_avg >= 1.5
    fail = global_avg < 1.0
    status = "PASS" if global_avg >= 1.5 else ("REJECT" if fail else "PARTIAL")
    return {
        "per_lineage": per_lineage,
        "global_avg": global_avg,
        "per_lineage_min_pass": per_lineage_min_pass,
        "global_avg_pass": global_avg_pass,
        "fail_condition_met": fail,
        "status": status,
    }


def check_forced_reversals(
    sign_sequences: list[list[str]],
    depth: int = 6,
) -> dict:
    """
    4차(Quaternary)·5차(Quinary)·6차(Senary) 강제 반전 ≥50% 검사.
    sign_sequence 인덱스: 0=Primary, 1=Secondary, 2=Tertiary,
                          3=Quaternary, 4=Quinary, 5=Senary
    depth < 6 이면 SKIP 반환.
    """
    if depth < 6:
        return {"skipped": True, "reason": f"depth={depth} < 6; MDE exception"}

    reversal_pairs = [
        ("T_to_Q",   2, 3, "Tertiary→Quaternary 1차 강제 반전"),
        ("Q_to_Qn",  3, 4, "Quaternary→Quinary 2차 강제 반전"),
        ("Qn_to_Sn", 4, 5, "Quinary→Senary 3차 강제 반전"),
    ]
    results: dict = {}
    for label, prev_idx, curr_idx, desc in reversal_pairs:
        valid = [
            seq for seq in sign_sequences
            if len(seq) > curr_idx
            and seq[prev_idx] != "🟡"
            and seq[curr_idx] != "🟡"
        ]
        if not valid:
            results[label] = {"pass": False, "reason": "no valid non-neutral lineages"}
            continue
        reversed_count = sum(1 for seq in valid if seq[curr_idx] != seq[prev_idx])
        rate = round(reversed_count / len(valid), 4)
        results[label] = {
            "description": desc,
            "valid_lineages": len(valid),
            "reversed_count": reversed_count,
            "reversal_rate": rate,
            "pass": rate >= 0.5,
        }
    all_pass = all(v.get("pass", False) for v in results.values())
    return {"checks": results, "all_pass": all_pass}


# ─── §10.3  Gate 11  SCBE Node Count & Fan-out Validation ────────────────────

def validate_node_count(frame: str, depth: int, fanout: int = 2) -> dict:
    """
    frame: "STEEPS" (6 categories) | "V2" (8 categories)
    depth: ring 수 (예: 6)
    fanout: 노드당 자식 수 (기본 2)
    반환: {frame, categories, depth, fanout, nodes_per_ring, expected_total}
    """
    categories = {"STEEPS": 6, "V2": 8}.get(frame.upper(), 6)
    nodes_per_ring = [categories * (fanout ** i) for i in range(depth)]
    expected = 1 + sum(nodes_per_ring)  # 1 = center node
    return {
        "frame": frame.upper(),
        "categories": categories,
        "depth": depth,
        "fanout": fanout,
        "nodes_per_ring": nodes_per_ring,
        "expected_total": expected,
    }


def check_fanout_uniformity(tree: dict) -> dict:
    """
    tree: {node_id: {"children": [child_id, ...], "is_leaf": bool}}
    반환: {compliance_rate, non_compliant_nodes, pass}
    Senary leaf 제외 — 모든 비-leaf 노드는 정확히 2 children이어야 함.
    """
    non_leaf = [nid for nid, data in tree.items() if not data.get("is_leaf", False)]
    if not non_leaf:
        return {"compliance_rate": 1.0, "non_compliant_nodes": [], "pass": True}
    non_compliant = [nid for nid in non_leaf if len(tree[nid].get("children", [])) != 2]
    rate = round(1.0 - len(non_compliant) / len(non_leaf), 4)
    return {
        "compliance_rate": rate,
        "non_compliant_nodes": non_compliant,
        "pass": rate == 1.0,
    }


# ─── §10.2b  Gate 10  MDE Compliance Check ───────────────────────────────────

EXCEPTION_KEYWORDS = ["간단히", "빠르게", "대충"]


def check_mde_compliance(
    depth_reached: int,
    user_message: str = "",
    master_override_depth: int | None = None,
) -> dict:
    """
    depth_reached: 실제 wheel 깊이 (1~6)
    user_message: 사용자 원문 (예외 키워드 포함 여부 검사)
    master_override_depth: 마스터가 명시한 허용 최소 깊이 (4 또는 5)
    반환: {required_depth, depth_reached, exception_triggered, pass, fail_reason}
    """
    required = 6
    exception_triggered = False
    exception_type = None

    user_exception = any(kw in user_message for kw in EXCEPTION_KEYWORDS)
    if user_exception:
        required = 3
        exception_triggered = True
        exception_type = "user_keyword"
    elif master_override_depth is not None and master_override_depth in (4, 5):
        required = master_override_depth
        exception_triggered = True
        exception_type = "master_override"

    ok = depth_reached >= required
    return {
        "required_depth": required,
        "depth_reached": depth_reached,
        "exception_triggered": exception_triggered,
        "exception_type": exception_type,
        "pass": ok,
        "fail_reason": None if ok else f"depth {depth_reached} < required {required}",
    }


# ─── §10.3b  Gate 9  Citation Rate Check (strictness-aware) ─────────────────

def check_citation_rate(
    impacts: list[dict],
    strictness: str = "wagschal",
) -> dict:
    """
    impacts: [{id, citation: str|None, has_number: bool, r1_source: str|None}]
    strictness: "wagschal" | "balanced" | "fast"
    반환: {citation_rate, vague_count, fabricated_count, pass, fail_reasons}
    """
    VAGUE_PATTERNS = ["(전문가 의견)", "(연구에 따르면)", "(보고서)"]
    FABRICATED_PATTERNS = ["study by", "research from", "according to"]

    if strictness == "fast":
        return {"skipped": True, "reason": "fast mode: Gate 9 inactive"}

    total = len(impacts)
    if total == 0:
        return {"citation_rate": 1.0, "vague_count": 0, "fabricated_count": 0,
                "pass": True, "fail_reasons": []}

    with_citation = sum(1 for i in impacts if i.get("citation"))
    vague = sum(1 for i in impacts
                if any(p in (i.get("citation") or "") for p in VAGUE_PATTERNS))
    fabricated = sum(1 for i in impacts
                     if any(p in (i.get("citation") or "").lower()
                            for p in FABRICATED_PATTERNS)
                     and not i.get("url_verified", False))
    rate = round(with_citation / total, 4)

    threshold = 1.0 if strictness == "wagschal" else 0.95  # balanced = 95%

    fail_reasons = []
    if rate < threshold:
        fail_reasons.append(f"citation_rate {rate} < {threshold}")
    if vague > 0:
        fail_reasons.append(f"vague_attribution_count={vague}")
    if fabricated > 0:
        fail_reasons.append(f"fabricated_source_count={fabricated}")

    return {
        "citation_rate": rate,
        "vague_count": vague,
        "fabricated_count": fabricated,
        "threshold_used": threshold,
        "pass": len(fail_reasons) == 0,
        "fail_reasons": fail_reasons,
    }


# ─── §10.4  Final Quality Score ───────────────────────────────────────────────

GATE_WEIGHTS: dict[int, float] = {
    1: 0.08, 2: 0.08, 3: 0.08, 4: 0.08,
    5: 0.08, 6: 0.08, 7: 0.08, 8: 0.08,
    9: 0.12, 10: 0.12, 11: 0.08,
}
GATE_STATUS_SCORES: dict[str, float] = {
    "PASS": 1.0, "PARTIAL": 0.5, "SKIP": 1.0, "FAIL": 0.0
}
SKIP_ELIGIBLE_GATES: set[int] = {11}  # 비-C9에서 자동 SKIP


def calculate_quality_score(gate_results: dict[int, str]) -> float:
    """
    gate_results: {gate_number: status}
      status: "PASS" | "PARTIAL" | "SKIP" | "FAIL"
    SKIP_ELIGIBLE_GATES 중 gate_results에 없는 항목은 자동 SKIP으로 처리.
    반환: quality_score (0.0~1.0), 가중 정규화 평균.
    """
    full: dict[int, str] = {**gate_results}
    for g in SKIP_ELIGIBLE_GATES:
        if g not in full:
            full[g] = "SKIP"

    weighted_sum = 0.0
    weight_used = 0.0
    for gate_num, status in full.items():
        w = GATE_WEIGHTS.get(gate_num, 0.08)
        s = GATE_STATUS_SCORES.get(status.upper(), 0.0)
        weighted_sum += w * s
        weight_used += w
    return round(weighted_sum / weight_used, 4) if weight_used > 0 else 0.0


# ─── 자가 테스트 ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=== §10.1 visual_clarity_score ===")
    assert calculate_visual_clarity_score() == 1.0
    assert calculate_visual_clarity_score(rings_unclear=1, no_line_types=True) == 0.75
    print("PASS: 1.0, 0.75")

    print("\n=== §10.1 spaghetti_risk ===")
    assert classify_spaghetti_risk(0.80) == "low"
    assert classify_spaghetti_risk(0.60) == "medium"
    assert classify_spaghetti_risk(0.40) == "high"
    print("PASS: low/medium/high")

    print("\n=== §10.2 calculate_srs ===")
    seqs = [
        ["🟢", "🔴", "🟢", "🔴", "🔴", "🟢"],  # reversals: 4+1 (🟢→🔴,🔴→🟢,🟢→🔴,🔴→🟢 at[4→5])
        ["🔴", "🔴", "🟡", "🟢", "🟢", "🔴"],  # 🟡 skip → prev=🔴,curr=🟢 reversal, then 🟢→🔴
    ]
    result = calculate_srs(seqs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    assert result["global_avg"] > 0

    print("\n=== §10.2 check_forced_reversals (depth<6 skip) ===")
    skip_result = check_forced_reversals(seqs, depth=3)
    assert skip_result.get("skipped") is True
    print("PASS: skipped=True for depth=3")

    print("\n=== §10.3 validate_node_count ===")
    r_steeps = validate_node_count("STEEPS", 6, 2)
    assert r_steeps["expected_total"] == 379, f"Got {r_steeps['expected_total']}"
    r_v2 = validate_node_count("V2", 6, 2)
    assert r_v2["expected_total"] == 505, f"Got {r_v2['expected_total']}"
    print(f"PASS: STEEPS={r_steeps['expected_total']}, V2={r_v2['expected_total']}")

    print("\n=== §10.4 calculate_quality_score ===")
    all_pass = {i: "PASS" for i in range(1, 12)}
    assert calculate_quality_score(all_pass) == 1.0, calculate_quality_score(all_pass)
    partial_3 = {**all_pass, 3: "PARTIAL"}
    score = calculate_quality_score(partial_3)
    assert 0.9 < score < 1.0, score
    print(f"PASS: all-PASS=1.0, partial-Gate3={score}")

    gate11_skip = {i: "PASS" for i in range(1, 11)}  # Gate 11 absent
    score_skip = calculate_quality_score(gate11_skip)
    assert score_skip == 1.0, score_skip  # Gate 11 auto-SKIP = PASS
    print(f"PASS: Gate11 auto-SKIP score={score_skip}")

    print("\n=== §10.3b check_citation_rate ===")
    impacts_ok = [{"id": f"P{i}", "citation": f"[Author, 202{i}]"} for i in range(5)]
    r_ok = check_citation_rate(impacts_ok, "wagschal")
    assert r_ok["pass"] is True
    print(f"PASS: all-cited wagschal → pass=True")

    impacts_vague = impacts_ok[:4] + [{"id": "P4", "citation": "(전문가 의견)"}]
    r_vague = check_citation_rate(impacts_vague, "wagschal")
    assert r_vague["pass"] is False and r_vague["vague_count"] == 1
    print(f"PASS: vague → pass=False, vague_count={r_vague['vague_count']}")

    # balanced: 4/5 = 80% < 95% threshold → fail
    impacts_missing = impacts_ok[:4] + [{"id": "P4", "citation": None}]
    r_bal = check_citation_rate(impacts_missing, "balanced")
    assert r_bal["pass"] is False  # 0.80 < 0.95
    print(f"PASS: balanced 80% citation → pass=False (threshold=0.95)")

    r_fast = check_citation_rate(impacts_ok, "fast")
    assert r_fast.get("skipped") is True
    print(f"PASS: fast mode → skipped=True")

    print("\n=== §10.2b check_mde_compliance ===")
    r_no_exc = check_mde_compliance(depth_reached=4)
    assert r_no_exc["pass"] is False and r_no_exc["required_depth"] == 6
    print(f"PASS: depth=4 no exception → fail (required=6)")

    r_user_exc = check_mde_compliance(depth_reached=3, user_message="빠르게 해줘")
    assert r_user_exc["pass"] is True and r_user_exc["required_depth"] == 3
    print(f"PASS: depth=3 + '빠르게' → pass (required=3)")

    r_master = check_mde_compliance(depth_reached=5, master_override_depth=5)
    assert r_master["pass"] is True and r_master["exception_type"] == "master_override"
    print(f"PASS: depth=5 + master_override=5 → pass")

    r_full = check_mde_compliance(depth_reached=6)
    assert r_full["pass"] is True
    print(f"PASS: depth=6 no exception → pass")

    print("\n모든 자가 테스트 PASS")
```
