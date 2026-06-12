---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Frontmatter Standard

Стандарт фиксирует минимальный frontmatter для активных Markdown-артефактов
Хаба и наследуемых шаблонов. Цель — сохранить traceability без превращения
metadata в параллельную базу связей.

## Стороны и область

Стандарт применяют contributors и AI-агенты, которые создают или существенно
изменяют активные Markdown-документы в `hybrid-Intelligence-lab`, `templates/`
и наследуемых HTOM/spoke-репозиториях.

Специализация минимального набора по классам документов зафиксирована в
[frontmatter-docs-standard.md](frontmatter-docs-standard.md). Этот файл остаётся
базовым контрактом, а специализированный стандарт объясняет necessary and
sufficient поля для standards, guides, RFC, ADR, research, templates и practice
nodes.

Не распространяется на YAML issue forms, workflow-файлы, код, JSON и внешние
репозитории. Legacy-документы приводятся к стандарту при следующем существенном
изменении, без массовой механической миграции.

## Обязательства

1. Markdown-документ с frontmatter **ДОЛЖЕН** иметь четыре обязательных поля:

   | Поле | Значение | Назначение |
   | --- | --- | --- |
   | `status` | `draft` / `reviewed` / `published` / `superseded` / `canonical` / `experimental` / доменный термин | Зрелость артефакта. |
   | `version` | SemVer `X.Y` или `X.Y.Z` | Версия содержания. |
   | `updated` | `YYYY-MM-DD` или `{{date}}` в source-template | Дата последнего смыслового изменения. |
   | `temperature` | число от `0` до `2` | Рекомендуемая температура AI-запуска для воспроизводимой работы с артефактом. |

2. `temperature: 0.1` **СЛЕДУЕТ** использовать для governance-контрактов,
   стандартов, валидаторов и шаблонов задач: там важнее стабильность, чем
   вариативность.
3. Дополнительные поля **НЕ СЛЕДУЕТ** добавлять для навигации, связей,
   маппинга процессов или владельцев. Эти данные живут в
   [governance/artifact-map.md](../governance/artifact-map.md), README, ADR/RFC,
   issue или PR.
4. Дополнительный frontmatter **МОЖНО** оставить только когда поле прямо
   потребляется текущим валидатором или исполнимым контрактом
   (`executable`, `entrypoint`) либо временно нужно для migration provenance
   (`source`, `source_hub`, `source_sha`, `based_on`).
5. `ai-generated` **НЕ ЯВЛЯЕТСЯ обязательным полем**. Авторство и доля AI
   фиксируются в issue, PR, changelog или audit, если это влияет на review.
6. `status`, `version`, `updated` и `temperature` **НЕ ДОЛЖНЫ** дублироваться в
   теле документа как отдельные строки "Версия", "Дата", "Статус" без
   операционной причины.

## Definition of Done

- Новый или существенно изменённый Markdown-артефакт имеет четыре обязательных
  поля.
- Связи вынесены в навигацию, карту артефактов, PR или ADR/RFC, а не разложены
  по множеству metadata-полей.
- `./tools/validate-frontmatter.sh .` не показывает новых предупреждений по
  изменённым файлам.
- Если добавлено исключение, в PR объяснено, какой валидатор или контракт его
  потребляет.

## Обоснование

Опыт `mango_ba_prompts` показал, что frontmatter с 18+ полями усложняет чтение
и провоцирует drift между документом, маппингами и реестрами. Четыре поля
закрывают минимальную операционную потребность: зрелость, версия, дата и
параметр воспроизводимого AI-запуска. Остальные связи лучше видны в явных
артефактах: карте, ADR/RFC, issue и PR.

Международные практики AI governance поддерживают этот подход как lightweight
контроль, а не бюрократию: NIST AI RMF предлагает документировать context и
управлять рисками через профили, ISO/IEC 42001 — поддерживать управляемую
систему менеджмента, EU AI Act — соразмерность обязательств риску, а industry
frameworks OpenAI, Anthropic и Google SAIF показывают ценность проверяемых
триггеров, оценок и security-by-design без переноса всех контролей в каждый
документ.

## Источники

- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- [ISO/IEC 42001 AI management systems](https://www.iso.org/standard/42001)
- [OpenAI Preparedness Framework](https://openai.com/safety/)
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)
- [Google Secure AI Framework](https://saif.google/)
- [mango_ba_prompts prompt standard](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md)
