---
name: vision-foresight-futures-wheel-scenario-forecast
description: |
  ## TLDR — Jerome C. Glenn (2009) Futures Wheel, Chapter 6 §III.C "Creating Forecasts within Alternative Scenarios". **vision-foresight-futures-wheel** 마스터 전용. Glenn 직접 인용: *"The Futures Wheel can also be used as a method to create forecasts within alternative scenarios. In this application, one selects a scenario and an item in that scenario to explore."* Figure 5의 VCR-in-conscious-technology 사례 — 시나리오 컨텍스트 안에서 특정 item(제품·기술·정책·조직)의 미래 features·design·response 예측. Decision Tree·Morphological Analysis 보조.

  ## Triggers — INTERNAL ONLY. 마스터 Cycle 5(Scenario Forecast)에서 자동 호출. 사용자가 'scenario 안에서 item 예측', 'alternative scenarios', 'VCR-in-conscious-technology 식', '제품 미래 features', 'decision tree 보조', 'morphological analysis 보조', '시나리오 컨텍스트 forecast', '낙관/비관/중립 각 시나리오 별 wheel', 'driving force별 wheel' 명시 시 마스터가 본 sub-skill 발동. consequence-linker가 contradiction을 critical_issue로 promote했을 때도 자동 발동.

  ## Detailed Methodology — Glenn (2009) §III.C + Figure 5 (VCR in Post-Information Age "conscious technology" scenario) 풀 구현. 7 Phase: ① **Phase 1 Scenario Selection** — 사용자 입력 또는 마스터 전달 시나리오 (낙관·비관·중립, 또는 driving force별 시나리오, 또는 사용자 custom scenario). ② **Phase 2 Item Selection** — 시나리오 안에서 forecast할 item 선택(제품·기술·정책·조직·서비스). PDF 예: VCR. ③ **Phase 3 Scenario Frame Lock-in** — 시나리오의 핵심 전제·driving force·world state 명시. PDF 예: *"conscious technology" (Post-Information Age in which distinctions between technology and consciousness blur)*. ④ **Phase 4 Item Re-imagination in Scenario** — 시나리오 전제 하에서 item이 어떻게 *변형*되어야 하는지 발굴. 각 feature는 반드시 특정 scenario assumption에 1:1 연결(grounding 필수). PDF 예: *"One could imagine that the VCR is a conscious entity capable of communicating; then identify what features would be required to make this 'real.'"* ⑤ **Phase 5 Feature·Design·Response Wheel** — 각 새 feature·design·response를 wheel의 spoke로 발굴. PDF 예(Figure 5): voice activation·microphone·voice reproduction program·built-in modem·search TV schedules·remote visual data banks·electronic funds transfer·viewing pattern analysis·feedback on previous patterns·computer memory of interests·on-line access·analysis computer program·telelink to visuals·automatically displayed. ⑥ **Phase 6 Decision Tree·Morphological Analysis 연동** — PDF 인용: *"This variation is similar in function to decision trees and morphological analysis."* 발굴한 features를 decision tree 분기 또는 morphological matrix로 export. 할루시네이션 차단: 모든 옵션은 Phase 5 wheel에서 도출된 features 또는 시나리오 전제에서 직접 파생해야 하며 출처 없는 추가는 금지. ⑦ **Phase 7 Cross-scenario Comparison** — 다중 시나리오 forecast 시 시나리오 별 wheel을 나란히 비교. divergence_score는 Jaccard 비유사도 공식으로 결정론적 계산: score = 1 − |A∩B| / |A∪B| (0=동일, 1=완전 상이). 연도 예측값은 반드시 ILLUSTRATIVE 표기 필수, 확정 수치로 제시 금지. AI Agents: Leader · Scenario Designer · Item Re-imaginer · Brainstorm Panel · Synthesizer · Visualizer 6인.
disable-model-invocation: true
---

# Sub-skill: Scenario Forecast (Alternative Scenarios)

