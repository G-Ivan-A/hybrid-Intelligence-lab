#!/usr/bin/env python3
"""Машинный гейт G-mach пакета исполнения BCREQ для GigaCode CLI.

Гейт fail-closed: непройденная проверка останавливает маршрут. Скрипт проверяет
сам пакет (компиляция), а не отдельный прогон: словари закрыты, граф маршрута
разрешим, каждый узел-агент имеет скомпилированный навык, эталоны ссылаются на
существующие слоты и узлы, а в runtime-артефактах нет ссылок в Source.

Запуск из корня пакета либо из корня Source
https://github.com/G-Ivan-A/hybrid-Intelligence-lab:

    python3 tools/validate-package.py [путь-к-пакету] [--input путь-к-A-IN.yaml]

Зависимость: PyYAML. Пакет разворачивается копированием в спутник, поэтому
зависимость объявлена здесь, а не подразумевается: `pip install pyyaml`.
"""

from __future__ import annotations

import json
import hashlib
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - диагностика вместо трассировки
    sys.stderr.write("ERROR: требуется PyYAML: pip install pyyaml\n")
    raise SystemExit(2)

ERRORS: list[str] = []

# Служебные узлы графа: не навыки, скомпилированного SKILL.md не имеют.
PSEUDO_NODES = {"entry", "exit", "refuse", "halt"}
ORCHESTRATOR_SKILLS = {"rg-bcreq-v1-dispatcher", "ba-debug-orchestrator"}

SKILL_SECTIONS = [
    "## Когда применять",
    "## Предусловия",
    "## Шаги",
    "## Обязательные слоты выхода",
    "## Самопроверка (G-self)",
    "## Отказ",
]

# Провенанс компиляции указывает на Source
# https://github.com/G-Ivan-A/hybrid-Intelligence-lab намеренно: это
# происхождение, а не ссылка времени выполнения.
PROVENANCE_KEYS = ("derived_from:", "compiled_from:", '"compiled_from"', "source:")
HUB_PATH = re.compile(r"\b(ba-meta-model|ba-process-taxonomy|ba-operation-taxonomy|research/|standards/|ops/|docs/rfc/)")
SOURCE_ONLY_FILENAMES = {
    "00-introduction.md",
    "10-theory.md",
    "20-taxonomy.md",
    "30-decision-framework.md",
    "40-practice-and-cases.md",
    "50-open-research.md",
    "backlog.md",
    "open-questions.md",
}
MUTABLE_OUTPUT_PREFIXES = ("docs/kb/", "golden/candidates/", "meta-model/", "runs/")


def fail(message: str) -> None:
    ERRORS.append(message)


def load_yaml(root: str, rel: str):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        fail(f"отсутствует обязательный файл пакета: {rel}")
        return None
    with open(path, encoding="utf-8") as handle:
        try:
            return yaml.safe_load(handle)
        except yaml.YAMLError as error:
            fail(f"{rel}: YAML не разбирается: {error}")
            return None


