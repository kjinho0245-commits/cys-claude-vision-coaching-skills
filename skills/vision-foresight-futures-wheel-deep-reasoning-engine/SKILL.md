---
name: vision-foresight-futures-wheel-deep-reasoning-engine
description: |
  ## TLDR — Futures Wheel **추론 검증·강화 엔진** sub-skill. `vision-foresight-futures-wheel` 마스터 전용. 박사님 2026-05-11 강화 명령 3 요구사항 통합 구현: ① 6차 이상 깊이 강제 (MDE) ② 차수마다 pre-research gate (PRRG 6 Gates) ③ 출처·근거 명시 강제 (CCP + CoER). *공상* 차단 + *근거 있는 6차 깊이 추론* 보장. 다른 sub-skill의 *각 차수 진입 직전* mandatory blocking gate 역할.

  ## Triggers — INTERNAL ONLY. `vision-foresight-futures-wheel` 마스터 또는 basic-v1·domain-v2·temporal-v3·consequence-linker 등 다른 sub-skill이 차수 산출 직전 *자동* 호출. blocking — 본 gate 통과 못하면 차수 산출 진행 차단. 사용자는 직접 호출하지 않음(disable-model-invocation: true).

  ## Detailed Methodology — 박사님 강화 명령 3종 통합 구현. 핵심 5 protocol: ① **MDE (Minimum Depth Enforcement)** — depth_target ≥6 강제, exception은 "간단히/빠르게" 명시 시만 ② **PRRG (Per-Ring Research Gate) 6 Gates** — Gate_P1_Pre~Gate_P6_Pre, 차수마다 WebSearch ≥3, primary count별 evidence search, historical analog 강제, backlash analog (4차+), paradigm shift analog (5차+), civilizational analog (6차+) ③ **CoER (Chain-of-Evidence Reasoning)** — 각 impact마다 base fact[R-1]→intermediate inference[R-2]→leap to impact[H 명시] 3-step reasoning chain 의무, inline citation 강제 ④ **CCP (Citation Completeness Protocol)** — vague attribution 금지, specific number 무근거 금지, fabricated source pattern 자동 탐지·삭제 ⑤ **SRS (Sewongjima Reversal Score)** — 각 lineage(Center→P→S→T→Q→Qn→Sn)에서 sign reversal ≥2 강제, 4차·5차·6차에서 *각각* 반전 강제, 미달 시 REVISIONS_REQUIRED 반환. 차수 명명 표준: Primary(1)·Secondary(2)·Tertiary(3)·Quaternary(4)·Quinary(5)·Senary(6)·Higher-order(7+). AI Agents: Pre-Research Coordinator · Evidence Hunter · Reasoning Chain Auditor · Hallucination Guard · Reversal Detector · Citation Validator 6인. 본 sub-skill은 다른 sub-skill의 산출을 BLOCK·VALIDATE·ENRICH·RETURN하는 *gate*이며, 통과 못한 차수는 fail 정보와 함께 caller에게 retry 지시.
disable-model-invocation: true
---

# Sub-skill: Deep Reasoning Engine


---

## 0. 결정론 환원 원칙

아래 연산은 **반드시 `reasoning_engine.py`를 호출해 수행**한다. LLM이 재계산하면 할루시네이션 위험이 차단되지 않는다.

