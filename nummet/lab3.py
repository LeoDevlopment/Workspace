# ============================================================
# Лабораторная работа 3
# Решение краевой задачи для уравнения эллиптического типа
# Вариант 1: u_xx + u_yy = 0, U(x,y) = x + y
# Методы: простых итераций (Якоби/Либмана), Зейделя, SOR
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


# ------------------------------------------------------------
# 1. Решатель
# ------------------------------------------------------------
def solve_elliptic(Nx, Ny, tol=1e-8, max_iter=100000, method='sor', omega=None):
    """
    Решение u_xx + u_yy = 0 на [0,1]x[0,1] с граничными условиями:
        u(0,y) = y,  u(1,y) = 1 + y,  u(x,0) = x,  u(x,1) = 1 + x

    Параметры:
        Nx, Ny   - число шагов по x и y
        tol      - допуск по максимальному изменению решения
        max_iter - максимальное число итераций
        method   - 'jacobi' | 'seidel' | 'sor'
        omega    - параметр релаксации (если None, выбирается оптимальный для SOR)

    Возвращает:
        X, Y       - сетки
        u          - численное решение
        U_exact    - аналитическое решение
        n_iter     - число выполненных итераций
        residuals  - история невязок
    """
    hx = 1.0 / Nx
    hy = 1.0 / Ny
    x = np.linspace(0.0, 1.0, Nx + 1)
    y = np.linspace(0.0, 1.0, Ny + 1)
    X, Y = np.meshgrid(x, y, indexing='ij')

    # Начальное приближение и точные граничные условия
    u = np.zeros((Nx + 1, Ny + 1))
    u[0, :]  = y            # u(0,y) = y
    u[Nx, :] = 1.0 + y      # u(1,y) = 1 + y
    u[:, 0]  = x            # u(x,0) = x
    u[:, Ny] = 1.0 + x      # u(x,1) = 1 + x

    # Аналитическое решение
    U_exact = X + Y

    # Параметр релаксации
    if omega is None:
        if method == 'sor':
            omega = 2.0 / (1.0 + np.sin(np.pi * min(hx, hy)))
        else:
            omega = 1.0

    residuals = []
    it = 0
    for it in range(1, max_iter + 1):
        u_old = u.copy()

        for i in range(1, Nx):
            for j in range(1, Ny):
                u_new = 0.25 * (u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1])

                if method == 'jacobi':
                    u[i, j] = u_new
                elif method == 'seidel':
                    u[i, j] = u_new
                elif method == 'sor':
                    u[i, j] = (1.0 - omega) * u[i, j] + omega * u_new
                else:
                    raise ValueError(f"Неизвестный метод: {method}")

        diff = np.max(np.abs(u - u_old))
        residuals.append(diff)
        if diff < tol:
            break

    return X, Y, u, U_exact, it, residuals


def compute_error(u, U_exact):
    """Максимальная и среднеквадратичная погрешность."""
    err = np.abs(u - U_exact)
    return np.max(err), np.sqrt(np.mean(err ** 2))


# ------------------------------------------------------------
# 2. Сравнение трёх методов на фиксированной сетке
# ------------------------------------------------------------
def compare_methods(Nx=20, Ny=20, tol=1e-8):
    print("=" * 70)
    print(f"Сравнение методов на сетке {Nx} x {Ny}")
    print("=" * 70)

    methods = ['jacobi', 'seidel', 'sor']
    results = {}

    for m in methods:
        X, Y, u, U_exact, n_iter, res = solve_elliptic(Nx, Ny, tol=tol, method=m)
        max_err, rms_err = compute_error(u, U_exact)
        results[m] = {
            'X': X, 'Y': Y, 'u': u, 'U_exact': U_exact,
            'n_iter': n_iter, 'residuals': res,
            'max_err': max_err, 'rms_err': rms_err
        }
        print(f"{m:8s}: итераций = {n_iter:6d}, "
              f"max_err = {max_err:.2e}, rms_err = {rms_err:.2e}")

    # График сходимости
    plt.figure(figsize=(8, 5))
    for m in methods:
        plt.semilogy(results[m]['residuals'], label=m, linewidth=1.5)
    plt.xlabel('Итерация')
    plt.ylabel('Максимальное изменение $\\|u^{(k+1)} - u^{(k)}\\|_\\infty$')
    plt.title(f'Сходимость итерационных методов (сетка {Nx}x{Ny})')
    plt.legend()
    plt.grid(True, which='both', alpha=0.4)
    plt.tight_layout()
    plt.savefig('convergence.png', dpi=150)
    plt.show()

    return results


