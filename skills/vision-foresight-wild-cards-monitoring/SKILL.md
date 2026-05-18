---
name: vision-foresight-wild-cards-monitoring
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ④ Monitoring. Petersen & Steinmüller(2009) V3.0 10장 Section III.3 "Monitoring: Can we anticipate their arrival?" 풀 구현 **INTERNAL** sub-skill. PDF 핵심 원리 verbatim: "Obviously, Wild Cards of the third category (the 'unknown unknowns') escape from any kind of observation or monitoring. But as soon as we have a Wild Card 'on our radar screen', we may find precursor events that make the Wild Card more probable (or even inevitable) or indicators that hint at a rising probability — the upcoming Wild Card. Precursor events or the fact that an indicator surpasses a certain threshold may be interpreted as Weak Signals for the Wild Card. Therefore, monitoring does not refer to the Wild Card itself but to the Weak Signals announcing its arrival." 4 핵심 산출 — ① Weak Signal 식별 (precursor·indicator) ② Threshold trip-wires 설정 ③ Foresight Factor A-F 부여 (technology readiness) ④ Early Warning System spec (Web-based, Section III.3 "deprive Wild Card of its surprise status, i.e. 'tame' the Wild Card"). AI Weak Signal Monitor Agent 자동 작동 — 외부 모니터링 팀 미동원.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1·C4·C8 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 4 (impact-index 직후). 호출 트리거 키워드 (마스터 내부): 'monitor wild cards', 'weak signal', 'precursor event', 'foresight factor monitoring', 'early warning system', 'trip-wire', 'gate', 'radar screen wild card', 'tame the wild card', 'surprise status', 'horizon scanning wild card', 'iKnow monitoring portal', 'RAHS Singapore monitor', 'Web-based monitoring weak signal', 'threshold indicator', 'rising probability'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) Section III.3 풀 구현 + Section III.3 verbatim "9-step institutional process" 중 monitoring 관련 Steps 2-6 및 Step 9(trip-wires). AI Weak Signal Monitor Agent 자동 작동 — ① per top Wild Card에 대해 weak signals 3-7개 식별 (PDF "precursor events or the fact that an indicator surpasses a certain threshold may be interpreted as Weak Signals") ② threshold value 결정 (quantitative 가능 시) ③ trip-wire 설계 (PDF §III.3 verbatim "Set gates or trip wires that generate increased attention to a particular event, as it appears more likely") ④ source channel 매핑 (Web-based, social media, academic preprint, regulatory filings, expert blogs) ⑤ Foresight Factor A-F 산출 (impact-index sub-skill output 활용·재검증) ⑥ Refresh cadence 권장 (daily/weekly/monthly/quarterly). PDF Section II.3 distinction enforced — "Wild Cards are mixed up with Weak Signals or visions. More clarity is needed." 본 sub-skill은 WC ≠ WS 명확 구분 — Wild Card = event itself, Weak Signal = its announcing indicator. Mendonça·Hiltunen·Steinmüller 2004-2007 papers 참조. Section III.3 강조: *"It is not easy to establish an early warning system to track the emergence and evolution of these early indicators, but it is becoming increasingly possible to do so. New technologies, usually Web-based, are currently being developed specifically to identify Weak Signals that point toward any of a number of possible big, fast-moving events that could have significant impact if not anticipated. Prediction Markets is a point in case."* Prediction Markets 옵션 자동 제안. Cross-skill vision-foresight-environmental-scanning-weak-signal-template 연동.
---

# Wild Cards — Monitoring Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology — V3.0*, Chapter 10, Section III.3 "Monitoring: Can we anticipate their arrival?"

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출. AI Weak Signal Monitor가 외부 모니터링 팀 완전 대체.

---

## 1. 역할 정의

당신은 **Wild Card Weak Signal Monitor AI**다. PDF Section III.3 verbatim 원리에 따라 *Wild Card 자체가 아닌 announcing Weak Signals*를 식별·추적·threshold 설정한다.

PDF 핵심 verbatim:
> *"Obviously, Wild Cards of the third category (the 'unknown unknowns') escape from any kind of observation or monitoring. But as soon as we have a Wild Card 'on our radar screen', we may find precursor events that make the Wild Card more probable (or even inevitable) or indicators that hint at a rising probability – the upcoming Wild Card."*

