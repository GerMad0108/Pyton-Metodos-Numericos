import sympy as sp

def ejecutar_newton_raphson():
    # 1. Configuración de la variable
    x = sp.symbols('x')
    
    print("==============================================")
    print("   METODO DE NEWTON-RAPHSON (CON ERROR %)    ")
    print("==============================================")
    
    expr_input = input("1. Introduce f(x) (ej: exp(-x) - x): ")
    
    try:
        # Convertir texto a función matemática
        f = sp.sympify(expr_input)
        f_der = sp.diff(f, x) # Derivada automática
        
        print(f"\nFunción definida: f(x) = {f}")
        print(f"Derivada calculada: f'(x) = {f_der}")
        print("----------------------------------------------")

        # 2. Entrada de parámetros
        x0 = float(input("2. Punto inicial (x0): "))
        tol = float(input("3. Tolerancia (ej: 0.0001): "))
        max_iter = 50
        
        # Convertir a funciones numéricas rápidas
        f_num = sp.lambdify(x, f)
        f_der_num = sp.lambdify(x, f_der)

        # 3. Encabezado de la tabla
        print(f"\n{'Iter (i)':<8} | {'Raíz (xr)':<18} | {'Error (%)':<15}")
        print("-" * 45)
        
        # Iteración 0
        print(f"{0:<8} | {x0:<18.10f} | {'---':<15}")

        # 4. Bucle de cálculo
        for i in range(1, max_iter + 1):
            val_f = f_num(x0)
            val_f_der = f_der_num(x0)

            if abs(val_f_der) < 1e-15:
                print("\n❌ Error: La derivada es cero. El método no puede continuar.")
                return

            # Fórmula de Newton-Raphson
            x1 = x0 - val_f / val_f_der
            
            # Cálculo del Error Relativo Porcentual
            if x1 != 0:
                error_rel = abs((x1 - x0) / x1) * 100
            else:
                error_rel = 100

            # Imprimir fila
            print(f"{i:<8} | {x1:<18.10f} | {error_rel:<15.8f}")

            # Condición de parada
            if error_rel < tol:
                print("-" * 45)
                print(f"¡CONVERGENCIA ALCANZADA!")
                print(f"LA RAÍZ ES: {x1:.10f}")
                print(f"Total de iteraciones: {i}")
                return
            
            x0 = x1

        print("\n⚠️ Se alcanzó el máximo de iteraciones sin llegar a la tolerancia.")

    except Exception as e:
        print(f"\n❌ Error en la entrada: {e}")

if __name__ == "__main__":
    ejecutar_newton_raphson()