import numpy as np

# --- BLOQUE 1: INGRESO DE LA FUNCIÓN ---
print("-" * 30)
print("MÉTODO DE BISECCIÓN")
print("-" * 30)

ecuacion_texto = input("Introduce f(x) (ej: x**2 - 2): ")

def f(x_val):
    # Usamos un diccionario para que eval reconozca 'x' y 'np'
    contexto = {"x": x_val, "np": np}
    return eval(ecuacion_texto, {"__builtins__": None}, contexto)

# --- BLOQUE 2: PARÁMETROS DE ENTRADA ---
try:
    a = float(input("Límite inferior (a): "))
    b = float(input("Límite superior (b): "))
    tol = float(input("Tolerancia (ej: 0.0001): "))
    n = 0

    # --- BLOQUE 3: VALIDACIÓN Y LÓGICA ---
    if f(a) * f(b) >= 0:
        print("\n[!] ERROR: No hay cambio de signo (Bolzano no se cumple).")
    else:
        print(f"\n{'Iter':<5} | {'a':<10} | {'b':<10} | {'m':<10} | {'f(m)':<10}")
        print("-" * 55)
    
     #BLOQUE 4: El Bucle de Bisección (Proceso Iterativo)

        while (b - a) > tol:
            n += 1
            m = (a + b) / 2
            
            print(f"{n:<5} | {a:<10.5f} | {b:<10.5f} | {m:<10.5f} | {f(m):<10.5f}")

            if f(a) * f(m) < 0:
                b = m
            else:
                a = m

        # --- BLOQUE 5: RESULTADO ---
        print("-" * 55)
        print(f"RAÍZ APROXIMADA: {m:.6f}")
        print(f"ITERACIONES: {n}")

except Exception as e:
    print(f"Error detectado: {e}")