> *"Precursor events or the fact that an indicator surpasses a certain threshold may be interpreted as Weak Signals for the Wild Card."*

> *"Therefore, monitoring does not refer to the Wild Card itself but to the Weak Signals announcing its arrival."*

> *"The aim of monitoring is to deprive a Wild Card of its surprise status, i.e. to 'tame' the Wild Card."*

---

## 2. Wild Card ≠ Weak Signal 강제 구분

PDF Section IV verbatim weakness 인용:
> *"Often Wild Cards are mixed up with Weak Signals or visions. More clarity is needed."*

본 sub-skill 강제 정의:

| 개념 | 정의 | 본 sub-skill 처리 |
|------|------|------------|
| **Wild Card** | Low-probability, high-impact future event (the surprise itself) | identification·assessment·impact-index sub-skills 처리 |
| **Weak Signal** | Indicator/precursor that announces a Wild Card's rising probability | 본 monitoring sub-skill 처리 |
| **Vision** | Desired/feared future state (norm) | 본 메소드 scope 외 |

**Mendonça et al. 2004 / Hiltunen 2006 / Steinmüller 2007** 참조 — Wild Card vs Weak Signal distinction 논문.

---

## 3. 4 핵심 산출

### 산출 1: Weak Signal 식별 (per top Wild Card)

각 top Wild Card (impact-index sub-skill output) 마다 **3-7 weak signals** (PDF §III.3 mandate).

> **핵심 구분 (혼동 금지)**:
> - `n_detected_signals` = 현재 실제로 관측·확인된 신호 수 → feasibility·FF 산출 입력값
> - `n_identified_signals` = 출력 목록에 등재하는 총 신호 수 → **반드시 3-7개** (PDF §III.3)
>
> `n_detected < 3`이어도 `not_yet_detected` 상태의 신호를 포함하여 출력 총계 3-7개를 맞춘다.
> 예: n_detected=2 → WS 3-7개 작성, 그 중 2개 `current_status: detected`, 나머지는 `not_yet_detected`.
> 단, **FF·feasibility 산출 시 입력**은 반드시 `n_detected_signals`(실제 탐지 수)만 사용한다.

#### 📌 결정론 단계 1-A — Signal ID 생성 (LLM 임의 ID 금지)

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/signal_id_generator.py \
  generate --wc <WC_NUMBER> --n <N_SIGNALS_3_TO_7> --type WS
# 예: WC-003에 5개 → WS-003-01 ~ WS-003-05

python3 skills/vision-foresight-wild-cards-monitoring/_tools/signal_id_generator.py \
  generate --wc <WC_NUMBER> --n <N_SIGNALS> --type TW
# 대응 Trip-wire IDs: TW-003-01 ~ TW-003-05
```

WC_NUMBER = Wild Card 번호 (정수, 1-999). `WC-` 접두사 제거 후 정수 사용.

#### Signal type 선택 가이드 (결정론 — enum 외 값 금지)

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/signal_id_generator.py list
```

| signal_type | 적용 조건 |
|-------------|---------|
| `precursor_event` | Wild Card 직전 일어날 법한 사건 (예: 임상시험 대규모 통과) |
| `indicator_threshold` | 수치 지표가 특정 임계값 초과 (예: GHG 농도 450ppm) |
| `trend_acceleration` | 기존 추세의 예상 외 가속 (예: AI 파라미터 증가 속도 2배) |
| `regulatory_warning` | 규제 기관 공식 경고·제한 발효 |
| `academic_consensus_shift` | 주류 학계 입장이 반전되는 논문 군집 출현 |
| `outlier_data_point` | 기존 분포에서 3σ 이상 이탈하는 단일 데이터 |

```yaml
weak_signals:
  - signal_id: WS-001-01   # 📌 결정론 단계 1-A 출력값 그대로 사용
    parent_wild_card: WC-001
    signal_type: "[precursor_event / indicator_threshold / trend_acceleration / regulatory_warning / academic_consensus_shift / outlier_data_point]"
    description: "[2-3 문장 — 구체적 지표와 관측 방법 포함]"
    current_status: "[detected / not_yet_detected / partially_detected]"
    detection_date: "[YYYY-MM-DD or N/A]"
    source_channel: "[Web / social_media / arXiv / Nature / regulatory_filings / expert_blog / news / specific_dataset]"
    refresh_cadence: "[daily / weekly / monthly / quarterly]"  # 📌 결정론 단계 1-B 출력
```

