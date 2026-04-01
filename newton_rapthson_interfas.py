import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewtonRaphsonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Newton-Raphson")
        self.root.geometry("1200x700")
        
        self.f_texto = tk.StringVar(value="exp(-x) - x")
        self.x0_val = tk.StringVar(value="0.5")
        self.tol_val = tk.StringVar(value="1e-6")
        
        self.setup_ui()
    
    # ================= UI =================
    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # -------- IZQUIERDA --------
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

        titulo = tk.Label(left_frame, text="⚡ NEWTON-RAPHSON", 
                         font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, pady=10)

        input_frame = ttk.LabelFrame(left_frame, text="Parámetros", padding=10)
        input_frame.grid(row=1, column=0, sticky="ew", pady=10)

        # f(x)
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0)
        ttk.Entry(input_frame, textvariable=self.f_texto, width=25)\
            .grid(row=0, column=1, pady=5)

        # 🔥 Derivada automática
        ttk.Label(input_frame, text="f'(x):").grid(row=1, column=0)
        self.derivada_label = ttk.Label(input_frame, text="---")
        self.derivada_label.grid(row=1, column=1, sticky="w")

        # x0
        ttk.Label(input_frame, text="x0:").grid(row=2, column=0)
        ttk.Entry(input_frame, textvariable=self.x0_val, width=10)\
            .grid(row=2, column=1, sticky="w")

        # tolerancia
        ttk.Label(input_frame, text="Tol:").grid(row=3, column=0)
        ttk.Entry(input_frame, textvariable=self.tol_val, width=10)\
            .grid(row=3, column=1, sticky="w")

        ttk.Button(input_frame, text="Calcular", command=self.calcular)\
            .grid(row=4, column=0, columnspan=2, pady=10)

        # Tabla
        tabla_frame = ttk.LabelFrame(left_frame, text="Iteraciones", padding=10)
        tabla_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        cols = ("n", "x_n", "f(x_n)", "error")
        self.tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings")
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=80)
        self.tabla.pack(fill=tk.BOTH, expand=True)

        self.resultado_label = tk.Label(left_frame, text="Raíz: ---", font=("Arial", 12, "bold"))
        self.resultado_label.grid(row=3, column=0, pady=10)

        # -------- DERECHA --------
        self.grafico_frame = ttk.Frame(self.root, padding=10)
        self.grafico_frame.grid(row=0, column=1, sticky="nsew")

    # ================= MÉTODO =================
    def calcular(self):
        try:
            for i in self.tabla.get_children():
                self.tabla.delete(i)

            x0 = float(self.x0_val.get())
            tol = float(self.tol_val.get())

            # 🔥 SymPy
            x = sp.Symbol('x')
            f_sym = sp.sympify(self.f_texto.get())
            df_sym = sp.diff(f_sym, x)

            # Mostrar derivada en pantalla
            self.derivada_label.config(text=str(df_sym))

            # Convertir a funciones numéricas
            f_num = sp.lambdify(x, f_sym, 'numpy')
            df_num = sp.lambdify(x, df_sym, 'numpy')

            n = 0
            error = 1

            while error > tol and n < 50:
                fx = f_num(x0)
                dfx = df_num(x0)

                if dfx == 0:
                    messagebox.showerror("Error", "Derivada cero")
                    return

                x_new = x0 - (fx / dfx)
                error = abs(x_new - x0)

                # 🔥 CORRECCIÓN: evaluar en x_new
                fx_new = f_num(x_new)

                self.tabla.insert("", "end", values=(
                    n+1, f"{x_new:.6f}", f"{fx_new:.6f}", f"{error:.6f}"
                ))

                x0 = x_new
                n += 1

            self.resultado_label.config(text=f"Raíz ≈ {x0:.6f}")
            self.plot_funcion(f_num, x0)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= GRÁFICO =================
    def plot_funcion(self, f, raiz):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 8))

        x_vals = np.linspace(raiz - 5, raiz + 5, 1000)

        y = []
        for xi in x_vals:
            try:
                y.append(f(xi))
            except:
                y.append(np.nan)

        y = np.array(y)

        ax.plot(x_vals, y, linewidth=2, label="f(x)")
        ax.axvline(raiz, linestyle="--", label="Raíz")
        ax.axhline(0)

        y_valid = y[np.isfinite(y)]
        if len(y_valid) > 0:
            y_min, y_max = np.min(y_valid), np.max(y_valid)
            margen = (y_max - y_min) * 0.1
            ax.set_ylim(y_min - margen, y_max + margen)

        ax.set_title("Newton-Raphson")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()