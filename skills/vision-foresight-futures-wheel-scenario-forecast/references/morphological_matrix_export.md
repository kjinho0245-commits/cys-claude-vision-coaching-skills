# Morphological Matrix Export — wheel → Zwicky box 변환

> **출처**: Glenn (2009) §III.C *"This variation is similar in function to decision trees and morphological analysis."*
> **Zwicky box 원전**: Zwicky, F. (1969). *Discovery, Invention, Research Through the Morphological Approach*. New York: Macmillan.

## 알고리즘

### 입력
- Phase 5 wheel features 목록 (출처 레이블 포함)
- 각 feature의 카테고리 (Decision Tree에서 사용한 카테고리 재활용)

### 처리 단계

```
1. Parameter(Row) 결정
   - Decision Tree의 최상위 카테고리를 Parameter로 사용
   - 각 Parameter = 하나의 설계 차원

2. Option 생성 규칙 (할루시네이션 차단 원칙)
   Option A: PDF 원전 feature (출처 레이블: PDF §III.C)
   Option B: 시나리오 전제에서 직접 파생 (출처 레이블: 시나리오 파생)
   Option C: [시나리오 확장] — 시나리오 논리상 가능한 확장, 출처 없음 레이블 필수
   Option C 이상: 추가 시 반드시 [시나리오 확장] + 근거 한 줄

   금지 사항:
   - "Telepathic"·"Mind-direct" 등 시나리오와 무관한 SF적 추가 금지
   - 출처 레이블 없는 추가 금지
   - wheel features에 없는 항목 추가 금지 (단, [시나리오 확장] 레이블 시 허용)

3. Options 수 결정
   - 각 row: 최소 2개, 최대 4개
   - options_total = ∏(각 row의 option 수)  ← 결정론적 계산
   - 예: 6 rows × 3 options each = 729 combinations

4. 출력 형식
   | Parameter | Option A (PDF) | Option B (시나리오파생) | Option C [시나리오 확장] |
   |-----------|----------------|------------------------|--------------------------|
   | {카테고리} | {PDF feature}  | {scenario feature}     | {extension feature}      |
```

### morphological_options_total 계산 (결정론적)

```python
options_per_row = [len(options_in_row) for options_in_row in matrix]
morphological_options_total = 1
for n in options_per_row:
    morphological_options_total *= n
# 예: [3, 3, 3, 3, 3, 3] → 729
```

## VCR 사례 적용 예시

| Parameter | Option A (PDF 출처) | Option B (PDF/시나리오 파생) | Option C [시나리오 확장] |
|-----------|---------|---------|---------|
| Interface | Voice activation (PDF §III.C) | On-line commands (PDF §III.C) | Gesture [시나리오 확장] |
| Connectivity | Built-in Modem (PDF §III.C) | Telelink to Visuals (PDF §III.C) | In-home network [시나리오 확장] |
| Storage | Local tape (baseline) | Computer memory (PDF §III.C) | Cloud [시나리오 확장] |
| Search | Manual (baseline) | TV Schedules Search (PDF §III.C) | Remote Visual Data Banks (PDF §III.C) |
| Personalization | None (baseline) | Memory of Interests (PDF §III.C) | Active learning [시나리오 확장] |
| Analysis/Output | Automatic display (PDF §III.C) | Pattern Feedback (PDF §III.C) | Viewing Analysis (PDF §III.C) |

**morphological_options_total**: 3 × 3 × 3 × 3 × 3 × 3 = **729** 조합

## 제약 사항

- "Telepathic" 연결: 시나리오 전제("Computing power approaches biological brain scale", "Voice/gesture/thought interface mainstream")와 무관한 SF 개념 → 사용 금지
- "Mind-direct" 출력: 동일 이유로 사용 금지
- "Holographic" 출력: 시나리오 전제에서 파생 가능하다면 [시나리오 확장] 레이블 하에 허용
- 모든 Option C 이상은 반드시 `[시나리오 확장 — PDF 미출처]` 레이블
