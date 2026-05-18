# Cross-Domain Matrix Visualization — Heat Map 시각화 가이드

> 출처: SKILL.md §7, Anchored + Tagged 모델 (references/anchored_tagged_model.md)
> 결정론 함수: `scbe_validator.py cross_domain_matrix`

---

## 1. Matrix 계산 (결정론)

모든 노드의 `secondary_tags`를 집계하여 카테고리 간 cross-domain influence 강도를 계산.

```bash
python3 scbe_validator.py cross_domain_matrix '{"nodes": [
  {"primary_tag": "Technology", "secondary_tags": ["Economy", "Society"]},
  {"primary_tag": "Technology", "secondary_tags": ["Economy"]},
  {"primary_tag": "Economy", "secondary_tags": ["Society", "Politics"]},
  ...
]}'
```

## 2. Heat Map 시각화 형식

### Markdown Table (기본)

```markdown
| from ↓ \ to → | Society | Technology | Economy | Environment | Politics | Spirituality |
|----------------|---------|------------|---------|-------------|----------|--------------|
| **Society**    | —       | 5          | 8       | 2           | 4        | 3            |
| **Technology** | 12      | —          | 15      | 4           | 6        | 2            |
| **Economy**    | 9       | 8          | —       | 7           | 11       | 1            |
| **Environment**| 3       | 5          | 6       | —           | 8        | 4            |
| **Politics**   | 7       | 4          | 9       | 5           | —        | 6            |
| **Spirituality**| 8      | 1          | 2       | 3           | 5        | —            |
```

### 강도 표시 (emoji 레이어)

```
0-2:   ⬜ (매우 약함)
3-5:   🟦 (약함)
6-9:   🟨 (중간)
10-14: 🟧 (강함)
15+:   🟥 (매우 강함)
```

예시 (위 숫자 적용):
```
| from ↓ \ to → | Soc | Tech | Eco | Env | Pol | Spi |
|----------------|-----|------|-----|-----|-----|-----|
| Society        | —   | 🟦   | 🟨  | ⬜  | 🟦  | 🟦  |
| Technology     | 🟧  | —    | 🟥  | 🟦  | 🟨  | ⬜  |
| Economy        | 🟨  | 🟨   | —   | 🟨  | 🟧  | ⬜  |
| Environment    | 🟦  | 🟦   | 🟨  | —   | 🟨  | 🟦  |
| Politics       | 🟨  | 🟦   | 🟨  | 🟦  | —   | 🟨  |
| Spirituality   | 🟨  | ⬜   | ⬜  | 🟦  | 🟦  | —   |
```

## 3. 해석 가이드

### 3.1 지배적 연결 식별

```python
# cross_domain_matrix 출력에서:
"strongest_connection": "Technology→Economy"
"strongest_count": 15
```

해석: "Technology 노드의 secondary_tags에 Economy가 15회 등장 → 현 시대 기술-경제 연결이 가장 강함"

### 3.2 패턴 해석 방법

| 패턴 | 의미 |
|------|------|
| Row 합계가 큰 카테고리 | 다른 카테고리에 많은 영향을 미치는 **driver** |
| Column 합계가 큰 카테고리 | 많은 카테고리로부터 영향받는 **receptor** |
| 대각선 양방향 강함 | 두 카테고리 간 **상호 강화 루프** |
| 특정 셀만 강함 | **단방향 지배 관계** |

### 3.3 현 시대 예상 패턴 (AI 전환 시대)

- **Technology→Economy**: 가장 강한 연결 (AI 경제화)
- **Economy→Politics**: 강함 (경제 불평등 → 정치화)
- **Technology→Society**: 강함 (AI-사회 구조 재편)
- **Spirituality→X**: 상대적으로 약함 (의미 위기 고립 경향)

### 3.4 해석 시 할루시네이션 방지

- Matrix 수치는 `scbe_validator.py cross_domain_matrix` 출력으로만 확정
- LLM이 수치를 자연어로 재추론하면 안 됨 — 항상 Python 출력을 그대로 사용
- "가장 강한 연결"도 `"strongest_connection"` 필드 값 그대로 인용

## 4. 출력 형식 통합 (Layer 1 Executive Summary 포함)

Layer 1에 Cross-Domain Influence Top 3를 반드시 포함:

```markdown
## Cross-Domain Influence Top 3
{cross_domain_matrix 결과 기반 — Python 출력 직접 인용}
1. Technology→Economy: N회 (현 시대 디지털 경제화)
2. Economy→Politics: N회 (경제 불안 → 정치 극화)
3. Technology→Society: N회 (AI 채용 → 직업·정체성 재편)
```

## 5. 학술 근거

Cross-domain influence matrix는 다음 학술 전통과 호환:

- **STEEPS 분석** (Environmental Scanning): Morrison (1992), Choo (1999)
- **Cross-Impact Analysis** (Gordon & Helmer 1966): 이벤트 간 조건부 확률 대신 카테고리 영향 강도로 적용
- **시스템 다이나믹스** (Forrester 1961): Secondary feedback loop 식별 도구로 활용 가능