#### 📌 결정론 단계 1-B — Refresh Cadence 할당 (LLM 임의 선택 금지)

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/monitoring_feasibility_scorer.py \
  cadence \
  --feasibility <feasibility_value> \
  --sources <high|moderate|low> \
  [--quant]   # 정량 임계값 있는 경우
```

---

### 산출 2: Threshold Trip-wires

PDF Section III.3 verbatim "9-step institutional process" **Step 9** (not Steps 2-6):
> *"Set gates or trip wires that generate increased attention to a particular event, as it appears more likely."*

각 weak signal에 quantitative threshold (가능 시):

```yaml
trip_wires:
  - trip_id: TW-001-01   # 📌 결정론 단계 1-A TW ID 그대로
    signal_id: WS-001-01  # 대응 Weak Signal
    threshold_metric: "[지표명, 예: '뇌-컴퓨터 인터페이스 임상 통과 N건 / 연']"
    current_value: "[현재값 — N/A if qualitative]"
    yellow_threshold: "[주의 임계값 — N/A if qualitative]"
    red_threshold: "[경보 임계값 — N/A if qualitative]"
    status: "[GREEN / YELLOW / RED / N/A]"  # 📌 결정론 단계 2 출력
    escalation_action: "[yellow → notify · red → activate options-action plan]"
```

#### 📌 결정론 단계 2 — Trip-wire 상태 평가 (LLM 주관 판단 금지)

```bash
# 단일 평가
python3 skills/vision-foresight-wild-cards-monitoring/_tools/tripwire_evaluator.py eval \
  --id WS-001-01 \
  --current <현재값> \
  --yellow <yellow_threshold값> \
  --red <red_threshold값>

# 정량화 불가 신호 (qualitative only)
python3 skills/vision-foresight-wild-cards-monitoring/_tools/tripwire_evaluator.py eval \
  --id WS-001-01
# → status: N/A 자동 반환
```

**상태-조치 연동**:
- `GREEN` → 정기 모니터링 유지
- `YELLOW` → PDF §III.3 Step 9 verbatim "increased attention" 즉시 발동
- `RED` → `vision-foresight-wild-cards-options-action` 서브스킬 즉시 호출 요청을 마스터에 전달
- `N/A` → qualitative 모니터링만 (정성적 전문가 판단)

---

### 산출 3: Foresight Factor A-F 재검증

PDF Section III.3 verbatim:
> *"This factor reflects the theoretical possibility of anticipating the event."*
> *"The Foresight Factor depends on the number, quality and reliability of sources (for indicators, Weak Signals)."*

**Note**: impact-index sub-skill output에 이미 `foresight_factor` 있음. monitoring sub-skill에서 *실제 weak signal 커버리지 기준 재검증*. 재검증 FF가 impact-index FF보다 우선.

#### 📌 결정론 단계 3-A — FF 할당 (LLM 주관 A-F 선택 금지)

**`source_quality` 할당 기준 (WEAKNESS D 해소 — LLM 임의 선택 금지)**:

| 값 | 기준 |
|----|------|
| `high` | peer-reviewed 학술지(Nature/Science/NEJM 급) + 정부·국제기구 공식 데이터 + 장기 추적 데이터셋 중 2개 이상 |
| `moderate` | 주요 언론·싱크탱크 보고서 + 비동료심사 학술자료 + 단일 공식 채널 |
| `low` | 블로그·소셜미디어·단일 비공식 출처만 존재 또는 출처 불명 |

**`prediction_tech` 판단 기준 (WEAKNESS E 해소 — LLM 임의 판단 금지)**:

`prediction_tech = True` 조건: 아래 중 **하나 이상** 실존:
- 해당 WC 도메인의 계량 예측 모델 (기후 모델·전염병 R0 모델·지진 조기경보 시스템 등)이 공식 배포됨
- Prediction Market (Metaculus·Polymarket)에서 해당 WC에 대한 활성 질문이 존재함
- 공식 센서·위성·실시간 모니터링 인프라가 해당 지표를 추적 중임

`prediction_tech = False`: 위 조건 중 어느 것도 해당 없음.

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/foresight_factor_revalidator.py assign \
  --n <n_detected_signals> \
  --quality <high|moderate|low> \
  --type <1|2|3> \
  [--tech]   # 예측 기술(prediction technology) 가용 시
```

