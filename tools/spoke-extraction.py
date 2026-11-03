#!/usr/bin/env python3
"""spoke-extraction.py — deterministic transfer of a Hub subtree into a spoke.

The tool reads the Hub *only* at a pinned commit (`--sha`, 40 hex) and never
from a floating branch. Every operation is a pure function of
(Hub repository, pinned SHA, path map), so two runs give byte-identical output,
and every copied byte can be re-verified against the Hub by git blob hash.
An agent that follows the extraction contract copies, rewrites and verifies
files by running these subcommands instead of re-typing content.

Subcommands
  manifest       Blob manifest of the mapped source paths at --sha (TSV).
  history-paths  Historical paths of the manifest files (for history import).
  materialize    Write manifest blobs into a target directory.
  rewrite-links  Rewrite relative Markdown links and in-set Hub URLs.
  scan           List remaining occurrences of renamed source prefixes.
  verify         Compare a target directory with the manifest by content hash.

Path map: --map SRC=DST, where SRC is a Hub path ending with "/" (directory)
or a file path, and DST is the target path ("" = target root). A file is
mapped by the longest matching SRC.

Exit codes: 0 ok, 1 verification or check failure, 2 usage or input error.

See ops/hub-project-extraction-contract.md (issue #717).
"""
import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
import urllib.parse

MANIFEST_HEADER = "# spoke-extraction manifest v1"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
INLINE_LINK_RE = re.compile(r"(!?\[(?:[^\[\]]|\[[^\[\]]*\])*\]\()(<[^>\n]*>|[^)\s]+)((?:\s+\"[^\"]*\")?\))")
REFDEF_RE = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(<[^>\n]*>|\S+)(.*)$")
CODE_SPAN_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")


def die(msg, code=2):
    print(f"spoke-extraction: {msg}", file=sys.stderr)
    sys.exit(code)


