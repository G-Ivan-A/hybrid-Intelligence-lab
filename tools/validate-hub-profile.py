#!/usr/bin/env python3
"""Read-only validation of a Hub inheritance profile."""

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).with_name("hub-profile.schema.json")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"{value} is not a JSON value")


def diagnostic(code, path, message):
    return {"code": code, "path": path, "message": message}


def validate_profile(profile_path, validator, require_pin):
    result = {
        "pin_status": "unavailable",
        "last_sync": None,
        "deviations": [],
        "drift_ready": False,
        "diagnostics": [],
    }
    diagnostics = result["diagnostics"]
    try:
        with profile_path.open(encoding="utf-8") as source:
            profile = json.load(
                source, object_pairs_hook=unique_keys, parse_constant=invalid_constant
            )
    except (OSError, ValueError) as error:
        diagnostics.append(diagnostic("profile_invalid", [], str(error)))
        return result, 2

    invalid_profile = False
    invalid_deviations = set()
    invalid_pin = False
    for error in validator.iter_errors(profile):
        path = list(error.absolute_path)
        message = error.message
        if path[:1] == ["last_sync"]:
            code = "pin_migration_required"
            invalid_pin = True
        elif path[:1] == ["deviations"]:
            code = "deviation_invalid"
            invalid_profile = True
            if len(path) > 1:
                invalid_deviations.add(path[1])
            if error.validator == "oneOf":
                message = "declare exactly one of path or section"
        else:
            code = "profile_invalid"
            invalid_profile = True
        diagnostics.append(diagnostic(code, path, message))

    if isinstance(profile, dict):
        declarations = profile.get("deviations")
        if isinstance(declarations, list):
            result["deviations"] = [
                entry for index, entry in enumerate(declarations)
                if index not in invalid_deviations
            ]

        if invalid_pin:
            result["pin_status"] = "migration_required"
        elif "last_sync" in profile:
            result["pin_status"] = "pinned"
            result["last_sync"] = profile["last_sync"]
        else:
            result["pin_status"] = "initial"
            if require_pin:
                diagnostics.append(diagnostic(
                    "first_sync_required", ["last_sync"], "run the first Hub sync"
                ))

    result["drift_ready"] = result["pin_status"] == "pinned" and not invalid_profile
    if invalid_profile:
        return result, 2
    if require_pin and not result["drift_ready"]:
        return result, 1
    return result, 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, nargs="?", default=Path(".hub-profile.json"))
    parser.add_argument(
        "--require-pin", action="store_true", help="require a canonical pin for drift checks"
    )
    args = parser.parse_args()

    with SCHEMA_PATH.open(encoding="utf-8") as source:
        schema = json.load(source)
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    report, exit_code = validate_profile(args.profile, validator, args.require_pin)
    print(json.dumps(report, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
