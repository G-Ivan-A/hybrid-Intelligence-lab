#!/usr/bin/env python3
"""Name availability probe for issue #717: exact-name collisions of candidate
repository names on GitHub, GitLab, Codeberg, Hugging Face, PyPI and npm.

Only public read-only APIs are queried. GitHub search needs a token in
GH_TOKEN (`GH_TOKEN=$(gh auth token)`); without it the GitHub column is skipped.

Usage: python3 -I name-availability.py [candidate ...]
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

OWNER = "G-Ivan-A"
DEFAULT = [
    "ba-ai-process", "universal-ba-ai-framework", "gra-ba-ai-framework",
    "ba-ai-framework", "ba-ai-metamodel", "ba-meta-model", "ba-ai-meta-model",
    "ba-ai-method", "ba-ai-source", "ba-ai-playbook", "ai-ba-playbooks",
    "aether-orbis-ba", "hybrid-ba-framework", "gra-ba-ai-process",
]
TOKEN = os.environ.get("GH_TOKEN", "")


def get(url, headers=None, allow=(404,)):
    req = urllib.request.Request(url, headers={"User-Agent": "hub-name-probe", **(headers or {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8") or "null"), resp.geturl()
        except urllib.error.HTTPError as exc:
            if exc.code in allow:
                return exc.code, None, url
            if exc.code in (403, 429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(20 * (attempt + 1))
                continue
            return exc.code, None, url
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            # network timeout / reset: retry, then report as status 0 (error)
            if attempt < 3:
                time.sleep(20 * (attempt + 1))
                continue
    return 0, None, url


def github(name):
    if not TOKEN:
        return {"skipped": True}
    hdr = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
    exact, contains, total = [], 0, None
    for page in (1, 2, 3):
        q = urllib.parse.quote(f"{name} in:name")
        code, data, _ = get(f"https://api.github.com/search/repositories?q={q}&per_page=100&page={page}", hdr)
        time.sleep(2.5)  # search API: 30 requests/min
        if code != 200 or not data:
            break
        total = data.get("total_count")
        for item in data.get("items", []):
            n = item["name"].lower()
            if n == name:
                exact.append(item["full_name"])
            elif name in n:
                contains += 1
        if len(data.get("items", [])) < 100:
            break
    # Own namespace: a renamed repository keeps a redirect for its old name.
    code, data, _ = get(f"https://api.github.com/repos/{OWNER}/{name}", hdr)
    own = None
    if code == 200 and data:
        own = data["full_name"] if data["full_name"].lower() != f"{OWNER}/{name}".lower() else "exists"
    return {"total_in_name": total, "exact": exact, "contains": contains, "own_namespace": own}


def gitlab(name):
    code, data, _ = get(f"https://gitlab.com/api/v4/projects?search={urllib.parse.quote(name)}&simple=true&per_page=100")
    if code != 200 or data is None:
        return {"error": code}
    exact = [p["path_with_namespace"] for p in data if p.get("path", "").lower() == name]
    return {"hits": len(data), "exact": exact}


def codeberg(name):
    code, data, _ = get(f"https://codeberg.org/api/v1/repos/search?q={urllib.parse.quote(name)}&limit=50")
    if code != 200 or not data:
        return {"error": code}
    items = data.get("data", [])
    return {"hits": len(items), "exact": [r["full_name"] for r in items if r["name"].lower() == name]}


def huggingface(name):
    out = {}
    for kind in ("models", "spaces", "datasets"):
        code, data, _ = get(f"https://huggingface.co/api/{kind}?search={urllib.parse.quote(name)}&limit=50")
        out[kind] = [d["id"] for d in (data or []) if d["id"].split("/")[-1].lower() == name]
    return out


def registry(url):
    code, _, _ = get(url)
    return {200: "taken", 404: "free"}.get(code, f"http {code}")


def main():
    names = [n.lower() for n in (sys.argv[1:] or DEFAULT)]
    rows = []
    for name in names:
        row = {
            "name": name,
            "github": github(name),
            "gitlab": gitlab(name),
            "codeberg": codeberg(name),
            "huggingface": huggingface(name),
            "pypi": registry(f"https://pypi.org/pypi/{name}/json"),
            "npm": registry(f"https://registry.npmjs.org/{name}"),
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    print()
    print("| Name | GitHub exact | GitHub `in:name` total | GitHub name contains | Own namespace | GitLab exact | Codeberg exact | HF exact | PyPI | npm |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        g = r["github"]
        hf = sum(len(v) for v in r["huggingface"].values())
        print("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["name"],
            "skipped" if g.get("skipped") else (", ".join(g["exact"]) or "0"),
            "-" if g.get("skipped") else g["total_in_name"],
            "-" if g.get("skipped") else g["contains"],
            "-" if g.get("skipped") else (g["own_namespace"] or "free"),
            ", ".join(r["gitlab"].get("exact", [])) or ("0" if "exact" in r["gitlab"] else r["gitlab"]),
            ", ".join(r["codeberg"].get("exact", [])) or ("0" if "exact" in r["codeberg"] else r["codeberg"]),
            hf, r["pypi"], r["npm"]))


if __name__ == "__main__":
    main()
