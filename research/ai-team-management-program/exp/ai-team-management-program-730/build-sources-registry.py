#!/usr/bin/env python3
"""Сборка Local Extension реестра внешних источников проекта (issue #730).

Читает разделы «Список источников» / «Источники» семи отчётов
research/ai-team-management-program/2026-11-10-*.md, дедуплицирует источники
по URL и печатает таблицу реестра в формате Base Registry
(research/external-knowledge/external-sources-registry.md) с локальной
нумерацией `atm-NNN`.

Запуск (из корня репозитория):
    python3 research/ai-team-management-program/exp/ai-team-management-program-730/build-sources-registry.py \
        > /tmp/registry-table.md
Таблица вставляется в external-sources-registry.md между маркерами
<!-- registry:begin --> и <!-- registry:end --> (флаг --write делает это сам).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research" / "ai-team-management-program"
REGISTRY = DOMAIN / "external-sources-registry.md"

# Тематические теги на уровне отчёта (одинаковы для всех источников отчёта).
REPORT_TAGS = {
    "2026-11-10-international-benchmarks-survey.md": "benchmark-programs, executive-education, ai-for-leaders",
    "2026-11-10-ru-universities-ai-programs-survey.md": "ru-universities, dpo, ai-for-business",
    "2026-11-10-ru-business-schools-ai-programs-survey.md": "ru-business-schools, executive-education, ai-for-business",
    "2026-11-10-ai-adoption-russia-statistics.md": "ai-adoption, ru-statistics, banking, managers",
    "2026-11-10-economics-market-benchmarks.md": "economics, pricing, taxes, market-rates",
    "2026-11-10-corporate-learning-methodology-evidence.md": "learning-science, leadership-development, evaluation, transfer",
    "2026-11-10-candidate-pool-facts.md": "candidate-pool, experts, partner-companies, moscow",
}
SHORT = {
    "2026-11-10-international-benchmarks-survey.md": "бенчмарки",
    "2026-11-10-ru-universities-ai-programs-survey.md": "вузы",
    "2026-11-10-ru-business-schools-ai-programs-survey.md": "бизнес-школы",
    "2026-11-10-ai-adoption-russia-statistics.md": "статистика",
    "2026-11-10-economics-market-benchmarks.md": "экономика",
    "2026-11-10-corporate-learning-methodology-evidence.md": "методологии",
    "2026-11-10-candidate-pool-facts.md": "кандидаты",
}

ITEM = re.compile(r"^\s*(\d+)\.\s+(.*)$")
URL = re.compile(r"https?://[^\s)>\]|]+")
HEADING = re.compile(r"^##\s+\d*\.?\s*(Список источников|Источники)", re.I)


def classify(url, text):
    u = url.lower()
    if "github.com" in u:
        return "github"
    if "habr.com" in u:
        return "habr"
    if any(k in u for k in ("doi.org", "apa.org", "wiley.com", "sciencedirect", "springer", "tandfonline",
                             "sagepub", "nber.org", "arxiv.org", "pnas.org", "nature.com", "jstor",
                             "ncbi.nlm.nih.gov", "pubmed", "researchgate", "journals.", "aom.org")) \
            or re.search(r"\bDOI\b|J Appl Psychol|Journal|meta-analysis|мета-анализ", text):
        return "paper"
    if any(k in u for k in ("consultant.ru", "garant.ru", "pravo.gov.ru", "nalog.gov.ru")):
        return "standard"
    if any(k in u for k in ("comnews", "rbc.ru", "vedomosti", "kommersant", "sostav", "incrussia", "skillbox.ru/media",
                             "tass", "interfax", "forbes", "cnews", "expert.ru", "kod.ru", "tks.ru", "/blog")):
        return "blog"
    return "docs"


def lang(url, name):
    host = re.sub(r"^https?://", "", url.lower()).split("/")[0]
    if host.endswith((".ru", ".su", ".xn--p1ai")) or "рф" in host:
        return "ru"
    if "habr.com" in host:
        return "en" if "/en/" in url else "ru"
    # не-.ru домен: русский, если название первоисточника — кириллица в кавычках «…»
    if re.search(r"«[^»]*[А-Яа-яЁё][^»]*»", name):
        return "ru"
    return "en"


def stage(text):
    t = text.lower()
    if "не открыл" in t or "сниппет" in t or "snippet" in t:
        return "observation"
    return "research"


def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out, inside = [], False
    for i, line in enumerate(lines):
        if line.startswith("## "):
            inside = bool(HEADING.match(line))
            continue
        if not inside:
            continue
        m = ITEM.match(line)
        if not m:
            continue
        # элемент списка может продолжаться на следующих строках
        text = m.group(2)
        j = i + 1
        while j < len(lines) and lines[j].startswith("   ") and not ITEM.match(lines[j]):
            text += " " + lines[j].strip()
            j += 1
        um = URL.search(text)
        if um:
            url = um.group(0).rstrip(".,;»")
            name = text[:um.start()].strip().rstrip("—–-:").strip() or url
        else:
            # URL не напечатан: восстанавливаем постоянную ссылку по идентификатору
            doi = re.search(r"DOI\s+(10\.\d{4,9}/[^\s,;)]+)", text)
            pmc = re.search(r"\b(PMC\d+)", text)
            pmid = re.search(r"PubMed\s+(\d{6,9})", text)
            if doi:
                url = "https://doi.org/" + doi.group(1).rstrip(".")
            elif pmc:
                url = "https://pmc.ncbi.nlm.nih.gov/articles/{}/".format(pmc.group(1))
            elif pmid:
                url = "https://pubmed.ncbi.nlm.nih.gov/{}/".format(pmid.group(1))
            else:
                url = ""
            name = text.split(" — ")[0] if not doi else " — ".join(text.split(" — ")[:2])
            if " — " in text and not doi:
                name = " — ".join(text.split(" — ")[:2])
        name = name.replace("|", "/").replace("[", "(").replace("]", ")")
        out.append((m.group(1), name, url, text))
    return out


def main():
    entries = {}
    order = []
    for fname in REPORT_TAGS:
        for num, name, url, text in parse(DOMAIN / fname):
            key = url.rstrip("/").lower().replace("://www.", "://") if url else "name:" + name.lower()
            if key not in entries:
                entries[key] = {"name": name, "url": url, "text": text, "refs": [], "tags": [], "stage": stage(text)}
                order.append(key)
            e = entries[key]
            e["refs"].append((fname, num))
            for tg in REPORT_TAGS[fname].split(", "):
                if tg not in e["tags"]:
                    e["tags"].append(tg)
            if stage(text) == "research":
                e["stage"] = "research"
    rows = ["| `id` | Источник | Тип | Язык | Теги | Теги будущих фаз / тем | Stage | Проекты | Запись в БЗ |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, key in enumerate(order, 1):
        e = entries[key]
        name = e["name"] if len(e["name"]) <= 160 else e["name"][:157] + "…"
        refs = "; ".join("[{} [{}]]({})".format(SHORT[f], num, f) for f, num in e["refs"])
        src = "[{}]({})".format(name, e["url"]) if e["url"] else name + " (URL в отчёте не зафиксирован)"
        st = e["stage"] if e["url"] else "observation"
        rows.append("| `atm-{:03d}` | {} | `{}` | `{}` | `{}` | `use-case: corporate-training` | `{}` | `ai-team-management-program` | ✅ {} |".format(
            n, src, classify(e["url"], e["text"]), lang(e["url"], e["name"]), ", ".join(e["tags"]), st, refs))
    table = "\n".join(rows)
    stats = "Записей: {} (из них без URL: {}); ссылок из отчётов: {}.".format(
        len(order), sum(1 for k in order if not entries[k]["url"]), sum(len(entries[k]["refs"]) for k in order))
    if "--write" in sys.argv:
        s = REGISTRY.read_text(encoding="utf-8")
        s = re.sub(r"<!-- registry:begin -->.*<!-- registry:end -->",
                   "<!-- registry:begin -->\n" + table + "\n\n" + stats + "\n<!-- registry:end -->", s, flags=re.S)
        REGISTRY.write_text(s, encoding="utf-8")
    print(table)
    print()
    print(stats)


if __name__ == "__main__":
    main()
