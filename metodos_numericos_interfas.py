import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MetodosNumericosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Métodos Numéricos")
        self.root.geometry("1300x750")

        self.metodo = tk.StringVar(value="Bisección")
        self.funcion = tk.StringVar(value="exp(-x) - x")

        self.setup_ui()

    # ================= UI =================
    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        # PANEL IZQUIERDO
        left = ttk.Frame(self.root, padding=10)
        left.grid(row=0, column=0, sticky="nsew")

        ttk.Label(left, text="MÉTODOS NUMÉRICOS", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(left, text="Método:").pack(anchor="w")
        metodo_box = ttk.Combobox(
            left,
            textvariable=self.metodo,
            state="readonly",
            values=["Bisección", "Falsa Posición", "Secante", "Punto Fijo", "Newton"]
        )
        metodo_box.pack(fill="x")
        metodo_box.bind("<<ComboboxSelected>>", self.actualizar_parametros)

        ttk.Label(left, text="Función:").pack(anchor="w", pady=(10, 0))
        ttk.Entry(left, textvariable=self.funcion).pack(fill="x")

        self.param_frame = ttk.LabelFrame(left, text="Parámetros")
        self.param_frame.pack(fill="x", pady=10)

        # TABLA
        self.tabla = ttk.Treeview(left, show="headings", height=12)
        self.tabla.pack(fill="both", expand=True)

        ttk.Button(left, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado = ttk.Label(left, text="Resultado: ---", font=("Arial", 11, "bold"))
        self.resultado.pack()

        # PANEL DERECHO (GRÁFICA)
        self.grafico_frame = ttk.Frame(self.root)
        self.grafico_frame.grid(row=0, column=1, sticky="nsew")

        self.actualizar_parametros()

    # ================= TABLA DINÁMICA =================
    def configurar_tabla(self, columnas):
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = columnas

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=100)

    # ================= PARAMETROS =================
    def actualizar_parametros(self, event=None):
        for w in self.param_frame.winfo_children():
            w.destroy()

        self.entries = {}

        def add(label):
            frame = ttk.Frame(self.param_frame)
            frame.pack(fill="x", pady=2)

            ttk.Label(frame, text=label, width=10, anchor="w").pack(side="left")

            e = ttk.Entry(frame)
            e.pack(side="left", padx=5)

            self.entries[label] = e

        metodo = self.metodo.get()

        if metodo in ["Bisección", "Falsa Posición"]:
            add("a")
            add("b")
            add("Tol")

        elif metodo == "Secante":
            add("x0")
            add("x1")
            add("Tol")

        elif metodo == "Punto Fijo":
            add("x0")
            add("Tol")
            add("MaxIter")

        elif metodo == "Newton":
            ttk.Label(self.param_frame, text="f'(x):").pack(anchor="w")
            self.derivada_label = ttk.Label(self.param_frame, text="---")
            self.derivada_label.pack(anchor="w", pady=(0, 5))

            add("x0")
            add("Tol")

    # ================= FUNCIÓN =================
    def f(self, x):
        return eval(self.funcion.get(), {"__builtins__": None},
                    {"x": x, "np": np, "exp": np.exp, "sin": np.sin,
                     "cos": np.cos, "log": np.log, "sqrt": np.sqrt})

    # ================= CONTROL =================
    def calcular(self):
        metodo = self.metodo.get()

        try:
            if metodo == "Bisección":
                self.configurar_tabla(("n", "a", "b", "m", "f(m)"))
                self.biseccion()

            elif metodo == "Falsa Posición":
                self.configurar_tabla(("n", "m", "f(m)", "error"))
                self.falsa_posicion()

            elif metodo == "Secante":
                self.configurar_tabla(("n", "x_n", "error"))
                self.secante()

            elif metodo == "Punto Fijo":
                self.configurar_tabla(("n", "x_n", "error"))
                self.punto_fijo()

            elif metodo == "Newton":
                self.configurar_tabla(("n", "x_n", "f(x_n)", "error"))
                self.newton()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= MÉTODOS =================
    def biseccion(self):
        a = float(self.entries["a"].get())
        b = float(self.entries["b"].get())
        tol = float(self.entries["Tol"].get())

        n = 1
        while abs(b - a) > tol:
            m = (a + b) / 2
            fm = self.f(m)

            self.tabla.insert("", "end", values=(n, a, b, m, fm))

            if self.f(a) * fm < 0:
                b = m
            else:
                a = m

            n += 1

        self.resultado.config(text=f"Raíz ≈ {m:.6f}")
        self.graficar(m)

    def falsa_posicion(self):
        a = float(self.entries["a"].get())
        b = float(self.entries["b"].get())
        tol = float(self.entries["Tol"].get())

        m_old = a
        n = 1

        while True:
            m = b - (self.f(b)*(a-b))/(self.f(a)-self.f(b))
            fm = self.f(m)
            error = abs(m - m_old)

            self.tabla.insert("", "end", values=(n, m, fm, error))

            if error < tol:
                break

            if self.f(a)*fm < 0:
                b = m
            else:
                a = m

            m_old = m
            n += 1

        self.resultado.config(text=f"Raíz ≈ {m:.6f}")
        self.graficar(m)

    def secante(self):
        x0 = float(self.entries["x0"].get())
        x1 = float(self.entries["x1"].get())
        tol = float(self.entries["Tol"].get())

        n = 1
        while True:
            x_new = x1 - (self.f(x1)*(x0-x1))/(self.f(x0)-self.f(x1))
            error = abs(x_new - x1)

            self.tabla.insert("", "end", values=(n, x_new, error))

            if error < tol:
                break

            x0, x1 = x1, x_new
            n += 1

        self.resultado.config(text=f"Raíz ≈ {x_new:.6f}")
        self.graficar(x_new)

    def punto_fijo(self):
        x0 = float(self.entries["x0"].get())
        tol = float(self.entries["Tol"].get())
        max_iter = int(self.entries["MaxIter"].get())

        n = 1
        for _ in range(max_iter):
            x_new = self.f(x0)
            error = abs(x_new - x0)

            self.tabla.insert("", "end", values=(n, x_new, error))

            if error < tol:
                break

            x0 = x_new
            n += 1

        self.resultado.config(text=f"Raíz ≈ {x_new:.6f}")
        self.graficar(x_new)

    def newton(self):
        x = sp.Symbol('x')
        f_sym = sp.sympify(self.funcion.get())
        df_sym = sp.diff(f_sym, x)

        self.derivada_label.config(text=str(df_sym))

        f_num = sp.lambdify(x, f_sym, 'numpy')
        df_num = sp.lambdify(x, df_sym, 'numpy')

        x0 = float(self.entries["x0"].get())
        tol = float(self.entries["Tol"].get())

        n = 1
        while True:
            fx = f_num(x0)
            dfx = df_num(x0)

            if dfx == 0:
                break

            x_new = x0 - fx/dfx
            error = abs(x_new - x0)

            self.tabla.insert("", "end", values=(n, x_new, fx, error))

            if error < tol:
                break

            x0 = x_new
            n += 1

        self.resultado.config(text=f"Raíz ≈ {x_new:.6f}")
        self.graficar(x_new)

    # ================= GRÁFICA =================
    def graficar(self, raiz):
        for w in self.grafico_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(7, 7))

        x_vals = np.linspace(raiz - 5, raiz + 5, 1000)
        y = []

        for xi in x_vals:
            try:
                y.append(self.f(xi))
            except:
                y.append(np.nan)

        y = np.array(y)

        ax.plot(x_vals, y)
        ax.axvline(raiz, linestyle="--")
        ax.axhline(0)

        ax.set_title("Gráfica")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = MetodosNumericosApp(root)
    root.mainloop()