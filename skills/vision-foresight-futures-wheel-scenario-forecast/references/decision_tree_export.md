# Decision Tree Export — wheel → decision tree 변환 알고리즘

> **출처**: Glenn (2009) §III.C *"This variation is similar in function to decision trees and morphological analysis."*

## 알고리즘

### 입력
- Phase 5 wheel에서 산출된 features 목록 (spokes + sub-spokes)
- 각 feature의 출처 레이블 (`PDF_sourced` | `scenario_extension`)

### 처리 단계

```
1. 그룹화 (Synthesizer Agent)
   - wheel의 spokes를 의미적 카테고리(2~6개)로 그룹화
   - 카테고리명은 wheel spokes의 공통 개념에서 추출
   - 카테고리 예: Interface, Connectivity, Intelligence, Output

2. 트리 구성
   [Root: "{item} Design Decision"]
   └── [Category A]
       ├── [Spoke A1] (출처 레이블)
       │   ├── [Sub-spoke A1a] (출처 레이블)
       │   └── [Sub-spoke A1b] (출처 레이블)
       └── [Spoke A2] (출처 레이블)
   ...

3. 출처 레이블 부착 (필수)
   - PDF 원전 feature: "(PDF §III.C)" 등 섹션 명시
   - 시나리오 전제 파생 feature: "[시나리오 확장 — PDF 미출처]"
   - 출처 없는 추가 금지

4. Depth 계산
   - decision_tree_depth = 최대 leaf까지의 depth (root = 0)
   - VCR 예시: root(0) → Category(1) → Spoke(2) → Sub-spoke(3) → depth = 3
```

### 출력 형식

```
[{item} Design Decision]
├── {Category A}
│   ├── {Spoke 1} ({출처})
│   │   ├── {Sub-spoke 1a} ({출처})
│   │   └── {Sub-spoke 1b} ({출처})
│   └── {Spoke 2} ({출처})
├── {Category B}
│   └── ...
```

## VCR 사례 적용 예시

```
[Future VCR Design Decision]
├── Interface
│   ├── Voice Activation (PDF §III.C)
│   │   ├── Microphone (PDF §III.C)
│   │   └── Voice Reproduction Program (PDF §III.C)
│   ├── Gesture [시나리오 확장 — PDF 미출처]
│   └── Thought-link [시나리오 확장 — PDF 미출처]
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

**decision_tree_depth**: 4 (root → Category → Sub-category → Feature → depth=3 for leaf at Microphone level)

실제 계산: `root(0) → Interface(1) → Voice Activation(2) → Microphone(3)` → depth = 3

## 제약 사항

- wheel에 없는 노드를 tree에 임의 추가 금지
- "Gesture"·"Thought-link" 추가 시 반드시 [시나리오 확장] 레이블 필수
- 카테고리는 wheel spokes에서 귀납적으로 도출; 사전에 정해진 틀 없음