> **출처**: Glenn, J. C. (2009). Futures Wheel. In J. C. Glenn & T. J. Gordon (Eds.), *Futures Research Methodology — Version 3.0* (Chapter 6, §III.C, Figure 5). Washington, DC: The Millennium Project.
> **상위 마스터**: `vision-foresight-futures-wheel`
> **호출 권한**: 마스터 orchestration 전용 (disable-model-invocation: true)

## 1. PDF 원전 정의

Glenn (2009) 직접 인용:

> *"The Futures Wheel can also be used as a method to create forecasts within alternative scenarios. In this application, one selects a scenario and an item in that scenario to explore. For example, one could forecast the future of the videocassette recorder (VCR) within the post-information age scenario of 'conscious technology,' (i.e., the Post-Information Age in which distinctions between technology and consciousness blur)."*
> — Glenn (2009) Ch. 6, §III.C

> *"One could imagine that the VCR is a conscious entity capable of communicating; then identify what features would be required to make this 'real.' The Futures Wheel could show a different variation of how to design the product as more 'conscious' or more immediately responsive to the user. Each new product feature could have spokes that identify what new elements need to be incorporated in the new design."*
> — Glenn (2009) Ch. 6, §III.C

> *"In the Futures Wheel below (Fig. 5), the new designs for the VCR would include voice activation so that you could tell it what to do. This implies that a microphone and voice recognition program would be added to future VCRs. The future VCR might also search TV programs or remote visual data banks by computer communications and match your previously computer-stored preferences..."*
> — Glenn (2009) Ch. 6, §III.C

> *"This Futures Wheel shows the more 'conscious' VCR of the future and what new product features are likely to bring it to market. This variation is similar in function to decision trees and morphological analysis (see paper by that title in this series)."*
> — Glenn (2009) Ch. 6, §III.C

> *"During a scenario construction exercise that has identified driving forces, Futures Wheels could be used on each driving force to explore the pattern of consequences for each. This could provide richer input for the content of the scenarios."*
> — Glenn (2009) Ch. 6, §V "Use in Combination"

## 2. 본 sub-skill의 4가지 사용 패턴

PDF 명시 1가지 + Glenn §V "Use in Combination" 명시 3가지:

| Pattern | 설명 | 출처 |
|---------|------|------|
| **P1: Item-in-Scenario** | 특정 시나리오 컨텍스트 안에서 특정 item의 features·design 예측 | PDF §III.C VCR 사례 |
| **P2: Driving Force별 Wheel** | 시나리오의 각 driving force마다 별도 wheel 작성, 시나리오 콘텐츠 강화 | PDF §V "During a scenario construction exercise..." |
| **P3: 낙관/비관/중립 분기** | 같은 중앙 이슈를 3 시나리오 frame으로 각각 wheel 그려서 비교 | P1을 3회 반복 적용 |
| **P4: Contradiction → Scenario Branch** | consequence-linker가 발견한 contradiction을 시나리오 분기점으로 전환 | 마스터 layer 연동 |

### P2 패턴 구체 흐름 (Driving Force별 Wheel)

PDF §V 명시: "Futures Wheels could be used on *each driving force* to explore the pattern of consequences for each."

```
[입력] scenarios[0].driving_forces = [DF1, DF2, ..., DFn]
[처리] for each DFi:
    1. DFi를 중앙 issue로 고정
    2. Phase 3 ~ Phase 5 실행 (해당 DF에 한정)
    3. 별도 wheel 산출
[출력] n개의 wheel → Phase 7 Cross-scenario Comparison에 통합
```

### P4 패턴 구체 흐름 (Contradiction → Scenario Branch)

```yaml
# P4 입력 (consequence-linker에서 전달)
contradiction_promoted:
  issue: "{중앙 이슈}"
  node_a: "{contradiction 발생 노드 A}"
  node_b: "{contradiction 발생 노드 B}"
  contradiction_type: "logical" | "empirical" | "value"
  description: "{모순 설명}"

# P4 처리 흐름
1. node_a가 참인 시나리오(Scenario-A) 구성 → Phase 1~7 실행
2. node_b가 참인 시나리오(Scenario-B) 구성 → Phase 1~7 실행
3. Phase 7 Cross-scenario Comparison으로 두 시나리오 wheel 비교
4. divergence_score 계산 (§7 알고리즘 적용)
5. 높은 divergence(≥ 0.6)는 critical branch로 마스터에 보고
```

