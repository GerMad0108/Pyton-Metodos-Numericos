import math

def f_libro(x, ecuacion):
    """Evalúa la función y redondea a 4 decimales como el libro."""
    # Usamos math.__dict__ para reconocer exp, log, etc.
    valor = eval(ecuacion, {"x": x, "__builtins__": None}, math.__dict__)
    return round(valor, 4)

def regula_falsi_libro():
    print("--- MÉTODO REGULA FALSI ---")
    
    # 1. Entrada de datos
    ecuacion = input("Ingresa la función f(x) (ej: exp(-x) - log(x)): ")
    a = float(input("Ingresa x1 (a): ")) # 1
    b = float(input("Ingresa x2 (b): ")) # 2
    tol = float(input("Cota de error (ej: 0.001): "))
    
    print(f"\n{'Iter':<5} {'an':<10} {'bn':<10} {'mn':<10} {'f(mn)':<10} {'Error':<10}")
    print("-" * 70)

    m_anterior = 0
    
    # El libro llega a la 20, pondremos un rango amplio
    for n in range(1, 31):
        fa = f_libro(a, ecuacion)
        fb = f_libro(b, ecuacion)
        
        # FÓRMULA DEL LIBRO: mn = (bn*f(an) - an*f(bn)) / (f(an) - f(bn))
        # Aplicamos redondeo a 4 decimales en cada paso de la fórmula
        numerador = round((b * fa) - (a * fb), 4)
        denominador = round(fa - fb, 4)
        m = round(numerador / denominador, 4)
        
        fm = f_libro(m, ecuacion)
        
        # Cálculo del error: |m_n - m_{n-1}|
        if n == 1:
            error_val = abs(b - a) # El primer error suele ser la amplitud
            error_str = "---"
        else:
            error_val = round(abs(m - m_anterior), 4)
            error_str = f"{error_val:.4f}"

        # Imprimir fila de la tabla
        print(f"{n:<5} {a:<10.4f} {b:<10.4f} {m:<10.4f} {fm:<10.4f} {error_str:<10}")

        # Condición de parada
        if n > 1 and error_val < tol:
            print("-" * 70)
            print(f"¡CONVERGENCIA! x = {m:.4f} en la iteración {n}")
            return

        # Lógica de decisión del libro:
        # Si f(an)*f(mn) < 0, la raíz está en [an, mn] -> b se convierte en m
        if fa * fm < 0:
            b = m
        else:
            a = m
            
        m_anterior = m

if __name__ == "__main__":
    regula_falsi_libro()