import json
nb = json.load(open(r'c:/Users/samgl/Documents/GitHub/ExamPrep/AI/lab2_regression_solution.ipynb', encoding='utf-8'))
cells = nb['cells']
out = []
for i, c in enumerate(cells):
    ct = c['cell_type']
    src = ''.join(c.get('source', []))
    out.append(f'===== CELL {i} [{ct}] =====')
    out.append(src)
    out.append('')
with open(r'c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/_review/labs/MLLab2-Regression/round1/_lab2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
print(f'cells={len(cells)}')
