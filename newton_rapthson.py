import numpy as np
import sympy as sp  # Librería para cálculo simbólico (derivadas)

# ==========================================================
# BLOQUE 1: MOTOR DE CÁLCULO SIMBÓLICO
# ==========================================================
# Definimos 'x' como un símbolo matemático
x_simbolo = sp.Symbol('x')

print("-" * 50)
print("SISTEMA DE MÉTODOS NUMÉRICOS: NEWTON-RAPHSON (AUTO-DERIVADA)")
print("-" * 50)

# Entrada de datos
f_texto = input("Introduce f(x) (ej: exp(-x) - x): ")
x0 = float(input("Punto inicial x0: "))
tol = float(input("Tolerancia (ej: 1e-8): "))

# --- EL CORAZÓN DEL BLOQUE 1 ---
# Convertimos el texto en una función matemática real y la DERIVAMOS
f_simbolica = sp.sympify(f_texto)
df_simbolica = sp.diff(f_simbolica, x_simbolo) # <--- Aquí ocurre la magia

print(f"\n[INFO] Función interpretada: f(x) = {f_simbolica}")
print(f"[INFO] Derivada calculada: f'(x) = {df_simbolica}")

# Convertimos las funciones simbólicas a funciones rápidas de Python (lambdify)
f_num = sp.lambdify(x_simbolo, f_simbolica, 'numpy')
df_num = sp.lambdify(x_simbolo, df_simbolica, 'numpy')

# ==========================================================
# BLOQUE 2: INICIALIZACIÓN
# ==========================================================
n = 0
error = 1.0
print(f"\n{'Iter':<5} | {'x_n':<12} | {'Error':<12}")
print("-" * 50)

# ==========================================================
# BLOQUE 3: EL CICLO DE NEWTON-RAPHSON
# ==========================================================
while error > tol and n < 50:
    # Evaluamos f(x) y f'(x) en el punto actual
    valor_f = f_num(x0)
    valor_df = df_num(x0)
    
    # Seguro: Si la derivada es 0, no podemos dividir
    if valor_df == 0:
        print("\n[!] ERROR: Derivada cero. La tangente es horizontal.")
        break
        
    # Fórmula de Newton-Raphson
    x_new = x0 - (valor_f / valor_df)
    
    error = abs(x_new - x0)
    n += 1
    
    print(f"{n:<5} | {x_new:<12.9f} | {error:<12.9f}")
    
    x0 = x_new

# ==========================================================
# BLOQUE 4: RESULTADO FINAL
# ==========================================================
print("-" * 50)
print(f"RESULTADO: Raíz encontrada en x = {x0:.9f}")
print(f"CONVERGENCIA: Lograda en {n} iteraciones.")
print("-" * 50)