| 연산 | 방법 | 명령 |
|---|---|---|
| Gate 요청 검증 (gate_id, prior state) | reasoning_engine.py | `validate_gate` |
| WebSearch 최소 횟수 (PRRG) | reasoning_engine.py | `gate_websearch_needed` |
| 부호 역전 ≥50% 검사 (P4~P6) | reasoning_engine.py | `check_sign_reversal` |
| SRS 4단계 계산 | reasoning_engine.py | `compute_srs` |
| CoER 3-step 구조 검증 | reasoning_engine.py | `check_coer` |
| CCP 유사 귀속·위조 출처 탐지 | reasoning_engine.py | `check_ccp` |
| MDE 깊이 검증·예외 키워드 탐지 | reasoning_engine.py | `check_mde` |
| Ring 품질 (시간 간극 검증) | reasoning_engine.py | `validate_ring_quality` |
| Gate_P3 historical_analog_count ≥1 검증 | reasoning_engine.py | `validate_ring_quality` (ring_num=3) |
| sign_reversal_directive 생성 (Section 4.2) | reasoning_engine.py | `sign_reversal_directive` |
| 과도 역전 경고 (>3.5) | reasoning_engine.py | `check_excessive_reversal` |
| Source Trail 마크다운 생성 | reasoning_engine.py | `generate_source_trail` |
| 과도 역전 경고 (avg>3.5) | reasoning_engine.py | `check_excessive_reversal` |
| 콘텐츠 생성 (analog 서술 등) | LLM | |
| CoER 내용 작성 | LLM | |
| Gate 통과 후 ring 산출 | LLM | |

```bash
echo '<JSON>' | python3 reasoning_engine.py <command>
```

---
> **출처**: 박사님 2026-05-11 강화 명령 — *6차 강제·차수별 검색 강제·출처 명시 강제* 3 요구사항 통합 구현
> **상위 마스터**: `vision-foresight-futures-wheel`
> **호출 권한**: 마스터 + 다른 sub-skill의 *blocking gate* 역할 (disable-model-invocation: true)
> **역할 분류**: validator/enricher (산출자가 아닌 *검증·강화* sub-skill)

---

## 1. 본 sub-skill의 존재 이유

박사님 인용:
> *"퓨처스 휠의 세옹지마 효과를 얻으려면 최소한 4차 이상에서부터다. 6차 이상의 단계를 가는 동안 의미있는 예측을 추출하려면, 강력한 추론 기능이 필요하다. 하지만 추론 기능이 '공상'이 되어서는 안된다. 추론 기능이 근거있는 정보와 지식을 근거로 해야 한다. 그래서 검색과 선행학습을 반드시 추론의 단계마다 '강제'해야 한다. 추론의 출처와 근거를 명시하는 것도 필수다."*

본 sub-skill은 이 3 요구사항을 *기술적으로 강제*하는 게이트다. 다른 sub-skill이 차수를 산출하기 직전, 본 sub-skill이 호출되어 **research-gate를 통과해야만 차수 산출이 진행**된다. 통과 못하면 BLOCK + REVISIONS_REQUIRED 반환.

---

## 2. 5대 Protocol 정식 정의

### 2.1 MDE (Minimum Depth Enforcement)

```yaml
MDE_Protocol:
  default_depth_target: 6   # Primary~Senary
  
  exception_conditions:
    user_says:
      - "간단히"
      - "빠르게"
      - "대충"
      - "Quick wheel"
      - "summary only"
    user_specifies: "N차까지" (N≥3 허용, N<3 거부)
  
  enforcement:
    - "마스터가 cycle 분류 후, depth_target<6이면 알림: '박사님 강화 protocol에 따라 6차 default. 명시적으로 줄이시려면 알려주세요.'"
    - "Quality-Control Gate 9가 최종 depth 점검 — 6차 미달 시 REVISIONS_REQUIRED"
  
  per_ring_quality_gate:
    each_ring_must_pass:
      - "이전 차수와 *시간* 5년 이상 간극"
      - "이전 차수와 *도메인* 또는 *대상 집단* 명확 구별"
      - "이전 차수와 *질적* 메커니즘 변화 (강도 증가 아닌 새 현상)"
    fail_action: "이 차수 reject + 재발굴 요청"
```

### 2.2 PRRG (Per-Ring Research Gate) — 6 Gates 정식 정의

