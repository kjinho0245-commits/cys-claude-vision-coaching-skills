# Balance Audit Algorithm — 카테고리 균형 강제 ±0 검증

> 출처: SKILL.md §6, §12 Success Metrics
> 결정론 함수: `scbe_validator.py balance_audit`, `scbe_validator.py validate_node_counts`

---

## 1. 균형 강제 원칙

**SCBE 카테고리 균형 규칙**: 각 ring에서 모든 STEEPS 카테고리가 동일한 수의 노드를 가져야 함.

```
tolerance: ±0 (완벽 균형, 타협 없음)
```

이는 Glenn 원전의 자유형 wheel (불균일 fan-out, 인간 brainstorming)과 다른 **AI 컴퓨팅 파워 모드**의 핵심 특성.

## 2. Ring별 기대 카테고리 노드 수

### STEEPS 6 기준 (n_primary=6, fan_out=2)

| Ring | 카테고리당 노드 수 | 6 카테고리 합계 |
|------|-----------------|----------------|
| Center | — | 1 |
| Primary (ring 1) | 1 | 6 |
| Secondary (ring 2) | 2 | 12 |
| Tertiary (ring 3) | 4 | 24 |
| Quaternary (ring 4) | 8 | 48 |
| Quinary (ring 5) | 16 | 96 |
| Senary (ring 6) | 32 | 192 |
| **Total** | **63** | **378 + 1 = 379** |

### V2 8-sector 기준 (n_primary=8)

| Ring | 카테고리당 노드 수 | 8 카테고리 합계 |
|------|-----------------|----------------|
| Center | — | 1 |
| Primary | 1 | 8 |
| Secondary | 2 | 16 |
| Tertiary | 4 | 32 |
| Quaternary | 8 | 64 |
| Quinary | 16 | 128 |
| Senary | 32 | 256 |
| **Total** | **63** | **504 + 1 = 505** |

## 3. Balance Audit 알고리즘

### 3.1 Per-Ring Audit

각 ring 완성 후:

```python
# SCBE sub-skill이 Claude에게 호출 요청하는 결정론 검증
python3 scbe_validator.py balance_audit '{
  "category_counts": {
    "Society": <count>,
    "Technology": <count>,
    "Economy": <count>,
    "Environment": <count>,
    "Politics": <count>,
    "Spirituality": <count>
  }
}'
```

### 3.2 기대 출력 (정상)

```json
{
  "expected_per_category": 63,
  "variance": 0,
  "violations": {},
  "pass": true,
  "verdict": "BALANCE PASS (±0 완벽 균형)"
}
```

### 3.3 위반 시 출력 및 처리

```json
{
  "expected_per_category": 63,
  "variance": 2,
  "violations": {"Society": 61, "Technology": 65},
  "pass": false,
  "verdict": "BALANCE FAIL: variance=4, violations={...}"
}
```

**처리 절차**:
1. 부족 카테고리(예: Society 61 → 63 필요): 2 노드 추가 발굴
2. 초과 카테고리(예: Technology 65 → 63 필요): 2 noise 노드 제거 또는 재배치
3. `balance_audit` 재실행으로 PASS 확인

### 3.4 최종 품질 게이트

```python
python3 scbe_validator.py final_quality_gate '{
  "node_counts_by_ring": {
    "Primary": 6, "Secondary": 12, "Tertiary": 24,
    "Quaternary": 48, "Quinary": 96, "Senary": 192
  },
  "category_counts": {"Society": 63, "Technology": 63, ...},
  "srs_avg": 1.8,
  "citation_rate": 0.97,
  "forced_reversal_pass": true
}'
```

## 4. 수학적 증명

**명제**: SCBE (n_primary, rings, fan_out=2)에서 각 카테고리 서브트리가 정확히 (fan_out^rings - 1) / (fan_out - 1) = 2^6 - 1 = 63 노드를 가짐.

**증명**:
```
카테고리 c의 노드 수 = Σ_{r=1}^{6} fan_out^(r-1)
                     = 1 + 2 + 4 + 8 + 16 + 32
                     = 2^6 - 1
                     = 63 (등비급수)

총 노드 = 1 (center) + n_primary × 63
        = 1 + 6 × 63
        = 1 + 378
        = 379
```

균일 2-fan-out이 유지되는 한 이 수식은 항등적으로 성립 → 결정론 검증 가능.

## 5. 오류 유형 분류

| 유형 | 원인 | 탐지 | 치료 |
|------|------|------|------|
| Category under-generation | 특정 카테고리 노드 부족 | `balance_audit` variance > 0 | 해당 카테고리 노드 추가 발굴 |
| Category over-generation | 특정 카테고리 노드 초과 | `balance_audit` variance > 0 | noise 제거 또는 올바른 카테고리로 재배치 |
| Ring skip | 특정 ring 전체 누락 | `validate_node_counts` ring_count 불일치 | 해당 ring 전체 재생성 |
| Fan-out violation | 노드가 2개 아닌 children | `validate_fanout` pass=false | children 추가 발굴 |
| ID mismatch | ID depth와 ring 불일치 | `parse_id` depth_ring_match=false | ID 재생성 |
