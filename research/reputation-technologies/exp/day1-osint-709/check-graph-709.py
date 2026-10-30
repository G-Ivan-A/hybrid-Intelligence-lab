#!/usr/bin/env python3
"""Bounded graph round-trip experiment for #709; stdlib only, no network or LLM."""
import copy
import csv
import io
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = {
    'nodes': ['Id', 'Label', 'Kind'],
    'edges': ['Id', 'Source', 'Target', 'Type', 'Relation', 'claim_ids', 'mass', 'distance', 'polarity', 'metric_claim_ids'],
    'claims': ['Id', 'node_ids', 'Marker', 'Statement', 'Time', 'source_ids', 'Basis', 'Status', 'Reason', 'Credibility', 'Assessment_reason'],
    'sources': ['Id', 'URL', 'Publisher', 'Published', 'Inspected', 'Access', 'Quote', 'Human_checked', 'Origin', 'Reliability', 'Assessment_reason'],
}


def read_packet(text):
    packet = {}
    for name, columns in SCHEMA.items():
        match = re.search(rf'^### {name}\.csv\n\n```csv\n(.*?)^```', text, re.M | re.S)
        if not match:
            raise ValueError(f'{name}: missing CSV block')
        reader = csv.DictReader(io.StringIO(match[1]))
        if reader.fieldnames != columns:
            raise ValueError(f'{name}: unexpected columns')
        packet[name] = list(reader)
    return packet


def validate(packet):
    errors = []
    indexes = {}
    for name, rows in packet.items():
        if any(set(row) != set(SCHEMA[name]) or None in row.values() for row in rows):
            errors.append(f'{name}: malformed CSV row')
            continue
        ids = [row['Id'] for row in rows]
        if len(ids) != len(set(ids)) or any(not id_ for id_ in ids):
            errors.append(f'{name}: duplicate/empty IDs')
        indexes[name] = {row['Id']: row for row in rows}
    if errors:
        return errors
    for edge in packet['edges']:
        if any(edge[key] not in indexes['nodes'] for key in ('Source', 'Target')):
            errors.append(f'{edge["Id"]}: dangling endpoint')
        ids = edge['claim_ids'].split(';')
        if not all(id_ in indexes['claims'] for id_ in ids):
            errors.append(f'{edge["Id"]}: dangling claim')
        if edge['metric_claim_ids']:
            errors.append(f'{edge["Id"]}: unexpected metric evidence in this fixture')
        if edge['Type'] != 'Directed':
            errors.append(f'{edge["Id"]}: unexpected direction')
        # This fixture contains no relationship measurements. Unknown != cold/0/+1.
        if any(edge[key] != '?' for key in ('mass', 'distance', 'polarity')):
            errors.append(f'{edge["Id"]}: unsupported metric in this experiment')
    for claim in packet['claims']:
        if any(id_ not in indexes['nodes'] for id_ in claim['node_ids'].split(';')):
            errors.append(f'{claim["Id"]}: dangling claim entity')
        if claim['Credibility'] not in ('1', '2', '3', '4', '5', '6') or not claim['Assessment_reason']:
            errors.append(f'{claim["Id"]}: information assessment missing')
        source_ids = claim['source_ids'].split(';') if claim['source_ids'] else []
        if any(id_ not in indexes['sources'] for id_ in source_ids):
            errors.append(f'{claim["Id"]}: dangling source')
        if not source_ids and (not claim['Basis'] or claim['Marker'] == '● ФАКТ'):
            errors.append(f'{claim["Id"]}: unsupported fact or missing basis')
        if claim['Marker'] not in ('● ФАКТ', '◐ ИНТЕРПРЕТАЦИЯ', '○ НЕ НАЙДЕНО'):
            errors.append(f'{claim["Id"]}: fourth marker')
        if claim['Status'] not in ('PARTIAL', 'VERIFIED', 'CONFLICT') or not claim['Reason']:
            errors.append(f'{claim["Id"]}: status/reason missing')
        if claim['Status'] == 'VERIFIED' and (
            claim['Marker'] != '● ФАКТ' or not source_ids or claim['Time'] == '?' or
            any(indexes['sources'].get(id_, {}).get('Human_checked') != 'yes' or
                indexes['sources'].get(id_, {}).get('Published') == '?' for id_ in source_ids)
        ):
            errors.append(f'{claim["Id"]}: unsupported VERIFIED')
    company_ids = {row['Id'] for row in packet['nodes'] if row['Kind'] == 'company'}
    if company_ids != {f'C{i:02}' for i in range(1, 11)}:
        errors.append('ten-company coverage lost')
    return errors


