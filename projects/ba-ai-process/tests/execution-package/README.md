---
status: draft
version: 1.4
updated: 2026-09-29
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

`test_package_gate.py` — отрицательные тесты `G-mach`: каждый случай ломает
одно правило компиляции во временной копии пакета и требует отказа с
ожидаемой причиной, целый пакет обязан проходить; там же проверяются
`--input` подтверждённого A-IN и компиляция Working в принимаемый Release.
Случаи перенесены из `tools/test-execution-package.sh`, который теперь
вызывает этот модуль, поэтому одинаково исполняются в Linux и Windows.

`test_runner.py` проверяет реальный локальный контроллер: каждый разрешённый
переход запускает `G-mach`, а запрещённое ребро, неверный предикат, ненулевой
exit code, отсутствие human checkpoint, потеря trace и ложное утверждение о
пройденном gate блокируют продолжение. Тест копирует пакет во временный каталог.
Строку APPROVE тест вводит через псевдотерминал, в Windows — через консоль
`pywinpty`.

`test_guides.py` проверяет кластер инструкций БА `docs/guides/`: состав файлов
совпадает с кластером Cline-пакета, относительные ссылки и якоря разрешаются,
документы пакета не содержат команд и путей других ОС, все блоки `powershell`
синтаксически корректны, блоки развёртывания, учебного прогона и обновления
исполняются дословно (APPROVE вводится через консоль) и печатают указанные в
инструкции результаты, команда запечатывания Working из справочника делает
черновик принимаемым `validate-working`, а каждый отказ `BLOCKED:` из таблицы
типичных ситуаций существует в runner. Оболочку задаёт `GUIDE_SHELL`
(`powershell` — Windows PowerShell 5.1, `pwsh` — PowerShell 7); CI исполняет
тест в обеих оболочках на `windows-latest`, для Windows нужен `pywinpty`.
Профиль пользователя (`USERPROFILE`) во время теста содержит пробел и
кириллицу, а `PYTHONUTF8` не задаётся: файлы читаются так же, как в реальной
учётной записи Windows с кодовой страницей ANSI.

Полный набор в Windows 10/11 (PowerShell, из корня репозитория):

```powershell
python -m pip install -r projects/ba-ai-process/dist/execution-package-gigacode-cli/requirements.txt pywinpty
$env:GUIDE_SHELL = "powershell"
python -m unittest discover -s projects/ba-ai-process/tests/execution-package/tests -v
```

В Linux тот же набор вместе с проверками Source-раскладки запускает
`bash tools/test-execution-package.sh`.

Временные task runs создаются только в системном temporary directory. Fixtures
и assertions — тестовые данные механизма, а не Golden Set предметного качества.