# ------------------------------------------------------------
# 3. Визуализация решения и погрешности
# ------------------------------------------------------------
def visualize_solution(Nx=20, Ny=20, method='sor'):
    X, Y, u, U_exact, n_iter, _ = solve_elliptic(Nx, Ny, method=method)
    err = np.abs(u - U_exact)

    print(f"\nВизуализация: метод={method}, итераций={n_iter}, "
          f"max_err={np.max(err):.2e}")

    fig = plt.figure(figsize=(13, 5))

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, u, cmap=cm.viridis, edgecolor='none')
    ax1.set_title('Численное решение $u(x,y)$')
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('u')

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot_surface(X, Y, err, cmap=cm.hot, edgecolor='none')
    ax2.set_title('Погрешность $|u - U|$')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('error')

    plt.tight_layout()
    plt.savefig('solution.png', dpi=150)
    plt.show()


# ------------------------------------------------------------
# 4. Исследование зависимости погрешности от шага сетки
# ------------------------------------------------------------
def study_grid_dependence(method='sor', tol=1e-10):
    print("\n" + "=" * 70)
    print(f"Зависимость погрешности от шага сетки (метод {method})")
    print("=" * 70)

    N_values = [5, 10, 20, 40, 80]
    hs, errs_max, errs_rms, iters = [], [], [], []

    for N in N_values:
        X, Y, u, U_exact, n_iter, _ = solve_elliptic(N, N, tol=tol, method=method)
        max_err, rms_err = compute_error(u, U_exact)
        h = 1.0 / N
        hs.append(h); errs_max.append(max_err)
        errs_rms.append(rms_err); iters.append(n_iter)
        print(f"N={N:3d}, h={h:.4f}, max_err={max_err:.2e}, "
              f"rms_err={rms_err:.2e}, итераций={n_iter}")

    hs = np.array(hs)
    errs_max = np.array(errs_max)

    # Исключаем нулевые значения для лог-графика
    mask = errs_max > 0
    if np.any(mask):
        plt.figure(figsize=(8, 5))
        plt.loglog(hs[mask], errs_max[mask], 'o-', label='max $|u-U|$')
        plt.loglog(hs, np.maximum(errs_max, 1e-16), 's--', alpha=0.4,
                   label='порог машинной точности')
        plt.xlabel('шаг $h = 1/N$')
        plt.ylabel('погрешность')
        plt.title('Зависимость погрешности от шага сетки')
        plt.legend()
        plt.grid(True, which='both', alpha=0.4)
        plt.tight_layout()
        plt.savefig('grid_dependence.png', dpi=150)
        plt.show()

    return hs, errs_max, errs_rms, iters


# ------------------------------------------------------------
# 5. Дополнительно: число итераций от N для разных методов
# ------------------------------------------------------------
def study_iterations_vs_N(methods=('jacobi', 'seidel', 'sor'),
                          N_values=(5, 10, 20, 40)):
    print("\n" + "=" * 70)
    print("Число итераций в зависимости от N")
    print("=" * 70)

    plt.figure(figsize=(8, 5))
    for m in methods:
        iters_list = []
        for N in N_values:
            _, _, _, _, n_iter, _ = solve_elliptic(N, N, tol=1e-8, method=m)
            iters_list.append(n_iter)
        print(f"{m:8s}: " + ", ".join(f"N={N}:{it}" for N, it in zip(N_values, iters_list)))
        plt.loglog(N_values, iters_list, 'o-', label=m)

    plt.xlabel('N')
    plt.ylabel('число итераций')
    plt.title('Число итераций до сходимости')
    plt.legend()
    plt.grid(True, which='both', alpha=0.4)
    plt.tight_layout()
    plt.savefig('iterations_vs_N.png', dpi=150)
    plt.show()


# ------------------------------------------------------------
# 6. Главная функция
# ------------------------------------------------------------
def main():
    # (а) Сравнение трёх методов на фиксированной сетке
    results = compare_methods(Nx=20, Ny=20, tol=1e-8)

    # (б) Визуализация решения и погрешности (SOR)
    visualize_solution(Nx=20, Ny=20, method='sor')

    # (в) Зависимость погрешности от шага сетки
    study_grid_dependence(method='sor', tol=1e-10)

    # (г) Число итераций от N для разных методов
    study_iterations_vs_N(methods=('jacobi', 'seidel', 'sor'),
                          N_values=(5, 10, 20, 40))

    # (д) Итоговая сводка
    print("\n" + "=" * 70)
    print("СВОДКА")
    print("=" * 70)
    for m, r in results.items():
        print(f"{m:8s}: итераций={r['n_iter']:6d}, "
              f"max_err={r['max_err']:.2e}, rms_err={r['rms_err']:.2e}")
    print("\nВсе графики сохранены в текущей директории:")
    print("  convergence.png, solution.png, grid_dependence.png, iterations_vs_N.png")


if __name__ == "__main__":
    main()