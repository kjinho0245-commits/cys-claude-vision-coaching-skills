# Anchored + Tagged 모델 — 카테고리 propagation B 모델 상세

> 출처: 박사님 승인 — SKILL.md §2.2, §7
> 결정론 함수: `scbe_validator.py cross_domain_matrix`

---

## 1. 모델 선택 근거

박사님이 A(순수 inheritance) vs B(Anchored + Tagged) 중 **B 모델** 승인.

- **A 모델 (순수 inheritance)**: 자손이 부모 카테고리 100% 계승. 단순하지만 cross-domain 영향 추적 불가.
- **B 모델 (Anchored + Tagged)**: 자손이 부모 카테고리 기본 계승(anchor) + cross-domain 영향은 secondary_tags로 명시.

## 2. Node Schema

```yaml
node_schema:
  id: "P_S_1"               # 결정론 생성 (scbe_validator.py generate_id)
  text: "..."               # impact 설명 (LLM 생성 + CoER 검증)
  
  primary_tag (필수, 항상 1개):
    options: [Society, Technology, Economy, Environment, Politics, Spirituality]
    inheritance: 부모 노드의 primary_tag 기본 계승
    exception: 사용자 명시 또는 cross-domain dominant 시 변경 가능
    exception_rate: 1.5% 미만 강제
    
  secondary_tags (옵션, 0~3개):
    purpose: "cross-domain influence 표시"
    examples:
      - primary_tag=Technology, secondary_tags=[Economy]
        → Technology 영향이 Economy 도메인으로 cross-influence
      - primary_tag=Society, secondary_tags=[Politics, Spirituality]
        → Society 변화가 Politics·Spirituality에도 영향
    constraint: primary_tag 자신은 secondary_tags에 포함 불가
    
  sign: 🟢 (+) | 🔴 (-) | 🟡 (0)
  time: ring별 시간 범위 (scbe_validator.py 또는 wheel_math.py ring_time_axis)
  
  reasoning_chain:
    step_1_R1: "{base fact} — [citation]"       # 검증 가능 사실
    step_2_R2: "{intermediate inference} — [citation]"  # 중간 추론
    step_3_H:  "{leap} — Disclosed assumption: {...}"   # 명시적 도약
    
  citation: "[저자, 연도, URL 또는 DOI]"
```

## 3. Category Inheritance 규칙

```
부모 P_T_1 (primary_tag=Technology)
  ↓ 기본 계승
자식 S_T_1a (primary_tag=Technology)
자식 S_T_1b (primary_tag=Technology, secondary_tags=[Economy])
  → S_T_1b: Tech 영역이지만 경제에 cross-influence
```

### 예외: Cross-Domain Primary Tag 변경 (1.5% 미만 강제)

```
P_T_1 (Technology) → S_E_1a (Economy로 primary 변경)
  조건: 해당 분기가 완전히 Economy 도메인으로 이행하는 경우만
  표기: note: "cross-domain primary shift from Technology"
```

## 4. Cross-Domain Matrix 계산 (결정론)

secondary_tags 집계로 카테고리 간 영향 강도 시각화:

```bash
python3 scbe_validator.py cross_domain_matrix '{"nodes": [
  {"primary_tag": "Technology", "secondary_tags": ["Economy", "Society"]},
  {"primary_tag": "Technology", "secondary_tags": ["Economy"]},
  {"primary_tag": "Society", "secondary_tags": ["Politics"]}
]}'
```

### 기대 출력 형식 (SKILL.md §7 heat map)

```
| from\to  | S  | T  | E  | Env | P  | Sp |
|----------|----|----|----|-----|----|----|
| Society  | -  | 0  | 0  | 0   | 1  | 0  |
| Technol  | 1  | -  | 2  | 0   | 0  | 0  |
| ...
```

## 5. secondary_tags 부여 기준

| 기준 | secondary_tag 부여 O | 부여 X |
|------|---------------------|--------|
| Cross-domain 영향이 명백하고 구체적 | O | |
| 영향이 미미하거나 간접적 | | X |
| 이미 primary_tag와 동일 카테고리 | | X (중복 불가) |
| 동시에 3개 초과 | | X (최대 3개) |