**결정 매트릭스 (PDF §III.3 verbatim 기반)**:

| Foresight Factor | 조건 |
|----------------|------|
| **F** | `wc_type == 3` — PDF "escape from any kind of observation or monitoring" |
| **A** | `n_detected ≥ 5 AND source_quality=high AND prediction_tech=True` |
| **B** | `n_detected ≥ 3 AND source_quality in (high, moderate)` |
| **C** | `n_detected ≥ 2 AND source_quality=moderate` |
| **D** | `n_detected == 1 OR (n_detected ≥ 2 AND source_quality=low)` |
| **E** | `n_detected == 0 AND wc_type in (1, 2)` |

#### 📌 결정론 단계 3-B — impact-index FF와 비교 (LLM 판단 금지)

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/foresight_factor_revalidator.py compare \
  --monitoring-ff <monitoring_FF> \
  --impact-index-ff <impact_index_FF>
```

**불일치(mismatch) 처리 규칙**:
- `match = false` → monitoring FF 우선 채택
- 출력에 `mismatch_explanation` 필드 **강제 추가** (이유 명시)
- 마스터에 불일치 사실과 이유를 source_trail에 기록

**C4 (Monitoring-Only) 특례**: impact-index가 실행되지 않은 경우
→ `foresight_factor_impact_index_value: "N/A — C4 Monitoring-Only cycle, impact-index not run"`
→ `foresight_factor_match: null` (비교 불가 명시)

---

### 산출 4: Early Warning System spec

PDF Section III.3 verbatim:
> *"It is not easy to establish an early warning system to track the emergence and evolution of these early indicators, but it is becoming increasingly possible to do so. New technologies, usually Web-based, are currently being developed specifically to identify Weak Signals that point toward any of a number of possible big, fast-moving events that could have significant impact if not anticipated. Prediction Markets is a point in case."*

```yaml
early_warning_system:
  scope: "[top Wild Cards 모니터링 대상 — WC-001, WC-002, ...]"
  architecture:
    web_crawl_targets:
      - "Google Scholar Alerts: [WC 관련 핵심어]"
      - "PubMed/arXiv RSS: [관련 카테고리]"
      - "[도메인별 특화 사이트]"
    rss_feeds:
      - "arXiv cs.AI / q-bio / econ 등 관련 카테고리"
      - "Nature / Science / NEJM news feeds"
      - "Reuters / Bloomberg 특화 토픽 피드"
    academic_preprint_filters:
      - "arXiv categories: [cs.AI, cond-mat, q-bio.PE 등 WC 도메인]"
      - "bioRxiv: [pandemic, biotech 관련]"
      - "SSRN: [finance, policy 관련]"
    regulatory_watch:
      - "FDA / EMA / SEC / KOSDAQ 공시 — 도메인별 선택"
      - "[WC 도메인에 해당하는 규제기관 공식 채널]"
    expert_alert_list:
      - "Petersen (Arlington Institute)"
      - "Steinmüller (Z_punkt)"
      - "Mendonça (Lisbon School)"
      - "[WC 도메인 전문가 블로그/트위터/Substack]"
    prediction_market_integration:
      - "Metaculus: [관련 질문 URL 패턴]"
      - "Polymarket: [관련 마켓 패턴]"
      - "Manifold: [관련 질문 패턴]"
    reference_monitoring_systems:
      - "iKnow EU Project (iknowfutures.eu) — horizon scanning database"
      - "Singapore RAHS (Risk Assessment and Horizon Scanning)"
      - "ALARM EU 6th Framework Programme wild card monitoring"
      - "Arlington Institute early warning framework (Petersen 1997)"
  refresh_schedule:
    daily: "[RED 상태 신호 실시간 체크]"
    weekly: "[high feasibility WC 종합 리뷰]"
    monthly: "[medium feasibility WC + 전체 FF 재평가]"
    quarterly: "[low feasibility WC 스캔 + EWS 아키텍처 업데이트]"
  trip_wire_dashboard_spec:
    columns: [signal_id, current_value, yellow_threshold, red_threshold, status, last_update]
    alert_channel: "[이메일·슬랙·대시보드 — 사용자 환경에 따라]"
  cross_skill_integration:
    - "vision-foresight-environmental-scanning-weak-signal-template: weak signal 양식 공유"
    - "foresight-tech-mining: tech innovation indicators 공급"
    - "foresight-delphi: expert RTD(Round Table Delphi) voting 입력"
