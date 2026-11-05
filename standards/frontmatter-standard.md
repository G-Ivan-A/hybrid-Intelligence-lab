---
status: accepted
version: 1.2
updated: 2026-11-04
temperature: 0.1
owner: G-Ivan-A
---

# Frontmatter Standard

Стандарт фиксирует базовый frontmatter для активных Markdown-артефактов Хаба и
наследуемых шаблонов. Цель - сохранить traceability без превращения metadata в
параллельную базу связей.

## Стороны и область

Стандарт применяют contributors и AI-агенты, которые создают или существенно
изменяют активные Markdown-документы в `hybrid-Intelligence-lab`, `templates/`
и наследуемых HTOM/spoke-репозиториях.

Специализация набора по классам документов зафиксирована в
[frontmatter-docs-standard.md](frontmatter-docs-standard.md). Этот файл остается
базовым контрактом, а специализированный стандарт объясняет necessary and
sufficient поля для standards, guides, RFC, ADR, research, templates и practice
nodes.

Не распространяется на YAML issue forms, workflow-файлы, код, JSON и внешние
репозитории. Legacy-документы приводятся к стандарту при следующем
существенном изменении, кроме полей, которые текущий валидатор уже блокирует
репозиторно.

## Обязательства

1. Markdown-документ с frontmatter **ДОЛЖЕН** иметь четыре базовых поля:

   | Поле | Значение | Назначение |
   | --- | --- | --- |
   | `status` | значение из словаря класса документа | Зрелость знания или стадия governance-решения. |
   | `version` | SemVer `X.Y` или `X.Y.Z` | Версия содержания. |
   | `updated` | `YYYY-MM-DD` или `{{date}}` в source-template | Дата последнего смыслового изменения. |
   | `temperature` | число от `0` до `2` | Рекомендуемая температура AI-запуска для воспроизводимой работы с артефактом. |

2. `temperature: 0.1` **СЛЕДУЕТ** использовать для governance-контрактов,
   стандартов, валидаторов и шаблонов задач: там важнее стабильность, чем
   вариативность.
3. Frontmatter **ДОЛЖЕН** быть necessary and sufficient: поле допускается только
   если его потребляет валидатор, шаблон, индекс, executable contract,
   provenance rule или governance-процесс.
4. Governance-артефакты **ДОЛЖНЫ** иметь `owner` в frontmatter. ADR также
   указывает `decision-type`, RFC - `rfc-scope`.
5. `ai-generated` **ЗАПРЕЩЕН** во frontmatter: метка не называет ни
   ответственного, ни модель. Участие ИИ, если оно влияет на review,
   фиксируется в issue, PR, changelog или audit и **МОЖЕТ** быть названо во
   frontmatter двумя полями
   ([ADR-023](../docs/adr/2026-11-adr-023-ai-participation-frontmatter-fields.md)):

   | Поле | Значение | Правило |
   | --- | --- | --- |
   | `contributors` | Люди, команды или роли, которые вели работу и отвечают за результат | Непустой скаляр или inline-список `[a, b]`; обобщённая метка (`ai`, `llm`, `bot`, `true`, `unknown` и т. п.) не допускается |
   | `ai-models` | Конкретные модели ИИ, участвовавшие в работе | Только вместе с `contributors`; скаляр или inline-список идентификаторов с версией (`claude-opus-5-5`, `gpt-5.1`), а не семейство (`claude`, `gpt`) |

   Поля необязательны и допустимы во всех собственных классах метаданных Хаба.
   Внешние форматы (issue form, команда OpenCode, пакет исполнения) их не
   получают. Блочные YAML-списки не поддерживаются: валидатор читает
   frontmatter построчно. Этот пункт — единственный нормативный источник полей;
   остальные стандарты ссылаются на него.
6. `status`, `version`, `updated` и `temperature` **НЕ ДОЛЖНЫ** дублироваться в
   теле документа как отдельные строки "Версия", "Дата", "Статус" без
   операционной причины.

## Definition of Done

- Новый или существенно измененный Markdown-артефакт имеет базовые поля и
  обязательные поля своего класса.
- Связи вынесены в навигацию, карту артефактов, PR или ADR/RFC, а не разложены
  по множеству metadata-полей.
- `./tools/validate-frontmatter.sh .` проходит без ошибок.
- Если указано `ai-models`, указано и `contributors`; значения названы
  конкретно, а не обобщённой меткой.
- Если добавлено исключение, в PR объяснено, какой валидатор или контракт его
  потребляет.

## Обоснование

Опыт `mango_ba_prompts` показал, что frontmatter с 18+ полями усложняет чтение
и провоцирует drift между документом, маппингами и реестрами. Базовые поля
закрывают общую операционную потребность: статус, версия, дата и параметр
воспроизводимого AI-запуска. Governance-поля добавляются только там, где они
нужны для маршрутизации и валидации решений. Остальные связи лучше видны в
явных артефактах: карте, ADR/RFC, issue и PR.

Международные практики AI governance поддерживают этот подход как lightweight
контроль, а не бюрократию: NIST AI RMF предлагает документировать context и
управлять рисками через профили, ISO/IEC 42001 - поддерживать управляемую
систему менеджмента, EU AI Act - соразмерность обязательств риску, а industry
frameworks OpenAI, Anthropic и Google SAIF показывают ценность проверяемых
триггеров, оценок и security-by-design без переноса всех контролей в каждый
документ.

## Источники

- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- [ISO/IEC 42001 AI management systems](https://www.iso.org/standard/42001)
- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [ADR-023: поля `contributors` и `ai-models`](../docs/adr/2026-11-adr-023-ai-participation-frontmatter-fields.md)
- [OpenAI Preparedness Framework](https://openai.com/safety/)
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)
- [Google Secure AI Framework](https://saif.google/)
- [mango_ba_prompts prompt standard](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md)
