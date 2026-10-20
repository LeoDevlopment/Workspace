import numpy as np
import matplotlib.pyplot as plt

def solve_hyperbolic(a, L, T, N, M, scheme='explicit', init_order=2, bc_type='dirichlet'):
    """
    Решение гиперболического уравнения u_tt = a^2 u_xx.
    Параметры:
    a : коэффициент
    L : длина отрезка
    T : конечное время
    N : число шагов по пространству
    M : число шагов по времени
    scheme : 'explicit' или 'implicit'
    init_order : 1 или 2 (порядок аппроксимации второго начального условия)
    bc_type : тип граничных условий ('dirichlet', 'neumann_2point_1', 'neumann_3point_2', 'neumann_2point_2')
    """
    h = L / N
    tau = T / M
    x = np.linspace(0, L, N+1)
    t = np.linspace(0, T, M+1)
    
    # Начальные условия
    u0 = np.sin(x)  # u(x,0)
    ut0 = -a * np.cos(x)  # u_t(x,0)
    
    # Массив для решения
    u = np.zeros((M+1, N+1))
    u[0, :] = u0
    
    # Второе начальное условие
    if init_order == 1:
        u[1, 1:N] = u0[1:N] + tau * ut0[1:N]
    else:  # второй порядок
        u[1, 1:N] = u0[1:N] + tau * ut0[1:N] + 0.5 * tau**2 * a**2 * (-np.sin(x[1:N]))
    
    # Граничные условия на первом слое
    u[1, 0] = -np.sin(a * t[1])
    u[1, N] = np.sin(a * t[1])
    
    # Параметр Куранта
    r = a * tau / h
    
    # Основной цикл по времени
    for j in range(1, M):
        if scheme == 'explicit':
            for i in range(1, N):
                u[j+1, i] = 2*u[j, i] - u[j-1, i] + r**2 * (u[j, i+1] - 2*u[j, i] + u[j, i-1])
            
            # Граничные условия
            if bc_type == 'dirichlet':
                u[j+1, 0] = -np.sin(a * t[j+1])
                u[j+1, N] = np.sin(a * t[j+1])
            # Другие типы граничных условий можно добавить аналогично
        
        elif scheme == 'implicit':
            # Решение системы методом прогонки
            alpha = np.zeros(N+1)
            beta = np.zeros(N+1)
            # Граничные условия
            alpha[0] = 0
            beta[0] = -np.sin(a * t[j+1])
            alpha[N] = 0
            beta[N] = np.sin(a * t[j+1])
            
            # Прямой ход прогонки
            for i in range(1, N):
                A = -r**2
                B = 1 + 2*r**2
                C = -r**2
                F = 2*u[j, i] - u[j-1, i]
                alpha[i] = -C / (A * alpha[i-1] + B)
                beta[i] = (F - A * beta[i-1]) / (A * alpha[i-1] + B)
            
            # Обратный ход
            u[j+1, N] = beta[N]
            for i in range(N-1, -1, -1):
                u[j+1, i] = alpha[i] * u[j+1, i+1] + beta[i]
    
    return x, t, u

# Параметры
a = 1.0
L = np.pi
T = 1.0
N = 50
M = 50

# Решение явной схемой
x, t, u_explicit = solve_hyperbolic(a, L, T, N, M, scheme='explicit', init_order=2)

# Точное решение
U_exact = np.zeros_like(u_explicit)
for j in range(M+1):
    U_exact[j, :] = np.sin(x - a * t[j])

# Погрешность
error = np.max(np.abs(u_explicit - U_exact))
print(f"Максимальная погрешность (явная схема): {error:.6e}")

# Визуализация
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(x, u_explicit[M, :], 'b-', label='Численное')
plt.plot(x, U_exact[M, :], 'r--', label='Аналитическое')
plt.xlabel('x')
plt.ylabel('u')
plt.title(f't = {T}')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.imshow(u_explicit, aspect='auto', extent=[0, L, T, 0])
plt.colorbar(label='u')
plt.xlabel('x')
plt.ylabel('t')
plt.title('Решение')
plt.tight_layout()
plt.show()