```yaml
Gate_P1_Pre (Primary, T+1~5y):
  invocation: basic-v1·domain-v2가 Phase 2 (Primary Ring) 진입 직전
  
  mandatory_web_searches: ≥3
  search_targets:
    - "{중앙 이슈} 2026 current state"
    - "{중앙 이슈} expert assessment 2026"
    - "{중앙 이슈} statistics latest"
  
  evidence_required:
    - "각 primary impact에 inline citation"
    - "specific number는 R-1 source 의무"
  
  fail_conditions:
    - web_searches_executed < 3
    - 모든 search result 2025 이전 (stale)
    - primary impact 중 citation 없는 항목 존재
  
  on_pass: "Primary Ring 산출 허가"
  on_fail: "BLOCK + return retry instructions"


Gate_P2_Pre (Secondary, T+5~10y):
  invocation: basic-v1·consequence-linker가 Secondary Ring 진입 직전
  
  mandatory_web_searches: ≥N (N = primary count, 최소 5)
  search_targets:
    - 각 primary impact별 evidence search
    - 각 primary → secondary 인과 chain 근거
  
  evidence_required:
    - "각 P→S 인과에 reasoning chain 3 step"
    - "각 step에 R-tag 부착 (R-1·R-2·H)"
  
  fail_conditions:
    - searches < N
    - primary→secondary 추론 chain 없이 곧바로 결과만 적힌 항목 존재


Gate_P3_Pre (Tertiary, T+10~20y):
  invocation: Tertiary Ring 진입 직전
  
  mandatory_web_searches: ≥M (M = secondary count, 최소 5)
  search_targets:
    - 각 secondary → tertiary emergent 사례
    - **historical analog 최소 1건** (역사적 유사 emergent)
  
  examples_of_historical_analog:
    - "산업혁명 → 도시화 → 노동운동 (3차 emergent 예시)"
    - "인터넷 → 전자상거래 → 오프라인 소매 붕괴"
  
  evidence_required:
    - "각 tertiary에 *어떤 historical analog가 유사한 emergent를 보였는지* 명시"
  
  fail_conditions:
    - historical_analog_count < 1
    - tertiary가 단순 secondary 강도 증가 (질적 변화 없음)


Gate_P4_Pre (Quaternary, T+15~25y) ⭐ 세옹지마 1차 반전 임계점:
  invocation: Quaternary Ring 진입 직전
  
  mandatory_web_searches: ≥3
  search_targets:
    - "{topic} backlash historical case"
    - "{topic} unintended consequences reversal"
    - "역사적 backlash·counter-movement"
  
  examples_of_backlash_analog:
    - "산업혁명 → 러다이트 운동 (기계파괴)"
    - "디지털화 → 디지털 디톡스 운동"
    - "글로벌화 → 반세계화·보호무역"
    - "도시화 → 귀농·로컬푸드"
    - "TV → 라디오 부활 (팟캐스트)"
    - "패스트패션 → 슬로우패션"
  
  ⭐ SIGN REVERSAL 강제 ⭐:
    - "Quaternary의 50% 이상이 직전 Tertiary와 *반대 부호*여야 함"
    - "예: T1·T2·T3가 🔴이면 Q1·Q2 중 ≥1는 🟢, 또는 그 반대"
    - "모두 같은 방향이면 REJECT — '직선적 단정 회피' 원칙 위배"
  
  evidence_required:
    - "각 quaternary에 backlash mechanism 명시"
    - "관련 historical analog citation"
  
  fail_conditions:
    - sign_reversal_fraction < 0.5  # CORRECT: ≥50% check (NOT count==0). Use reasoning_engine.py check_sign_reversal
    - backlash_analog_count < 1


Gate_P5_Pre (Quinary, T+20~30y) ⭐ 세옹지마 2차 반전 + 패러다임 전환:
  invocation: Quinary Ring 진입 직전
  
  mandatory_web_searches: ≥3
  search_targets:
    - "{topic} paradigm shift historical"
    - "worldview transformation case"
    - "institutional reconfiguration"
  
  examples_of_paradigm_shift_analog:
    - "코페르니쿠스 → 지구중심 세계관 붕괴"
    - "다윈 → 인간=특별창조 신화 해체"
    - "프로이트 → 합리적 자아 신화 해체"
    - "양자역학 → 결정론 세계관 균열"
    - "AGI → 인지우월성 신화 붕괴 ← 본 wheel 핵심"
  
  ⭐ SIGN REVERSAL 강제 ⭐:
    - "Quinary의 50% 이상이 직전 Quaternary와 *반대 부호*"
    - "세옹지마 2차 반전 (반전의 반전) 패턴 명시"
  
  evidence_required:
    - "각 quinary가 어떤 *세계관·언어·제도*를 재구성하는지"
    - "관련 paradigm shift analog citation"


Gate_P6_Pre (Senary, T+25~50y) ⭐ 세옹지마 3차 반전 + 문명 단위:
  invocation: Senary Ring 진입 직전
  
  mandatory_web_searches: ≥2
  search_targets:
    - "{topic} civilizational transformation"
    - "species-level change case"
    - "long-arc historical analog"
  
  examples_of_civilizational_analog:
    - "농업혁명 (12,000년 전) → 정착·문명·국가 출현"
    - "문자혁명 (5,000년 전) → 기록·법·도시"
    - "산업혁명 (250년 전) → 근대 자본주의·민족국가"
    - "정보혁명 (50년 전) → 글로벌 네트워크·개인"
    - "AGI 혁명 (현재~) → ?"
  
  ⭐ SIGN REVERSAL 강제 ⭐:
    - "Senary의 50% 이상이 직전 Quinary와 *반대 부호*"
    - "세옹지마 3차 반전 — *문명 단위 재정의*에서 의미 회복 또는 상실 결정"
  
  ⭐ CHAOS ATTRACTOR 강제 표시 ⭐:
    - "Senary에 attractor·butterfly effect 후보 ≥1 명시"
    - "PDF Glenn 인용 적용"
  
  evidence_required:
    - "각 senary에 civilizational analog citation"
    - "attractor 후보의 amplification 메커니즘"
```

