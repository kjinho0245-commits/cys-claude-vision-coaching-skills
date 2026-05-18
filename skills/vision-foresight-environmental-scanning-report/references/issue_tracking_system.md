# Issue Tracking System — Issue ID·Timeline·Cross-Month·Dashboard

> Item 7 (Updates on Previously Identified Issues)의 *연속성*을 운영하기 위한 인프라

## Issue ID 체계

### Format
```
ISSUE-YYYY-NNN

- YYYY: 첫 등장 연도
- NNN: 그 해 issue 순서 번호 (3자리, 001~999)
```

### 예시
- ISSUE-2024-001: AGI 한국 산업 침투 (2024년 1번째 issue)
- ISSUE-2025-012: 한국 기독교 인구 ≤22% (2025년 12번째)
- ISSUE-2026-001: AGI 화이트칼라 침투 가속 (2026년 1번째)
- ISSUE-2026-002: 한국 출산율 0.7 진입 잠정

### Issue 평생 ID
한 issue가 *지속적으로 update*되어도 *원래 ID 유지*. 새 issue로 분기되면 *새 ID*.

#### 원래 ID 유지 vs 새 ID 분기 — 결정 기준
- **원래 ID 유지**: status·data update, 같은 underlying dynamic
- **새 ID 분기**: 본질적으로 다른 새 dynamic (예: AGI 일반 → AGI 화이트칼라 *세분화*)

## Issue Lifecycle

```
1. Identification (첫 records 등장)
        ↓
2. Tracking (분기 records 누적)
        ↓
3. Strategic (보고서 Item 1~5 등장)
        ↓
4. Updating (Item 7로 후속 보고서)
        ↓
5. Resolution (issue 해소·convergence·divergence)
        ↓
6. Archive (역사 record로 저장)
```

### Status 라벨
- **Emerging** — 첫 식별, 추가 검증 필요
- **Active** — 정기 보고·monitoring
- **Strategic** — Top 3-5 priority
- **Wild card** — Low prob × high impact, 모니터링
- **Resolved** — 해소·확정 결과
- **Archived** — 더 이상 active monitoring X

## Cross-Month Tracking 인프라

### 옵션 A — Markdown DB

#### 디렉터리 구조
```
~/Documents/foresight-issues/
├── issues/
│   ├── ISSUE-2024-001-agi-korea-industry.md
│   ├── ISSUE-2025-012-christian-population.md
│   ├── ISSUE-2026-001-agi-white-collar.md
│   └── ...
├── reports/
│   ├── 2024-01-monthly.md
│   ├── 2024-02-monthly.md
│   └── ...
└── _index.md  (issues + reports 종합 index)
```

#### Issue file 양식

```markdown
---
id: ISSUE-2026-001
title: AGI 화이트칼라 침투 가속
domain: [S&T, Economy, Population]
first_identified: 2026-04-15
status: Strategic
priority: T1
last_updated: 2026-05-09
---

# ISSUE-2026-001: AGI 화이트칼라 침투 가속

## Description
[1~2 단락]

## Timeline
- **2026-04**: First identification (2026-04 records 5건)
- **2026-05**: Strategic 격상 (2026-05 monthly report Item 1)
- **2026-06**: (예정 update)

## Status History
- 2026-04-15: Emerging
- 2026-05-09: Active → Strategic

## Reports References
- 2026-05 monthly Item 1
- (이후 update)

## Linked Issues
- Parent: ISSUE-2024-001 (AGI 한국 산업 침투, 일반)
- Related: ISSUE-2025-008 (한국 부동산·인구), ISSUE-2026-005 (한국 청년 정신건강)
- Sub-issues: (분기될 시 새 ID)

## Sources
[누적 sources list — 새 sources 추가될 때마다]

## Implications History
### Futurology
- 2026-05: [implication v1]
- 2026-06: (예정)

### Pastoral
- 2026-05: ...

### Investment
- 2026-05: ...

## Strategic Decisions Log
- 2026-05-09: 박사님 단행본 시리즈 priority 격상 결정
- 2026-05-15: 자문위원 panel 외부 expert 추가
- (이후)

## Reviews·Comments
- 박사님 코멘트
- 자문위원 코멘트
- 외부 expert 코멘트
```

### 옵션 B — Notion·Airtable DB

#### Properties (column)
- ID (string, primary)
- Title (string)
- Domain (multi-select)
- Status (single-select)
- Priority (single-select: T1·T2·T3·Wild card)
- First identified (date)
- Last updated (date)
- Reports references (relation)
- Linked issues (relation)
- Implications (rich text)
- Notes (rich text)

#### Views
- All issues
- By Status (Emerging·Active·Strategic·Wild card·Resolved)
- By Priority
- By Domain
- Recent updates
- Strategic Top 5

### 옵션 C — Git + Markdown (박사님 cmux 환경 친화)

#### 장점
- Version control (issue evolution 추적)
- grep 강력
- LLM 통합 친화 (Claude·Notion AI가 markdown 처리 우수)
- 무료·오픈소스

#### 권고 워크플로우
- 매 월간 보고서 작성 시 issue files update commit
- Branch는 *main only* (단일 source of truth)
- Tag로 보고서 release 표시 (예: `v2026-05-monthly`)

## Dashboard 인프라

### Dashboard 구조

