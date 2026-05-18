# Four Usage Patterns — P1~P4

> **출처**: Glenn (2009) Ch. 6, §III.C + §V; 마스터 layer 확장

## 패턴 비교표

| 항목 | P1: Item-in-Scenario | P2: Driving Force별 | P3: 낙관/비관/중립 | P4: Contradiction Branch |
|------|---------------------|---------------------|-------------------|--------------------------|
| **시나리오 수** | 1 | 1 (driving force N개) | 3 (낙관/비관/중립) | 2 (node_a 참, node_b 참) |
| **item 수** | 1 | 1 | 1 | 1 |
| **wheel 수** | 1 | N (DF당 1) | 3 | 2 |
| **PDF 출처** | §III.C VCR 사례 직접 | §V "Use in Combination" | P1 × 3 반복 | 마스터 layer |
| **cross-scenario 비교** | 불필요 | 불필요 | 필수 | 필수 |
| **divergence score** | 해당없음 | 해당없음 | 3개 pair 평균 | 1 pair |
| **P4 특수 입력** | — | — | — | contradiction_promoted |

## P1: Item-in-Scenario

**출처**: Glenn (2009) §III.C 직접 명시

```
[입력] scenario (1개) + item (1개)
[처리] Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 (optional) → Phase 7 (skip)
[출력] feature_design_wheel × 1 + decision_tree (optional) + morphological_matrix (optional)
```

**체크리스트**:
- [ ] scenario.type 유효값
- [ ] item.type 유효값
- [ ] Phase 4 features 각각 [가정 N] 인용 포함
- [ ] Phase 5 spoke 수 ≥ 5
- [ ] pdf_citations에 Glenn 2009 §III.C 포함

## P2: Driving Force별 Wheel

**출처**: Glenn (2009) §V *"Futures Wheels could be used on each driving force to explore the pattern of consequences for each."*

```
[입력] scenario (1개, driving_forces ≥ 2) + item (1개)
[처리] for DFi in driving_forces:
           wheel_i = run(Phase 3~5, center_issue=DFi)
[출력] wheel_i × N (N = driving_forces 수)
[Cross-compare] 비교 불필요 (같은 item의 DF별 전개를 독립적으로 보여주는 것이 목적)
```

**체크리스트**:
- [ ] driving_forces 2~7개 확인 (validate_inputs.py로 검증)
- [ ] 각 DF별로 독립 wheel 작성 (wheel 간 혼용 금지)
- [ ] 각 wheel에 해당 DF 이름 명시

## P3: 낙관/비관/중립 분기

**출처**: P1을 3회 반복 적용 (같은 item, 3가지 시나리오 frame)

```
[입력] scenarios × 3 (type: optimistic, pessimistic, neutral) + item (1개)
[처리] P1 × 3회 실행
[출력] wheel × 3 + cross_scenario_comparison + divergence_score
```

**체크리스트**:
- [ ] scenarios 3개 모두 type 다름 (optimistic/pessimistic/neutral)
- [ ] 같은 item 사용 확인
- [ ] Phase 7 Cross-scenario Comparison 필수
- [ ] divergence_score: calculate_divergence.py 호출 (LLM 추론 금지)
- [ ] 연도 예측값 있으면 반드시 [ILLUSTRATIVE] 표기

## P4: Contradiction → Scenario Branch

**출처**: 마스터 consequence-linker 연동

```
[입력] contradiction_promoted { issue, node_a, node_b, contradiction_type, description }
[처리]
   Scenario-A: node_a가 참인 world state 구성 → P1 실행
   Scenario-B: node_b가 참인 world state 구성 → P1 실행
[출력] wheel × 2 + cross_scenario_comparison + divergence_score
```

**판정 기준**:
- divergence_score ≥ 0.6 → "critical branch" → 마스터에 에스컬레이션
- divergence_score < 0.6 → "minor branch" → 일반 완료로 보고

**체크리스트**:
- [ ] node_a와 node_b가 실제로 논리적/경험적/가치 모순인지 확인
- [ ] 각 시나리오 world_state_assumptions에 node 반영
- [ ] divergence_score: calculate_divergence.py 호출 (LLM 추론 금지)