### 2.3 CoER (Chain-of-Evidence Reasoning)

```yaml
CoER_Protocol:
  applied_to: "각 impact 항목 (모든 차수)"
  
  required_structure:
    impact_id: "P1, S1a, T1, Q1, Qn1, Sn1, ..."
    claim: "{impact 한 문장}"
    reasoning_chain:
      step_1_base_fact:
        content: "{현재 검증 가능한 사실}"
        tier: R-1
        citation: "[저자/기관, 연도, URL]"
      step_2_intermediate_inference:
        content: "{base fact으로부터 도출되는 중간 추론}"
        tier: R-2
        citation: "[저자/기관, 연도, URL or analog]"
      step_3_leap_to_impact:
        content: "{최종 impact 도출}"
        tier: R-3 or H
        disclosure: "본 step은 {가정명}을 전제로 함"
    sign: 🟢 / 🔴 / 🟡
    time_range: "T+Ny ~ T+My"
    domain: "Glenn V2 sector 중 하나"
  
  rejection_criteria:
    - "reasoning_chain 없이 곧바로 impact만 적힌 항목 → REJECT"
    - "모든 step이 H tag (가정만) → REJECT (근거 부족)"
    - "step_3에 가정 disclosure 누락 → REJECT"
```

**Example — AGI wheel P1 (인지우월성 신화 붕괴)**:

```yaml
impact_id: P1
claim: "인간 인지 우월성 신화 붕괴 — '내가 가장 똑똑한 동물' 종 정체성 균열"

reasoning_chain:
  step_1_base_fact:
    content: "2026.2 Claude Opus 4.6·GPT-5.3 출시 — 전문 직무 12~18개월 내 human-level"
    tier: R-1
    citation: "Suleyman M, Microsoft AI, 2026, https://..."
  
  step_2_intermediate_inference:
    content: "인지 도구가 일반 노동·창작·판단을 초과하면 인간 self-concept의 '인지 우월성' 핵심 기둥이 흔들림. 역사적 analog: 산업혁명에서 '근력 우월성' 신화 붕괴."
    tier: R-2
    citation: "Psychology Today 2026.12, 'AI as 4th injury to identity', https://..."
  
  step_3_leap_to_impact:
    content: "AGI 시대 3~5년 내 인간 종 정체성 위기 본격화"
    tier: H
    disclosure: "본 step은 AGI 2026~2030 출현 가정 + 인지 우월성이 인간 self-concept 핵심이라는 인류학 가정을 전제로 함"

sign: 🔴
time_range: T+1~5y
domain: Cultural + Psychological + Spirituality
```

