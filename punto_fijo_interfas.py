import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PuntoFijoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Punto Fijo ")
        self.root.geometry("1200x700")
        
        self.g_texto = tk.StringVar(value="")
        self.x0_val = tk.StringVar(value="")
        self.tol_val = tk.StringVar(value="")
        self.max_iter_val = tk.StringVar(value="")
        
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

        titulo = tk.Label(left_frame, text="Método de Punto Fijo", 
                         font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, pady=10)

        input_frame = ttk.LabelFrame(left_frame, text="Parámetros", padding=10)
        input_frame.grid(row=1, column=0, sticky="ew", pady=10)

        ttk.Label(input_frame, text="g(x):").grid(row=0, column=0)
        ttk.Entry(input_frame, textvariable=self.g_texto, width=25)\
            .grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="x0:").grid(row=1, column=0)
        ttk.Entry(input_frame, textvariable=self.x0_val, width=10)\
            .grid(row=1, column=1, sticky="w")

        ttk.Label(input_frame, text="Tol:").grid(row=2, column=0)
        ttk.Entry(input_frame, textvariable=self.tol_val, width=10)\
            .grid(row=2, column=1, sticky="w")

        ttk.Label(input_frame, text="Max Iter:").grid(row=3, column=0)
        ttk.Entry(input_frame, textvariable=self.max_iter_val, width=10)\
            .grid(row=3, column=1, sticky="w")

        ttk.Button(input_frame, text="Calcular", command=self.calcular)\
            .grid(row=4, column=0, columnspan=2, pady=10)

        # Tabla
        tabla_frame = ttk.LabelFrame(left_frame, text="Iteraciones", padding=10)
        tabla_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        cols = ("n", "x_n", "error")
        self.tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings")
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=90)
        self.tabla.pack(fill=tk.BOTH, expand=True)

        self.resultado_label = tk.Label(left_frame, text="Resultado: ---", font=("Arial", 12, "bold"))
        self.resultado_label.grid(row=3, column=0, pady=10)

        # -------- DERECHA --------
        self.grafico_frame = ttk.Frame(self.root, padding=10)
        self.grafico_frame.grid(row=0, column=1, sticky="nsew")

    # ================= FUNCIÓN SEGURA =================
    def g(self, x):
        safe_dict = {
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "pi": np.pi,
            "e": np.e
        }
        return eval(self.g_texto.get(), {"__builtins__": None}, safe_dict)

    def safe_eval(self, x):
        try:
            return self.g(x)
        except:
            return None

    # ================= MÉTODO PUNTO FIJO =================
    def calcular(self):
        try:
            for i in self.tabla.get_children():
                self.tabla.delete(i)

            x0 = float(self.x0_val.get())
            tol = float(self.tol_val.get())
            max_iter = int(self.max_iter_val.get())

            n = 0
            error = 1

            while error > tol and n < max_iter:
                n += 1

                x_new = self.safe_eval(x0)

                if x_new is None:
                    messagebox.showerror("Error", "Función inválida")
                    return

                error = abs(x_new - x0)

                self.tabla.insert("", "end", values=(
                    n, f"{x_new:.6f}", f"{error:.6f}"
                ))

                x0 = x_new

                if error > 1e10:
                    messagebox.showwarning("Divergencia", "El método diverge")
                    break

            self.resultado_label.config(text=f"Punto fijo ≈ {x0:.6f}")
            self.plot_funcion(x0)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= GRÁFICO =================
    def plot_funcion(self, raiz):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 8))

        x = np.linspace(raiz - 5, raiz + 5, 1000)

        y = []
        for xi in x:
            try:
                y.append(self.g(xi))
            except:
                y.append(np.nan)

        y = np.array(y)

        ax.plot(x, y, label="g(x)")
        ax.plot(x, x, linestyle="--", label="y = x")  # 🔥 clave en punto fijo
        ax.axvline(raiz, linestyle="--", label="Punto fijo")

        ax.grid(True)
        ax.legend()
        ax.set_title("Método de Punto Fijo")

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoFijoApp(root)
    root.mainloop()