## 3. AI Agent 6인 구성

| Agent | 역할 | 운영 원칙 |
|-------|------|-----------|
| **Leader Agent** | 시나리오·item 선택 진행, 변형 phase 진행 | Phase 순서 엄수, 건너뜀 금지 |
| **Scenario Designer** | 시나리오 frame lock-in, driving force 명시 | 가정은 최소 3개, 최대 7개 |
| **Item Re-imaginer** | item을 시나리오 전제 하 *변형* 상상 | 각 변형은 반드시 scenario assumption에 연결 |
| **Brainstorm Panel** | 각 새 feature·design 발굴 | PDF 원전 features 우선, 시나리오 파생 features 2순위, 출처 없는 추가 금지 |
| **Synthesizer** | 시나리오 간 비교, decision tree·morphological export | wheel features에서만 옵션 추출, 임의 추가 금지 |
| **Visualizer** | Figure 5 스타일 wheel + decision tree + morphological matrix | PDF 원전과 1:1 대조 필수 |

## 4. 7 Phase 처리 흐름

### Phase 1 — Scenario Selection

사용자/마스터에서 전달받은 시나리오 정보. **Python 스크립트로 전체 입력 검증**: `python3 validate_inputs.py --input <input_json_path>` (Phase 1 진입 전 1회 실행):

```yaml
scenario_input:
  type: "optimistic" | "pessimistic" | "neutral" | "driving_force" | "custom"  # 필수, enum 검증
  name: "{시나리오 이름}"            # 필수, 1~100자
  description: "{한 문단 시나리오 묘사}"  # 필수, 최소 20자
  driving_forces: [...]             # 필수, 최소 2개, 최대 7개
  world_state_assumptions: [...]    # 필수, 최소 2개
```

PDF Example:
```yaml
scenario_input:
  type: "custom"
  name: "Conscious Technology (Post-Information Age)"
  description: "Distinctions between technology and consciousness blur. Devices become responsive entities capable of communicating with users."
  driving_forces:
    - AI capability advance
    - Human-machine interface evolution
    - User intolerance for friction
  world_state_assumptions:
    - "Computing power approaches biological brain scale"
    - "Voice/gesture/thought interface mainstream"
```

### Phase 2 — Item Selection

시나리오 안에서 forecast할 item 선택. (스키마 검증은 Phase 1 이전 `validate_inputs.py` 1회 실행으로 완료):

```yaml
item:
  name: "{item 이름}"         # 필수
  type: "product" | "technology" | "policy" | "organization" | "service" | "concept"  # 필수, enum 검증
  current_state: "{T+0 시점 현재 형태}"  # 필수
  baseline_features: [...]    # 필수, 최소 2개. Phase 4에서 '변형 전 기준'으로 사용
```

PDF Example:
```yaml
item:
  name: "VCR (Videocassette Recorder)"
  type: "product"
  current_state: "Tape-based recording/playback device"
  baseline_features: ["record", "play", "pause", "rewind", "fast-forward"]
```

### Phase 3 — Scenario Frame Lock-in

Scenario Designer Agent가 시나리오 핵심 전제 명시. `references/scenario_frame_lock_template.md` 참조:

```markdown
## Scenario Frame: "{이름}"

### 핵심 가정 (최소 3개, 최대 7개)
1. {가정 1}
2. {가정 2}
...

### Driving Forces (2~7개)
- DF1: {force} (strength: high/medium/low)
- DF2: ...

### World State (T+의 세계)
- {state 1}
- {state 2}
...

### Item이 적응해야 할 압력 (각 pressure는 위 핵심 가정 중 하나에 연결)
- {pressure 1} → [가정 N 연결]
- {pressure 2} → [가정 M 연결]
```