### 2.4 CCP (Citation Completeness Protocol)

```yaml
CCP_Rules:
  mandatory_inline_citation:
    every_impact: "≥1 citation"
    every_reasoning_step: "step별 citation"
    every_quantitative_claim: "R-1 출처 필수"
  
  acceptable_citation_formats:
    minimum: "[저자/기관, 연도]"
    preferred: "[저자/기관, 연도, URL]"
    optimal: "[저자/기관, 연도, *작품/논문 제목*, URL, page/section]"
  
  REJECT_PATTERNS:
    - vague_attribution:
        examples:
          - "(전문가 의견)"
          - "(많은 연구에 따르면)"
          - "(보고서에 의하면)"
          - "(여러 미래학자들이 지적)"
          - "(통념상)"
        action: 자동 삭제 + 구체 citation 재요청
    
    - fabricated_source_pattern:
        regex:
          - "study by .* University" (검증 없으면)
          - "research from .* Institute" (검증 없으면)
          - "report from .* (Foundation|Center)" (검증 없으면)
          - "according to .* (paper|article)" (URL 없으면)
        action: hallucination guard 발동, 자동 삭제
    
    - unsourced_specific_numbers:
        examples:
          - "50% increase" (출처 없으면)
          - "약 N개의 X" (출처 없으면)
          - "T+Ny에 도달" (출처 없으면 H tag 강제)
        action: R-1 출처 보강 또는 "추정" tag 강제
```

### 2.5 SRS (Sewongjima Reversal Score)

```yaml
SRS_Calculation:
  for_each_lineage:
    lineage_definition: "Center → P{n} → S{n}a → T{n}a1 → Q{n}a1a → Qn{n}a1a1 → Sn{n}a1a1α"
    sign_sequence: 
      example: [P:🟢, S:🔴, T:🔴, Q:🟢, Qn:🟢, Sn:🟡]
    
    reversal_count:
      definition: "연속된 두 차수의 부호가 다른 횟수 (🟡는 reversal 아님)"
      example_calculation: "🟢→🔴(1), 🔴→🔴(0), 🔴→🟢(1), 🟢→🟢(0) = 2 reversals"
  
  Quality_Thresholds:
    excellent: avg ≥2.0 reversals per lineage      # reasoning_engine.py status='EXCELLENT'
    good: avg 1.5~2.0                              # reasoning_engine.py status='GOOD'
    acceptable: avg 1.0~1.5                        # reasoning_engine.py status='ACCEPTABLE'
    insufficient: avg <1.0 → 직선적 단정 → REVISIONS_REQUIRED  # reasoning_engine.py status='REVISIONS_REQUIRED'
    excessive_guard: avg >3.5 → wishful thinking 경고 (reasoning_engine.py check_excessive_reversal)
  
  Forced_Reversal_Points:
    - "P→Q (Primary → Quaternary): 4차에서 *반드시* 1차 반전"
    - "Q→Qn (Quaternary → Quinary): 5차에서 *반드시* 2차 반전"
    - "Qn→Sn (Quinary → Senary): 6차에서 *반드시* 3차 반전"
  
  Excessive_Reversal_Guard:
    threshold: avg >3.5 reversals
    action: "wishful thinking·dramatic narrative 의심, plausibility 재검증"
```

---

## 3. AI Agent 6인 구성

