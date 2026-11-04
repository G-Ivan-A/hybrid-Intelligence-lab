#!/usr/bin/env python3
"""Теги архива `archive/*` для `path_migrations` (ADR-022, RFC #721 Ш4.3, issue #725).

Решение Q-5: форма архива — аннотированный тег на коммите архива
(`archive_commit` записи `path_migrations`). Решение Q-6: теги `archive/*`
защищены ruleset, запрещающим их обновление и удаление.

Подкоманды:

* `plan` — для каждой записи `path_migrations` с полями `archive` и
  `archive_commit` печатает строку `<действие>\\t<тег>\\t<коммит>`:
  `create` — тега ещё нет, `ok` — тег уже указывает на коммит архива.
  Падает, если коммит архива недоступен из HEAD (PR влит squash или rebase,
  а не merge-коммитом) или существующий тег указывает на другой коммит:
  тег архива не переписывается.
* `ruleset-check <rulesets.json> <тег>...` — по JSON-массиву подробных
  ruleset (`gh api repos/<owner>/<repo>/rulesets/<id>`) проверяет, что каждый
  тег защищён активным ruleset с целью `tag` и правилами `update` и `deletion`.
* `message <тег> <коммит>` — текст аннотации тега.

Только стандартная библиотека; данные репозитория не исполняются.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys

REQUIRED_RULES = ("update", "deletion")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def archives(root: str) -> list[dict]:
    path = os.path.join(root, ".hub-profile.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as source:
        profile = json.load(source)
    return [item for item in profile.get("path_migrations", [])
            if isinstance(item, dict) and item.get("archive") and item.get("archive_commit")]


def plan(root: str) -> int:
    errors = []
    for item in archives(root):
        tag, commit = item["archive"], item["archive_commit"]
        full = git(root, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
        if full.returncode != 0:
            errors.append(f"{tag}: archive_commit {commit} недоступен — PR влит squash или rebase, нужен merge-коммит")
            continue
        commit = full.stdout.strip()
        if git(root, "merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
            errors.append(f"{tag}: archive_commit {commit[:7]} не предок HEAD")
            continue
        existing = git(root, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}")
        if existing.returncode != 0:
            print(f"create\t{tag}\t{commit}")
        elif existing.stdout.strip() == commit:
            print(f"ok\t{tag}\t{commit}")
        else:
            errors.append(f"{tag}: тег указывает на {existing.stdout.strip()[:7]}, а не на archive_commit {commit[:7]}; тег архива не переписывается")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


def matches(ruleset: dict, ref: str) -> bool:
    names = (ruleset.get("conditions") or {}).get("ref_name") or {}
    include = names.get("include") or []
    exclude = names.get("exclude") or []
    hit = any(p == "~ALL" or fnmatch.fnmatchcase(ref, p) for p in include)
    return hit and not any(fnmatch.fnmatchcase(ref, p) for p in exclude)


def ruleset_check(path: str, tags: list[str]) -> int:
    with open(path, encoding="utf-8") as source:
        rulesets = json.load(source)
    if not isinstance(rulesets, list):
        print("ERROR: ожидается JSON-массив ruleset", file=sys.stderr)
        return 2
    failed = 0
    for tag in tags:
        ref = f"refs/tags/{tag}"
        covered: set[str] = set()
        names = []
        for ruleset in rulesets:
            if ruleset.get("target") != "tag" or ruleset.get("enforcement") != "active":
                continue
            if not matches(ruleset, ref):
                continue
            types = {rule.get("type") for rule in ruleset.get("rules") or []}
            covered |= types & set(REQUIRED_RULES)
            names.append(ruleset.get("name", "?"))
        missing = [rule for rule in REQUIRED_RULES if rule not in covered]
        if missing:
            failed += 1
            print(f"FAIL {ref}: нет активного ruleset с правилами {', '.join(missing)}")
        else:
            print(f"OK {ref}: защищён ({', '.join(names)})")
    return 1 if failed else 0


def message(tag: str, commit: str) -> int:
    print(f"""Архив домена: {tag}

Аннотированный тег архива (RFC #721, ADR-022, решение Q-5 issue #725) на коммите
{commit}. Коммит архива — последний, где выведенный домен лежит в дереве Хаба
целиком, без удалённого по мандату Q-2 и без персональных данных (Q-4).

Адрес каждого прежнего пути — манифест redirect в надгробии, запись
path_migrations в .hub-profile.json. Тег не обновляется и не удаляется (Q-6).

RFC: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/722
Issue: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/725""")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan")
    check = sub.add_parser("ruleset-check")
    check.add_argument("rulesets")
    check.add_argument("tags", nargs="+")
    msg = sub.add_parser("message")
    msg.add_argument("tag")
    msg.add_argument("commit")
    args = parser.parse_args(argv)
    if args.command == "plan":
        return plan(args.root)
    if args.command == "ruleset-check":
        return ruleset_check(args.rulesets, args.tags)
    return message(args.tag, args.commit)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