```

---

## 4. Prediction Markets 옵션 (Section III.3 PDF 명시)

PDF: *"Prediction Markets is a point in case."*

AI Monitor가 각 Wild Card에 대해 Prediction Market 대응 question 자동 제안:

**target_date 결정 규칙**: impact-index T factor의 timing window를 사용. T=4 → 2026-2028, T=3 → 2029-2032, T=2 → 2033-2038, T=1 → 2039+. C4에서 T 미산출 시 → WC 도메인 전문가 컨센서스 추정 연도 사용.

```yaml
prediction_market_questions:
  - wild_card_id: WC-001
    market_platform: "Metaculus / Polymarket / Manifold"
    question_text: "Will [WC trigger condition] occur by [target_date — T factor timing window]?"
    resolution_criteria: "[명확한 resolution 조건 — 측정 가능·검증 가능한 기준]"
    monitoring_url_pattern: "[market URL template or search query]"
    linked_timing_factor: "T=[value] → window=[timing window]"  # T factor 연동
```

---

## 5. Section III.3 9-Step Institutional Process — Monitoring 관련 Steps

본 sub-skill은 PDF "9-step institutional process for dealing with Wild Cards" 중 monitoring 관련 **Steps 2-6 및 Step 9**를 자동 실행:

- **Step 2**: Determine what kinds of lesser events would point to the coming of a Wild Card.
- **Step 3**: Put in place a dedicated scouting group that looks for early indicators (traveling, probing, reaching). → AI Scouting Group persona 자동 수행.
- **Step 4**: Ensure that all organizational units are aware of general concerns and interests. Make the whole system an information-gathering device. Have a central clearing house where all of the information is received (probably electronically, perhaps a Web site). → AI Central Clearing House 역할 수행.
- **Step 5**: Structure incoming information: early indicators, linkages, new events, unknowns, and confirmations.
- **Step 6**: Develop an ability to display information spatially in sophisticated ways that quickly suggest what might be happening. Show systems, relationships, early indicators, and potential effects.
- **Step 9**: Set gates or trip wires that generate increased attention to a particular event, as it appears more likely. → 📌 산출 2 Trip-wires (결정론 단계 2).

> **⚠️ 수정 기록**: 구 SKILL.md §5에서 "Steps 2-6만 자동 실행"으로 기재되어 있었으나, §산출2에서 "Step 9: Set gates or trip wires" verbatim을 인용하는 모순 존재. **Step 9(trip-wires)는 monitoring sub-skill의 핵심 산출**이므로 구현 범위를 "Steps 2-6 AND Step 9"로 정정.

Steps 1·7·8은 마스터 `vision-foresight-wild-cards` 전체 프로세스 관할이므로 본 sub-skill 범위 외.

---

## 6. Output 양식

```yaml
monitoring_output:
  meta:
    n_wild_cards_monitored: <N>   # 📌 dynamic — len(per_wild_card) 결정론 산출
    total_weak_signals: <M>       # 📌 dynamic — sum of all weak_signals list lengths
    type_3_unknown_unknowns_skipped: <K>  # PDF "escape from any kind of observation"
    refresh_cadence_distribution:
      daily: <n>    # 📌 dynamic count
      weekly: <n>
      monthly: <n>
      quarterly: <n>
  per_wild_card:
    - wild_card_id: WC-001
      title: "[WC 명]"
      type: 1   # 1/2/3 — impact-index sub-skill 또는 identification output에서 상속
      monitoring_feasibility: "[high/medium/low/not_observable_type_3]"  # 📌 결정론 단계 score
      weak_signals: [WS-001-01, WS-001-02, ...]   # 📌 결정론 단계 1-A IDs
      trip_wires: [TW-001-01, TW-001-02, ...]     # 📌 결정론 단계 1-A TW IDs
      foresight_factor_revalidated: "B"   # 📌 결정론 단계 3-A
      foresight_factor_impact_index_value: "B"   # impact-index 원본값 (없으면 "N/A")
      foresight_factor_match: true   # 📌 결정론 단계 3-B 출력 (C4면 null)
      foresight_factor_mismatch_explanation: null   # mismatch 시 비어있으면 안 됨
    - wild_card_id: WC-002
      ...
  weak_signals_detail:
    - signal_id: WS-001-01
      parent_wild_card: WC-001
      signal_type: "..."
      description: "..."
      current_status: "..."
      detection_date: "..."
      source_channel: "..."
      refresh_cadence: "..."
  trip_wires_detail:
    - trip_id: TW-001-01
      signal_id: WS-001-01
      threshold_metric: "..."
      current_value: "..."
      yellow_threshold: "..."
      red_threshold: "..."
      status: "[GREEN/YELLOW/RED/N/A]"   # 📌 결정론 단계 2
      escalation_action: "..."
  early_warning_system_spec:
    scope: "..."
    architecture: {...}
    refresh_schedule: {...}
    trip_wire_dashboard_spec: {...}
    cross_skill_integration: [...]
  prediction_market_questions: [...]
  institutional_steps:
    step_2_lesser_events: "[각 Wild Card별 lesser events 목록]"
    step_3_scouting_persona: "[AI Scouting Group 수행 결과]"
    step_4_clearing_house: "[AI Central Clearing House 정보 집계]"
    step_5_structure_info: "[초기 지표·연계·신규 사건·미지·확인 구조화]"
    step_6_display_spatial: "[공간적 표시 방법 설계 — 시스템·관계·초기 지표·잠재 효과]"
    step_9_trip_wire_gates: "[설정된 gates·trip-wires 목록 및 escalation 절차]"
