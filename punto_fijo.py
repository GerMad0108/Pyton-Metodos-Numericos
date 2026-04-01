import numpy as np

# ==========================================================
# BLOQUE 1: DEFINICIÓN Y ENTRADA (SET-UP)
# ==========================================================
def g(x_val, g_texto):
    """Evalúa la función despejada g(x) que el usuario ingresa"""
    # El contexto permite usar 'x' y funciones de 'np' como np.exp o np.sin
    contexto = {"x": x_val, "np": np}
    return eval(g_texto, {"__builtins__": None}, contexto)

print("-" * 50)
print("SISTEMA DE MÉTODOS NUMÉRICOS: PUNTO FIJO")
print("-" * 50)

# Datos de entrada basados en la teoría del libro
g_input = input("Introduce g(x) despejada (ej: np.exp(-x)): ")
x0 = float(input("Punto inicial x0: "))
tol = float(input("Tolerancia (ej: 0.0001): "))
max_iter = int(input("Máximo de iteraciones (ej: 50): "))

# ==========================================================
# BLOQUE 2: INICIALIZACIÓN DE LA SUCESIÓN
# ==========================================================
n = 0
error = 1.0  # Valor inicial para romper la primera barrera del while
print(f"\n{'Iter':<5} | {'x_n':<12} | {'Error':<12}")
print("-" * 50)

# ==========================================================
# BLOQUE 3: EL CICLO DE ITERACIÓN (p_n = g(p_n-1))
# ==========================================================
while error > tol and n < max_iter:
    n += 1
    
    # Aplicamos la fórmula del Teorema 2.5
    try:
        x_new = g(x0, g_input)
    except Exception as e:
        print(f"\n[!] Error matemático en la función: {e}")
        break
    
    # ==========================================================
    # BLOQUE 4: CONTROL DE CONVERGENCIA Y DIVERGENCIA
    # ==========================================================
    error = abs(x_new - x0)
    
    # Imprimimos la fila de la tabla
    print(f"{n:<5} | {x_new:<12.6f} | {error:<12.6f}")
    
    # Actualizamos el valor anterior para la siguiente vuelta
    x0 = x_new

    # Seguro de Divergencia: Si el error crece sin control
    if error > 1e10:
        print("\n[!] EL MÉTODO DIVERGE: La pendiente |g'(x)| > 1.")
        break

# ==========================================================
# BLOQUE 5: SALIDA DE RESULTADOS (VERIFICACIÓN)
# ==========================================================
print("-" * 50)
if error <= tol:
    print(f"RESULTADO: Punto fijo encontrado en x = {x0:.6f}")
    print(f"CONVERGENCIA: Alcanzada con éxito en {n} iteraciones.")
elif n >= max_iter:
    print("AVISO: Se alcanzó el máximo de iteraciones sin lograr la tolerancia.")
    print(f"Último valor calculado: x = {x0:.6f}")
print("-" * 50)