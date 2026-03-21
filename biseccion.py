import math

def biseccion_totalmente_interactiva():
    print("--- CALCULADORA DE BISECCIÓN PROFESIONAL ---")
    print("Instrucciones para la función:")
    print(" - Usa 'x' como variable.")
    print(" - Exponencial: exp(x) | Logaritmo natural: log(x)")
    print(" - Potencia: x**2 | Raíz cuadrada: sqrt(x)")
    print("-" * 45)

    # 1. Ingreso de la función como texto
    ecuacion = input("Ingresa la función f(x): ")

    def f(x):
        # Evaluamos el texto ingresado como una expresión matemática
        # math.__dict__ permite usar funciones como exp, log, sin sin escribir 'math.'
        return eval(ecuacion, {"x": x, "__builtins__": None}, math.__dict__)

    # 2. Ingreso de parámetros numéricos
    try:
        a = float(input("Límite inferior (a): "))
        b = float(input("Límite superior (b): "))
        tol = float(input("Tolerancia (ej. 0.001): "))
        max_iter = int(input("Máximo de iteraciones: "))
    except Exception as e:
        print(f"Error en los datos: {e}")
        return

    # 3. Validación de Signos (Teorema de Bolzano)
    try:
        if f(a) * f(b) >= 0:
            print("\n[!] Error: No hay cambio de signo en f(a) y f(b).")
            return
    except Exception as e:
        print(f"Error al evaluar la función: {e}")
        return

    # 4. Tabla de resultados
    print(f"\n{'Iter':<5} {'a':<12} {'b':<12} {'m (Raíz)':<12} {'f(m)':<12} {'Error':<12}")
    print("-" * 80)

    for i in range(1, max_iter + 1):
        m = (a + b) / 2
        fm = f(m)
        error = (b - a) / 2

        print(f"{i:<5} {a:<12.6f} {b:<12.6f} {m:<12.6f} {fm:<12.6g} {error:<12.6f}")

        if error < tol:
            print("-" * 80)
            print(f"¡CONVERGENCIA! Raíz final: {m:.6f}")
            return

        if f(a) * fm < 0:
            b = m
        else:
            a = m

    print("-" * 80)
    print("Se alcanzó el límite de iteraciones.")

if __name__ == "__main__":
    biseccion_totalmente_interactiva()