### Phase 4 — Item Re-imagination in Scenario

**할루시네이션 차단 원칙**: Item Re-imaginer Agent가 생성하는 모든 변형(feature)은 Phase 3에서 명시한 핵심 가정 목록 중 하나의 번호를 `[가정 N]` 형식으로 반드시 인용해야 한다. 인용 없는 feature는 Synthesizer Agent가 자동 기각한다.

PDF 핵심 아이디어: *"One could imagine that the VCR is a conscious entity..."* — Item Re-imaginer Agent가 시나리오 전제 하에서 item을 *근본적으로 재상상*.

질문 시퀀스:
1. "이 시나리오에서 item이 살아남으려면 어떤 모습으로 변해야 하는가?" → 각 답에 `[가정 N]` 명시
2. "사용자가 이 시나리오에서 item에게 기대하는 가장 큰 가치는 무엇인가?" → 각 답에 `[가정 N]` 명시
3. "현재 form이 시나리오 전제에 부합하지 않는 부분은 어디인가?" → 각 답에 `[가정 N]` 명시
4. "기존 boundary를 넘는 변형(merge·split·invert·dematerialize)은 가능한가?" → 각 답에 `[가정 N]` 명시

PDF VCR Example (conscious-technology 시나리오 하):
> *"VCR is a conscious entity capable of communicating"*
- 변형 1: voice activation [가정: "Voice/gesture/thought interface mainstream"]
- 변형 2: search TV programs/remote visual data banks [가정: "Computing power approaches biological brain scale"]
- 변형 3: match user preferences — computer memory of interests [가정: "Computing power approaches biological brain scale"]
- 변형 4: feedback on previous patterns [가정: "Computing power approaches biological brain scale"]
- 변형 5: on-line access / telelink to visuals [가정: "Voice/gesture/thought interface mainstream"]

### Phase 5 — Feature·Design·Response Wheel

basic-v1과 같은 wheel 구조이지만 *각 spoke가 새 feature·design 요소*.

**일반 템플릿** (모든 item에 적용):
```
                [sub-feature 1a]
                   │
    [feature 1] ───┼──── [sub-feature 1b]
                   │
    ┌──────────────●──────────────┐
    │          [{item}]           │
    └──────────────●──────────────┘
                   │
    [feature 2] ───┼──── [sub-feature 2a]
                   │     ├── [sub-feature 2b]
                   │     └── [sub-feature 2c]
                   │
    [feature 3] ───┘
```

**PDF Figure 5 재현 (VCR in Conscious Technology scenario)** — `references/figure5_vcr_conscious_tech.md` 참조:

```
                Microphone
                   │
        Voice ─────┼───── Voice Reproduction Program
        Activation │
                   │
                   │      ┌─ Built-in Modem
                   │      │
        On-line ───┤      ├─ Telelink to Visuals
        Access     │      │
                   │      ├─ Electronic Funds Transfer
                   │      │
        ┌──────────●──────●────────────┐
        │      [VCR-Conscious]         │
        └──────────●──────●────────────┘
                   │      │
                   │      ├─ Remote Visual Data Banks
                   │      │
        Search ────┤      ├─ Analysis Computer Program
        TV         │      │
        Schedules  │      └─ Automatically Displayed
                   │
        Viewing ───┼───── Viewing Pattern Analysis
        Pattern    │
                   │
        Feedback ──┼───── Computer Memory of Interests
        on Previous│
        Patterns
```

**PDF Figure 5 features 전체 목록** (Glenn 2009 §III.C, 14개):
voice activation · microphone · voice reproduction program · built-in modem · search TV schedules · remote visual data banks · electronic funds transfer · viewing pattern analysis · feedback on previous patterns · computer memory of interests · on-line access · analysis computer program · telelink to visuals · automatically displayed

### Phase 6 — Decision Tree·Morphological Analysis 연동

