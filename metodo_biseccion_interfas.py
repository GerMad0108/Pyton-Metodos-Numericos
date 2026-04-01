import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class BiseccionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Bisección")
        self.root.geometry("1200x700")
        
        self.ecuacion_texto = tk.StringVar(value="")
        self.a_val = tk.StringVar(value="")
        self.b_val = tk.StringVar(value="")
        self.tol_val = tk.StringVar(value="")
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # -------- IZQUIERDA --------
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

        titulo = tk.Label(left_frame, text="Método de la Bisección", 
                         font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, pady=10)

        input_frame = ttk.LabelFrame(left_frame, text="Parámetros", padding=10)
        input_frame.grid(row=1, column=0, sticky="ew", pady=10)

        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0)
        ttk.Entry(input_frame, textvariable=self.ecuacion_texto, width=25)\
            .grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="a:").grid(row=1, column=0)
        ttk.Entry(input_frame, textvariable=self.a_val, width=10)\
            .grid(row=1, column=1, sticky="w")

        ttk.Label(input_frame, text="b:").grid(row=2, column=0)
        ttk.Entry(input_frame, textvariable=self.b_val, width=10)\
            .grid(row=2, column=1, sticky="w")

        ttk.Label(input_frame, text="Tol:").grid(row=3, column=0)
        ttk.Entry(input_frame, textvariable=self.tol_val, width=10)\
            .grid(row=3, column=1, sticky="w")

        ttk.Button(input_frame, text="Calcular", command=self.calcular_biseccion)\
            .grid(row=4, column=0, columnspan=2, pady=10)

        # Tabla
        tabla_frame = ttk.LabelFrame(left_frame, text="Iteraciones", padding=10)
        tabla_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        cols = ("n", "a", "b", "m", "f(m)")
        self.tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=70)
        self.tabla.pack(fill=tk.BOTH, expand=True)

        self.resultado_label = tk.Label(left_frame, text="Raíz: ---", font=("Arial", 12, "bold"))
        self.resultado_label.grid(row=3, column=0, pady=10)

        # -------- DERECHA --------
        self.grafico_frame = ttk.Frame(self.root, padding=10)
        self.grafico_frame.grid(row=0, column=1, sticky="nsew")

    # 🔥 FUNCIÓN SEGURA Y FLEXIBLE
    def f(self, x):
        safe_dict = {
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "pi": np.pi,
            "e": np.e
        }
        return eval(self.ecuacion_texto.get(), {"__builtins__": None}, safe_dict)

    def calcular_biseccion(self):
        try:
            for i in self.tabla.get_children():
                self.tabla.delete(i)

            a = float(self.a_val.get())
            b = float(self.b_val.get())
            tol = float(self.tol_val.get())

            a_original, b_original = a, b

            fa, fb = self.safe_eval(a), self.safe_eval(b)

            if fa is None or fb is None or fa * fb > 0:
                messagebox.showerror("Error", "No hay cambio de signo o función inválida")
                return

            n = 0

            while (b - a) > tol:
                n += 1
                m = (a + b) / 2
                fm = self.safe_eval(m)

                self.tabla.insert("", "end", values=(n, f"{a:.4f}", f"{b:.4f}", f"{m:.4f}", f"{fm:.4f}"))

                if fa * fm < 0:
                    b = m
                    fb = fm
                else:
                    a = m
                    fa = fm

            self.resultado_label.config(text=f"Raíz ≈ {m:.6f}")
            self.plot_funcion(a_original, b_original, m)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 🔥 EVALUACIÓN SEGURA (NO ROMPE EL GRÁFICO)
    def safe_eval(self, x):
        try:
            return self.f(x)
        except:
            return None

    def plot_funcion(self, a, b, raiz):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 8))

        rango = abs(b - a)
        x = np.linspace(raiz - rango*2, raiz + rango*2, 1000)

        y = []
        for xi in x:
            try:
                y.append(self.f(xi))
            except:
                y.append(np.nan)

        y = np.array(y)

        ax.plot(x, y, linewidth=2, label="f(x)")
        ax.axvline(raiz, linestyle="--", label="Raíz")
        ax.axhline(0)
        ax.axvspan(a, b, alpha=0.2)

        y_valid = y[np.isfinite(y)]
        if len(y_valid) > 0:
            y_min, y_max = np.min(y_valid), np.max(y_valid)
            margen = (y_max - y_min) * 0.1
            ax.set_ylim(y_min - margen, y_max + margen)

        ax.set_title("Gráfico de la función")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = BiseccionApp(root)
    root.mainloop()