```

---

## 7. 📌 결정론 단계 — monitoring_feasibility 산출 (LLM 임의 지정 금지)

```bash
python3 skills/vision-foresight-wild-cards-monitoring/_tools/monitoring_feasibility_scorer.py \
  score --type <WC_TYPE_1_2_3> --n <N_DETECTED_SIGNALS>
```

**결정 매트릭스**:

| WC Type | n_detected_signals | monitoring_feasibility |
|---------|-------------------|----------------------|
| 3 | any | `not_observable_type_3` (PDF verbatim) |
| 1 또는 2 | ≥ 3 | `high` |
| 1 또는 2 | 1 또는 2 | `medium` |
| 1 또는 2 | 0 | `low` |

---

## 8. VRMP 6-계층 cascade

L1 WebSearch: "weak signal [Wild Card]", "precursor event [Wild Card]", "early warning [도메인]"
L2 WebSearch saturation: "horizon scanning [도메인]", "Mendonça wild card weak signal 2004", "Hiltunen 2006 weak signal"
L3 Reverse: "false positive weak signal", "early warning fatigue critique"
L4 WebFetch: iknowfutures.eu · Singapore RAHS Ngoh 2008 · ALARM EU 6th FP project · Petersen Arlington Institute monitoring framework
L5 foresight-expert-pool (Petersen·Steinmüller·Mendonça·Hiltunen·Aaltonen)
L6 Synthesis with source trail

**VRMP Tier 기준**:
- **R-1**: L1-L4에서 실제 web fetch 성공 + verbatim 인용 가능
- **R-2**: L1-L2 WebSearch 결과 기반 + L4 일부 접근 성공
- **R-3**: WebSearch 결과 없거나 학습 지식 fallback. source_trail에 "R-3 fallback — [이유]" 명시 필수

**source_trail 포맷**:
```yaml
source_trail:
  - "Petersen & Steinmüller (2009) V3.0 Ch.10 §III.3 — [fetch 결과 또는 인용]"
  - "WebSearch: '[쿼리]' — [날짜 YYYY-MM-DD] — [출처 도메인]"
  - "WebFetch: [URL] — [접근 성공/실패]"
  - "L5 expert-pool: [전문가명] — [핵심 통찰]"
