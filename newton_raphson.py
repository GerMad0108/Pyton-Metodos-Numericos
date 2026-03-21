import sympy as sp

def newton_raphson():
    # 1. Definimos la variable simbólica
    x = sp.symbols('x')
    
    print("--- Calculadora de Newton-Raphson ---")
    expr_input = input("Introduce la función f(x) (ejemplo: x**2 - 2 o exp(x) - 3*x): ")
    
    try:
        # Convertimos el texto en una expresión de SymPy
        f = sp.sympify(expr_input)
        # Calculamos la derivada automáticamente
        f_der = sp.diff(f, x)
        
        print(f"f(x) = {f}")
        print(f"f'(x) = {f_der}")

        # 2. Parámetros del método
        x0 = float(input("Punto inicial (x0): "))
        tol = float(input("Tolerancia (ej: 0.0001): "))
        max_iter = 50
        
        # Convertimos las expresiones a funciones de Python rápidas (lambdify)
        f_func = sp.lambdify(x, f)
        f_der_func = sp.lambdify(x, f_der)

        # 3. Bucle de iteración
        for i in range(max_iter):
            fx = f_func(x0)
            fdx = f_der_func(x0)

            if abs(fdx) < 1e-10: # Evitar división por cero
                print("Error: Derivada cercana a cero. El método no converge.")
                return

            x1 = x0 - fx / fdx
            
            print(f"Iteración {i+1}: x = {x1:.6f}")

            # Condición de parada
            if abs(x1 - x0) < tol:
                print(f"\n¡Raíz encontrada! x ≈ {x1:.6f} después de {i+1} iteraciones.")
                return
            
            x0 = x1

        print("\nSe alcanzó el máximo de iteraciones sin converger totalmente.")

    except Exception as e:
        print(f"Error en la expresión: {e}")

# Ejecutar el programa
newton_raphson()