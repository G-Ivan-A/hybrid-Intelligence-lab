#!/usr/bin/env python3
"""Manifest redirect для `path_migrations` (ADR-022, RFC #721 Ш4, issue #725).

Запись `path_migrations` в `.hub-profile.json` с полем `manifest` выводит из
дерева целый префикс: файлов под `from` больше нет, кроме надгробия `manifest`,
а адрес каждого прежнего пути записан в манифесте — таблице надгробия.

Строка манифеста:

    | `<прежний путь от корня репозитория>` | <диспозиция> | <адрес> |

Адрес — ровно один из вариантов стандарта выбытия (раздел Manifest redirect):

* SHA-ссылка на приёмник: `https://github.com/<owner>/<repo>/blob/<sha>/...`;
* ссылка на тот же путь на теге архива: `.../blob/<archive>/<прежний путь>`;
* отметка «удалён; последняя версия — `<sha>`»;
* относительная ссылка на файл, который остался в этом репозитории.

Подкоманды:

* `resolve <path>...` — код 0, если каждый путь разрешается объявленной
  миграцией: локальным `to + suffix` или строкой манифеста;
* `check` — проверяет каждую запись с полем `manifest`: надгробие с сигналом
  выбытия, единственность и адрес каждой строки, пустоту префикса в дереве и,
  если объявлен `archive_commit`, полноту манифеста по git: каждый путь под
  префиксом в коммите архива и в его первом родителе перечислен, путь с адресом
  на теге есть в коммите архива, удалённый путь в нём отсутствует; если тег уже
  существует, он указывает на `archive_commit`.

Только стандартная библиотека; данные репозитория не исполняются.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|(.*)\|\s*$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
DELETED_RE = re.compile(r"удалён; последняя версия — `([0-9a-f]{7,40})`")
SHA_URL_RE = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/(?:blob|tree)/([0-9a-f]{7,40})/\S+$")
TAG_URL_RE = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/(?:blob|tree)/(archive/[\w.-]+)/(\S+)$")
STATUS_RE = re.compile(r"^status:\s*([A-Za-z-]+)", re.M)


@dataclass
class Row:
    path: str
    line: int
    kind: str = ""  # sha | tag | deleted | local
    target: str = ""
    errors: list[str] = field(default_factory=list)


def load_profile(root: str) -> dict:
    path = os.path.join(root, ".hub-profile.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as source:
        return json.load(source)


def migrations(profile: dict) -> list[dict]:
    result = []
    for item in profile.get("path_migrations", []):
        if not isinstance(item, dict):
            continue
        old, new = item.get("from"), item.get("to")
        if isinstance(old, str) and old and isinstance(new, str) and new and old != new:
            result.append(item)
    return result


def under(path: str, prefix: str) -> str | None:
    """Суффикс пути под префиксом или None."""
    normalized = os.path.normpath(path)
    prefix_normalized = os.path.normpath(prefix)
    if normalized == prefix_normalized:
        return ""
    if normalized.startswith(prefix_normalized + os.sep):
        return normalized[len(prefix_normalized):]
    return None


def classify(row: Row, cells: str, manifest_dir: str, archive: str | None, root: str) -> None:
    found: list[tuple[str, str]] = []
    deleted = DELETED_RE.search(cells)
    if deleted:
        found.append(("deleted", deleted.group(1)))
    for link in LINK_RE.findall(cells):
        sha = SHA_URL_RE.match(link)
        tag = TAG_URL_RE.match(link)
        if tag:
            name, tag_path = tag.group(1), tag.group(2).split("#")[0]
            if archive and name != archive:
                row.errors.append(f"тег {name} не совпадает с archive {archive}")
            if tag_path != row.path:
                row.errors.append(f"путь на теге {tag_path} не совпадает с прежним путём")
            found.append(("tag", name))
        elif sha:
            found.append(("sha", link))
        elif not re.match(r"^[a-z]+:", link):
            local = os.path.normpath(os.path.join(manifest_dir, link.split("#")[0]))
            if not os.path.isfile(os.path.join(root, local)):
                row.errors.append(f"локальный адрес {link} не существует")
            found.append(("local", local))
    if len(found) != 1:
        row.errors.append(f"нужен ровно один адрес, найдено {len(found)}")
        return
    row.kind, row.target = found[0]


def parse_manifest(root: str, entry: dict) -> tuple[list[Row], list[str]]:
    manifest = entry["manifest"]
    errors: list[str] = []
    full = os.path.join(root, manifest)
    if not os.path.isfile(full):
        return [], [f"надгробие {manifest} не найдено"]
    with open(full, encoding="utf-8") as source:
        text = source.read()
    rows = []
    manifest_dir = os.path.dirname(manifest)
    for number, line in enumerate(text.splitlines(), 1):
        match = ROW_RE.match(line)
        if not match:
            continue
        row = Row(path=match.group(1).strip(), line=number)
        if under(row.path, entry["from"]) is None:
            continue
        classify(row, match.group(2), manifest_dir, entry.get("archive"), root)
        rows.append(row)
    if text.startswith("---\n"):
        frontmatter = text.split("\n---", 1)[0]
        status = STATUS_RE.search(frontmatter)
        if not status or status.group(1) not in ("deprecated", "superseded"):
            errors.append(f"{manifest}: надгробию нужен status deprecated или superseded")
    else:
        errors.append(f"{manifest}: нет frontmatter с сигналом выбытия")
    return rows, errors


def resolve(root: str, targets: list[str]) -> int:
    entries = migrations(load_profile(root))
    cache: dict[str, set[str]] = {}
    for target in targets:
        resolved = False
        for entry in entries:
            suffix = under(target, entry["from"])
            if suffix is None:
                continue
            manifest = entry.get("manifest")
            if isinstance(manifest, str) and manifest:
                if manifest not in cache:
                    rows, _ = parse_manifest(root, entry)
                    cache[manifest] = {row.path for row in rows if row.kind and not row.errors}
                if os.path.normpath(target) in cache[manifest]:
                    resolved = True
                    break
            elif not re.match(r"^[a-z]+://", entry["to"]):
                candidate = entry["to"].rstrip("/") + suffix
                if os.path.isfile(os.path.join(root, candidate)):
                    resolved = True
                    break
        if not resolved:
            return 1
    return 0


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=False)


def tree_paths(root: str, commit: str, prefix: str) -> set[str]:
    out = git(root, "ls-tree", "-r", "--name-only", commit, "--", prefix.rstrip("/"))
    return {line for line in out.stdout.splitlines() if line}


def check_entry(root: str, entry: dict) -> list[str]:
    prefix, manifest = entry["from"], entry["manifest"]
    label = f"path_migrations[{prefix}]"
    errors: list[str] = []
    if under(manifest, prefix) is None:
        errors.append(f"{label}: manifest {manifest} должен лежать под префиксом {prefix}")
    rows, manifest_errors = parse_manifest(root, entry)
    errors += [f"{label}: {e}" for e in manifest_errors]
    if not rows and not manifest_errors:
        errors.append(f"{label}: в {manifest} нет ни одной строки манифеста")
    seen: dict[str, int] = {}
    for row in rows:
        where = f"{manifest}:{row.line} `{row.path}`"
        if row.path in seen:
            errors.append(f"{label}: {where} повторяет строку {seen[row.path]}")
        seen.setdefault(row.path, row.line)
        if row.path == manifest:
            errors.append(f"{label}: {where} — надгробие не перечисляется в манифесте")
        errors += [f"{label}: {where}: {e}" for e in row.errors]
        if row.kind == "tag" and not entry.get("archive"):
            errors.append(f"{label}: {where}: адрес на теге, а поле archive не объявлено")
    # Префикс выведен из дерева: остаётся только надгробие.
    base = os.path.join(root, prefix.rstrip("/"))
    for directory, _, files in os.walk(base):
        for name in files:
            rel = os.path.relpath(os.path.join(directory, name), root)
            if rel != manifest:
                errors.append(f"{label}: {rel} остался в дереве под выведенным префиксом")
    commit = entry.get("archive_commit")
    if isinstance(commit, str) and commit:
        if git(root, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
            errors.append(
                f"{label}: archive_commit {commit} недоступен. Нужен checkout с fetch-depth: 0; "
                "если PR слит squash или rebase, коммит архива не попал в историю"
            )
            return errors
        archived = tree_paths(root, commit, prefix)
        parent = tree_paths(root, f"{commit}^1", prefix) if git(root, "cat-file", "-e", f"{commit}^1").returncode == 0 else set()
        expected = (archived | parent) - {manifest}
        listed = set(seen)
        for missing in sorted(expected - listed):
            errors.append(f"{label}: {missing} нет в манифесте {manifest}")
        for extra in sorted(listed - expected):
            errors.append(f"{label}: {extra} в манифесте, но такого пути не было под префиксом")
        for row in rows:
            if row.kind == "tag" and row.path not in archived:
                errors.append(f"{label}: {row.path} адресован на тег, но его нет в archive_commit")
            if row.kind == "deleted" and row.path in archived:
                errors.append(f"{label}: {row.path} отмечен удалённым, но попал в archive_commit")
        tag = entry.get("archive")
        if isinstance(tag, str) and tag:
            peeled = git(root, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}")
            full = git(root, "rev-parse", f"{commit}^{{commit}}").stdout.strip()
            if peeled.returncode == 0 and peeled.stdout.strip() != full:
                errors.append(f"{label}: тег {tag} указывает на {peeled.stdout.strip()[:12]}, а не на archive_commit")
    return errors


def check(root: str) -> int:
    errors: list[str] = []
    checked = 0
    for entry in migrations(load_profile(root)):
        manifest = entry.get("manifest")
        if not (isinstance(manifest, str) and manifest):
            continue
        checked += 1
        errors += check_entry(root, entry)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Path migration manifests passed ({checked} manifest(s)).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".", help="корень репозитория")
    sub = parser.add_subparsers(dest="command", required=True)
    resolve_parser = sub.add_parser("resolve")
    resolve_parser.add_argument("paths", nargs="+")
    sub.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "resolve":
        return resolve(args.root, args.paths)
    return check(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
