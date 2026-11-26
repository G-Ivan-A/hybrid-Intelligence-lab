#!/usr/bin/env python3
"""hub-sync.py — canonical Hub sync with a pinned revision (B-239, ADR-024).

One tool resolves the Hub revision, applies the genome in the selected scope,
validates the spoke profile with the B-238 schema and writes
`last_sync = {hub_sha, date, scope, tool}`. Spoke wrappers only pass
parameters and the exit status (see tools/hub-sync-wrapper.sh).

Subcommands
  resolve  Resolve --ref to a commit SHA (I-3) and print it.
  plan     Compute the sync plan as JSON; nothing is written.
  sync     Apply the plan transactionally and write the pin.
  verify   Read-only check of managed files against the recorded pin.

Revision (I-3): --ref takes a full 40-hex commit SHA or a Hub tag. Branches
(including `main`), HEAD-like names, revision expressions, abbreviated SHAs,
ambiguous names and unresolvable revisions are refused before any write.
A tag is resolved to its commit once; that SHA is used at every stage.

Genome: tools/hub-genome.json read from the resolved SHA. Units of the
archetype are the scope tokens: `genome` (base structure) and practices.
Files are rendered from Hub blobs with the placeholders {{date}},
{{hub_url}} and {{project_name}}; {{date}} is last_sync.date.

Scope: --scope selects the units to apply (comma- or plus-separated). The
recorded scope is the set of all managed units (previous + selected), with
`genome` first. Managed files outside the selected units must stay compatible:
their Hub source may not change, otherwise the old pin is kept and the files
are reported as `incompatible`.

Repeat sync: with the same SHA, recorded scope and tool version the recorded
date is reused, so a repeat on a clean tree changes no file, the profile
included.

Exit codes: 0 ok, 1 refused (conflict, incompatible element, failed check;
nothing changed), 2 usage, revision, profile or genome error.

See CONTRIBUTING.md («Синхронизация спицы с Хабом») and ADR-024.
"""
import argparse
import datetime
import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL_NAME = "tools/hub-sync.py"
TOOL_VERSION = "1.0.0"
TOOL_ID = f"{TOOL_NAME}@{TOOL_VERSION}"
GENOME_SPEC = "tools/hub-genome.json"
PROFILE_NAME = ".hub-profile.json"
DEFAULT_HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
BASE_UNIT = "genome"
UNIT_RE = re.compile(r"^[a-z][a-z0-9-]*$")
HEX_RE = re.compile(r"^[0-9a-fA-F]+$")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FLOATING_RE = re.compile(r"^(?:[A-Z_]*HEAD|@)$")
FORBIDDEN_REF_CHARS = set("~^:@{}*?[\\ \t\n")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
TOOLS = Path(__file__).resolve().parent

_EXTRACTION = None


class SyncError(Exception):
    """Refusal with an exit code; nothing has been written."""

    def __init__(self, message, code=2, problems=None):
        super().__init__(message)
        self.code = code
        self.problems = problems or []


def extraction():
    """spoke-extraction.py: the shared path map and manifest mechanism."""
    global _EXTRACTION
    if _EXTRACTION is None:
        _EXTRACTION = runpy.run_path(str(TOOLS / "spoke-extraction.py"))
    return _EXTRACTION


def guarded(func, *args):
    """Run a spoke-extraction helper; its die() becomes a SyncError."""
    try:
        return func(*args)
    except SystemExit as exc:
        raise SyncError("genome map error (see message above)") from exc


# ---------------------------------------------------------------- git

