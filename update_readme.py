import requests
from datetime import datetime
import re
from pathlib import Path

USERNAME = "zzzogi"
README_PATH = Path("README.md")


def fetch_latest_repos(username: str, limit: int = 4) -> str:
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page={limit}"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()

    lines = []
    for repo in data:
        name = repo["name"]
        html_url = repo["html_url"]
        desc = repo.get("description") or ""
        pushed = repo.get("pushed_at", "")[:10]
        lines.append(f"- [{name}]({html_url}) — {desc} *(updated: {pushed})*")
    return "\n".join(lines) if lines else "_No recent repositories found._"


def build_auto_section() -> str:
    latest_repos_md = fetch_latest_repos(USERNAME)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    block = f"""### 📰 Latest updates

<!-- AUTO_SECTION_START -->
_Last updated: **{now_str}** (UTC)_

**Latest repositories:**
{latest_repos_md}
<!-- AUTO_SECTION_END -->"""
    return block


def main():
    content = README_PATH.read_text(encoding="utf-8")

    new_block = build_auto_section()

    pattern = r"### 📰 Latest updates[\\s\\S]*?<!-- AUTO_SECTION_END -->"
    new_content = re.sub(pattern, new_block, content, flags=re.MULTILINE)

    README_PATH.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    main()
