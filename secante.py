import numpy as np

# ==========================================================
# BLOQUE 1: DEFINICIÓN Y ENTRADA (SET-UP)
# ==========================================================
def f(x_val, ecuacion_texto):
    """Evalúa la función matemática ingresada como texto"""
    contexto = {"x": x_val, "np": np}
    return eval(ecuacion_texto, {"__builtins__": None}, contexto)

print("-" * 45)
print("SISTEMA DE MÉTODOS NUMÉRICOS: MÉTODO DE LA SECANTE")
print("-" * 45)

# Datos de entrada según el Ejemplo 2.3 del libro
ecuacion = input("Introduce f(x) (ej: np.exp(-x) - np.log(x)): ")
x0 = float(input("Punto inicial x0: "))
x1 = float(input("Punto inicial x1: "))
tol = float(input("Tolerancia (ej: 1e-7): "))

# ==========================================================
# BLOQUE 2: VALIDACIÓN DE PENDIENTE
# ==========================================================
# En la secante no validamos Bolzano, validamos que no haya división por cero
if f(x0, ecuacion) == f(x1, ecuacion):
    print("\n[!] ERROR: f(x0) y f(x1) son iguales. División por cero.")
else:
    # ==========================================================
    # BLOQUE 3 Y 4: ITERACIÓN Y CONTROL DE CONVERGENCIA
    # ==========================================================
    n = 1
    print(f"\n{'Iter':<5} | {'x_n+1':<12} | {'Error':<12}")
    print("-" * 45)

    while True:
        # Calculamos los valores de la función en los puntos actuales
        fx0 = f(x0, ecuacion)
        fx1 = f(x1, ecuacion)

        # Paso A: Fórmula de la Secante para hallar x_n+1
        # x_n+1 = x1 - (f(x1) * (x0 - x1)) / (f(x0) - f(x1))
        x_new = x1 - (fx1 * (x0 - x1)) / (fx0 - fx1)
        
        # Paso B: Cálculo del Error (Cota de error permisible)
        error = abs(x_new - x1)

        print(f"{n+1:<5} | {x_new:<12.7f} | {error:<12.7f}")

        # Condición de Parada
        if error < tol:
            break
        
        # Paso C: Actualización de valores para la siguiente sucesión
        # El x0 viejo desaparece, el x1 viejo ahora es x0, y el nuevo es x1
        x0 = x1
        x1 = x_new
        n += 1

        # Seguridad para evitar bucles infinitos en métodos abiertos
        if n > 100:
            print("\n[!] El método no converge tras 100 iteraciones.")
            break

    # ==========================================================
    # BLOQUE 5: SALIDA DE RESULTADOS
    # ==========================================================
    print("-" * 45)
    print(f"RESULTADO: Raíz encontrada en x = {x_new:.7f}")
    print(f"CONVERGENCIA: Lograda en {n} iteraciones.")
    print("-" * 45)