def git(repo, *args, binary=False):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if proc.returncode != 0:
        die(f"git {' '.join(args)} failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout if binary else proc.stdout.decode("utf-8")


def check_sha(repo, sha):
    if not SHA_RE.match(sha or ""):
        die(f"--sha must be a full 40-hex commit id, got {sha!r}")
    kind = git(repo, "cat-file", "-t", sha).strip()
    if kind != "commit":
        die(f"{sha} is a {kind}, not a commit")


def blob_hash(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ---------------------------------------------------------------- path map

def parse_maps(values):
    maps = []
    for value in values:
        if "=" not in value:
            die(f"--map needs SRC=DST, got {value!r}")
        src, dst = value.split("=", 1)
        if not src or src.startswith("/") or ".." in src.split("/"):
            die(f"bad map source {src!r}")
        if src.endswith("/") and dst and not dst.endswith("/"):
            die(f"directory map {src!r} needs a directory target ending with '/' or empty, got {dst!r}")
        if not src.endswith("/") and (not dst or dst.endswith("/")):
            die(f"file map {src!r} needs a file target, got {dst!r}")
        if dst.startswith("/") or ".." in dst.split("/"):
            die(f"bad map target {dst!r}")
        maps.append((src, dst))
    if not maps:
        die("at least one --map is required")
    # longest source first: the most specific rule wins
    return sorted(maps, key=lambda m: (-len(m[0]), m[0]))


def map_path(maps, path):
    for src, dst in maps:
        if src.endswith("/"):
            if path.startswith(src):
                return dst + path[len(src):]
        elif path == src:
            return dst
    return None


def map_dir(maps, path):
    """Map a directory path (no trailing slash) that lies inside a mapped dir."""
    probe = path.rstrip("/") + "/"
    for src, dst in maps:
        if src.endswith("/") and probe.startswith(src):
            return (dst + probe[len(src):]).rstrip("/")
    return None


def is_excluded(path, excludes):
    return any(path == e or (e.endswith("/") and path.startswith(e)) for e in excludes)


# ---------------------------------------------------------------- manifest

def build_manifest(repo, sha, maps, excludes):
    roots = sorted({src.rstrip("/") for src, _ in maps})
    out = git(repo, "ls-tree", "-r", "-z", "--full-tree", sha, "--", *roots)
    entries, seen = [], {}
    for record in out.split("\0"):
        if not record:
            continue
        meta, path = record.split("\t", 1)
        mode, kind, blob = meta.split()
        if kind != "blob":
            die(f"{path}: unsupported entry type {kind} (submodule?)")
        if is_excluded(path, excludes):
            continue
        target = map_path(maps, path)
        if target is None:
            continue
        if target in seen:
            die(f"target collision: {seen[target]} and {path} both map to {target}")
        seen[target] = path
        entries.append({"mode": mode, "blob": blob, "target": target, "source": path})
    for src, _ in maps:
        if not any(e["source"] == src or (src.endswith("/") and e["source"].startswith(src)) for e in entries):
            die(f"map source {src!r} matches no file at {sha}")
    return sorted(entries, key=lambda e: e["target"])


def write_manifest(entries, sha, maps, excludes, stream):
    stream.write(MANIFEST_HEADER + "\n")
    stream.write(f"# hub_sha: {sha}\n")
    for src, dst in sorted(maps):
        stream.write(f"# map: {src}={dst}\n")
    for e in sorted(excludes):
        stream.write(f"# exclude: {e}\n")
    stream.write(f"# files: {len(entries)}\n")
    for e in entries:
        stream.write(f"{e['mode']}\t{e['blob']}\t{e['target']}\t{e['source']}\n")


def read_manifest(path):
    sha, maps, excludes, entries = None, [], [], []
    with open(path, encoding="utf-8") as fh:
        first = fh.readline().rstrip("\n")
        if first != MANIFEST_HEADER:
            die(f"{path}: not a spoke-extraction manifest")
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("# hub_sha: "):
                sha = line[len("# hub_sha: "):]
            elif line.startswith("# map: "):
                src, dst = line[len("# map: "):].split("=", 1)
                maps.append((src, dst))
            elif line.startswith("# exclude: "):
                excludes.append(line[len("# exclude: "):])
            elif line.startswith("#") or not line:
                continue
            else:
                mode, blob, target, source = line.split("\t")
                entries.append({"mode": mode, "blob": blob, "target": target, "source": source})
    if not sha or not SHA_RE.match(sha):
        die(f"{path}: missing or invalid hub_sha")
    maps = sorted(maps, key=lambda m: (-len(m[0]), m[0]))
    return sha, maps, excludes, entries


# ---------------------------------------------------------------- links

class HubTree:
    def __init__(self, repo, sha):
        names = git(repo, "ls-tree", "-r", "-z", "--name-only", "--full-tree", sha).split("\0")
        self.files = {n for n in names if n}
        self.dirs = set()
        for name in self.files:
            parts = name.split("/")[:-1]
            for i in range(1, len(parts) + 1):
                self.dirs.add("/".join(parts[:i]))


class Rewriter:
    """Deterministic link rewrite for files moved by the path map.

    Rule L1 (Markdown only): a relative link is resolved against the file's
    Hub location. If it points into the transferred set, it becomes a relative
    link to the new location; if it points to another Hub path that exists at
    the pinned SHA, it becomes a Hub permalink at that SHA; otherwise it stays
    and is reported as unresolved.
    Rule L2 (any text file, only with --target-url): an absolute URL
    `<hub-url>/(blob|tree)/main/<path>` whose path lies in the transferred set
    becomes `<target-url>/(blob|tree)/main/<mapped path>`.
    """

    def __init__(self, tree, maps, in_set, sha, hub_url, target_url):
        self.tree, self.maps, self.in_set, self.sha = tree, maps, in_set, sha
        self.hub_url = hub_url.rstrip("/")
        self.target_url = target_url.rstrip("/") if target_url else None
        # only the floating `main` ref is rewritten: a SHA permalink stays valid
        self.url_re = re.compile(re.escape(self.hub_url) + r"/(blob|tree)/(main)/([^\s)\"'<>#?`]+)")

    def map_target(self, resolved):
        """Return (kind, new_path) for a resolved Hub path."""
        if resolved in self.in_set:
            return "file-in", map_path(self.maps, resolved)
        if resolved in self.tree.dirs or resolved == "":
            mapped = map_dir(self.maps, resolved)
            if mapped is not None:
                return "dir-in", mapped
            return "dir-out", resolved
        if resolved in self.tree.files:
            return "file-out", resolved
        return "missing", resolved

    def rewrite_target(self, raw, source, target):
        bracketed = raw.startswith("<") and raw.endswith(">")
        link = raw[1:-1] if bracketed else raw
        if not link or link.startswith("#") or SCHEME_RE.match(link) or link.startswith("//"):
            return None
        cut = min([i for i in (link.find("#"), link.find("?")) if i >= 0] or [len(link)])
        path, suffix = link[:cut], link[cut:]
        if not path:
            return None
        decoded = urllib.parse.unquote(path)
        if decoded.startswith("/"):
            resolved = posixpath.normpath(decoded.lstrip("/"))
        else:
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), decoded))
        if resolved == ".":
            resolved = ""
        if resolved.startswith("../") or resolved == "..":
            return ("outside-repo", link, None)
        kind, mapped = self.map_target(resolved)
        if kind in ("file-in", "dir-in"):
            if not decoded.startswith("/"):
                still = posixpath.normpath(posixpath.join(posixpath.dirname(target), decoded))
                if (still if still != "." else "") == (mapped or ""):
                    return None  # the link already resolves to the moved file
            base = posixpath.dirname(target) or "."
            new = posixpath.relpath(mapped or ".", base)
            if kind == "dir-in" and decoded.endswith("/") and not new.endswith("/"):
                new += "/"
            new = urllib.parse.quote(new, safe="/-_.~!$&'()*+,;=:@")
        elif kind == "file-out":
            new = f"{self.hub_url}/blob/{self.sha}/{urllib.parse.quote(resolved, safe='/-_.~')}"
        elif kind == "dir-out":
            new = f"{self.hub_url}/tree/{self.sha}/{urllib.parse.quote(resolved, safe='/-_.~')}".rstrip("/")
        else:
            return ("unresolved", link, None)
        new_link = new + suffix
        if bracketed:
            new_link = f"<{new_link}>"
        if new_link == raw:
            return None
        return (kind, raw, new_link)

    def rewrite_url(self, match):
        view, _ref, path = match.groups()
        path_dec = urllib.parse.unquote(path).rstrip("/")
        if path_dec in self.in_set:
            mapped = map_path(self.maps, path_dec)
        else:
            mapped = map_dir(self.maps, path_dec)
        if mapped is None:
            return None
        if mapped == "":
            return f"{self.target_url}/tree/main"
        return f"{self.target_url}/{view}/main/{urllib.parse.quote(mapped, safe='/-_.~')}"

    def apply(self, data, source, target):
        """Return (new_bytes, events). Non-UTF-8 content is left untouched."""
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return data, []
        events = []
        is_md = source.lower().endswith(".md")
        out_lines, in_fence = [], None
        for lineno, line in enumerate(text.split("\n"), 1):
            if is_md:
                fence = FENCE_RE.match(line)
                if in_fence:
                    if fence and fence.group(1) == in_fence:
                        in_fence = None
                    out_lines.append(self._urls(line, lineno, events))
                    continue
                if fence:
                    in_fence = fence.group(1)
                    out_lines.append(self._urls(line, lineno, events))
                    continue
                line = self._links(line, lineno, source, target, events)
            out_lines.append(self._urls(line, lineno, events))
        new = "\n".join(out_lines).encode("utf-8")
        return new, events

    def _links(self, line, lineno, source, target, events):
        spans = [(m.start(), m.end()) for m in CODE_SPAN_RE.finditer(line)]

        def in_code(pos):
            return any(a <= pos < b for a, b in spans)

        def inline(match):
            if in_code(match.start()):
                return match.group(0)
            res = self.rewrite_target(match.group(2), source, target)
            if res is None:
                return match.group(0)
            kind, old, new = res
            events.append({"line": lineno, "rule": "L1", "kind": kind, "old": old, "new": new})
            if new is None:
                return match.group(0)
            return match.group(1) + new + match.group(3)

        line = INLINE_LINK_RE.sub(inline, line)
        ref = REFDEF_RE.match(line)
        if ref and not in_code(0):
            res = self.rewrite_target(ref.group(2), source, target)
            if res is not None:
                kind, old, new = res
                events.append({"line": lineno, "rule": "L1", "kind": kind, "old": old, "new": new})
                if new is not None:
                    line = ref.group(1) + new + ref.group(3)
        return line

    def _urls(self, line, lineno, events):
        if not self.target_url or self.hub_url not in line:
            return line

        def sub(match):
            new = self.rewrite_url(match)
            if new is None or new == match.group(0):
                return match.group(0)
            events.append({"line": lineno, "rule": "L2", "kind": "url-in", "old": match.group(0), "new": new})
            return new

        return self.url_re.sub(sub, line)