PDF 명시: *"This variation is similar in function to decision trees and morphological analysis."* (Glenn 2009 §III.C)

**Decision Tree Export 원칙**: wheel features만 사용. PDF 사례 VCR에서 파생되지 않은 옵션(예: "Gesture", "Thought-link")은 **[시나리오 확장]** 레이블을 반드시 부착하고 PDF 출처 없음을 명시. 레이블 없는 추가 금지.

**Decision Tree Export (PDF Figure 5 VCR 사례)**:

```
[Future VCR Design Decision]
├── Interface
│   ├── Voice Activation (PDF §III.C: voice activation)
│   │   ├── Microphone (PDF §III.C)
│   │   └── Voice Reproduction Program (PDF §III.C)
│   ├── Gesture [시나리오 확장 — PDF 미출처, 시나리오 전제 파생]
│   └── Thought-link [시나리오 확장 — PDF 미출처, 시나리오 전제 파생]
├── Connectivity
│   ├── Built-in Modem (PDF §III.C)
│   ├── Telelink to Visuals (PDF §III.C)
│   └── Electronic Funds Transfer (PDF §III.C)
├── Intelligence
│   ├── Search Engine
│   │   ├── TV Schedules Search (PDF §III.C)
│   │   └── Remote Visual Data Banks (PDF §III.C)
│   ├── Personalization
│   │   ├── Computer Memory of Interests (PDF §III.C)
│   │   └── Feedback on Previous Patterns (PDF §III.C)
│   └── Analysis
│       ├── Analysis Computer Program (PDF §III.C)
│       └── Viewing Pattern Analysis (PDF §III.C)
└── Output
    └── Automatically Displayed (PDF §III.C)
```

**Morphological Matrix Export 원칙** (Zwicky 1969 morphological box):
- 각 row의 Option은 wheel features 또는 scenario assumption에서 직접 파생
- wheel features에 없는 옵션 추가 시 반드시 `[시나리오 확장]` 레이블
- "Telepathic"·"Mind-direct"·"Holographic" 등 scenario와 무관한 SF적 추가 절대 금지
- 각 row는 최소 2개, 최대 4개 옵션

**Morphological Matrix Export (VCR 사례, ILLUSTRATIVE ONLY)**:

| Parameter | Option A (PDF 출처) | Option B (PDF/시나리오 파생) | Option C [시나리오 확장] |
|-----------|---------|---------|---------|
| Interface | Voice activation (PDF) | On-line commands (PDF) | Gesture [시나리오 확장] |
| Connectivity | Built-in Modem (PDF) | Telelink to Visuals (PDF) | In-home network [시나리오 확장] |
| Storage | Local tape (baseline) | Computer memory (PDF) | Cloud [시나리오 확장] |
| Search | Manual (baseline) | TV Schedules Search (PDF) | Remote Visual Data Banks (PDF) |
| Personalization | None (baseline) | Memory of Interests (PDF) | Active learning [시나리오 확장] |
| Intelligence Output | Automatic display (PDF) | Pattern Feedback (PDF) | Viewing Analysis (PDF) |

> ⚠ **ILLUSTRATIVE EXAMPLE**: 위 matrix는 구조 설명용 예시. 실제 실행 시 각 row의 Option은 Phase 5 wheel에서 식별된 features 목록에서만 추출한다. Option 수는 `morphological_options_total = ∏(각 row의 option 수)`로 결정론적 계산.

**참고**: Zwicky, F. (1969). *Discovery, Invention, Research Through the Morphological Approach*. New York: Macmillan.

### Phase 7 — Cross-scenario Comparison (다중 시나리오 시)

같은 item을 여러 시나리오에서 forecast한 경우.

**Cross-scenario divergence_score 계산 알고리즘 (결정론적 Python 함수)**: `python3 calculate_divergence.py` 호출.

