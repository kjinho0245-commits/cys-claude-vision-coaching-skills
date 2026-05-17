# 설치 가이드 / Installation Guide

> **컴퓨터를 잘 모르셔도 괜찮습니다.** 한 줄 한 줄 풀어쓴 가이드입니다.
> 처음부터 끝까지 따라하시는 데 **약 10분** 걸립니다.

---

## 📋 이 가이드는 누구를 위한 것인가?

- 박사님 비전 코칭 스킬 26개를 본인 컴퓨터의 Claude Code에 처음 설치하시는 분
- 이미 설치하셨고 새 버전으로 업데이트하시는 분
- 설치 도중 문제가 생겨서 해결 방법을 찾으시는 분

**필요한 것 단 3가지**:
1. 컴퓨터 (Mac · Windows · Linux 모두 가능)
2. 인터넷 연결
3. 약 10분의 시간

---

## 🧭 단계 한눈에 보기

```
0단계  Claude Code 설치되어 있는지 확인
1단계  터미널 열기
2단계  Git이 깔려있는지 확인
3단계  패키지 내려받기 (git clone)
4단계  26개 스킬을 Claude Code에 등록
5단계  Claude Code 재시작
6단계  스킬이 작동하는지 확인
```

---

## 0단계 — Claude Code 설치 확인

**Claude Code**는 Anthropic이 만든 코딩·작업 도우미 앱입니다. 이게 깔려있어야 본 패키지를 쓸 수 있습니다.

