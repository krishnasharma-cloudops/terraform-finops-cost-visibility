#!/usr/bin/env python3
"""Offline FinOps report from Infracost and/or OpenCost JSON (standard library only)."""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def money(value):
    try:
        return Decimal(str(value or '0'))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0')


def infracost_report(data):
    projects = data.get('projects', [])
    if not isinstance(projects, list):
        raise ValueError('Expected Infracost JSON with `projects` array')
    rows = []
    for p in projects:
        breakdown = p.get('breakdown') or {}
        total = money(breakdown.get('totalMonthlyCost'))
        if not total:
            total = sum((money(r.get('monthlyCost')) for r in breakdown.get('resources', [])), Decimal('0'))
        rows.append((str(p.get('name', 'unnamed project')), total))
    return rows


def opencost_report(data):
    windows = data.get('data') or []
    if not isinstance(windows, list):
        raise ValueError('Expected OpenCost JSON with `data` array')
    combined = {}
    for window in windows:
        if not isinstance(window, dict):
            continue
        for name, payload in window.items():
            if not isinstance(payload, dict):
                continue
            namespace = str(payload.get('properties', {}).get('namespace', name))
            combined[namespace] = combined.get(namespace, Decimal('0')) + money(payload.get('totalCost'))
    return sorted(combined.items(), key=lambda item: item[1], reverse=True)


def report(infracost=None, opencost=None):
    lines = ['# Infrastructure Cost Visibility Report', '', '> Use sample results only as illustrative data, not a real cloud bill.', '']
    if infracost is not None:
        rows = infracost_report(infracost)
        lines += ['## Infracost — Estimated Monthly IaC Costs (USD)', '']
        for name, value in rows:
            lines.append(f'- **{name}**: ${value:,.2f}/month')
        lines.append(f"- **Total across examples**: ${sum((x[1] for x in rows), Decimal('0')):,.2f}/month")
        lines.append('')
    if opencost is not None:
        rows = opencost_report(opencost)
        lines += ['## OpenCost — Kubernetes Allocated Costs (USD)', '']
        for name, value in rows:
            lines.append(f'- **{name}**: ${value:,.2f} in the requested API window')
        lines.append(f"- **Total across returned allocations**: ${sum((x[1] for x in rows), Decimal('0')):,.2f}")
        lines.append('')
    lines.append('Note: Infracost monthly projections and OpenCost window totals have different time bases. Do not add them into a single bill.')
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--infracost', type=Path)
    p.add_argument('--opencost', type=Path)
    p.add_argument('--markdown', type=Path)
    args = p.parse_args()
    if not args.infracost and not args.opencost:
        p.error('Provide --infracost and/or --opencost JSON file')
    try:
        infra = json.loads(args.infracost.read_text(encoding='utf-8')) if args.infracost else None
        open_cost = json.loads(args.opencost.read_text(encoding='utf-8')) if args.opencost else None
        rendered = report(infra, open_cost)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        p.error(str(exc))
    print(rendered)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(rendered + '\n', encoding='utf-8')
        print('Saved:', args.markdown)

if __name__ == '__main__':
    main()
