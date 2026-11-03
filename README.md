# agent-toolkit-for-ops

시스템 운영에 사용하는 **MCP 서버**와 **Skill** 모음입니다.
로컬의 Claude Code와 Codex에서 함께 사용할 수 있습니다.

## 구조

```
agent-toolkit-for-ops/
├── mcp-servers/
│   ├── common/          # 서버 간 공통 로직 (mcp-common)
│   └── <대상>/          # 대상 시스템별 MCP 서버 (예: kubernetes, prometheus)
├── skills/
│   └── <작업>/          # 운영 작업 단위 skill (예: incident-triage)
├── scripts/
│   └── mcpctl.py        # MCP 서버 로컬 등록/삭제
├── tests/               # 저장소 공통 테스트 (skill 호환성 검사 등)
└── docs/
```

## 시작하기

[uv](https://docs.astral.sh/uv/)가 필요합니다.

```sh
uv sync --all-packages   # 워크스페이스 전체 설치
uv run pytest            # 테스트
```

## MCP 서버

### 로컬 에이전트에 등록/삭제

`scripts/mcpctl.py`가 `claude mcp` / `codex mcp` CLI를 호출해 서버를 등록합니다.
Claude Code는 user scope로 등록되어 모든 프로젝트에서 사용할 수 있습니다.

```sh
uv run scripts/mcpctl.py list                 # 등록 상태 확인
uv run scripts/mcpctl.py add                  # 전체 등록
uv run scripts/mcpctl.py add kubernetes       # 특정 서버만
uv run scripts/mcpctl.py remove               # 전체 삭제
uv run scripts/mcpctl.py add --agent codex    # 특정 에이전트만
```

서버는 `uv run`으로 실행되도록 등록되므로 코드를 수정해도 다시 등록할 필요가 없습니다.
서버 폴더를 지우기 전에는 먼저 `remove` 해 주세요.

### 새 서버 추가

`mcp-servers/example`을 복사해서 시작합니다. 이름은 **연결 대상 시스템**으로 짓습니다.

| 항목 | 규칙 | 예시 |
|---|---|---|
| 폴더 | `mcp-servers/<대상>` | `mcp-servers/kubernetes` |
| 패키지 / 실행 명령 | `mcp-<대상>` | `mcp-kubernetes` |
| import 이름 | `mcp_<대상>` | `mcp_kubernetes` |
| 도구 모듈 | `tools/<기능>.py` | `tools/pods.py` |

- `server.py`는 서버 조립만 하고, 도구는 `tools/` 아래 모듈에서 `register(mcp)`로 등록합니다.
- 두 개 이상의 서버가 쓰는 로직은 `mcp-servers/common`에 둡니다.
- MCP Python SDK 2.x를 사용합니다 (`from mcp.server.mcpserver import MCPServer`).

## Skills

하나의 `SKILL.md`를 Claude Code와 Codex가 함께 사용합니다. 이름은 **작업 단위**로 짓습니다.

```
skills/<name>/
├── SKILL.md              # frontmatter: name, description
├── agents/openai.yaml    # Codex 전용 설정 (선택)
├── scripts/
└── references/
```

호환성 규칙은 `tests/test_skills.py`가 검사합니다.

- `name`: kebab-case, 64자 이하, 폴더명과 동일
- `description`: 1024자 이하
- frontmatter 키: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`

### 로컬 에이전트에 연결

```sh
ln -s "$PWD/skills/<name>" ~/.claude/skills/   # Claude Code
ln -s "$PWD/skills/<name>" ~/.agents/skills/   # Codex
```