def git(repo, *args, binary=False, check=True):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if check and proc.returncode != 0:
        raise SyncError(f"git {' '.join(args)} failed: "
                        f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    if not check:
        return proc
    return proc.stdout if binary else proc.stdout.decode("utf-8")


def rev_commit(repo, rev):
    proc = git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
               f"{rev}^{{commit}}", check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode().strip()


def check_hub(repo):
    proc = git(repo, "rev-parse", "--git-dir", check=False)
    if proc.returncode != 0:
        raise SyncError(f"--hub {repo} is not a git repository")


def resolve_ref(repo, ref):
    """I-3: return the commit SHA for a full SHA or a tag; refuse the rest."""
    check_hub(repo)
    if not ref:
        raise SyncError("--ref is required: a full 40-hex Hub commit SHA or a Hub tag")
    if FLOATING_RE.match(ref):
        raise SyncError(f"--ref {ref!r} is a floating revision; use a commit SHA or a tag")
    if ref.startswith("-") or ".." in ref or any(ch in FORBIDDEN_REF_CHARS for ch in ref):
        raise SyncError(f"--ref {ref!r} is a revision expression; use a commit SHA or a tag")
    if len(ref) == 40 and HEX_RE.match(ref):
        sha = ref.lower()
        if rev_commit(repo, sha) != sha:
            raise SyncError(f"commit {sha} is not available in the Hub clone {repo} "
                            f"(fetch it or check the SHA)")
        return sha
    name = ref[len("refs/tags/"):] if ref.startswith("refs/tags/") else ref
    explicit_tag = name != ref
    if git(repo, "check-ref-format", f"refs/tags/{name}", check=False).returncode != 0:
        raise SyncError(f"--ref {ref!r} is not a valid tag name")
    tag = git(repo, "show-ref", "--verify", "--quiet", f"refs/tags/{name}",
              check=False).returncode == 0
    branches = [line for line in git(repo, "for-each-ref", "--format=%(refname)",
                                     "refs/heads", "refs/remotes").splitlines()
                if line in (f"refs/heads/{name}", f"refs/remotes/{name}")
                or (line.startswith("refs/remotes/") and line.split("/", 3)[-1] == name)]
    if not explicit_tag and branches:
        if tag:
            raise SyncError(f"--ref {ref!r} is ambiguous: both a tag and a branch "
                            f"({', '.join(branches)}); use the commit SHA")
        raise SyncError(f"--ref {ref!r} is a branch ({', '.join(branches)}); "
                        f"branches float, use a commit SHA or a tag")
    if not tag:
        if HEX_RE.match(name):
            raise SyncError(f"--ref {ref!r} is not a full 40-hex SHA and no such tag exists")
        raise SyncError(f"tag {name!r} is not found in the Hub clone {repo}")
    sha = rev_commit(repo, f"refs/tags/{name}")
    if not sha:
        raise SyncError(f"tag {name!r} does not point to a commit")
    return sha


def show(repo, sha, path):
    proc = git(repo, "show", f"{sha}:{path}", binary=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout


# ---------------------------------------------------------------- genome

def load_spec(repo, sha):
    data = show(repo, sha, GENOME_SPEC)
    if data is None:
        return None
    try:
        spec = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise SyncError(f"{GENOME_SPEC} at {sha}: {error}")
    check_spec(spec, sha)
    return spec


def check_spec(spec, sha):
    where = f"{GENOME_SPEC} at {sha[:12]}"
    if not isinstance(spec, dict) or not isinstance(spec.get("archetypes"), dict):
        raise SyncError(f"{where}: 'archetypes' object is required")
    placeholders = spec.get("placeholders", [])
    if not isinstance(placeholders, list) or not all(isinstance(p, str) for p in placeholders):
        raise SyncError(f"{where}: 'placeholders' must be a list of names")
    for archetype, entry in spec["archetypes"].items():
        units = entry.get("units") if isinstance(entry, dict) else None
        if not isinstance(units, dict) or BASE_UNIT not in units:
            raise SyncError(f"{where}: archetype {archetype} needs units.{BASE_UNIT}")
        if not isinstance(entry.get("profile_template"), str):
            raise SyncError(f"{where}: archetype {archetype} needs profile_template")
        for name, unit in units.items():
            if not UNIT_RE.match(name):
                raise SyncError(f"{where}: bad unit name {name!r}")
            if not isinstance(unit, dict) or not unit.get("map"):
                raise SyncError(f"{where}: unit {archetype}/{name} needs a non-empty map")
            for key in ("map", "exclude", "delegated"):
                value = unit.get(key, [])
                if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                    raise SyncError(f"{where}: unit {archetype}/{name}.{key} must be a list")


def archetype_units(spec, archetype, sha):
    entry = spec["archetypes"].get(archetype)
    if entry is None:
        raise SyncError(f"archetype {archetype!r} has no genome in {GENOME_SPEC} at {sha[:12]} "
                        f"(known: {', '.join(sorted(spec['archetypes'])) or 'none'})")
    return entry


def unit_manifest(repo, sha, unit, profile_rel):
    ex = extraction()
    maps = guarded(ex["parse_maps"], unit["map"])
    excludes = sorted(set(unit.get("exclude", [])))
    entries = guarded(ex["build_manifest"], str(repo), sha, maps, excludes)
    for entry in entries:
        if entry["mode"] not in ("100644", "100755"):
            raise SyncError(f"{entry['source']}: unsupported mode {entry['mode']} at {sha[:12]}")
        if entry["target"] == profile_rel:
            raise SyncError(f"{entry['source']} maps onto the profile {profile_rel}; "
                            f"the profile is written only by the tool")
    return entries


def genome_files(repo, sha, spec, archetype, units, profile_rel):
    """Return {target: {unit, source, blob, mode}} for the given units."""
    entry = archetype_units(spec, archetype, sha)
    files = {}
    for name in units:
        unit = entry["units"].get(name)
        if unit is None:
            continue
        for item in unit_manifest(repo, sha, unit, profile_rel):
            if item["target"] in files:
                raise SyncError(f"target collision at {sha[:12]}: {item['target']} is in units "
                                f"{files[item['target']]['unit']} and {name}")
            files[item["target"]] = dict(item, unit=name)
    return files


def delegated_paths(spec, archetype):
    entry = spec["archetypes"].get(archetype, {})
    return [path for unit in entry.get("units", {}).values() for path in unit.get("delegated", [])]


def render(repo, item, variables, placeholders, cache):
    """Expected (bytes, executable) for a manifest entry."""
    blob = item["blob"]
    if blob not in cache:
        cache[blob] = git(repo, "cat-file", "blob", blob, binary=True)
    data = cache[blob]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data, item["mode"] == "100755"
    for key in sorted(placeholders):
        if key in variables:
            text = text.replace("{{" + key + "}}", variables[key])
    return text.encode("utf-8"), item["mode"] == "100755"


# ---------------------------------------------------------------- scope and pin

def parse_units(value, what):
    tokens = [t for t in re.split(r"[+,\s]+", value or "") if t]
    if not tokens:
        raise SyncError(f"{what} is empty")
    for token in tokens:
        if not UNIT_RE.match(token):
            raise SyncError(f"{what}: bad unit {token!r}")
    return set(tokens)


def format_scope(units):
    return "+".join(sorted(units, key=lambda u: (u != BASE_UNIT, u)))


def covered(path, prefix):
    return path == prefix or (prefix.endswith("/") and path.startswith(prefix))


def deviation_for(target, deviations, delegated):
    """I-6: an owner declaration covers any path; a project declaration covers
    only paths the genome delegates explicitly. Section entries do not exempt
    whole files."""
    for entry in deviations:
        path = entry.get("path")
        if not path or not covered(target, path):
            continue
        if entry.get("declared_by") == "owner":
            return entry
        if entry.get("declared_by") == "project" and any(covered(target, d) for d in delegated):
            return entry
    return None


def today():
    value = os.environ.get("HUB_SYNC_TODAY")
    if value:
        if not DATE_RE.match(value):
            raise SyncError(f"HUB_SYNC_TODAY must be YYYY-MM-DD, got {value!r}")
        return value
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


# ---------------------------------------------------------------- profile

def profile_validator():
    try:
        module = runpy.run_path(str(TOOLS / "validate-hub-profile.py"))
    except ImportError as error:
        raise SyncError(f"B-238 validator is unavailable ({error}); install "
                        f"tools/requirements-hub-profile.txt")
    schema = json.loads(module["SCHEMA_PATH"].read_text(encoding="utf-8"))
    validator_cls = module["Draft202012Validator"]
    validator = validator_cls(schema, format_checker=validator_cls.FORMAT_CHECKER)
    return lambda path, require_pin: module["validate_profile"](path, validator, require_pin)


def dump_profile(profile):
    return (json.dumps(profile, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def check_profile_bytes(validate, data, require_pin):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / PROFILE_NAME
        path.write_bytes(data)
        return validate(path, require_pin)


def diagnostics_text(result):
    return [f"{d['code']} at /{'/'.join(map(str, d['path']))}: {d['message']}"
            for d in result.get("diagnostics", [])]


# ---------------------------------------------------------------- plan

def file_state(path):
    if not os.path.lexists(path):
        return None
    if os.path.islink(path) or not os.path.isfile(path):
        return ("not-a-file", False)
    with open(path, "rb") as handle:
        data = handle.read()
    return data, bool(os.stat(path).st_mode & 0o100)


def target_path(target, rel):
    return os.path.join(target, *rel.split("/"))


def build_plan(args, validate):
    hub = Path(args.hub)
    target = Path(args.target)
    if not target.is_dir():
        raise SyncError(f"--target {target} is not a directory")
    profile_path = Path(args.profile) if args.profile else target / PROFILE_NAME
    try:
        profile_rel = profile_path.resolve().relative_to(target.resolve()).as_posix()
    except ValueError:
        raise SyncError(f"--profile {profile_path} must lie inside --target {target}")

    sha = resolve_ref(hub, args.ref)
    spec = load_spec(hub, sha)
    if spec is None:
        raise SyncError(f"{GENOME_SPEC} is missing at {sha}; this Hub revision has no "
                        f"declared genome for the canonical sync")

    # -- current profile
    old_profile, old_profile_bytes, old_pin, migration = None, None, None, None
    if os.path.lexists(profile_path):
        old_profile_bytes = profile_path.read_bytes()
        result, code = validate(profile_path, False)
        if code != 0:
            raise SyncError(f"profile {profile_rel} is invalid; fix it before the sync",
                            problems=diagnostics_text(result))
        old_profile = json.loads(old_profile_bytes.decode("utf-8"))
        if result["pin_status"] == "pinned":
            old_pin = old_profile["last_sync"]
        elif result["pin_status"] == "migration_required":
            migration = old_profile["last_sync"]
        deviations = result["deviations"]
        archetype = old_profile["archetype"]
        if args.archetype and args.archetype != archetype:
            raise SyncError(f"--archetype {args.archetype} differs from profile archetype "
                            f"{archetype}; change the profile explicitly")
        if args.environment and args.environment != old_profile.get("environment"):
            raise SyncError(f"--environment {args.environment} differs from the profile; "
                            f"change the profile explicitly")
    else:
        if not args.archetype:
            raise SyncError(f"profile {profile_rel} is absent: pass --archetype to create the "
                            f"spoke genome")
        archetype = args.archetype
        deviations = []

    entry = archetype_units(spec, archetype, sha)
    known_units = set(entry["units"])

    # -- scope
    old_units = parse_units(old_pin["scope"], "last_sync.scope") if old_pin else set()
    selected = parse_units(args.scope, "--scope") if args.scope else (old_units or {BASE_UNIT})
    unknown = sorted(selected - known_units)
    if unknown:
        raise SyncError(f"--scope: unit(s) {', '.join(unknown)} are not in the genome of "
                        f"archetype {archetype} at {sha[:12]} "
                        f"(known: {', '.join(sorted(known_units))})")
    if not old_pin and BASE_UNIT not in selected:
        raise SyncError(f"the first canonical sync must include the base unit {BASE_UNIT!r}")
    managed = old_units | selected
    problems = []
    for unit in sorted(old_units - known_units):
        problems.append({"path": None, "unit": unit, "action": "incompatible",
                         "reason": f"managed unit {unit!r} no longer exists at {sha[:12]}"})

    # -- render variables
    hub_url = args.hub_url or (old_profile or {}).get("hub_url") or DEFAULT_HUB_URL
    project_name = (args.project_name or (old_profile or {}).get("project_name")
                    or target.resolve().name)
    scope = format_scope(managed)
    if old_pin and (old_pin["hub_sha"].lower(), old_pin["scope"], old_pin["tool"]) == \
            (sha, scope, TOOL_ID):
        date = old_pin["date"]
    else:
        date = today()
    placeholders = spec.get("placeholders", [])
    new_vars = {"date": date, "hub_url": hub_url, "project_name": project_name}

    # -- expected files: new pin and previous pin
    cache = {}
    new_files = genome_files(hub, sha, spec, archetype, sorted(managed & known_units), profile_rel)
    old_files, old_vars, old_placeholders, old_sha = {}, {}, [], None
    if old_pin:
        old_sha = old_pin["hub_sha"].lower()
        if rev_commit(hub, old_sha) != old_sha:
            raise SyncError(f"the pinned commit {old_sha} is not available in the Hub clone; "
                            f"fetch the Hub history first")
        old_spec = load_spec(hub, old_sha) or spec
        old_placeholders = old_spec.get("placeholders", [])
        old_vars = {"date": old_pin["date"],
                    "hub_url": old_profile.get("hub_url") or hub_url,
                    "project_name": old_profile.get("project_name") or project_name}
        if archetype in old_spec["archetypes"]:
            for unit in sorted(old_units):
                try:
                    old_files.update(genome_files(hub, old_sha, old_spec, archetype, [unit],
                                                  profile_rel))
                except SyncError as error:
                    print(f"hub-sync: no baseline for unit {unit} at {old_sha[:12]}: {error}",
                          file=sys.stderr)

    delegated = delegated_paths(spec, archetype)
    actions = []
    for rel in sorted(set(new_files) | set(old_files)):
        new_item, old_item = new_files.get(rel), old_files.get(rel)
        unit = (new_item or old_item)["unit"]
        in_scope = unit in selected
        new_state = render(hub, new_item, new_vars, placeholders, cache) if new_item else None
        old_state = render(hub, old_item, old_vars, old_placeholders, cache) if old_item else None
        current = file_state(target_path(target, rel))
        record = {"path": rel, "unit": unit}
        deviation = deviation_for(rel, deviations, delegated)
        if deviation is not None:
            record.update(action="keep", reason=f"deviation declared_by={deviation['declared_by']}")
        elif current == new_state:
            record.update(action="keep")
        elif current is not None and current[0] == "not-a-file":
            record.update(action="conflict", reason="target is not a regular file")
        elif not in_scope and (new_item is None or old_item is None
                               or new_item["blob"] != old_item["blob"]
                               or new_item["mode"] != old_item["mode"]):
            record.update(action="incompatible",
                          reason="Hub source changed outside the selected scope; "
                                 "select the unit or declare a deviation")
        elif current == old_state and old_state is not None:
            record.update(action="delete" if new_state is None else "update")
        elif current is None and old_state is None:
            record.update(action="create")
        elif current is None:
            record.update(action="conflict", reason="managed file was deleted locally")
        else:
            record.update(action="conflict", reason="local edits in the managed area")
        record["_new"] = new_state
        actions.append(record)
    problems += [a for a in actions if a["action"] in ("conflict", "incompatible")]

    # -- new profile
    if old_profile is not None:
        profile = json.loads(old_profile_bytes.decode("utf-8"))
    else:
        data = show(hub, sha, entry["profile_template"])
        if data is None:
            raise SyncError(f"profile template {entry['profile_template']} is missing at {sha}")
        profile = json.loads(data.decode("utf-8"))
        profile["archetype"] = archetype
        if args.environment:
            profile["environment"] = args.environment
    if migration is not None:
        history = profile.get("sync_history", [])
        if not isinstance(history, list):
            raise SyncError("profile sync_history must be a list to keep the historical record")
        profile["sync_history"] = history + [migration]
    profile["project_name"] = project_name
    profile["hub_url"] = hub_url
    profile["last_sync"] = {"hub_sha": sha, "date": date, "scope": scope, "tool": TOOL_ID}
    profile_bytes = dump_profile(profile)
    if old_profile is not None and profile == old_profile:
        profile_bytes = old_profile_bytes  # unchanged inputs: leave the file byte-identical
    result, code = check_profile_bytes(validate, profile_bytes, True)
    if code != 0:
        raise SyncError("the new profile fails the B-238 validator",
                        problems=diagnostics_text(result))

    return {
        "hub": hub, "target": target, "profile_path": profile_path,
        "profile_rel": profile_rel, "sha": sha, "scope": scope, "date": date,
        "selected": format_scope(selected), "previous_sha": old_sha,
        "actions": actions, "problems": problems, "profile_bytes": profile_bytes,
        "old_profile_bytes": old_profile_bytes, "migration": migration is not None,
        "deviations": deviations, "delegated": delegated,
    }


def report(plan, command, status):
    changes = [a for a in plan["actions"] if a["action"] in ("create", "update", "delete")]
    profile_changed = plan["profile_bytes"] != plan["old_profile_bytes"]
    return {
        "command": command,
        "status": status,
        "tool": TOOL_ID,
        "hub_sha": plan["sha"],
        "previous_hub_sha": plan["previous_sha"],
        "selected": plan["selected"],
        "scope": plan["scope"],
        "date": plan["date"],
        "migration": plan["migration"],
        "profile": plan["profile_rel"],
        "profile_changed": profile_changed and status in ("planned", "synced"),
        "changes": len(changes),
        "actions": [{k: v for k, v in a.items() if not k.startswith("_")}
                    for a in plan["actions"]],
        "problems": [{k: v for k, v in p.items() if not k.startswith("_")}
                     for p in plan["problems"]],
    }


# ---------------------------------------------------------------- apply

def write_state(path, state):
    directory = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".hub-sync-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(state[0])
        os.chmod(tmp, 0o755 if state[1] else 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.lexists(tmp):
            os.unlink(tmp)
        raise


def apply_plan(plan, validate):
    target = plan["target"]
    fail_after = os.environ.get("HUB_SYNC_FAIL_AFTER_WRITES")
    fail_after = int(fail_after) if fail_after not in (None, "") else None
    backups, created_dirs, writes = [], [], 0

    def checkpoint():
        nonlocal writes
        writes += 1
        if fail_after is not None and writes > fail_after:
            raise RuntimeError(f"simulated failure after {fail_after} write(s) "
                               f"(HUB_SYNC_FAIL_AFTER_WRITES)")

    def ensure_dir(directory):
        missing = []
        while directory and not os.path.isdir(directory):
            missing.append(directory)
            directory = os.path.dirname(directory)
        for item in reversed(missing):
            os.mkdir(item)
            created_dirs.append(item)

    try:
        for action in plan["actions"]:
            if action["action"] not in ("create", "update", "delete"):
                continue
            path = target_path(target, action["path"])
            checkpoint()
            backups.append((path, file_state(path)))
            if action["action"] == "delete":
                os.unlink(path)
            else:
                ensure_dir(os.path.dirname(path))
                write_state(path, action["_new"])
        if plan["profile_bytes"] != plan["old_profile_bytes"]:
            path = str(plan["profile_path"])
            checkpoint()
            backups.append((path, file_state(path)))
            ensure_dir(os.path.dirname(path))
            write_state(path, (plan["profile_bytes"], False))
        # post-write check: written bytes and the profile
        mismatched = [a["path"] for a in plan["actions"]
                      if a["action"] in ("create", "update", "delete")
                      and file_state(target_path(target, a["path"])) != a["_new"]]
        if mismatched:
            raise RuntimeError(f"written files differ from the genome: {', '.join(mismatched)}")
        result, code = validate(Path(plan["profile_path"]), True)
        if code != 0 or result["last_sync"] != json.loads(plan["profile_bytes"])["last_sync"]:
            raise RuntimeError("profile check failed after the write: "
                               + "; ".join(diagnostics_text(result)))
    except BaseException as error:
        for path, state in reversed(backups):
            if state is None:
                if os.path.lexists(path):
                    os.unlink(path)
            else:
                write_state(path, state)
        for directory in reversed(created_dirs):
            try:
                os.rmdir(directory)
            except OSError:
                pass
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        raise SyncError(f"sync stopped and rolled back: {error}", code=1)


# ---------------------------------------------------------------- verify

def cmd_verify(args, validate):
    target = Path(args.target)
    profile_path = Path(args.profile) if args.profile else target / PROFILE_NAME
    try:
        profile_rel = profile_path.resolve().relative_to(target.resolve()).as_posix()
    except ValueError:
        raise SyncError(f"--profile {profile_path} must lie inside --target {target}")
    if not profile_path.is_file():
        raise SyncError(f"profile {profile_rel} is absent; run the first sync")
    result, code = validate(profile_path, True)
    if code == 2:
        raise SyncError(f"profile {profile_rel} is invalid", problems=diagnostics_text(result))
    if code != 0:
        raise SyncError(f"profile {profile_rel} has no canonical pin; run the sync",
                        code=1, problems=diagnostics_text(result))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    pin = profile["last_sync"]
    sha = pin["hub_sha"].lower()
    hub = Path(args.hub)
    check_hub(hub)
    if rev_commit(hub, sha) != sha:
        raise SyncError(f"the pinned commit {sha} is not available in the Hub clone")
    spec = load_spec(hub, sha)
    if spec is None and args.genome_ref:
        spec = load_spec(hub, resolve_ref(hub, args.genome_ref))
    if spec is None:
        raise SyncError(f"{GENOME_SPEC} is missing at {sha}; pass --genome-ref with a Hub "
                        f"revision that declares the genome")
    units = parse_units(pin["scope"], "last_sync.scope")
    archetype = profile["archetype"]
    entry = archetype_units(spec, archetype, sha)
    missing = sorted(units - set(entry["units"]))
    if missing:
        raise SyncError(f"scope unit(s) {', '.join(missing)} are unknown at {sha[:12]}", code=1)
    files = genome_files(hub, sha, spec, archetype, sorted(units), profile_rel)
    variables = {"date": pin["date"],
                 "hub_url": profile.get("hub_url") or DEFAULT_HUB_URL,
                 "project_name": profile.get("project_name") or target.resolve().name}
    delegated = delegated_paths(spec, archetype)
    cache, findings = {}, []
    for rel, item in sorted(files.items()):
        if deviation_for(rel, result["deviations"], delegated):
            continue
        if file_state(target_path(target, rel)) != render(hub, item, variables,
                                                          spec.get("placeholders", []), cache):
            findings.append({"path": rel, "unit": item["unit"], "action": "drift"})
    out = {"command": "verify", "status": "ok" if not findings else "drift",
           "tool": TOOL_ID, "hub_sha": sha, "scope": pin["scope"], "files": len(files),
           "problems": findings}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if not findings else 1


# ---------------------------------------------------------------- CLI

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="hub-sync.py", description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    parser.add_argument("--version", action="version", version=TOOL_ID)
    sub = parser.add_subparsers(dest="command", required=True)

    hub_parent = argparse.ArgumentParser(add_help=False)
    hub_parent.add_argument("--hub", default=os.environ.get("HUB_SYNC_HUB"),
                            help="local clone of the Hub (default: $HUB_SYNC_HUB)")

    p = sub.add_parser("resolve", parents=[hub_parent], help="resolve --ref to a commit SHA")
    p.add_argument("--ref", required=True, help="full commit SHA or Hub tag")

    target_parent = argparse.ArgumentParser(add_help=False)
    target_parent.add_argument("--target", default=".", help="spoke root (default: .)")
    target_parent.add_argument("--profile", help="profile path (default: TARGET/.hub-profile.json)")

    for name in ("plan", "sync"):
        p = sub.add_parser(name, parents=[hub_parent, target_parent],
                           help="compute the plan" if name == "plan" else "apply and pin")
        p.add_argument("--ref", required=True, help="full commit SHA or Hub tag (I-3)")
        p.add_argument("--scope", help="units to apply, e.g. 'genome' or 'genome,practice' "
                                       "(default: managed units, or 'genome' on first sync)")
        p.add_argument("--archetype", choices=["A", "B", "C", "D"],
                       help="archetype for a spoke without a profile")
        p.add_argument("--environment", choices=["local", "gigacode", "serverless"],
                       help="environment for a spoke without a profile")
        p.add_argument("--project-name", help="value of {{project_name}} (stored in the profile)")
        p.add_argument("--hub-url", help="value of {{hub_url}} (stored in the profile)")

    p = sub.add_parser("verify", parents=[hub_parent, target_parent],
                       help="check managed files against last_sync (read-only)")
    p.add_argument("--genome-ref", help="Hub SHA or tag whose genome spec is used when the "
                                        "pinned commit predates tools/hub-genome.json")

    args = parser.parse_args(argv)
    try:
        if not args.hub:
            raise SyncError("--hub (or $HUB_SYNC_HUB) is required: a local clone of the Hub")
        if args.command == "resolve":
            print(resolve_ref(Path(args.hub), args.ref))
            return 0
        validate = profile_validator()
        if args.command == "verify":
            return cmd_verify(args, validate)
        plan = build_plan(args, validate)
        if plan["problems"]:
            print(json.dumps(report(plan, args.command, "refused"), ensure_ascii=False, indent=2))
            for problem in plan["problems"]:
                print(f"hub-sync: {problem['action']}: {problem['path'] or problem['unit']}: "
                      f"{problem['reason']}", file=sys.stderr)
            print(f"hub-sync: refused; previous pin kept, nothing written", file=sys.stderr)
            return 1
        if args.command == "sync":
            apply_plan(plan, validate)
            status = "synced"
        else:
            status = "planned"
        print(json.dumps(report(plan, args.command, status), ensure_ascii=False, indent=2))
        return 0
    except SyncError as error:
        print(f"hub-sync: {error}", file=sys.stderr)
        for problem in error.problems:
            print(f"hub-sync:   {problem}", file=sys.stderr)
        if error.code == 1:
            print("hub-sync: previous pin kept", file=sys.stderr)
        return error.code


if __name__ == "__main__":
    sys.exit(main())
