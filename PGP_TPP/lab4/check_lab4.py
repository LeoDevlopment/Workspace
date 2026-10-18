"""Самопроверка ЛР 4, вариант 2 (обратная матрица).
Запуск: python3 check_lab4.py [n1 n2 ...]   (размеры для замера времени; по умолчанию 500 1000 2000)
Рядом должен лежать ./lab4
"""
import subprocess, sys, time
import numpy as np

BIN = './lab4'

def run(A):
    n = A.shape[0]
    txt = f'{n}\n' + '\n'.join(' '.join(repr(float(x)) for x in row) for row in A) + '\n'
    t = time.time()
    r = subprocess.run([BIN], input=txt, text=True, capture_output=True)
    return r, time.time() - t

def parse(r):
    return np.array([[float(x) for x in l.split()] for l in r.stdout.strip().split('\n')])

def report(name, ok, extra=''):
    print(f'{name:36} {"OK" if ok else "FAIL"}  {extra}')

# 1. Пример из условия: точное совпадение текста вывода
r, _ = run(np.array([[1, 2], [3, 4]]))
report('Пример из PDF (2x2), текст вывода',
       r.stdout == '-2.0000000000e+00 1.0000000000e+00\n1.5000000000e+00 -5.0000000000e-01\n')

# 2. Случайные матрицы и матрицы, требующие выбора главного элемента
rng = np.random.default_rng(11)
cases = [(f'случайная n={n}', rng.standard_normal((n, n))) for n in (1, 2, 3, 7, 33, 64, 65, 130, 300)]
cases += [('нули на диагонали', np.array([[0, 2, 1], [1, 0, 3], [4, 1, 0.]])),
          ('матрица перестановки 12x12', np.eye(12)[rng.permutation(12)]),
          ('очень малые элементы (1e-8)', rng.standard_normal((20, 20)) * 1e-8),
          ('очень большие элементы (1e8)', rng.standard_normal((20, 20)) * 1e8)]
for name, A in cases:
    r, _ = run(A)
    if r.returncode != 0 or r.stderr.strip():
        report(name, False, r.stderr.strip()); continue
    ref = np.linalg.inv(A)
    rel = np.abs(parse(r) - ref).max() / np.abs(ref).max()
    cond = np.linalg.cond(A)
    report(name, rel < max(1e-9, cond * 1e-14), f'отн. погрешность={rel:.1e}')

# 3. Ошибки: ERROR в stderr, код возврата 0
for name, txt in [('Вырожденная матрица', '2\n1 2\n2 4\n'), ('Нулевая матрица', '2\n0 0\n0 0\n'),
                  ('Не хватает чисел', '2\n1 2\n3\n'), ('Пустой ввод', '')]:
    r = subprocess.run([BIN], input=txt, text=True, capture_output=True)
    report(name, 'ERROR:' in r.stderr and r.returncode == 0 and r.stdout == '')

# 4. Большие матрицы: невязка A * A^-1 - E и время работы
sizes = [int(x) for x in sys.argv[1:]] or [500, 1000, 2000]
for n in sizes:
    A = rng.standard_normal((n, n)) + np.eye(n) * 0.1
    r, dt = run(A)
    if r.returncode != 0 or r.stderr.strip():
        report(f'n={n}', False, r.stderr.strip()); continue
    res = np.abs(A @ parse(r) - np.eye(n)).max()
    report(f'n={n}: невязка A*A^-1 - E', res < 1e-6, f'{res:.1e}, время {dt:.2f} с (с вводом/выводом)')
