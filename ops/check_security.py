"""Deterministic baseline check; see security/audit.md for limitations."""
from pathlib import Path
import ast
import sys

root=Path(__file__).resolve().parent.parent
issues=[]
for f in (root/'backend').glob('*.py'):
    code=f.read_text(encoding='utf8')
    tree=ast.parse(code)
    for n in ast.walk(tree):
        if isinstance(n,(ast.Call,)) and isinstance(n.func,ast.Name) and n.func.id in ('eval','exec'):
            issues.append(f'{f.relative_to(root)}:{n.lineno} uses {n.func.id}')
    if 'shell=True' in code:
        issues.append(f'{f.relative_to(root)} contains shell=True')
for f in root.rglob('*'):
    if f.is_file() and not any(x in f.parts for x in ('.git','.venv')) and f.name in ('.env', 'id_rsa'):
        issues.append(f'Forbidden secret file: {f.relative_to(root)}')
if issues:
    print('\n'.join(issues))
    sys.exit(1)
print('Security baseline passed; not a penetration test.')