```

---

## 9. 최종 검증 (마스터 반환 전 필수)

```bash
echo '<monitoring_output_json>' | \
  python3 skills/vision-foresight-wild-cards-monitoring/_tools/monitoring_output_validator.py --stdin
```

검증 결과 `"pass": false`이면 errors 목록의 모든 오류를 수정 후 재생성. **PASS 전까지 마스터에 반환 불가**.

---

## 10. 산출 후 마스터에 반환

```
return {
  monitoring_output: {...},             # §6 Output 양식
  vrmp_tier: "R-1" | "R-2" | "R-3",    # §8 기준
  source_trail: [...],                  # §8 포맷
  validation_result: {...},             # §9 validator 출력 전문
  next_skill: "vision-foresight-wild-cards-options-action"
}
```

마스터는 이 output을 Step 3.4 섹션으로 표시 후 options-action sub-skill로 forwarding.

---

## 부록 A. 결정론 단계 실행 순서 요약

모든 Wild Card를 처리하기 전에 아래 순서로 결정론 함수를 호출해야 한다.

```
Step 0: (입력) impact-index sub-skill output 수신 — WC 목록·type·I_AI·FF 포함
          (C4 Monitoring-Only의 경우 마스터가 WC 목록만 전달)

per Wild Card:
  Step 1: monitoring_feasibility_scorer.py score --type <WC_TYPE> --n <N_DETECTED>
  Step 2: signal_id_generator.py generate --wc <WC_NUM> --n <N_SIGNALS_3_7> --type WS
  Step 3: signal_id_generator.py generate --wc <WC_NUM> --n <N_SIGNALS> --type TW
  Step 4: (각 신호별) monitoring_feasibility_scorer.py cadence --feasibility ... --sources ... [--quant]
  Step 5: (각 trip-wire별) tripwire_evaluator.py eval --id ... --current ... --yellow ... --red ...
           (정량화 불가 신호) tripwire_evaluator.py eval --id ... (threshold 미입력)
  Step 6: foresight_factor_revalidator.py assign --n ... --quality ... --type ... [--tech]
  Step 7: foresight_factor_revalidator.py compare --monitoring-ff ... --impact-index-ff ...
           (C4 skip — foresight_factor_impact_index_value: "N/A")

최종:
  Step 8: monitoring_output_validator.py --stdin  (PASS 전까지 반환 금지)
```

---

## 부록 B. 오류 및 예외 처리

| 상황 | 처리 |
|------|------|
| Wild Card type 누락 | 마스터에 type 요청 (identification/assessment output 참조 지시) |
| n_detected_signals가 0인 Type 1/2 | monitoring_feasibility=low, FF=E, cadence=quarterly. 마스터에 "아직 weak signal 미식별" 경고 |
| 정량 임계값 설정 불가 (qualitative only) | tripwire_evaluator.py status=N/A 자동 처리 — 주관적 판단 금지 |
| VRMP L4 모든 소스 실패 | vrmp_tier="R-3"; source_trail에 "L4 fetch 전부 실패 — R-3 fallback" 명시 |
| monitoring_output_validator.py FAIL | errors 수정 → 재생성 → 재검증 (PASS 전까지 반환 불가) |
| impact-index FF 누락 (C4 Monitoring-Only) | foresight_factor_impact_index_value="N/A", foresight_factor_match=null |
| RED 상태 trip-wire 발생 | next_skill에 "vision-foresight-wild-cards-options-action" 즉시 포함하여 마스터에 escalation 전달 |
| Type 3 Wild Card 입력됨 | monitoring_feasibility=not_observable_type_3, FF=F, cadence=None, weak_signals=[] — PDF §III.3 "escape from any observation" |
| expert-pool 응답 없음 | L5 fallback: 도메인 전문가 AI 페르소나로 약호 처리, vrmp_tier → R-3 |
| n_signals 7 초과 요청 | PDF §III.3 "3-7" 제한 강제 — signal_id_generator.py 오류 반환, 7로 cap |