```
알고리즘: Jaccard 비유사도
  입력: 시나리오 A의 features 집합 SetA, 시나리오 B의 features 집합 SetB
  계산: score(A,B) = 1 − |SetA ∩ SetB| / |SetA ∪ SetB|
  범위: 0 (두 시나리오 features 완전 동일) ~ 1 (두 시나리오 features 완전 상이)
  다중 시나리오: 모든 pair의 score를 평균하여 overall_divergence_score 산출
```

> ⚠ **날짜·연도 경고**: 아래 Cross-scenario Comparison 예시 테이블의 연도(2027/2030/2035+)는 **ILLUSTRATIVE EXAMPLE ONLY**. 실제 실행 시 specific 연도 예측은 근거 없는 할루시네이션에 해당하므로 절대 확정 수치로 제시하지 않는다. 연도가 필요하면 반드시 "(ILLUSTRATIVE — source 없음)" 표기 또는 범위(예: "2025~2035")로 대체한다.

```markdown
| Feature | Optimistic Scenario | Pessimistic Scenario | Neutral Scenario |
|---------|---------------------|----------------------|-------------------|
| Voice activation | Strong adoption | Limited (privacy concern) | Mainstream |
| Cloud connectivity | Universal | Distrusted | Selective |
| Personalization | Hyper-personal | Manual only | Opt-in |
| Cost trajectory | Declining rapidly | Expensive (luxury) | Moderate decline |
| Mass adoption timing | [ILLUSTRATIVE: early] | [ILLUSTRATIVE: late] | [ILLUSTRATIVE: mid] |
```

시나리오에 따라 같은 item이 *얼마나 다르게 발달하는지* divergence_score로 수치화.

## 5. PDF 인용 fragment (검증됨)

> *"The Futures Wheel can also be used as a method to create forecasts within alternative scenarios. In this application, one selects a scenario and an item in that scenario to explore."* (Glenn 2009, Ch. 6, §III.C)

> *"This variation is similar in function to decision trees and morphological analysis."* (Glenn 2009, Ch. 6, §III.C)

> *"During a scenario construction exercise that has identified driving forces, Futures Wheels could be used on each driving force to explore the pattern of consequences for each. This could provide richer input for the content of the scenarios."* (Glenn 2009, Ch. 6, §V)

## 6. 마스터 입력 인터페이스

```yaml
sub_skill: vision-foresight-futures-wheel-scenario-forecast
inputs:
  pattern: "P1" | "P2" | "P3" | "P4"      # 필수, enum 검증
  scenarios:
    - { type, name, description, driving_forces, world_state_assumptions }
  item: { name, type, current_state, baseline_features }
  contradiction_promoted:                   # P4 패턴 시 필수
    issue: "{중앙 이슈}"
    node_a: "{노드 A}"
    node_b: "{노드 B}"
    contradiction_type: "logical" | "empirical" | "value"
    description: "{모순 설명}"
  decision_tree_export: true|false
  morphological_export: true|false
  expert_pool_cast: [...]
outputs:
  - scenario_frame_lockin
  - feature_design_wheel
  - decision_tree        # decision_tree_export: true 시만
  - morphological_matrix # morphological_export: true 시만
  - cross_scenario_comparison  # scenarios 2개 이상 시만
  - pdf_citations
```

## 7. 호출 후 마스터로 반환

```yaml
sub_skill_output:
  status: "completed" | "error" | "partial"
  error_detail: "{error 시만 기재}"
  pattern_applied: "P1"|"P2"|"P3"|"P4"
  scenarios_processed: N                  # 처리된 시나리오 수 (정수)
  features_identified: M                  # Phase 5 wheel spoke 총수 (정수, 최소 5)
  decision_tree_depth: K                  # 최대 leaf depth (정수, 최대 branch 기준)
  morphological_options_total: O          # ∏(각 row option 수) 결정론적 계산
  cross_scenario_divergence_score: 0~1    # Jaccard 비유사도, python3 calculate_divergence.py 출력
  visualizations:
    wheel: "{ASCII 또는 markdown 표현}"
    decision_tree: "{트리 텍스트}"
    morphological_matrix: "{마크다운 테이블}"
  pdf_citations:
    - { author: "Glenn, J.C.", year: 2009, work: "Futures Research Methodology V3.0", chapter: 6, section: "§III.C", quote: "{인용 원문}" }
```

