import numpy as np

# ==========================================================
# BLOQUE 1: DEFINICIÓN Y ENTRADA (SET-UP)
# ==========================================================
def f(x_val, ecuacion_texto):
    """Evalúa la función matemática ingresada como texto"""
    contexto = {"x": x_val, "np": np}
    return eval(ecuacion_texto, {"__builtins__": None}, contexto)

print("-" * 40)
print("FALSA POSICIÓN")
print("-" * 40)

# Datos de entrada del usuario
ecuacion = input("Introduce f(x) (ej: np.exp(-x) - np.log(x)): ")
a = float(input("Límite inferior (a): "))
b = float(input("Límite superior (b): "))
tol = float(input("Tolerancia (ej: 0.001): "))

# ==========================================================
# BLOQUE 2: VALIDACIÓN DE BOLZANO (¿EXISTE RAÍZ?)
# ==========================================================
fa = f(a, ecuacion)
fb = f(b, ecuacion)

if fa * fb >= 0:
    print("\n[!] ERROR DE BOLZANO: f(a) y f(b) tienen el mismo signo.")
    print("No se puede garantizar una raíz en este intervalo.")
else:
    # Variables de control
    n = 0
    m_ant = a  # Guardamos el punto anterior para iniciar el error
    
    print(f"\n{'Iter':<5} | {'m_n':<10} | {'f(m_n)':<12} | {'Error':<10}")
    print("-" * 55)

    # ==========================================================
    # BLOQUE 3: EL CICLO DE ITERACIÓN (INTERPOLACIÓN LINEAL)
    # ==========================================================
    while True:
        n += 1
        fa = f(a, ecuacion)
        fb = f(b, ecuacion)

        # Paso A: Fórmula de la Recta Secante (Falsa Posición)
        # m = b - (f(b) * (a - b)) / (f(a) - f(b))
        m = b - (fb * (a - b)) / (fa - fb)
        fm = f(m, ecuacion)
        
        # ==========================================================
        # BLOQUE 4: CONTROL DE CONVERGENCIA (FRENO DE MANO)
        # ==========================================================
        # Calculamos el error comparando con el punto de la iteración anterior
        error = abs(m - m_ant)

        # Imprimimos el progreso en la tabla
        print(f"{n:<5} | {m:<10.6f} | {fm:<12.6f} | {error:<10.6f}")

        # Si el error es menor a la tolerancia, salimos del bucle
        if error < tol:
            break
        
        # Paso C (Bloque 3 cont.): Reasignación de subintervalos
        if fa * fm < 0:
            b = m  # La raíz está a la izquierda del punto m
        else:
            a = m  # La raíz está a la derecha del punto m
            
        m_ant = m  # Actualizamos el valor anterior para la siguiente vuelta

    # ==========================================================
    # BLOQUE 5: SALIDA DE RESULTADOS
    # ==========================================================
    print("-" * 55)
    print(f"RESULTADO: Raíz aproximada encontrada en x = {m:.6f}")
    print(f"CONVERGENCIA: Alcanzada en {n} iteraciones.")
    print("-" * 40)