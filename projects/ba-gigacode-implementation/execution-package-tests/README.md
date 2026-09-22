---
status: draft
version: 1.0
updated: 2026-09-21
temperature: 0.1
---

# Тесты пакета исполнения GigaCode CLI

Этот модуль проверяет механизм исполнения отдельно от копируемого пакета. Он
не вызывает LLM, GigaCode CLI или MCP: YAML-fixtures задают решения на рёбрах,
а эмулятор доказывает, что маршрут разрешает траекторию, каждый агентский узел
имеет native skill и human gate сохраняет читаемый Markdown checkpoint.

Запуск из корня репозитория:

```sh
python3 projects/ba-gigacode-implementation/execution-package-tests/tests/test_emulation.py
```

Временные task runs создаются только в системном temporary directory. Fixtures
и assertions — тестовые данные механизма, а не Golden Set предметного качества.
