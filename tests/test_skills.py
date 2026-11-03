"""Every skill must load in both Claude Code (.claude/skills) and Codex (.agents/skills).

Both read the same SKILL.md; we enforce the stricter of the two rule sets.
"""

import re
from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).parents[1] / "skills"
SKILL_DIRS = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())

# Frontmatter keys from the Agent Skills spec that both agents accept.
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def read_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text()
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    return yaml.safe_load(text[4 : text.index("\n---", 4)]) or {}


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda d: d.name)
def test_skill_is_portable(skill_dir):
    meta = read_frontmatter(skill_dir / "SKILL.md")

    assert NAME_RE.match(meta.get("name", "")), "'name' must be kebab-case"
    assert len(meta["name"]) <= 64
    assert meta["name"] == skill_dir.name, "'name' must match folder name"
    assert 0 < len(meta.get("description", "")) <= 1024
    assert set(meta) <= PORTABLE_KEYS, f"non-portable keys: {set(meta) - PORTABLE_KEYS}"