def make_rewriter(args, sha, maps, entries):
    tree = HubTree(args.hub, sha)
    in_set = {e["source"] for e in entries}
    return Rewriter(tree, maps, in_set, sha, args.hub_url, args.target_url)


def expected_bytes(args, entry, rewriter):
    data = git(args.hub, "cat-file", "blob", entry["blob"], binary=True)
    if rewriter is None:
        return data, []
    return rewriter.apply(data, entry["source"], entry["target"])


# ---------------------------------------------------------------- commands

def load(args):
    sha, maps, excludes, entries = read_manifest(args.manifest)
    check_sha(args.hub, sha)
    return sha, maps, excludes, entries


def target_file(args, entry):
    return os.path.join(args.target, *entry["target"].split("/"))


def cmd_manifest(args):
    check_sha(args.hub, args.sha)
    maps = parse_maps(args.map)
    excludes = sorted(set(args.exclude or []))
    entries = build_manifest(args.hub, args.sha, maps, excludes)
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
            write_manifest(entries, args.sha, maps, excludes, fh)
    else:
        write_manifest(entries, args.sha, maps, excludes, sys.stdout)
    print(f"manifest: {len(entries)} files at {args.sha}", file=sys.stderr)


def cmd_history_paths(args):
    sha, _maps, _excludes, entries = load(args)
    current = {e["source"] for e in entries}
    tree = HubTree(args.hub, sha)
    historical, shadowed = set(), set()
    for e in entries:
        log = git(args.hub, "log", "--follow", "--name-only", "--format=", sha, "--", e["source"])
        for name in log.split("\n"):
            name = name.strip()
            if not name or name in current:
                continue
            (shadowed if name in tree.files else historical).add(name)
    for name in sorted(historical):
        print(name)
    for name in sorted(shadowed):
        print(f"shadowed (still exists at {sha[:12]}, not imported): {name}", file=sys.stderr)
    print(f"history-paths: {len(historical)} historical, {len(shadowed)} shadowed", file=sys.stderr)