| Agent | 역할 |
|-------|------|
| **Pre-Research Coordinator** | 차수 진입 직전 PRRG Gate 선정·web search 호출 orchestration |
| **Evidence Hunter** | WebSearch·WebFetch 실행, R-1·R-2·R-3 tier 분류 |
| **Reasoning Chain Auditor** | 각 impact의 CoER 3-step chain 검증 |
| **Hallucination Guard** | fabricated source pattern 탐지·삭제, vague attribution reject |
| **Reversal Detector** | SRS 계산, sign reversal 강제 점검 |
| **Citation Validator** | CCP 형식 점검, URL 검증 가능성 확인 |

---

## 4. 호출 인터페이스 (caller — basic-v1, domain-v2, temporal-v3, consequence-linker)

### 4.1 caller가 본 sub-skill 호출 시 payload

```yaml
caller_request:
  caller_skill: "vision-foresight-futures-wheel-basic-v1"
  gate_requested: "Gate_P4_Pre"   # P1~P6
  
  prior_state:
    center_issue: { ... }
    ring_already_completed: { Primary, Secondary, Tertiary }
    upcoming_ring: "Quaternary"
    sign_distribution_so_far: 
      primary: [🟢, 🔴, 🔴, 🟡, ...]
      secondary: [🔴, 🔴, 🟡, 🟢, ...]
      tertiary: [🔴, 🔴, 🟢, ...]
  
  user_context:
    domains_frame: "Glenn V2 8 sector"
    user_id_signals: { ysfuture, 박사님 layer 활성 }
  
  blocking: true
```

### 4.2 본 sub-skill의 response

```yaml
response:
  gate: "Gate_P4_Pre"
  status: "PASSED" | "BLOCKED"
  
  web_searches_executed:
    count: 4
    queries: [...]
    results_summary: [...]
  
  enrichment:
    backlash_analogs_found:
      - { event: "산업혁명→러다이트", year: 1811, source: "..." }
      - { event: "디지털화→디지털디톡스", year: 2015, source: "..." }
      - { event: "TV→팟캐스트", year: 2010, source: "..." }
    citations_collected: [...]
  
  sign_reversal_directive:
    primary_dominant_sign: 🔴
    secondary_dominant_sign: 🔴
    tertiary_dominant_sign: 🔴
    QUATERNARY_REQUIRED: "≥50% must be 🟢 (세옹지마 1차 반전 강제)"
  
  on_pass: "caller may proceed with Quaternary Ring 산출"
  on_fail: 
    reasons: [...]
    retry_instructions: [...]
```

---

## 4.3 ⭐ SCBE 모드 호환 (박사님 2026-05-11 2차 강화)

Cycle 9 SCBE 모드에서 caller가 `categorical-binary-expansion`일 때, 본 sub-skill은 다음 batching 최적화 적용:

```yaml
SCBE_mode_evidence_batching:
  activation_condition: caller == 'categorical-binary-expansion'
  
  batching_strategy:
    rule: "같은 STEEPS 카테고리 + 같은 차수 노드들은 *공통 historical analog 1건*을 evidence로 공유"
    benefit: "web search 효율 — 카테고리당 1 query × 6 categories = 6 query per ring (현 30+ 대신)"
    
  per_ring_search_pattern:
    Gate_P1_Pre: "6 queries (카테고리당 1, 각 카테고리 fact)"
    Gate_P2_Pre: "6 queries (카테고리당 1, evidence chain)"
    Gate_P3_Pre: "6 queries (카테고리당 1, emergent analog)"
    Gate_P4_Pre: "6 queries (카테고리당 1, backlash analog) ★ analog batching 핵심"
    Gate_P5_Pre: "6 queries (카테고리당 1, paradigm shift)"
    Gate_P6_Pre: "6 queries (카테고리당 1, civilizational)"
    TOTAL: 36 searches (균형 ✓ + 효율 ✓)
  
  analog_propagation:
    rule: "1 analog ← 같은 카테고리 8 quaternary 노드 공통 evidence"
    example:
      analog: "산업혁명 → 러다이트 운동 (1811)"
      applies_to:
        - Society 카테고리 8 quaternary 노드 모두
      reasoning: "Society 카테고리 내 자동화 backlash 패턴 공통 근거"

→ 결과: SCBE 모드에서 30+ search 유지하면서 192~256 senary 노드 모두 evidence-grounded
```