def round_trip(packet):
    restored = {}
    for name, rows in packet.items():
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=SCHEMA[name], lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        restored[name] = list(csv.DictReader(io.StringIO(stream.getvalue())))
    assert restored == packet, 'CSV round trip lost evidence or IDs'


def self_test(packet):
    probes = []
    def change(name, table, row, field, value):
        broken = copy.deepcopy(packet)
        broken[table][row][field] = value
        probes.append((name, broken))
    change('missing endpoint', 'edges', 0, 'Target', 'MISSING')
    change('missing claim', 'edges', 0, 'claim_ids', 'MISSING')
    change('missing source', 'claims', 0, 'source_ids', 'MISSING')
    change('duplicate ID', 'nodes', 1, 'Id', 'N00')
    change('unknown becomes zero', 'edges', 0, 'mass', '0')
    change('unknown becomes cold', 'edges', 0, 'distance', 'cold')
    change('unknown becomes positive', 'edges', 0, 'polarity', '+1')
    change('uninspected/date-free promotion', 'claims', 0, 'Status', 'VERIFIED')
    change('hypothesis promotion', 'claims', 1, 'Status', 'VERIFIED')
    change('invented fourth marker', 'claims', 1, 'Marker', '○ ГИПОТЕЗА')
    change('no hypothesis basis', 'claims', 1, 'Basis', '')
    change('lost company', 'nodes', 2, 'Kind', 'unknown')
    for name, broken in probes:
        assert validate(broken), f'unsafe packet mutation survived: {name}'
    return len(probes)


def factual_edges(packet):
    claims = {row['Id']: row for row in packet['claims']}
    return [edge for edge in packet['edges'] if edge['Relation'] not in ('intention', 'role_hypothesis') and
            all(claims[id_]['Status'] == 'VERIFIED' and claims[id_]['Marker'] == '● ФАКТ'
                for id_ in edge['claim_ids'].split(';'))]


def analysis_controls(packet):
    # Synthetic positive control: do not change the saved real-source observation.
    checked = copy.deepcopy(packet)
    checked['claims'][0].update(
        Status='VERIFIED', Time='2026-10-30', Credibility='2',
        Reason='Синтетический контроль: точное датированное упоминание сверено человеком',
        Assessment_reason='Условие положительного теста, не новая находка о компании')
    checked['sources'][0].update(
        Human_checked='yes', Published='2026-10-30', Reliability='B',
        Assessment_reason='Синтетическое условие: первичный каталог и дата проверены')
    assert not validate(checked)
    assert [edge['Id'] for edge in factual_edges(checked)] == ['E01a']
    # One verified claim must not promote the other claims attached to an edge.
    checked['edges'][0]['claim_ids'] += ';CL01d'
    assert not validate(checked)
    assert not factual_edges(checked)


def main():
    packet = read_packet((HERE / '2026-10-30-ten-company-example.md').read_text(encoding='utf-8'))
    errors = validate(packet)
    assert not errors, '\n'.join(errors)
    round_trip(packet)
    count = self_test(packet)
    # Reproducible analysis, not a recommendation: filter exact VERIFIED relations.
    fact_edges = factual_edges(packet)
    assert not fact_edges, 'this uninspected, date-free sample cannot yield verified relations'
    analysis_controls(packet)
    kinds = Counter(row['Kind'] for row in packet['nodes'])
    print(f'PASS: {len(packet["nodes"])} nodes ({kinds["company"]} companies), {len(packet["edges"])} edges, '
          f'{len(packet["claims"])} claims, {len(packet["sources"])} source; CSV round trip preserved')
    print(f'PASS: {count} unsafe graph mutations rejected; VERIFIED factual subgraph: 0 edges; '
          f'{len(packet["edges"])} draft edges excluded')
    print('PASS: synthetic positive control admits one verified edge; mixed-status control excludes it')


if __name__ == '__main__':
    main()
