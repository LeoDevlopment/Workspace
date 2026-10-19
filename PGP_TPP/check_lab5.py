"""Самопроверка ЛР 5, вариант 2 (сортировка подсчётом).
Запуск: python3 check_lab5.py [БИТЫ_ДИАПАЗОНА [N1 N2 ...]]
  БИТЫ_ДИАПАЗОНА -- значения берутся из [0, 2^БИТЫ - 1]; по умолчанию 24 (как в задании)
  N1 N2 ...      -- размеры больших массивов для замера времени (по умолчанию 1000000 10000000)
Рядом должен лежать ./lab5
"""
import struct, subprocess, sys, time
import numpy as np

BIN = './lab5'
BITS = int(sys.argv[1]) if len(sys.argv) > 1 else 24
BIG = [int(x) for x in sys.argv[2:]] or [1_000_000, 10_000_000]
R = 1 << BITS
rng = np.random.default_rng(2026)

def run(arr=None, raw=None):
    if raw is None:
        raw = struct.pack('<i', len(arr)) + np.asarray(arr, dtype='<i4').tobytes()
    t = time.time()
    r = subprocess.run([BIN], input=raw, capture_output=True)
    return r, time.time() - t

def check(name, arr, extra=''):
    arr = np.asarray(arr, dtype=np.int64)
    r, dt = run(arr)
    ok = r.returncode == 0 and not r.stderr and r.stdout == np.sort(arr).astype('<i4').tobytes()
    print(f'{name:38} {"OK" if ok else "FAIL"}  {extra}{"" if ok else r.stderr.decode()[:80]}')
    return ok, dt

# 1. Пример из условия, побайтово
pdf_in = bytes.fromhex('0A000000 00000000 09000000 08000000 07000000 06000000 05000000 04000000 03000000 02000000 01000000'.replace(' ', ''))
pdf_out = bytes.fromhex('00000000 01000000 02000000 03000000 04000000 05000000 06000000 07000000 08000000 09000000'.replace(' ', ''))
r, _ = run(raw=pdf_in)
print(f'{"Пример из PDF (10 чисел)":38} {"OK" if r.stdout == pdf_out and not r.stderr else "FAIL"}')

# 2. Малые и граничные случаи
check('n = 1', [min(7, R - 1)])
check('все нули (n=1000)', np.zeros(1000, dtype=int))
check('все равны максимуму (n=1000)', np.full(1000, R - 1))
check('только 0 и максимум', rng.choice([0, R - 1], 5000))
check('уже отсортирован', np.arange(min(R, 3000)))
check('обратный порядок', np.arange(min(R, 3000))[::-1])
for n in (63, 64, 65, 127, 128, 129):
    check(f'случайный n = {n}', rng.integers(0, R, n))
check('случайный n = 100000', rng.integers(0, R, 100_000))
check('99% одинаковых', np.where(rng.random(200_000) < 0.99, R // 3, rng.integers(0, R, 200_000)))
check('всего 3 разных значения', rng.choice([1, R // 2, R - 2], 200_000))

# 3. Большие массивы + время
for n in BIG:
    a = rng.integers(0, R, n)
    ok, dt = check(f'случайный n = {n:,}', a)
    print(f'{"":38} программа вместе с чтением/записью: {dt:.2f} с')
    ok, dt = check(f'все равны, n = {n:,}', np.full(n, R // 2))
    print(f'{"":38} время: {dt:.2f} с')

# 4. Ошибки: ERROR в stderr, код возврата 0
bad = [('пустой ввод', b''), ('отрицательная длина', struct.pack('<i', -5)),
       ('данных меньше, чем n', struct.pack('<i', 5) + struct.pack('<2i', 1, 2)),
       ('значение вне диапазона', struct.pack('<2i', 1, R)), ('отрицательное значение', struct.pack('<2i', 1, -1))]
for name, raw in bad:
    r, _ = run(raw=raw)
    ok = r.returncode == 0 and r.stdout == b'' and b'ERROR:' in r.stderr
    print(f'{name:38} {"OK" if ok else "FAIL"}')
r, _ = run(raw=struct.pack('<i', 0))
print(f'{"n = 0 (пустой вывод, без ошибки)":38} {"OK" if r.stdout == b"" and not r.stderr else "FAIL"}')
