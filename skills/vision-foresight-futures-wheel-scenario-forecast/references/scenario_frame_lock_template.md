# Scenario Frame Lock-in Template

> **용도**: Phase 3에서 Scenario Designer Agent가 시나리오 frame을 구조화하는 템플릿.
> **출처**: Glenn (2009) §III.C VCR 사례 구조 분석 + §V driving force 활용법.

## 템플릿

```markdown
## Scenario Frame: "{시나리오 이름}"

> Pattern: {P1|P2|P3|P4}
> Item: {item 이름}
> Scenario type: {optimistic|pessimistic|neutral|driving_force|custom}

### 핵심 가정 (최소 3개, 최대 7개)

각 가정에 번호를 부여한다. Phase 4에서 feature grounding 시 이 번호를 인용한다.

1. {가정 1} — [DF: {연결 driving force}]
2. {가정 2} — [DF: {연결 driving force}]
3. {가정 3} — [DF: {연결 driving force}]
...

### Driving Forces ({2~7개})

| # | Driving Force | Strength | 시나리오 내 역할 |
|---|---------------|----------|----------------|
| DF1 | {force} | high/medium/low | {역할 한 줄} |
| DF2 | {force} | high/medium/low | {역할 한 줄} |
...

### World State (시나리오 내 T+의 세계 묘사)

- {state 1}
- {state 2}
- {state 3}
...

### Item이 적응해야 할 압력

각 압력은 반드시 위 핵심 가정 번호에 연결된다.

- {pressure 1} → [가정 1 연결]
- {pressure 2} → [가정 2 연결]
- {pressure 3} → [가정 3 연결]
...

### Scenario Frame Lock 확인

- [ ] 핵심 가정 3개 이상 작성
- [ ] 모든 pressure가 핵심 가정과 1:1 연결됨
- [ ] Driving Forces 강도 기재 (high/medium/low)
- [ ] World State가 시나리오 type (낙관/비관/중립)과 일치
```

## VCR 사례 적용 예시

```markdown
## Scenario Frame: "Conscious Technology (Post-Information Age)"

> Pattern: P1
> Item: VCR (Videocassette Recorder)
> Scenario type: custom

### 핵심 가정

1. Computing power approaches biological brain scale — [DF: AI capability advance]
2. Voice/gesture/thought interface is mainstream — [DF: Human-machine interface evolution]
3. User intolerance for friction drives radical simplicity — [DF: User intolerance for friction]

### Driving Forces

| # | Driving Force | Strength | 시나리오 내 역할 |
|---|---------------|----------|----------------|
| DF1 | AI capability advance | high | 기기 자체 지능 가능하게 함 |
| DF2 | Human-machine interface evolution | high | Voice/gesture 인터페이스 현실화 |
| DF3 | User intolerance for friction | medium | 완전 자동화 압력 |

### World State

- Devices are expected to understand natural language commands
- Personalization is default, not optional
- Electronic funds transfer integrated into consumer devices
- Remote data bank access is a standard consumer feature

### Item이 적응해야 할 압력

- VCR must respond to voice, not manual buttons → [가정 2 연결]
- VCR must learn and remember user preferences → [가정 1 연결]
- VCR must connect to external networks and data sources → [가정 1 연결]
- VCR must operate without user friction → [가정 3 연결]

### Scenario Frame Lock 확인

- [x] 핵심 가정 3개 작성
- [x] 모든 pressure가 핵심 가정과 연결됨
- [x] Driving Forces 강도 기재
- [x] World State가 custom 시나리오와 일치
```

## 사용 방법

1. Phase 3 시작 시 Scenario Designer Agent가 이 템플릿을 로드
2. 시나리오 입력 정보(scenario_input YAML)를 템플릿에 매핑
3. 압력(pressure) 목록에서 각 pressure에 가정 번호 연결
4. Lock 확인 체크리스트 통과 후 Phase 4로 진행
5. Phase 4에서 각 feature는 반드시 압력 또는 핵심 가정 번호 인용
