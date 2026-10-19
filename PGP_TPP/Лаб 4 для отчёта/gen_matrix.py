#!/usr/bin/env python3
"""Генератор тестовых матриц для ЛР 4 (формат: n, затем n строк по n чисел).

Использование:
    python3 gen_matrix.py N out.txt [--seed S] [--kind KIND]

Виды матриц (--kind):
    random    элементы ~ N(0, 1); обратимая с вероятностью 1, число обусловленности ~ O(n)
    dominant  случайная матрица с диагональным преобладанием (хорошо обусловлена)
    pivot     строки dominant-матрицы случайно переставлены: на диагонали много нулей/малых
              элементов, выбор главного элемента обязателен
    hilbert   матрица Гильберта (очень плохо обусловлена; только для n <= 10)
    singular  вырожденная (две одинаковые строки). Внимание: в арифметике с плавающей точкой
              ведущий элемент обычно не получается ровно 0, поэтому программа может
              не выдать ERROR, а вернуть большие числа; ровно нулевой ведущий элемент
              гарантирован только для n = 1 (матрица [0]) и простых целочисленных случаев

Из Python:
    from gen_matrix import gen_matrix
    gen_matrix(1000, 'in_1000.txt', seed=1, kind='random')
"""
import argparse
import numpy as np


def make_matrix(n, seed=0, kind='random'):
    rng = np.random.default_rng(seed)
    if kind == 'random':
        return rng.standard_normal((n, n))
    if kind == 'dominant':
        A = rng.uniform(-1.0, 1.0, (n, n))
        A[np.diag_indices(n)] += np.sign(rng.standard_normal(n) + 1e-9) * (n + 1.0)
        return A
    if kind == 'pivot':
        A = make_matrix(n, seed, 'dominant')
        return A[rng.permutation(n)]
    if kind == 'hilbert':
        i = np.arange(n)
        return 1.0 / (i[:, None] + i[None, :] + 1.0)
    if kind == 'singular':
        A = rng.standard_normal((n, n))
        if n >= 2:
            A[-1] = A[0]
        else:
            A[0, 0] = 0.0
        return A
    raise ValueError(f'unknown kind: {kind}')


def gen_matrix(n, path, seed=0, kind='random', block_rows=256):
    """Записывает матрицу в файл блоками (экономит память при больших n)."""
    A = make_matrix(n, seed, kind)
    with open(path, 'w') as f:
        f.write(f'{n}\n')
        for i0 in range(0, n, block_rows):
            np.savetxt(f, A[i0:i0 + block_rows], fmt='%.15e')
    return A


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n', type=int)
    ap.add_argument('out')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--kind', default='random',
                    choices=['random', 'dominant', 'pivot', 'hilbert', 'singular'])
    a = ap.parse_args()
    gen_matrix(a.n, a.out, a.seed, a.kind)
    print(f'{a.kind} matrix {a.n}x{a.n} written to {a.out}')