---

## 5. 6 Gate 실행 흐름 (전체 architecture)

```
┌─────────────────────────────────────────────────────────────┐
│ 사용자 명령 → 마스터 (cycle 분류) → VRMP L1·L2 initial cascade │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌──────────────────────────────────────────┐
│ basic-v1.Phase_2 (Primary Ring) 시작     │
└────────────────┬─────────────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P1_Pre (NEW)            │
   │ Pre-Research Coordinator 호출    │
   │ - WebSearch ≥3                  │
   │ - 각 primary 후보에 evidence    │
   │ - hallucination guard           │
   └─────────────┬───────────────────┘
                 │ PASSED → 진행
                 ↓
   ┌─────────────────────────────────┐
   │ Primary Ring 산출 (with CoER)   │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P2_Pre                  │
   │ - WebSearch ≥N (primary count)  │
   │ - 각 P→S 인과 chain 근거        │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ Secondary Ring 산출             │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P3_Pre                  │
   │ - historical analog ≥1          │
   │ - emergent pattern search       │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ Tertiary Ring 산출              │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P4_Pre ⭐                │
   │ - backlash analog ≥1            │
   │ - 🔄 SIGN REVERSAL 강제 (1차)    │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ Quaternary Ring 산출            │
   │   ← 세옹지마 1차 반전 시작       │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P5_Pre ⭐                │
   │ - paradigm shift analog ≥1      │
   │ - 🔄🔄 SIGN REVERSAL 강제 (2차)   │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ Quinary Ring 산출               │
   │   ← 세옹지마 2차 반전 (반전의 반전) │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ ⛩️ Gate_P6_Pre ⭐                │
   │ - civilizational analog ≥1      │
   │ - 🔄🔄🔄 SIGN REVERSAL 강제 (3차)  │
   │ - chaos attractor 표시          │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ Senary Ring 산출                │
   │   ← 세옹지마 3차 반전 (문명 단위) │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ quality-control (10 Gates)      │
   │ - 기존 8 Gate                   │
   │ - Gate 9 Citation Completeness  │
   │ - Gate 10 Reasoning Chain·SRS   │
   └─────────────┬───────────────────┘
                 ↓
   ┌─────────────────────────────────┐
   │ 마스터 통합 Synthesis           │
   │ + Source Trail 섹션 (NEW)       │
   │ + per-ring search log           │
   └─────────────────────────────────┘
```

---

## 6. Source Trail 출력 형식

마스터 출력에 본 sub-skill이 누적한 search log를 다음 형식으로 export:

```markdown
## 📚 Source Trail (deep-reasoning-engine 누적)

### Per-Ring Pre-Research Log
| Ring | Gate | Searches | Citations | Analog | Tier |
|------|------|----------|-----------|--------|------|
| Primary | P1_Pre | 4 | 12 | n/a | R-1 dominant |
| Secondary | P2_Pre | 12 | 22 | n/a | R-1·R-2 mix |
| Tertiary | P3_Pre | 8 | 15 | 3 historical | R-2 dominant |
| Quaternary | P4_Pre | 5 | 10 | 3 backlash | R-2·R-3 |
| Quinary | P5_Pre | 4 | 8 | 2 paradigm | R-3·H |
| Senary | P6_Pre | 3 | 6 | 2 civilizational | R-3·H |
| **TOTAL** | | **36** | **73** | **10** | |

### SRS (Sewongjima Reversal Score)
- Total lineages tracked: 12
- Per-lineage reversal count: [2, 3, 2, 3, 2, 1, 2, 3, 2, 2, 3, 2]
- Avg reversal: **2.25** ★ EXCELLENT
- Forced reversal compliance:
  - P→Q: 67% reversed (target ≥50%) ✓
  - Q→Qn: 58% reversed ✓
  - Qn→Sn: 75% reversed ✓

### Citations (R-tier 분포)
- R-1 (실증 fact): 28
- R-2 (전문가·이론): 31
- R-3 (역사적 analog): 10
- H (가정·추정, disclosed): 4
- TOTAL: 73

### Hallucination Guard Activity
- Vague attribution rejected: 3 ("(전문가 의견)" 패턴)
- Fabricated source detected: 0
- Unsourced specific numbers flagged: 2 → R-1 보강 완료

### CCP Compliance
- 모든 impact에 inline citation: ✓ 100%
- 모든 quantitative claim에 R-1 source: ✓ 100%
- Reasoning chain ≥3 step: ✓ 96% (4 impacts revisited)
```

