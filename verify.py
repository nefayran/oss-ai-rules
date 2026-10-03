#!/usr/bin/env python3
"""Check every quote in table.md against the file it links to, at the commit it links to.

Each file is downloaded once from raw.githubusercontent.com into .cache/. The Deskflow wiki has no
line anchors, so its wiki repository is cloned with git and read at the linked revision.
Quotes are compared after normalising markup, so `**bold**`, list dashes and line breaks do not
count as differences. Exit status 1 when a quote is not found.
"""
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).parent
CACHE = ROOT / ".cache"
BLOB = re.compile(r"https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]{40})/([^?#]+)(?:\?plain=1)?#L(\d+)-L(\d+)")
WIKI = re.compile(r"https://github\.com/([^/]+)/([^/]+)/wiki/([^/]+)/([0-9a-f]{40})")


def norm(text: str) -> str:
    text = text.replace("**", "").replace("`", "").replace("<!--", " ").replace("-->", " ")
    text = re.sub(r"^\s*[>#-]+\s*", " ", text, flags=re.M)
    text = text.replace("- [ ]", " ").replace("[ ]", " ")
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # markdown links -> their text
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)  # reference links -> their text
    text = re.sub(r"[\[\]#>*]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def blob_lines(owner: str, repo: str, sha: str, path: str) -> list[str]:
    local = CACHE / owner / repo / sha / path
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{path}"
        with urllib.request.urlopen(url, timeout=60) as response:
            local.write_bytes(response.read())
    return local.read_text(encoding="utf-8").splitlines()


def wiki_page(owner: str, repo: str, page: str, revision: str) -> str:
    clone = CACHE / f"{owner}__{repo}.wiki"
    if not clone.exists():
        CACHE.mkdir(exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", f"https://github.com/{owner}/{repo}.wiki.git", str(clone)], check=True)
    return subprocess.run(
        ["git", "-C", str(clone), "show", f"{revision}:{page}.md"], check=True, capture_output=True, text=True
    ).stdout


def main() -> int:
    rows = [line for line in (ROOT / "table.md").read_text(encoding="utf-8").splitlines()
            if line.startswith("| ") and "github.com" in line]
    checked = problems = 0
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split(" | ")]
        if len(cells) < 5:
            print("cannot parse:", row[:80])
            problems += 1
            continue
        kinds, quote, link = cells[1], cells[2], cells[3]
        if kinds.startswith("none found"):
            continue
        if m := BLOB.match(link):
            owner, repo, sha, path, first, last = m.groups()
            source = "\n".join(blob_lines(owner, repo, sha, path)[int(first) - 1:int(last)])
        elif m := WIKI.match(link):
            source = wiki_page(*m.groups())
        else:
            print("unknown link:", link)
            problems += 1
            continue
        if quote.startswith('"'):
            quote = quote[1:quote.rfind('"')]
        source = norm(source)
        checked += 1
        for fragment in re.split(r"…| / ", quote):
            fragment = norm(fragment.strip().strip('"').strip())
            if len(fragment) >= 4 and fragment not in source:
                problems += 1
                print(f"not found at {link}\n    {fragment[:160]}\n")
    print(f"quotes checked: {checked}, problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