## 8. 오류 및 예외 처리

| 오류 조건 | 처리 방법 | 출력 |
|-----------|-----------|------|
| `pattern` 이 P1~P4 외 값 | 즉시 중단 | `status: error`, `error_detail: "invalid pattern"` |
| `scenarios` 비어있음 | 즉시 중단 | `status: error`, `error_detail: "no scenario provided"` |
| `item` 누락 | 즉시 중단 | `status: error`, `error_detail: "item required"` |
| P4 패턴에 `contradiction_promoted` 누락 | 즉시 중단 | `status: error`, `error_detail: "P4 requires contradiction_promoted"` |
| Phase 4 feature에 `[가정 N]` 인용 누락 | 해당 feature 기각, 계속 | `status: partial`, 기각 feature 목록 포함 |
| `features_identified` < 5 | 경고 + 계속 | `status: partial`, `error_detail: "low feature count"` |
| Decision tree / morphological export 요청인데 features < 3 | 해당 export 생략 | 해당 출력 키 null |
| `cross_scenario_divergence_score` 계산 실패 | -1 반환 | `error_detail: "divergence calc failed"` |

## 9. 결정론적 Python 스크립트

### `validate_inputs.py`

```python
#!/usr/bin/env python3
"""결정론적 입력 스키마 검증 — LLM 판단 대체."""
import json, sys, argparse

VALID_SCENARIO_TYPES = {"optimistic", "pessimistic", "neutral", "driving_force", "custom"}
VALID_ITEM_TYPES = {"product", "technology", "policy", "organization", "service", "concept"}
VALID_PATTERNS = {"P1", "P2", "P3", "P4"}
VALID_CONTRADICTION_TYPES = {"logical", "empirical", "value"}

def validate_scenario(s):
    errors = []
    if s.get("type") not in VALID_SCENARIO_TYPES:
        errors.append(f"scenario.type must be one of {VALID_SCENARIO_TYPES}, got: {s.get('type')}")
    if not s.get("name") or not (1 <= len(str(s["name"])) <= 100):
        errors.append("scenario.name required (1-100 chars)")
    if not s.get("description") or len(str(s["description"])) < 20:
        errors.append("scenario.description required (min 20 chars)")
    dfs = s.get("driving_forces", [])
    if not (2 <= len(dfs) <= 7):
        errors.append(f"driving_forces count must be 2-7, got {len(dfs)}")
    wsa = s.get("world_state_assumptions", [])
    if len(wsa) < 2:
        errors.append(f"world_state_assumptions count must be >= 2, got {len(wsa)}")
    return errors

def validate_item(item):
    errors = []
    if not item.get("name"):
        errors.append("item.name required")
    if item.get("type") not in VALID_ITEM_TYPES:
        errors.append(f"item.type must be one of {VALID_ITEM_TYPES}, got: {item.get('type')}")
    if not item.get("current_state"):
        errors.append("item.current_state required")
    bf = item.get("baseline_features", [])
    if len(bf) < 2:
        errors.append(f"baseline_features must have >= 2 items, got {len(bf)}")
    return errors

def validate_full(data):
    errors = []
    pattern = data.get("pattern")
    if pattern not in VALID_PATTERNS:
        errors.append(f"pattern must be one of {VALID_PATTERNS}, got: {pattern}")
        return errors  # 이하 검증 불가
    scenarios = data.get("scenarios", [])
    if not scenarios:
        errors.append("scenarios list required")
    for i, s in enumerate(scenarios):
        for e in validate_scenario(s):
            errors.append(f"scenarios[{i}]: {e}")
    if "item" not in data:
        errors.append("item required")
    else:
        for e in validate_item(data["item"]):
            errors.append(f"item: {e}")
    if pattern == "P4":
        cp = data.get("contradiction_promoted", {})
        if not cp:
            errors.append("P4 requires contradiction_promoted")
        else:
            for field in ["issue", "node_a", "node_b", "description"]:
                if not cp.get(field):
                    errors.append(f"contradiction_promoted.{field} required for P4")
            if cp.get("contradiction_type") not in VALID_CONTRADICTION_TYPES:
                errors.append(f"contradiction_type must be one of {VALID_CONTRADICTION_TYPES}")
    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON input file path")
    args = parser.parse_args()
    with open(args.input) as f:
        data = json.load(f)
    errors = validate_full(data)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}))
        sys.exit(1)
    print(json.dumps({"valid": True, "errors": []}))
```