def cmd_materialize(args):
    sha, _maps, _excludes, entries = load(args)
    subst = {}
    for item in args.substitute or []:
        if "=" not in item:
            die(f"--substitute needs KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        subst["{{" + key + "}}"] = value
    clashes = [e["target"] for e in entries if os.path.lexists(target_file(args, e))]
    if clashes and not args.overwrite:
        for c in clashes:
            print(f"exists: {c}", file=sys.stderr)
        die(f"{len(clashes)} target file(s) already exist; nothing written", code=1)
    leftovers = []
    for e in entries:
        data = git(args.hub, "cat-file", "blob", e["blob"], binary=True)
        if subst:
            try:
                text = data.decode("utf-8")
                for key, value in subst.items():
                    text = text.replace(key, value)
                data = text.encode("utf-8")
                leftovers += [f"{e['target']}: {m}" for m in sorted(set(re.findall(r"\{\{[a-z_]+\}\}", text)))]
            except UnicodeDecodeError:
                pass
        path = target_file(args, e)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if e["mode"] == "120000":
            die(f"{e['source']}: symlinks are not supported")
        with open(path, "wb") as fh:
            fh.write(data)
        os.chmod(path, 0o755 if e["mode"] == "100755" else 0o644)
    for item in leftovers:
        print(f"placeholder left: {item}", file=sys.stderr)
    print(f"materialize: {len(entries)} files from {sha}", file=sys.stderr)


def cmd_rewrite_links(args):
    sha, maps, _excludes, entries = load(args)
    rewriter = make_rewriter(args, sha, maps, entries)
    changed, drift, log = 0, [], []
    for e in entries:
        path = target_file(args, e)
        if not os.path.isfile(path):
            drift.append(f"missing: {e['target']}")
            continue
        with open(path, "rb") as fh:
            current = fh.read()
        new, events = expected_bytes(args, e, rewriter)
        for ev in events:
            log.append({"file": e["target"], **ev})
        if current == new:
            continue
        if blob_hash(current) != e["blob"]:
            drift.append(f"modified after import: {e['target']}")
            continue
        changed += 1
        if not args.check:
            with open(path, "wb") as fh:
                fh.write(new)
    stream = open(args.log, "w", encoding="utf-8", newline="\n") if args.log else sys.stdout
    for item in log:
        stream.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    if args.log:
        stream.close()
    kinds = {}
    for item in log:
        kinds[item["kind"]] = kinds.get(item["kind"], 0) + 1
    print(f"rewrite-links: {changed} file(s) {'to change' if args.check else 'changed'}; events {json.dumps(kinds, sort_keys=True)}", file=sys.stderr)
    for d in drift:
        print(d, file=sys.stderr)
    if drift or (args.check and changed):
        sys.exit(1)


def cmd_scan(args):
    _sha, maps, _excludes, entries = load(args)
    prefixes = sorted({src for src, dst in maps if src != dst})
    # a directory prefix is also found without its trailing slash
    # ("projects/x" in `ROOT / "projects/x"`), but not inside a longer name
    patterns = [(p, re.compile(re.escape(p.rstrip("/")) + (r"(?![\w.-])" if p.endswith("/") else r"(?![\w/.-])")))
                for p in prefixes]
    hits = 0
    for e in entries:
        path = target_file(args, e)
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as fh:
            data = fh.read()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            for prefix, pattern in patterns:
                if pattern.search(line):
                    hits += 1
                    print(f"{e['target']}:{lineno}: {prefix}: {line.strip()[:200]}")
    print(f"scan: {hits} occurrence(s) of renamed source prefixes", file=sys.stderr)


def cmd_verify(args):
    sha, maps, _excludes, entries = load(args)
    rewriter = make_rewriter(args, sha, maps, entries) if args.links else None
    missing, mismatch, mode_diff, ok = [], [], [], 0
    for e in entries:
        path = target_file(args, e)
        if not os.path.isfile(path):
            missing.append(e["target"])
            continue
        with open(path, "rb") as fh:
            current = fh.read()
        expected, _ = expected_bytes(args, e, rewriter)
        if current != expected:
            mismatch.append(e["target"])
            continue
        executable = os.access(path, os.X_OK)
        if (e["mode"] == "100755") != executable:
            mode_diff.append(e["target"])
            continue
        ok += 1
    extra = []
    if args.extra_scope is not None:
        listed = {e["target"] for e in entries}
        scope = args.extra_scope.strip("/")
        root = os.path.join(args.target, *scope.split("/")) if scope else args.target
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for name in filenames:
                rel = os.path.relpath(os.path.join(dirpath, name), args.target).replace(os.sep, "/")
                if rel not in listed:
                    extra.append(rel)
    report = {
        "hub_sha": sha,
        "mode": "links" if args.links else "verbatim",
        "files": len(entries),
        "ok": ok,
        "missing": missing,
        "mismatch": mismatch,
        "mode_mismatch": mode_diff,
        "extra": sorted(extra),
    }
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if missing or mismatch or mode_diff or extra:
        sys.exit(1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--hub", default=".", help="path to a Hub git repository (default: .)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("manifest", help="blob manifest of mapped paths at a pinned SHA")
    p.add_argument("--sha", required=True)
    p.add_argument("--map", action="append", required=True, metavar="SRC=DST")
    p.add_argument("--exclude", action="append", metavar="PATH")
    p.add_argument("--output", "-o")
    p.set_defaults(func=cmd_manifest)

    p = sub.add_parser("history-paths", help="historical paths of manifest files")
    p.add_argument("--manifest", required=True)
    p.set_defaults(func=cmd_history_paths)

    p = sub.add_parser("materialize", help="write manifest blobs into a directory")
    p.add_argument("--manifest", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--substitute", action="append", metavar="KEY=VALUE", help="replace {{KEY}} placeholders")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_materialize)

    for name, func, helptext in (
        ("rewrite-links", cmd_rewrite_links, "deterministic link rewrite"),
        ("verify", cmd_verify, "hash comparison with the manifest"),
    ):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--manifest", required=True)
        p.add_argument("--target", required=True)
        p.add_argument("--hub-url", default="https://github.com/G-Ivan-A/hybrid-Intelligence-lab")
        p.add_argument("--target-url", help="enables rule L2 (in-set absolute Hub URLs)")
        if name == "rewrite-links":
            p.add_argument("--check", action="store_true", help="report only; exit 1 if a file would change")
            p.add_argument("--log", help="write the JSONL transformation log here")
        else:
            p.add_argument("--links", action="store_true", help="expect content after rewrite-links")
            p.add_argument("--extra-scope", metavar="DIR", help="also fail on files under DIR missing from the manifest")
        p.set_defaults(func=func)

    p = sub.add_parser("scan", help="remaining occurrences of renamed source prefixes")
    p.add_argument("--manifest", required=True)
    p.add_argument("--target", required=True)
    p.set_defaults(func=cmd_scan)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
