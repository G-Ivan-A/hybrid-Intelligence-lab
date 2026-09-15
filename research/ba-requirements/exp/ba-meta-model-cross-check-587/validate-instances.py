#!/usr/bin/env python3
"""Прогон эмпирических экземпляров задачи #587 через контракты пакета исполнения.

Проверяет два реальных входа (`TASK-1059`, `TASK-0975`) против `C-IN` и
собранные из них `A-BCREQ` против `C-OUT`. Замер отвечает на вопрос #587:
исполнимы ли контракты на сыром входе реальной практики, а не только на
синтетическом Golden Set.

Запуск: python3 validate-instances.py   (нужны jsonschema и pyyaml)
"""
from __future__ import annotations

import json
import pathlib
import sys

from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACTS = ROOT / (
    "projects/ba-gigacode-implementation/execution-package-mvp-bcreq/contracts"
)

CASES = [
    ("runs/bcreq-1059/a-in.json", "c-in.schema.json"),
    ("runs/bcreq-975/a-in.json", "c-in.schema.json"),
    ("runs/bcreq-1059/a-out.json", "c-out-bcreq.schema.json"),
    ("runs/bcreq-975/a-out.json", "c-out-bcreq.schema.json"),
    ("runs/bcreq-1059-routed/a-in.json", "c-in.schema.json"),
    ("runs/bcreq-1059-routed/a-out.json", "c-out-bcreq.schema.json"),
]


def main() -> int:
    failures = 0
    for instance_path, schema_name in CASES:
        instance_file = HERE / instance_path
        if not instance_file.exists():
            print(f"SKIP {instance_path}: экземпляр не собран")
            continue
        schema = json.loads((CONTRACTS / schema_name).read_text(encoding="utf-8"))
        instance = json.loads(instance_file.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda e: list(e.path),
        )
        if errors:
            failures += 1
            print(f"FAIL {instance_path} против {schema_name}:")
            for err in errors:
                where = "/".join(str(p) for p in err.path) or "<корень>"
                print(f"    {where}: {err.message}")
        else:
            print(f"PASS {instance_path} против {schema_name}")
    if failures:
        print(f"экземпляров с ошибками: {failures}")
        return 1
    print("все собранные экземпляры проходят контракты")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