설치 안 되어 있다면 → **[claude.com/claude-code](https://claude.com/claude-code)** 에서 본인 운영체제에 맞는 버전 다운로드 후 설치하세요.

이미 설치되어 있는지 모르겠다면:
- **Mac**: 응용 프로그램 폴더에 "Claude" 아이콘이 있는지 확인
- **Windows**: 시작 메뉴에서 "Claude" 검색

---

## 1단계 — 터미널 열기

**터미널(Terminal)**은 명령어를 입력해 컴퓨터에 일을 시키는 검은 창입니다. 이번 설치는 터미널에 몇 줄 복붙하면 끝납니다.

### Mac 사용자

1. 화면 우측 상단의 **돋보기 아이콘** 클릭 (또는 키보드 `Cmd` + `Space`)
2. 검색창에 **`터미널`** 입력 후 Enter
3. 검은 창(또는 흰 창)이 뜨면 준비 완료

### Windows 사용자

1. 시작 메뉴에서 **`PowerShell`** 검색 후 Enter
2. 또는 (권장) **Git Bash** 설치 후 Git Bash 실행
   - Git Bash는 다음 단계 Git 설치 시 함께 깔립니다

### Linux 사용자

`Ctrl` + `Alt` + `T` 또는 응용 프로그램에서 "Terminal" 실행

---

## 2단계 — Git 설치 확인

**Git**은 GitHub에서 코드·문서를 내려받는 도구입니다.

터미널에 아래 한 줄을 복사·붙여넣기 후 Enter:

```bash
git --version
```

- **`git version 2.xx.x` 같은 글이 나오면**: 설치되어 있음. 다음 단계로.
- **`command not found`나 비슷한 에러가 나오면**: Git이 없는 상태.

### Git이 없다면

- **Mac**: 터미널에 `xcode-select --install` 입력 후 Enter → 안내 따라 설치
- **Windows**: [git-scm.com/download/win](https://git-scm.com/download/win) 에서 다운로드 후 설치
  - 설치 마법사는 기본값 그대로 Next 눌러도 됩니다
  - 설치 완료 후 **Git Bash** 앱이 함께 깔립니다 (이걸 터미널로 쓰세요)
- **Linux**: `sudo apt install git` (Ubuntu/Debian) 또는 `sudo dnf install git` (Fedora)

설치 후 터미널을 한 번 닫고 다시 열어주세요.

---

## 3단계 — 패키지 내려받기

이제 GitHub에서 박사님 비전 코칭 스킬 패키지를 통째로 내려받습니다.

터미널에 **아래 두 줄을 차례로** 복붙:

```bash
cd ~
```

> `cd ~` 는 "내 홈 폴더로 이동"이라는 뜻입니다.
> 홈 폴더 위치는 Mac에서 `/Users/내이름`, Windows에서 `C:\Users\내이름` 입니다.

```bash
git clone https://github.com/idoforgod/cys-claude-vision-coaching-skills.git
```

> `git clone`은 "GitHub에서 통째로 내 컴퓨터로 복사"라는 뜻입니다.

진행 상황 표시가 잠시 흐른 뒤 명령이 끝나면 홈 폴더 안에 `cys-claude-vision-coaching-skills` 라는 새 폴더가 생깁니다.

### 확인

```bash
ls cys-claude-vision-coaching-skills
```

`README.md`, `skills`, `docs` 같은 글자가 보이면 성공.

---

## 4단계 — 26개 스킬을 Claude Code에 등록

Claude Code는 `~/.claude/skills/` 라는 약속된 폴더 안에 있는 스킬만 인식합니다. 그래서 방금 받은 26개 스킬을 그 폴더에 *등록*해야 합니다.

### Mac · Linux 사용자 (심볼릭 링크 방식 — 권장)

터미널에 **아래 한 덩어리 전체를** 통째로 복붙 후 Enter:

```bash
cd ~/cys-claude-vision-coaching-skills
mkdir -p ~/.claude/skills
for d in skills/*/; do
  name=$(basename "$d")
  ln -sf "$(pwd)/$d" ~/.claude/skills/$name
done
```

> - `cd ~/...` : 방금 내려받은 패키지 폴더로 이동
> - `mkdir -p ...` : Claude Code 스킬 폴더가 없으면 만들기
> - `for ... done` : 26개 스킬을 한꺼번에 *심볼릭 링크*로 등록
>
> **심볼릭 링크란?** 원본 폴더로 가는 *바로가기*입니다. 나중에 `git pull`로 업데이트하면 자동 반영되어 편합니다.

### Windows 사용자 (Git Bash · 복사 방식)

Windows는 심볼릭 링크 권한이 까다로워서 *복사*가 더 안전합니다. Git Bash에서:

```bash
cd ~/cys-claude-vision-coaching-skills
mkdir -p ~/.claude/skills
for d in skills/*/; do
  name=$(basename "$d")
  cp -r "$(pwd)/$d" ~/.claude/skills/$name
done
```

> 단점: 업데이트 시 같은 명령을 다시 한 번 돌려야 합니다 ([업데이트 절차](#-업데이트--updates) 참고).

### 등록 확인

```bash
ls ~/.claude/skills/ | grep vision-
```

`vision-cys-competence-visioncoding`부터 `vision-values-visioncoding`까지 **26줄**이 나오면 성공.

---

## 5단계 — Claude Code 재시작

Claude Code는 시작할 때 한 번만 스킬 목록을 읽습니다. 그래서 *완전히 종료* 후 다시 열어야 새 스킬을 인식합니다.

### 완전히 종료하는 방법

- **Mac**: Claude Code 창에서 `Cmd` + `Q` (단순 창 닫기 ❌)
- **Windows**: 작업 표시줄 아이콘 우클릭 → "닫기" 또는 `Alt` + `F4`
- **터미널에서 사용 중**: `Ctrl` + `C`로 빠져나가기

종료 후 다시 실행하세요.

---

## 6단계 — 설치 확인

Claude Code 입력창에 다음을 입력:

```
/vision-five-stages
```

박사님 비전 5단계 안내가 나오면 **설치 성공** 🎉

또 다른 스킬도 시험해 보세요:

```
/vision-cys-competence-visioncoding
```

CYS 비전 역량 진단이 시작되면 정상 작동.

---

## 🔄 업데이트 / Updates

### 이미 설치하신 분이 새 버전을 받으려면

#### Mac · Linux (심볼릭 링크로 설치한 경우)

```bash
cd ~/cys-claude-vision-coaching-skills
git pull origin main
```

이 두 줄이면 끝. 심볼릭 링크가 원본을 바라보기 때문에 *자동 반영*됩니다.

#### Windows (복사로 설치한 경우)

```bash
cd ~/cys-claude-vision-coaching-skills
git pull origin main

# 업데이트된 내용을 다시 복사
for d in skills/*/; do
  name=$(basename "$d")
  rm -rf ~/.claude/skills/$name
  cp -r "$(pwd)/$d" ~/.claude/skills/$name
done
```

업데이트 후에는 **Claude Code를 한 번 재시작**하면 새 내용이 반영됩니다.

---

## 🗑 제거 / Uninstall

전체 삭제가 필요하시면:

```bash
# 1. ~/.claude/skills/에 등록된 vision-* 스킬 모두 제거
ls ~/.claude/skills/ | grep "^vision-" | xargs -I {} rm -rf ~/.claude/skills/{}

# 2. 내려받은 패키지 폴더 제거
rm -rf ~/cys-claude-vision-coaching-skills
```

---

## 🛠 일부만 설치하고 싶다면 / Partial Install

26개 전부가 아니라 *필요한 스킬만* 골라서 설치할 수 있습니다.

### 예시 1: 진단 7종만 (자기 자신 파악용)

```bash
cd ~/cys-claude-vision-coaching-skills
SKILLS=(
  vision-cys-competence-visioncoding
  vision-mbti-visioncoding
  vision-enneagram-visioncoding
  vision-strong-visioncoding
  vision-multipleintel-visioncoding
  vision-values-visioncoding
  vision-readiness-visioncoding
)
for s in "${SKILLS[@]}"; do
  ln -sf "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

### 예시 2: 박사님 책 척추 5종만 (책 따라가기용)

```bash
cd ~/cys-claude-vision-coaching-skills
SKILLS=(
  vision-five-stages
  vision-mission-frame
  vision-statement-writer
  vision-smart-five-competence
  vision-eight-training-areas
)
for s in "${SKILLS[@]}"; do
  ln -sf "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

사용자 유형별 추천 패키지는 → **[SKILL_CATALOG.md](SKILL_CATALOG.md)**

---

## 🐛 문제 해결 / Troubleshooting

### "Claude Code에서 스킬이 안 보여요"

원인 1: **Claude Code를 완전히 종료하지 않았습니다.**
- 해결: `Cmd+Q` (Mac) 또는 `Alt+F4` (Windows)로 완전 종료 후 다시 실행

원인 2: **스킬 폴더에 제대로 등록 안 됨.**
- 확인:
  ```bash
  ls ~/.claude/skills/ | grep vision-
  ```
- 26줄이 안 나오면 4단계를 다시 실행하세요.

원인 3: **각 스킬 폴더 안에 SKILL.md가 없음.**
- 확인:
  ```bash
  ls ~/.claude/skills/vision-five-stages/SKILL.md
  ```
- 파일이 없다고 나오면 다운로드가 깨진 것. 3단계부터 다시.

### "command not found: git"

→ 2단계 Git 설치로 돌아가세요.

### "Permission denied" 또는 권한 오류

```bash
ls -la ~/.claude/skills/ | head
```
- 만약 `Permission denied`가 다시 나오면 폴더 권한 문제. 다음 명령으로 본인 소유로 복구:
  ```bash
  sudo chown -R $(whoami) ~/.claude
  ```
  Mac/Linux 사용자 비밀번호 한 번 입력.

### "심볼릭 링크가 깨졌다 (broken symlink)"

```bash
# 깨진 링크 모두 제거 후 다시 등록
find ~/.claude/skills/ -maxdepth 1 -type l ! -exec test -e {} \; -delete

cd ~/cys-claude-vision-coaching-skills
for d in skills/*/; do
  name=$(basename "$d")
  ln -sf "$(pwd)/$d" ~/.claude/skills/$name
done
```

### "git clone 시 'Repository not found'"

→ 인터넷 연결 확인. 그래도 안 되면 GitHub 주소가 바뀌었을 수 있으니 GitHub 페이지에서 최신 URL 확인.

### macOS Gatekeeper / Windows Defender 경고

본 패키지는 **Markdown 텍스트 파일만** 들어 있고 실행 코드가 없으므로 안전합니다. 보안 경고가 떠도 "허용" 후 진행하셔도 됩니다.

---

## 📚 다른 박사님 시리즈와의 연계 / Integration

### foresight-* 시리즈 (미래 예측)

박사님 본업인 미래학 도구 시리즈. 별도 패키지이며 본 패키지의 2단계(미래 예측)에서 함께 사용합니다.
- 예: `foresight-futures-wheel` — 박사님 책 미래 자극 단계 핵심 도구

### sermon-* 시리즈 (설교)

박사님 담임목사 활용 설교 도구 시리즈. 본 패키지와 별도이지만 같이 설치해도 충돌 없습니다.

---

## 💡 설치 후 다음 단계 / Next Steps

설치가 끝나면:

1. **[PHILOSOPHY.md](PHILOSOPHY.md)** — 박사님 비전 철학 먼저 읽기
2. **[SKILL_CATALOG.md](SKILL_CATALOG.md)** — 26개 스킬 카탈로그 둘러보기
3. **박사님 원서** — 『최윤식의 미래준비학교』(지식노마드, 2016, ISBN 9788993322972) 구입·정독 권장
4. **첫 스킬 실행**:
   ```
   /vision-five-stages
   ```

---

## 📞 도움말 / Help

설치가 끝까지 안 되거나 막히는 부분이 있다면:

- **GitHub Issues**: [github.com/idoforgod/cys-claude-vision-coaching-skills/issues](https://github.com/idoforgod/cys-claude-vision-coaching-skills/issues)
- **이메일**: cysinsight@gmail.com

---

*비전, 그 깊은 데로 가라. 비전, 그 행복으로 가라.*
*— 최윤식 박사, 『미래준비학교』*