```markdown
# Foresight Issues Dashboard

**Last Updated**: 2026-05-09

## Strategic Top 5 (T1)
| Rank | ID | Title | Last Updated | Trend |
|---|---|---|---|---|
| 1 | ISSUE-2026-001 | AGI 화이트칼라 침투 | 2026-05-09 | ↑↑ |
| 2 | ISSUE-2025-012 | 한국 기독교 인구 ≤22% | 2026-05-09 | ↑ |
| 3 | ISSUE-2026-002 | 한국 출산율 0.7 | 2026-05-09 | → |
| 4 | ISSUE-2025-008 | 부동산·인구 동시 변곡 | 2026-05-09 | ↑ |
| 5 | ISSUE-2026-003 | 한반도 지정학 | 2026-05-09 | ↑ |

## Wild Cards (Low prob × High impact)
| ID | Title | Probability | Impact |
|---|---|---|---|
| ISSUE-2024-007 | 한반도 통일 | Low | High |
| ISSUE-2025-015 | 글로벌 금융 위기 | Low | High |

## Recent Updates (지난 30일)
- ISSUE-2026-001 (2026-05-09): Strategic 격상
- ISSUE-2025-012 (2026-04-25): 통계청 자료 update
- ...

## Issues by Domain
- **AI/S&T**: 12 active issues
- **Population**: 8
- **Economy**: 7
- **Conflict**: 5
- **Spirituality**: 6
- **Energy**: 4
- **Environment**: 3
- ...

## Issues by Status
- Emerging: 15
- Active: 32
- Strategic: 5
- Wild card: 8
- Resolved: 22 (지난 1년)
- Archived: 45 (전체 누적)

## Trends·Patterns
- *Cross-domain dynamics* 식별: AGI → 인구·기독교·청년 정신건강 모두에 영향
- *Convergent inflection* 신호: 다중 한국 indicators 동시 임계 접근

## Next Cycle Priorities
[다음 월·분기·연간 priorities]
```

### Dashboard 자동 갱신
- 매 월간 보고서 생성 시 dashboard auto update
- 박사님 cmux 환경에서 cron job 또는 manual trigger

## Cross-Month Cross-Reference 자동화

### Item 7 자동 update protocol

#### Step 1 — 지난 보고서 issues list
```
이전 보고서 (2026-04 monthly)에서 *active issues*:
- ISSUE-2024-001 (AGI 한국 산업)
- ISSUE-2025-008 (부동산·인구)
- ISSUE-2025-012 (한국 기독교)
- ISSUE-2026-002 (출산율)
- ISSUE-2026-001 (AGI 화이트칼라) — Strategic 신규
```

#### Step 2 — 새 records로 업데이트
- vision-foresight-environmental-scanning-weak-signal-template DB grep
- 각 issue ID로 새 records 식별
- Status·Priority·Implications 변경 추출

#### Step 3 — Item 7 자동 생성
```markdown
## Item 7. Updates on Previously Identified Issues

### 7.1 AGI 한국 산업 침투 (ISSUE-2024-001) - update
**Status change**: Active → Strategic (Item 1로 격상)
**Update**: [본 월간 새 records 종합]
**Implications update**: [delta]

### 7.2 한국 부동산·인구 동시 변곡 (ISSUE-2025-008) - update
**Status**: Active (no change)
**Update**: [한국은행 금융안정보고서 2026 상반기 발표 — 가설 강화]
...
```

### LLM 활용 자동화
- Records → Item 7 entries: Claude prompt
- Implications delta: LLM diff
- Cross-reference 자동 link: markdown grep

## 박사님 권고 운영 protocol

### Daily
- Records 입력 (vision-foresight-environmental-scanning-weak-signal-template)

### Weekly (30분)
- 누적 records review
- 새 issue 후보 식별 → Issue ID 부여
- Active issues 새 sources update

### Monthly (4~6시간)
- 월간 보고서 생성 (vision-foresight-environmental-scanning-report)
- Issue files update
- Dashboard 갱신
- Strategic priority 재평가

### Quarterly (1~2일)
- 분기 종합 보고서 (컨텍스트별 분리 가능)
- QUEST workshop 검토 (vision-foresight-environmental-scanning-quest-workshop)
- Renfro 4-stage cycle Stage 3·4 (vision-foresight-environmental-scanning-issues-management)

### Annually (1주)
- 연간 종합 보고서
- 모든 issues review·archive
- 차년도 priority·issue id reset

## 박사님 cmux 환경 통합

### File 위치
```
~/Documents/foresight/
├── issues/                     # Issue files
├── reports/                    # Monthly·Quarterly·Annual
├── records/                    # vision-foresight-environmental-scanning-weak-signal-template DB
├── dashboard.md                # Auto-updated dashboard
├── _scripts/                   # 자동화 스크립트
│   ├── generate_monthly.sh
│   ├── update_dashboard.sh
│   └── ...
└── _templates/                 # 보고서·issue 템플릿
```

### cmux 워커 활용
- 매 월간 보고서: 자동 생성 → 박사님 review
- 매 분기·연간: 별도 worker 워크스페이스
- Records: 박사님 일상 입력

### Claude·LLM 통합
- 보고서 generation: Claude prompt (template 기반)
- Cross-reference 자동: grep + Claude
- Dashboard summary: Claude

### 백업·sync
- Git commit (매 보고서 release)
- iCloud·Google Drive backup (안정성)
- 박사님 다른 기기와 sync (cmux 워커들)

## 1년 운영 후 review·평가

### Yearly review questions
1. 식별한 issues 중 *실제 important 것*은 몇 %?
2. *놓친 issues* (event 후 후행적으로 발견)는 무엇?
3. Implications 권고가 박사님 *행동에 활용된* 비율?
4. Dashboard·Item 7 cross-reference가 박사님 의사결정에 *실제 도움*?
5. 시스템 효율성: 시간 투자 대비 산출 가치?

### 시스템 calibration
- 매년 1월: 시스템 자체 review·개선
- 분기별: 운영 protocol 미세 조정
- 자문위원 panel 의견 수렴

→ 박사님 환경 스캐닝 시스템이 *지속적으로 자기 학습·개선*하는 framework. Gordon-Glenn의 *Feedback Loop* 원칙 그대로.