### `calculate_divergence.py`

```python
#!/usr/bin/env python3
"""결정론적 Jaccard 비유사도 계산 — LLM 판단 대체."""
import json, sys, argparse
from itertools import combinations

def jaccard_dissimilarity(set_a: set, set_b: set) -> float:
    """Jaccard 비유사도: 0(완전동일) ~ 1(완전상이)"""
    if not set_a and not set_b:
        return 0.0
    union_size = len(set_a | set_b)
    if union_size == 0:
        return 0.0
    intersection_size = len(set_a & set_b)
    return round(1.0 - intersection_size / union_size, 4)

def normalize_feature(f: str) -> str:
    """feature 정규화: 소문자, 공백 제거, 구분자 통일"""
    return f.strip().lower().replace("-", " ").replace("_", " ")

def calculate_overall_divergence(scenarios_features: list[list[str]]) -> dict:
    """
    입력: 각 시나리오의 features 리스트 (list of list)
    출력: pairwise scores + overall_divergence_score
    """
    sets = [set(normalize_feature(f) for f in feats) for feats in scenarios_features]
    n = len(sets)
    if n < 2:
        return {"error": "at least 2 scenarios required", "overall_divergence_score": -1}
    pairwise = []
    for i, j in combinations(range(n), 2):
        score = jaccard_dissimilarity(sets[i], sets[j])
        pairwise.append({"scenario_i": i, "scenario_j": j, "jaccard_dissimilarity": score})
    overall = round(sum(p["jaccard_dissimilarity"] for p in pairwise) / len(pairwise), 4)
    return {
        "pairwise_scores": pairwise,
        "overall_divergence_score": overall,
        "interpretation": (
            "near-identical" if overall < 0.2 else
            "low divergence" if overall < 0.4 else
            "moderate divergence" if overall < 0.6 else
            "high divergence (critical branch)" if overall < 0.8 else
            "extreme divergence"
        )
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON file: {scenarios: [[feat1,...], [feat1,...], ...]}")
    args = parser.parse_args()
    with open(args.input) as f:
        data = json.load(f)
    result = calculate_overall_divergence(data["scenarios"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 10. references/ 파일 목록

| 파일 | 용도 |
|------|------|
| `references/figure5_vcr_conscious_tech.md` | PDF Figure 5 VCR 사례 상세 재현 (14 features 전체) |
| `references/four_usage_patterns.md` | P1~P4 패턴 비교 가이드 |
| `references/decision_tree_export.md` | wheel → decision tree 변환 알고리즘 |
| `references/morphological_matrix_export.md` | wheel → Zwicky box 변환 (출처 레이블 포함) |
| `references/scenario_frame_lock_template.md` | 시나리오 frame lock-in markdown 템플릿 |

## 11. 완전한 출처 정보

Glenn, J. C. (2009). Futures Wheel. In J. C. Glenn & T. J. Gordon (Eds.), *Futures Research Methodology — Version 3.0* (Chapter 6). Washington, DC: The Millennium Project.

- **§III.C** "Creating Forecasts within Alternative Scenarios": VCR-in-conscious-technology 사례, Figure 5
- **§V** "Use in Combination": Driving force별 wheel 활용법
- **Morphological Analysis 보조 출처**: Zwicky, F. (1969). *Discovery, Invention, Research Through the Morphological Approach*. New York: Macmillan.