def load_json(root: str, rel: str):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        fail(f"отсутствует обязательный файл пакета: {rel}")
        return None
    with open(path, encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError as error:
            fail(f"{rel}: JSON не разбирается: {error}")
            return None


def check_layout(root: str) -> None:
    """Проверяет копируемый конверт и нативные точки входа GigaCode CLI."""
    required_directories = (
        ".gigacode/skills",
        "contracts",
        "docs/kb",
        "evaluation",
        "golden",
        "meta-model",
        "routes",
        "runs",
        "taxonomy",
        "templates",
        "tools",
    )
    for rel in required_directories:
        if not os.path.isdir(os.path.join(root, rel)):
            fail(f"отсутствует обязательный каталог пакета: {rel}")

    for rel in (
        ".gitignore",
        ".gigacode/settings.example.json",
        ".gigacode/skills/rg-bcreq-v1-dispatcher/SKILL.md",
        ".gigacode/skills/ba-debug-orchestrator/SKILL.md",
        "AGENTS.md",
        "README.md",
        "docs/kb/.gitkeep",
        "meta-model/.gitkeep",
        "package-manifest.yaml",
        "runs/.gitkeep",
        "tools/validate-package.sh",
    ):
        if not os.path.isfile(os.path.join(root, rel)):
            fail(f"отсутствует обязательный файл копируемого пакета: {rel}")

    if os.path.exists(os.path.join(root, ".agents")):
        fail("legacy-каталог .agents запрещён: GigaCode CLI обнаруживает project skills только в .gigacode/skills")

    load_json(root, ".gigacode/settings.example.json")


def check_distribution_boundary(root: str) -> None:
    """Не допускает Source rationale и process-артефакты в Distribution."""
    source_only_directories = ("build/", "decisions/", "docs/rfc/", "experiments/", "ops/")
    decision_name = re.compile(r"(?:^|[-_])(adr|rfc)(?:[-_.]|$)", re.IGNORECASE)

    for current, directories, files in os.walk(root):
        rel_current = os.path.relpath(current, root).replace(os.sep, "/")
        if rel_current == ".":
            rel_current = ""
        for directory in sorted(directories):
            rel = "/".join(part for part in (rel_current, directory) if part) + "/"
            if rel.startswith(source_only_directories) or "feedback/inbox/" in rel:
                fail(f"запрещённый Source-артефакт в Distribution: {rel}")
        for filename in sorted(files):
            rel = "/".join(part for part in (rel_current, filename) if part)
            if (
                rel.startswith(source_only_directories)
                or "feedback/inbox/" in rel
                or filename in SOURCE_ONLY_FILENAMES
                or decision_name.search(filename)
            ):
                fail(f"запрещённый Source-артефакт в Distribution: {rel}")


def check_manifest(root: str) -> None:
    """Проверяет provenance и полное соответствие immutable-выходов манифесту."""
    manifest = load_yaml(root, "package-manifest.yaml") or {}
    source = manifest.get("source") or {}
    adapter = manifest.get("adapter") or {}
    inputs = manifest.get("inputs") or {}
    outputs = manifest.get("outputs") or {}

    if manifest.get("manifest") != "execution-package-gigacode-cli":
        fail("package-manifest.yaml: неизвестный идентификатор пакета")
    if not manifest.get("package_version"):
        fail("package-manifest.yaml: отсутствует package_version")
    if not re.fullmatch(r"[0-9a-f]{40}", str(source.get("revision", ""))):
        fail("package-manifest.yaml: source.revision обязан быть полным Git SHA")
    if not str(source.get("repository", "")).startswith("https://"):
        fail("package-manifest.yaml: source.repository обязан быть абсолютным HTTPS URL")
    if not adapter.get("name") or not adapter.get("version"):
        fail("package-manifest.yaml: обязательны adapter.name и adapter.version")
    if not inputs.get("allowlist"):
        fail("package-manifest.yaml: inputs.allowlist не может быть пустым")
    if outputs.get("hash_algorithm") != "sha256":
        fail("package-manifest.yaml: поддерживается только outputs.hash_algorithm=sha256")

    declared = outputs.get("hashes") or {}
    if not isinstance(declared, dict) or not declared:
        fail("package-manifest.yaml: outputs.hashes не может быть пустым")
        declared = {}

    actual: set[str] = set()
    for current, _directories, files in os.walk(root):
        for filename in files:
            path = os.path.join(current, filename)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if rel == "package-manifest.yaml" or rel == ".gigacode/settings.json":
                continue
            if rel.startswith(MUTABLE_OUTPUT_PREFIXES):
                continue
            actual.add(rel)

    declared_paths = set(declared)
    for rel in sorted(declared_paths - actual):
        fail(f"package-manifest.yaml: объявленный immutable-выход отсутствует: {rel}")
    for rel in sorted(actual - declared_paths):
        fail(f"package-manifest.yaml: immutable-выход не объявлен: {rel}")
    for rel in sorted(actual & declared_paths):
        expected = str(declared[rel])
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            fail(f"package-manifest.yaml: некорректный SHA-256 для {rel}")
            continue
        with open(os.path.join(root, rel), "rb") as handle:
            actual_hash = hashlib.sha256(handle.read()).hexdigest()
        if actual_hash != expected:
            fail(f"package-manifest.yaml: SHA-256 не совпадает для {rel}")


def frontmatter(path: str) -> dict[str, str]:
    """Читает frontmatter построчно, как валидатор Source-репозитория."""
    fields: dict[str, str] = {}
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([a-z_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def check_taxonomies(root: str) -> dict:
    loaded = {}
    for name in (
        "artifacts",
        "operations",
        "processes",
        "products",
        "mango-products",
        "telecom-products",
        "source-tiers",
        "projections",
        "domain-glossary",
    ):
        data = load_yaml(root, f"taxonomy/{name}.yaml")
        loaded[name] = data
        if data is None:
            continue
        if name != "domain-glossary" and data.get("closed") is not True:
            fail(f"taxonomy/{name}.yaml: словарь среза обязан быть закрытым (closed: true)")

    operations = loaded.get("operations") or {}
    items = operations.get("items") or []
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    pattern = re.compile(r"^OP-(EXT|TRN|GEN|CHK|ASM)-\d{2}$")
    for item in items:
        op_id = item.get("id", "")
        if not pattern.match(op_id):
            fail(f"taxonomy/operations.yaml: идентификатор вне формата OP-(EXT|TRN|GEN|CHK|ASM)-NN: {op_id!r}")
        if op_id in seen_ids:
            fail(f"taxonomy/operations.yaml: повторяющийся идентификатор операции: {op_id}")
        seen_ids.add(op_id)
        slug = item.get("slug")
        if slug in seen_slugs:
            fail(f"taxonomy/operations.yaml: повторяющийся slug операции: {slug}")
        seen_slugs.add(slug)
        if not item.get("refusal"):
            fail(f"{op_id}: условие отказа обязательно и пустым не бывает")

    processes = loaded.get("processes") or {}
    for skill in processes.get("l3") or []:
        if not skill.get("in_slice"):
            continue
        for slug in skill.get("operations") or []:
            if slug not in seen_slugs:
                fail(f"taxonomy/processes.yaml: навык {skill.get('id')} ссылается на операцию вне словаря: {slug}")

    artifacts = loaded.get("artifacts") or {}
    for item in artifacts.get("items") or []:
        schema = item.get("schema")
        if schema and not os.path.isfile(os.path.join(root, schema)):
            fail(f"taxonomy/artifacts.yaml: {item.get('id')} ссылается на несуществующую схему {schema}")

    check_product_taxonomies(
        loaded.get("mango-products") or {},
        loaded.get("telecom-products") or {},
    )
    return loaded


def check_product_taxonomies(mango: dict, telecom: dict) -> None:
    """Проверяет полный snapshot MANGO и взаимно-однозначное отраслевое покрытие."""
    if mango.get("taxonomy") != "mango-products":
        fail("taxonomy/mango-products.yaml: неизвестный идентификатор таксономии")
    if telecom.get("taxonomy") != "telecom-products":
        fail("taxonomy/telecom-products.yaml: неизвестный идентификатор таксономии")

    for rel, data in (
        ("taxonomy/mango-products.yaml", mango),
        ("taxonomy/telecom-products.yaml", telecom),
    ):
        provenance = data.get("provenance") or {}
        if not str(provenance.get("compiled_from", "")).startswith("https://"):
            fail(f"{rel}: provenance.compiled_from обязан быть абсолютным HTTPS URL")
        if not re.fullmatch(r"[0-9a-f]{40}", str(provenance.get("source_revision", ""))):
            fail(f"{rel}: provenance.source_revision обязан быть полным Git SHA")

    if (mango.get("provenance") or {}).get("compiled_from") != (
        telecom.get("provenance") or {}
    ).get("compiled_from"):
        fail("product taxonomies: MANGO snapshot и отраслевые соответствия скомпилированы из разных источников")

    domains = mango.get("domains") or []
    if len(domains) != 8:
        fail(f"taxonomy/mango-products.yaml: ожидается 8 доменов snapshot v3.0, получено {len(domains)}")

    domain_ids: set[str] = set()
    capabilities: dict[str, int] = {}
    for domain in domains:
        domain_id = str(domain.get("id", ""))
        if not domain_id or domain_id in domain_ids:
            fail(f"taxonomy/mango-products.yaml: пустой или повторяющийся domain id: {domain_id!r}")
        domain_ids.add(domain_id)
        if not domain.get("name"):
            fail(f"taxonomy/mango-products.yaml: домен {domain_id!r} без имени")

        for capability in domain.get("capabilities") or []:
            capability_id = str(capability.get("id", ""))
            path = f"{domain_id}/{capability_id}"
            if not capability_id or path in capabilities:
                fail(f"taxonomy/mango-products.yaml: пустая или повторяющаяся capability: {path!r}")
                continue
            source_row = capability.get("source_row")
            if not isinstance(source_row, int) or source_row < 1:
                fail(f"taxonomy/mango-products.yaml: {path} без валидного source_row")
                continue
            capabilities[path] = source_row
            if not capability.get("name") or not capability.get("features"):
                fail(f"taxonomy/mango-products.yaml: {path} не содержит имя или features")
            atomic_functions = capability.get("atomic_functions") or []
            if not atomic_functions:
                fail(f"taxonomy/mango-products.yaml: {path} не содержит atomic functions")
            atomic_ids: set[str] = set()
            for atomic in atomic_functions:
                atomic_id = str(atomic.get("id", ""))
                if not atomic_id or atomic_id in atomic_ids:
                    fail(f"taxonomy/mango-products.yaml: {path} содержит пустую или повторяющуюся atomic function")
                atomic_ids.add(atomic_id)
                if not atomic.get("parameters"):
                    fail(f"taxonomy/mango-products.yaml: {path}/{atomic_id} не содержит parameters")

    if len(capabilities) != 42:
        fail(
            "taxonomy/mango-products.yaml: ожидается 42 capabilities snapshot v3.0, "
            f"получено {len(capabilities)}"
        )

    mappings: dict[str, dict] = {}
    for mapping in telecom.get("mappings") or []:
        path = str(mapping.get("mango_capability", ""))
        if not path or path in mappings:
            fail(f"taxonomy/telecom-products.yaml: пустое или повторяющееся соответствие: {path!r}")
            continue
        mappings[path] = mapping
        for field in ("product_or_service", "tm_forum", "unspsc", "babok"):
            if not mapping.get(field):
                fail(f"taxonomy/telecom-products.yaml: {path} не содержит поле {field}")

    for path in sorted(set(capabilities) - set(mappings)):
        fail(f"taxonomy/telecom-products.yaml: для MANGO capability {path} нет отраслевого соответствия")
    for path in sorted(set(mappings) - set(capabilities)):
        fail(f"taxonomy/telecom-products.yaml: соответствие ссылается на неизвестную MANGO capability: {path}")
    for path in sorted(set(capabilities) & set(mappings)):
        if mappings[path].get("source_row") != capabilities[path]:
            fail(f"taxonomy/telecom-products.yaml: source_row расходится для {path}")

    frameworks = {item.get("id"): item for item in telecom.get("frameworks") or []}
    for framework_id in ("tm-forum", "unspsc", "babok-v3"):
        framework = frameworks.get(framework_id) or {}
        if not str(framework.get("url", "")).startswith("https://"):
            fail(f"taxonomy/telecom-products.yaml: framework {framework_id} не содержит абсолютный HTTPS URL")


def canonical_product_digest(products: list[dict]) -> str:
    """Возвращает переносимый digest подтверждённого продуктового реестра."""
    payload = json.dumps(products, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def product_binding_errors(document: dict, mango: dict, routing: dict) -> list[str]:
    """Проверяет подтверждённую привязку без фиксированного перечня доменов."""
    errors: list[str] = []
    products = document.get("products") or []
    attribution = document.get("product_attribution") or {}
    if attribution.get("status") != "confirmed":
        errors.append("product_attribution.status обязан быть confirmed")
    for field in ("confirmed_by", "confirmed_at", "decision_ref", "binding_digest"):
        if not attribution.get(field):
            errors.append(f"product_attribution.{field} обязателен после G-human")
    if not products:
        errors.append("подтверждённый реестр products не может быть пустым")

    profiles = {item.get("id") for item in routing.get("profiles") or []}
    domains = {item.get("id"): item for item in mango.get("domains") or []}
    markers: set[str] = set()
    required = {"marker", "domain", "capability", "feature", "atomic_function", "profile", "owner"}
    for number, product in enumerate(products, start=1):
        missing = required - set(product)
        if missing:
            errors.append(f"products[{number}]: неполная цепочка, отсутствуют {sorted(missing)}")
            continue
        marker = product.get("marker")
        if marker in markers:
            errors.append(f"products[{number}]: marker {marker!r} повторяется")
        markers.add(marker)
        if product.get("profile") not in profiles:
            errors.append(f"products[{number}]: неизвестный profile {product.get('profile')!r}")

        domain = domains.get(product.get("domain"))
        if domain is None:
            errors.append(f"products[{number}]: domain {product.get('domain')!r} отсутствует в MANGO taxonomy")
            continue
        capabilities = {item.get("id"): item for item in domain.get("capabilities") or []}
        capability = capabilities.get(product.get("capability"))
        if capability is None:
            errors.append(
                f"products[{number}]: capability {product.get('capability')!r} не принадлежит domain {product.get('domain')!r}"
            )
            continue
        if product.get("feature") not in (capability.get("features") or []):
            errors.append(
                f"products[{number}]: feature {product.get('feature')!r} не принадлежит capability {product.get('capability')!r}"
            )
        atomic = {item.get("id") for item in capability.get("atomic_functions") or []}
        if product.get("atomic_function") not in atomic:
            errors.append(
                f"products[{number}]: atomic_function {product.get('atomic_function')!r} не принадлежит capability {product.get('capability')!r}"
            )

    digest = attribution.get("binding_digest")
    if products and digest and digest != canonical_product_digest(products):
        errors.append("product_attribution.binding_digest не совпадает с каноническим products")
    return errors


def check_product_routing(root: str, taxonomies: dict, skills: dict, graph: dict) -> None:
    """Связывает ранний Human Gate, полный MANGO-каталог и downstream-контракты."""
    routing = taxonomies.get("products") or {}
    attribution = routing.get("attribution") or {}
    if routing.get("scope") != "mango-portfolio":
        fail("taxonomy/products.yaml: scope обязан однозначно означать весь портфель MANGO")
    if routing.get("catalog") != "taxonomy/mango-products.yaml":
        fail("taxonomy/products.yaml: каталог маршрутизации обязан ссылаться на полный MANGO snapshot")
    if routing.get("classes"):
        fail("taxonomy/products.yaml: статический перечень product classes запрещён")
    if attribution.get("node") != "n0" or attribution.get("confirmation_gate") != "G-human":
        fail("taxonomy/products.yaml: продуктовая атрибуция обязана подтверждаться G-human в n0")
    if set(attribution.get("propagation_fields") or []) != {"products", "product_attribution"}:
        fail("taxonomy/products.yaml: propagation_fields обязаны включать products и product_attribution")

    entry_targets = [
        edge.get("to")
        for edge in graph.get("edges") or []
        if edge.get("from") == "entry" and edge.get("to") != "refuse"
    ]
    if entry_targets != ["n0"]:
        fail("routes/rg-bcreq-v1.yaml: n0 обязан быть единственным рабочим переходом из entry")
    n0 = next((node for node in graph.get("nodes") or [] if node.get("node") == "n0"), {})
    if n0.get("skill") != "SK-product-attribution" or "G-human" not in (n0.get("gates") or []):
        fail("routes/rg-bcreq-v1.yaml: n0 обязан исполнять SK-product-attribution с G-human")

    for name, fields in skills.items():
        if fields.get("product_class"):
            fail(f".gigacode/skills/{name}/SKILL.md: статическая product_class запрещена")

    expected_fields = {"marker", "domain", "capability", "feature", "atomic_function", "profile", "owner"}
    for schema_name in ("c-in", "c-core", "c-quest", "c-out-bcreq", "c-rk"):
        schema = load_json(root, f"contracts/{schema_name}.schema.json") or {}
        required = set(schema.get("required") or [])
        if not {"products", "product_attribution"}.issubset(required):
            fail(f"contracts/{schema_name}.schema.json: подтверждённая привязка не является обязательной")
        if schema_name == "c-core":
            product_schema = (schema.get("definitions") or {}).get("product") or {}
        else:
            product_schema = (((schema.get("properties") or {}).get("products") or {}).get("items") or {})
            if "$ref" in product_schema:
                ref_name = product_schema["$ref"].rsplit("/", 1)[-1]
                product_schema = (schema.get("definitions") or {}).get(ref_name) or {}
        if not expected_fields.issubset(set(product_schema.get("required") or [])):
            fail(f"contracts/{schema_name}.schema.json: полная продуктовая цепочка не обязательна")


def load_input_document(path: str):
    if not os.path.isfile(path):
        fail(f"A-IN отсутствует: {path}")
        return {}
    with open(path, encoding="utf-8") as handle:
        try:
            data = yaml.safe_load(handle)
        except yaml.YAMLError as error:
            fail(f"A-IN не разбирается как YAML/JSON: {error}")
            return {}
    if not isinstance(data, dict):
        fail("A-IN обязан быть объектом")
        return {}
    return data


def check_skills(root: str) -> dict[str, dict]:
    skills_dir = os.path.join(root, ".gigacode", "skills")
    compiled: dict[str, dict] = {}
    if not os.path.isdir(skills_dir):
        fail("отсутствует каталог .gigacode/skills: пакет не разворачивается в спутник копированием")
        return compiled
    for entry in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, entry, "SKILL.md")
        rel = f".gigacode/skills/{entry}/SKILL.md"
        if not os.path.isfile(path):
            fail(f"каталог навыка без SKILL.md: .gigacode/skills/{entry}")
            continue
        fields = frontmatter(path)
        for required in ("name", "description", "packs", "inputs", "outputs", "contracts", "gates", "compiled_from", "derived_from"):
            if not fields.get(required):
                fail(f"{rel}: обязательное поле frontmatter отсутствует или пусто: {required}")
        if fields.get("name") != entry:
            fail(f"{rel}: поле name ({fields.get('name')!r}) не совпадает с именем каталога ({entry!r})")
        if fields.get("name") in compiled:
            fail(f"{rel}: имя навыка не уникально: {fields.get('name')}")
        if entry in ORCHESTRATOR_SKILLS and fields.get("disable-model-invocation") != "true":
            fail(f"{rel}: оркестратор обязан запускаться только явно (disable-model-invocation: true)")
        body = open(path, encoding="utf-8").read()
        for section in SKILL_SECTIONS:
            if f"\n{section}\n" not in body:
                fail(f"{rel}: отсутствует обязательный раздел {section}")
        for dropped in ("prompts/", "runs/"):
            if dropped in fields.get("derived_from", ""):
                fail(f"{rel}: слой {dropped} отброшен компиляцией и в derived_from попадать не должен")
        compiled[entry] = fields
    return compiled


def check_route(root: str, processes: dict, skills: dict[str, dict]) -> dict:
    graph = load_yaml(root, "routes/rg-bcreq-v1.yaml") or {}
    nodes = graph.get("nodes") or []
    l2_ids = {item.get("id") for item in (processes or {}).get("l2") or []}
    declared = {item.get("id") for item in (processes or {}).get("l2") or [] if item.get("in_slice")}

    for process in graph.get("processes") or []:
        if process not in l2_ids:
            fail(f"routes/rg-bcreq-v1.yaml: процесс вне закрытого словаря: {process}")
        elif process not in declared:
            fail(f"routes/rg-bcreq-v1.yaml: процесс {process} не объявлен входящим в срез (in_slice)")

    # Навык узла записан идентификатором таксономии (SK-*), навык на диске —
    # именем каталога. Связь задаётся полем packs скомпилированного навыка.
    by_pack = {}
    for name, fields in skills.items():
        pack = fields.get("packs", "")
        if "/" in pack:
            by_pack[pack.split("/", 1)[1]] = name

    node_ids: set[str] = set()
    for node in nodes:
        node_id = node.get("node")
        if node_id in node_ids:
            fail(f"routes/rg-bcreq-v1.yaml: повторяющийся узел {node_id}")
        node_ids.add(node_id)
        if node.get("process") not in l2_ids:
            fail(f"{node_id}: процесс узла вне закрытого словаря: {node.get('process')}")
        if not node.get("gates"):
            fail(f"{node_id}: узел без гейта запрещён")
        actor = node.get("actor")
        if actor == "agent":
            if node.get("skill") not in by_pack:
                fail(f"{node_id}: узел-агент ссылается на навык без скомпилированного SKILL.md: {node.get('skill')}")
        elif actor == "human":
            if not node.get("note"):
                fail(f"{node_id}: человеческий узел обязан нести основание, почему навык не скомпилирован")
        else:
            fail(f"{node_id}: actor обязан быть agent или human, получено {actor!r}")

    known = node_ids | PSEUDO_NODES
    outgoing: set[str] = set()
    reachable = {"entry"}
    edges = graph.get("edges") or []
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        for endpoint in (source, target):
            if endpoint not in known:
                fail(f"routes/rg-bcreq-v1.yaml: ребро ссылается на неизвестный узел: {endpoint}")
        if not edge.get("condition"):
            fail(f"ребро {source} → {target}: условие перехода обязательно (ребро «по усмотрению» запрещено)")
        outgoing.add(source)

    changed = True
    while changed:
        changed = False
        for edge in edges:
            if edge.get("from") in reachable and edge.get("to") not in reachable:
                reachable.add(edge.get("to"))
                changed = True
    for node_id in sorted(node_ids):
        if node_id not in reachable:
            fail(f"{node_id}: узел недостижим из entry")
        if node_id not in outgoing:
            fail(f"{node_id}: у узла нет исходящего ребра, траектория обрывается")

    policy = graph.get("gate_policy") or {}
    if policy.get("fail_closed") is not True:
        fail("routes/rg-bcreq-v1.yaml: gate_policy.fail_closed обязан быть true")
    if policy.get("corrective_attempts") != 0:
        fail("routes/rg-bcreq-v1.yaml: автоматические корректирующие попытки запрещены")
    if policy.get("on_reject") != "halt_and_request_human":
        fail("routes/rg-bcreq-v1.yaml: reject обязан останавливать маршрут и возвращать решение человеку")
    trace_required = set((graph.get("trace") or {}).get("required") or [])
    if not trace_required:
        fail("routes/rg-bcreq-v1.yaml: состав обязательного следа не объявлен")
    required_event_fields = {"seq", "at", "event_type", "actor", "input_ref", "output_ref"}
    if not required_event_fields.issubset(trace_required):
        fail("routes/rg-bcreq-v1.yaml: trace не задаёт обязательный микро-событийный след")
    schema = load_json(root, "contracts/c-rk.schema.json") or {}
    event_properties = set(
        (((schema.get("properties") or {}).get("events") or {}).get("items") or {}).get("properties") or {}
    )
    unknown_trace_fields = trace_required - event_properties
    if unknown_trace_fields:
        fail(
            "routes/rg-bcreq-v1.yaml: trace требует поля вне C-RK: "
            + ", ".join(sorted(unknown_trace_fields))
        )
    return graph


def check_run_contract(root: str) -> None:
    """Проверяет, что исполняемый run-sheet не расходится со своей JSON Schema."""
    schema = load_json(root, "contracts/c-rk.schema.json") or {}
    template = load_yaml(root, "routes/run-sheet-template.yaml") or {}

    properties = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    missing = required - set(template)
    unknown = set(template) - set(properties)
    if missing:
        fail(f"routes/run-sheet-template.yaml: отсутствуют обязательные поля C-RK: {sorted(missing)}")
    if unknown:
        fail(f"routes/run-sheet-template.yaml: поля вне C-RK: {sorted(unknown)}")

    event_schema = ((properties.get("events") or {}).get("items") or {})
    event_properties = set(event_schema.get("properties") or {})
    event_required = set(event_schema.get("required") or [])
    for number, event in enumerate(template.get("events") or [], start=1):
        missing = event_required - set(event)
        unknown = set(event) - event_properties
        if missing:
            fail(f"routes/run-sheet-template.yaml: event {number} без обязательных полей C-RK: {sorted(missing)}")
        if unknown:
            fail(f"routes/run-sheet-template.yaml: event {number} содержит поля вне C-RK: {sorted(unknown)}")

    handover_schema = properties.get("handover") or {}
    handover = template.get("handover") or {}
    handover_required = set(handover_schema.get("required") or [])
    handover_properties = set(handover_schema.get("properties") or {})
    missing = handover_required - set(handover)
    unknown = set(handover) - handover_properties
    if missing:
        fail(f"routes/run-sheet-template.yaml: handover без обязательных полей C-RK: {sorted(missing)}")
    if unknown:
        fail(f"routes/run-sheet-template.yaml: handover содержит поля вне C-RK: {sorted(unknown)}")


def check_golden(root: str, graph: dict, skills: dict, glossary: dict) -> None:
    schema = load_json(root, "contracts/c-out-bcreq.schema.json") or {}
    slots = set(((schema.get("properties") or {}).get("slots") or {}).get("required") or [])
    cases = load_yaml(root, "golden/cases.yaml") or {}
    node_ids = {node.get("node") for node in graph.get("nodes") or []}
    terms = {term.get("id") for term in (glossary or {}).get("terms") or []}

    case_list = cases.get("cases") or []
    kinds = {case.get("kind") for case in case_list}
    if "positive" not in kinds or "negative" not in kinds:
        fail("golden/cases.yaml: минимальный Golden Set обязан содержать и положительный, и отрицательный случай")

    for case in case_list:
        case_id = case.get("id")
        rel = case.get("file", "")
        if not os.path.isfile(os.path.join(root, rel)):
            fail(f"{case_id}: файл эталона отсутствует: {rel}")
        expect = case.get("expect") or {}
        if case.get("kind") == "positive":
            filled = set(expect.get("filled") or [])
            empty = set((expect.get("empty_with_reason") or {}).keys())
            unknown = (filled | empty) - slots
            if unknown:
                fail(f"{case_id}: слоты вне закрытого перечня контракта: {sorted(unknown)}")
            missing = slots - filled - empty
            if missing:
                fail(f"{case_id}: слот не объявлен ни заполненным, ни пустым с причиной: {sorted(missing)}")
            overlap = filled & empty
            if overlap:
                fail(f"{case_id}: слот объявлен одновременно заполненным и пустым: {sorted(overlap)}")
            if not expect.get("trace_nonempty"):
                fail(f"{case_id}: положительный эталон без требования непустого следа")
        else:
            if expect.get("outcome") != "refused":
                fail(f"{case_id}: отрицательный эталон обязан ожидать отказ")
            if expect.get("refusing_node") not in node_ids:
                fail(f"{case_id}: отказывающий узел вне графа маршрута: {expect.get('refusing_node')}")
            if expect.get("refusing_skill") not in skills:
                fail(f"{case_id}: отказывающий навык не скомпилирован: {expect.get('refusing_skill')}")
            for term in case.get("glossary_pair") or []:
                if term not in terms:
                    fail(f"{case_id}: термин вне словаря домена: {term}")


def check_source_tiers(root: str, tiers: dict) -> None:
    """Контракт источников: параллельный поиск и обязательное подтверждение."""
    tiers = tiers or {}
    forms = {form.get("id") for form in tiers.get("evidence_forms") or []}
    declared = [tier.get("id") for tier in tiers.get("tiers") or []]
    if not declared:
        fail("taxonomy/source-tiers.yaml: словарь уровней источников пуст — маршрутизация знания не объявлена")
    if tiers.get("collection_mode") != "complementary":
        fail("taxonomy/source-tiers.yaml: локальная KB и Confluence обязаны дополнять друг друга, а не образовывать fallback")
    if tiers.get("confirmation_gate") != "G-human":
        fail("taxonomy/source-tiers.yaml: источник обязан подтверждаться человеком через G-human")
    citation_fields = set(tiers.get("citation_fields") or [])
    if not {"title", "section", "page_or_anchor", "quote", "locator"}.issubset(citation_fields):
        fail("taxonomy/source-tiers.yaml: форма подтверждения источника неполна")
    for tier in tiers.get("tiers") or []:
        if tier.get("evidence_form") not in forms:
            fail(f"{tier.get('id')}: форма доказательства вне перечня evidence_forms")
        if not tier.get("rationale"):
            fail(f"{tier.get('id')}: уровень источника без обоснования применимости")
    order = tiers.get("order") or []
    if sorted(order) != sorted(declared):
        fail("taxonomy/source-tiers.yaml: порядок применения не покрывает ровно объявленные уровни")
    for rule in ("conflict_rule", "escalation_rule", "investment_rule"):
        if not tiers.get(rule):
            fail(f"taxonomy/source-tiers.yaml: отсутствует {rule} — расхождение источников разрешалось бы усмотрением")
    for item in tiers.get("out_of_slice") or []:
        if not item.get("why"):
            fail(f"{item.get('id')}: уровень вне среза без объявленной причины — необъявленная ветка")

    schema = load_json(root, "contracts/c-in.schema.json") or {}
    source_item = (((schema.get("properties") or {}).get("sources") or {}).get("items") or {})
    if "tier" not in (source_item.get("required") or []):
        fail("contracts/c-in.schema.json: уровень источника обязан быть обязательным полем (fail-closed)")
    enum = ((source_item.get("properties") or {}).get("tier") or {}).get("enum") or []
    in_slice = [tier.get("id") for tier in tiers.get("tiers") or [] if tier.get("in_slice")]
    if sorted(enum) != sorted(in_slice):
        fail("contracts/c-in.schema.json: перечень уровней источника расходится с закрытым словарём source-tiers")


def check_projections(root: str, projections: dict) -> None:
    """Проекция перестаёт быть пустой веткой: обязательна в контракте и разрешима в словарь."""
    projections = projections or {}
    schema = load_json(root, "contracts/c-out-bcreq.schema.json") or {}
    slots = set(((schema.get("properties") or {}).get("slots") or {}).get("required") or [])
    if "projection" not in (schema.get("required") or []):
        fail("contracts/c-out-bcreq.schema.json: проекция обязана быть обязательным полем — иначе ветка не исполняется")
    enum = ((schema.get("properties") or {}).get("projection") or {}).get("enum") or []
    declared = [item.get("id") for item in projections.get("items") or []]
    if sorted(enum) != sorted(declared):
        fail("contracts/c-out-bcreq.schema.json: перечень проекций расходится с закрытым словарём projections")
    for item in projections.get("items") or []:
        unknown = set(item.get("required_slots") or []) - slots
        if unknown:
            fail(f"{item.get('id')}: обязательные слоты проекции вне закрытого перечня: {sorted(unknown)}")
        if not item.get("required_slots"):
            fail(f"{item.get('id')}: проекция без обязательных слотов не отличается от отсутствия проекции")
        for field in ("addressee", "wording_rule"):
            if not item.get(field):
                fail(f"{item.get('id')}: проекция без поля {field} не задаёт предмет проверки гейта")


def check_confusable_coverage(root: str, glossary: dict, cases: dict) -> None:
    """Правило EP-G7 в исполняемом виде: пара близких терминов обязана иметь отрицательный случай.

    До этой проверки EP-G7 существовало как текст правила и один эталон: три из
    четырёх объявленных пар словаря не имели ни одного теста, то есть правило
    было выполнено формально.
    """
    terms = (glossary or {}).get("terms") or []
    id_by_name: dict[str, str] = {}
    for term in terms:
        id_by_name[term.get("term")] = term.get("id")
        for alias in term.get("aliases") or []:
            id_by_name.setdefault(alias, term.get("id"))

    covered: set[frozenset[str]] = set()
    for case in (cases or {}).get("cases") or []:
        pair = case.get("glossary_pair") or []
        if len(pair) == 2:
            covered.add(frozenset(pair))

    expected: set[frozenset[str]] = set()
    for term in terms:
        for other in term.get("confusable_with") or []:
            name = other.get("term") if isinstance(other, dict) else other
            target = id_by_name.get(name)
            if target is None:
                fail(f"{term.get('id')}: confusable_with ссылается на термин вне словаря: {name!r}")
                continue
            if not (other.get("why") if isinstance(other, dict) else True):
                fail(f"{term.get('id')}: пара близких терминов без объяснения подмены не проверяема")
            expected.add(frozenset({term.get("id"), target}))

    missing = expected - covered
    if missing:
        listed = sorted(" + ".join(sorted(pair)) for pair in missing)
        fail(
            "EP-G7: пара близких терминов словаря домена не покрыта отрицательным случаем Golden Set: "
            + "; ".join(listed)
        )


def check_metrics(root: str) -> None:
    data = load_yaml(root, "evaluation/metrics.yaml") or {}
    declared = {item.get("id") for item in data.get("metrics") or []}
    expected = {f"M-{i}" for i in range(1, 6)} | {f"MP-{i}" for i in range(1, 7)}
    missing = expected - declared
    if missing:
        fail(f"evaluation/metrics.yaml: базовая линия неполна, отсутствуют метрики: {sorted(missing)}")
    for item in data.get("metrics") or []:
        if not item.get("formula") or not item.get("target"):
            fail(f"{item.get('id')}: метрика без формулы или цели не измеряется")


def check_runtime_independence(root: str) -> None:
    """Контракт 2: runtime-артефакт не зависит от Source-репозитория."""
    runtime_dirs = (".gigacode", "routes", "templates", "golden", "evaluation", "taxonomy", "contracts", "docs", "meta-model")
    for directory in runtime_dirs:
        base = os.path.join(root, directory)
        for current, _dirs, files in os.walk(base):
            for filename in sorted(files):
                path = os.path.join(current, filename)
                rel = os.path.relpath(path, root)
                with open(path, encoding="utf-8") as handle:
                    for number, line in enumerate(handle, start=1):
                        if line.lstrip().startswith("#") or line.lstrip().startswith("//"):
                            continue
                        if any(key in line for key in PROVENANCE_KEYS):
                            continue
                        if HUB_PATH.search(line):
                            fail(
                                f"{rel}:{number}: ссылка в документ Source во время выполнения "
                                "(дефект компиляции, контракт 2): " + line.strip()[:80]
                            )


def main() -> int:
    arguments = list(sys.argv[1:])
    input_path = None
    if "--input" in arguments:
        position = arguments.index("--input")
        if position + 1 >= len(arguments):
            sys.stderr.write("ERROR: --input требует путь к A-IN.yaml\n")
            return 2
        input_path = os.path.abspath(arguments[position + 1])
        del arguments[position : position + 2]
    if len(arguments) > 1:
        sys.stderr.write("ERROR: использование: validate-package.py [пакет] [--input A-IN.yaml]\n")
        return 2
    root = arguments[0] if arguments else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(root)
    if not os.path.isdir(os.path.join(root, "taxonomy")):
        sys.stderr.write(f"ERROR: каталог не похож на пакет исполнения: {root}\n")
        return 2

    check_layout(root)
    check_distribution_boundary(root)
    check_manifest(root)
    taxonomies = check_taxonomies(root)
    skills = check_skills(root)
    graph = check_route(root, taxonomies.get("processes") or {}, skills)
    check_product_routing(root, taxonomies, skills, graph)
    check_run_contract(root)
    check_golden(root, graph, skills, taxonomies.get("domain-glossary") or {})
    check_source_tiers(root, taxonomies.get("source-tiers") or {})
    check_projections(root, taxonomies.get("projections") or {})
    check_confusable_coverage(
        root,
        taxonomies.get("domain-glossary") or {},
        load_yaml(root, "golden/cases.yaml") or {},
    )
    check_metrics(root)
    check_runtime_independence(root)

    if input_path:
        document = load_input_document(input_path)
        for message in product_binding_errors(
            document,
            taxonomies.get("mango-products") or {},
            taxonomies.get("products") or {},
        ):
            fail(f"{input_path}: {message}")

    for schema in ("c-in", "c-core", "c-quest", "c-out-bcreq", "c-rk"):
        load_json(root, f"contracts/{schema}.schema.json")

    if ERRORS:
        for message in ERRORS:
            sys.stderr.write(f"ERROR: {message}\n")
        sys.stderr.write(f"G-mach: пакет отвергнут, ошибок: {len(ERRORS)}.\n")
        return 1

    print(f"G-mach: пакет принят (навыков: {len(skills)}, узлов маршрута: {len(graph.get('nodes') or [])}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
