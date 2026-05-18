# SCBE Protocol — 정식 정의 및 균일 fan-out 강제 알고리즘

> 출처: 박사님 2026-05-11 두 번째 강화 명령 — SKILL.md §2.1, §2.2, §6
> 결정론 함수: `scbe_validator.py validate_node_counts`, `scbe_validator.py validate_fanout`

---

## 1. SCBE 정의

**SCBE (STEEPS Categorical Binary Expansion)** = 균일 2-fan-out 이진 트리 + STEEPS 카테고리 propagation을 결합한 퓨처스 휠 확장 프로토콜.

Glenn(2009) 원전 wheel의 *불균일 fan-out*(인간 brainstorming 시뮬레이션)을 **AI 컴퓨팅 파워** 활용 모드로 전환.

## 2. 균일 2-fan-out 강제 알고리즘

### 규칙

```
SCBE_uniform_fanout:
  - Senary leaf(ring 6)를 제외한 모든 노드: 정확히 2 children
  - 기본 branching: 2 (binary)
  - 옵션 branching: 3 (사용자 명시 시, 3-fan-out → senary 729 노드)
```

### 검증 절차 (결정론)

```bash
# 부모 노드의 fan-out 검증
python3 scbe_validator.py validate_fanout \
  '{"node_id": "T_S_1a1", "children": ["Q_S_1a1a", "Q_S_1a1b"]}'

# 기대 출력: "pass": true, "children_count": 2 == expected: 2
```

### 위반 시 처리

```
- on_violation: "해당 노드에 children 추가 발굴 또는 초과 children 재배치"
- tolerance: 0 (완전 강제, 예외 없음)
```

## 3. 노드 수 결정론 계산

```
ring r의 노드 수 = n_primary × fan_out^(r-1)

STEEPS 6 (n_primary=6, fan_out=2, rings=6):
  Center:      1
  Primary:     6
  Secondary:   12
  Tertiary:    24
  Quaternary:  48
  Quinary:     96
  Senary:      192
  Total:       379

V2 8-sector (n_primary=8, fan_out=2, rings=6):
  Center:      1
  Primary:     8
  Secondary:   16
  Tertiary:    32
  Quaternary:  64
  Quinary:     128
  Senary:      256
  Total:       505
```

```bash
# STEEPS 6 검증
python3 scbe_validator.py validate_node_counts '{"n_primary": 6}'

# V2 8-sector 검증
python3 scbe_validator.py validate_node_counts '{"n_primary": 8}'
```

## 4. Per-Category Subtree 구조

각 STEEPS 카테고리는 독립된 서브트리를 형성:

```
카테고리당 노드 수 = 2^0 + 2^1 + 2^2 + 2^3 + 2^4 + 2^5
                   = 1 + 2 + 4 + 8 + 16 + 32 = 63
```

총 노드 = Center(1) + 6 카테고리 × 63 = 1 + 378 = **379**

## 5. 오류 처리

| 오류 유형 | 처리 |
|-----------|------|
| Fan-out ≠ 2 | 해당 노드 재발굴 강제 |
| Ring 누락 | 누락 ring 전체 재생성 |
| Category 불균형 | 부족 카테고리 노드 추가 발굴 |
| Total mismatch | `scbe_validator.py validate_node_counts` 재실행 후 차이 수정 |
