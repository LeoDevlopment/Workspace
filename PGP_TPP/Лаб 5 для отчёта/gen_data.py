#!/usr/bin/env python3
"""Генератор бинарных тестов для ЛР 5 (формат: int32 n, затем n чисел int32).

Использование:
    python3 gen_data.py N out.bin [--kind KIND] [--seed S] [--bits B]

Виды данных (--kind), значения лежат в [0, 2^B - 1], по умолчанию B = 24:
    random    равномерно случайные
    equal     все числа одинаковы (худший случай для атомарных операций гистограммы)
    skewed    90% одинаковых, остальные случайные
    sorted    уже отсортированы (неубывающие)
    reversed  отсортированы в обратном порядке
    few       всего 16 различных значений
    zeros     все нули

Из Python:
    from gen_data import gen_data
    gen_data('in.bin', 1_000_000, 'random', seed=1)
"""
import argparse
import numpy as np

KINDS = ['random', 'equal', 'skewed', 'sorted', 'reversed', 'few', 'zeros']


def _chunk(kind, start, size, n, R, rng):
    if kind == 'random':
        return rng.integers(0, R, size, dtype=np.int64)
    if kind == 'equal':
        return np.full(size, R // 2, dtype=np.int64)
    if kind == 'skewed':
        a = rng.integers(0, R, size, dtype=np.int64)
        a[rng.random(size) < 0.9] = R // 3
        return a
    if kind in ('sorted', 'reversed'):
        idx = np.arange(start, start + size, dtype=np.int64)
        if kind == 'reversed':
            idx = n - 1 - idx
        return idx * R // n
    if kind == 'few':
        return rng.integers(0, 16, size, dtype=np.int64) * (R // 16)
    if kind == 'zeros':
        return np.zeros(size, dtype=np.int64)
    raise ValueError(f'unknown kind: {kind}')


def gen_data(path, n, kind='random', seed=0, bits=24, block=8_000_000):
    """Записывает файл блоками по `block` чисел (мало памяти даже для n = 135 млн)."""
    R = 1 << bits
    rng = np.random.default_rng(seed)
    with open(path, 'wb') as f:
        f.write(np.array([n], dtype='<i4').tobytes())
        for start in range(0, n, block):
            size = min(block, n - start)
            f.write(_chunk(kind, start, size, n, R, rng).astype('<i4').tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n', type=int)
    ap.add_argument('out')
    ap.add_argument('--kind', default='random', choices=KINDS)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--bits', type=int, default=24)
    a = ap.parse_args()
    gen_data(a.out, a.n, a.kind, a.seed, a.bits)
    print(f'{a.kind}: {a.n} int32 values written to {a.out}')