---

## 7. PDF 원전 호환

본 sub-skill은 Glenn (2009)에 *없는* 강화 layer이지만, Glenn 본인의 다음 명시와 부합:

> *"The output of a Futures Wheel should be used as a basis for further thinking, for more systematic exploration, and for the application of other techniques for probing the future. Put simply, the Futures Wheel is a creative tool that generates input to futures thinking."* (§IV)

본 sub-skill은 *"more systematic exploration"*의 시스템화 — Glenn의 의도를 *기술적으로 강제* 형태로 구현.

또한 Glenn endnote 4 (Hume·de Jouvenel 인과 vs 상관 철학)과 정확히 정렬: 각 reasoning step의 tier가 *causation 주장 강도*를 명시.

---

## 8. references/

| 파일 | 용도 |
|------|------|
| `references/mde_protocol.md` | Minimum Depth Enforcement 상세·예외 케이스·차수 명명 |
| `references/prrg_6_gates.md` | 6 Gate 상세 protocol·검색 query 템플릿 |
| `references/coer_protocol.md` | Chain-of-Evidence Reasoning 양식·예시 |
| `references/ccp_rules.md` | Citation Completeness Protocol·reject pattern catalog |
| `references/srs_calculation.md` | Sewongjima Reversal Score 계산·예시 |
| `references/historical_analog_catalog.md` | backlash·paradigm·civilizational analog 카탈로그 (50+ 사례) |
| `references/hallucination_patterns.md` | fabricated source 탐지 regex·검증 알고리즘 |

---

## 9. Success Metrics

본 sub-skill이 properly 작동하면 wheel 산출이 다음 지표를 충족:

| Metric | Target |
|--------|--------|
| 평균 차수 깊이 | ≥6.0 |
| 평균 web search per wheel | ≥30 |
| inline citation 비율 | ≥95% |
| 세옹지마 SRS | ≥1.5 avg reversal |
| fabricated source | 0% |
| Quality Score | ≥0.95 |

---

## 10. 마스터로의 반환

본 sub-skill은 *각 Gate별로* 마스터·caller에게 다음 반환:

```yaml
response_to_caller:
  gate_id: P{N}_Pre
  status: PASSED | BLOCKED
  searches_executed: count + queries + summaries
  citations_collected: [...]
  enrichment_data:
    analogs_found: [...]
    sign_reversal_directive: { dominant_signs, required_reversal_for_next_ring }
  retry_instructions (if BLOCKED): [...]
  
  cumulative_log_to_master: 
    (for final Source Trail export)
```

caller는 PASSED 받으면 진행, BLOCKED 받으면 retry_instructions 따라 재시도.

마스터는 분석 끝에 본 sub-skill의 누적 log를 Source Trail 섹션으로 출력.

---

본 sub-skill의 존재 자체가 박사님 *"공상이 되어서는 안 된다"* 명령의 기술적 구현. 다른 sub-skill의 산출을 *gate*하여 wheel 전체 품질을 보장한다.
