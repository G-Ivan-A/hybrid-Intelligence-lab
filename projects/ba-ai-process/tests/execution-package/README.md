---
status: draft
version: 1.2
updated: 2026-09-26
temperature: 0.1
---

# Тесты пакета исполнения GigaCode CLI

Этот модуль проверяет механизм исполнения отдельно от копируемого пакета. Он
не вызывает LLM, GigaCode CLI или MCP: YAML-fixtures задают решения на рёбрах,
а эмулятор доказывает, что маршрут разрешает траекторию, первым выполняет
обязательную продуктовую атрибуцию, каждый агентский узел имеет native skill и
human gate сохраняет читаемый Markdown checkpoint. Регрессии отдельно
проверяют не–Contact Center цепочки `platform` и `ai-automation`, их разрешение
по полному MANGO-каталогу и неизменность подтверждённого контекста в run sheet.

Запуск из корня репозитория:

```sh
python3 projects/ba-ai-process/tests/execution-package/tests/test_emulation.py
```

`test_runner.py` проверяет реальный локальный контроллер: каждый разрешённый
переход запускает `G-mach`, а запрещённое ребро, неверный предикат, ненулевой
exit code, отсутствие human checkpoint, потеря trace и ложное утверждение о
пройденном gate блокируют продолжение. Тест копирует пакет во временный каталог.

Временные task runs создаются только в системном temporary directory. Fixtures
и assertions — тестовые данные механизма, а не Golden Set предметного качества.
