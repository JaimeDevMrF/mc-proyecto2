import customtkinter as ctk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("800x450")
app.title("Regresiones")
app.resizable(False, False)

x = []
y = []
regresiones = []
indice_regresion = 0
canvas_actual = None

entradax = ctk.CTkEntry(app, placeholder_text="Ingrese punto para x")
entraday = ctk.CTkEntry(app, placeholder_text="Ingrese punto para y")
entradax.grid(column=0, row=0, padx=5, pady=5)
entraday.grid(column=0, row=1, padx=5, pady=5)

recuadro = ctk.CTkTextbox(app, height=200, width=300, state='disabled')
recuadro.grid(column=0, row=3, columnspan=2, padx=5, pady=10)

frame_grafica = tk.Frame(app, width=400, height=400)
frame_grafica.grid(column=2, row=0, rowspan=4, padx=10, pady=10)

mejor_r2 = -1
mejor_index = 0

def actualizar_recuadro():
    recuadro.configure(state='normal')
    recuadro.delete("1.0", "end")
    recuadro.insert("end", "x\t|\ty\n" + "-"*15 + "\n")
    for xi, yi in zip(x, y):
        recuadro.insert("end", f"{xi}\t|\t{yi}\n")
    recuadro.configure(state='disabled')

def registrar_punto(eje):
    try:
        if eje == "x":
            valor = float(entradax.get())
            if valor in x:
                entradax.delete(0, "end")
                return
            x.append(valor)
            entradax.delete(0, "end")
        elif eje == "y":
            valor = float(entraday.get())
            if len(y) == len(x):
                entraday.delete(0, "end")
                return
            y.append(valor)
            entraday.delete(0, "end")
        if len(x) == len(y):
            actualizar_recuadro()
    except:
        entradax.delete(0, "end") if eje == "x" else entraday.delete(0, "end")

def borrar_puntos():
    global x, y, regresiones, indice_regresion, canvas_actual
    x = []
    y = []
    regresiones = []
    indice_regresion = 0
    if canvas_actual:
        canvas_actual.get_tk_widget().destroy()
        canvas_actual = None
    actualizar_recuadro()
    botonsiguiente.configure(state="normal")

def calcular_r2(y, y_est):
    prom = sum(y) / len(y)
    st = sum((yi - prom)**2 for yi in y)
    sr = sum((yi - fi)**2 for yi, fi in zip(y, y_est))
    return 1 - sr/st if st != 0 else 1

def resolver_sistema(matriz, vector):
    n = len(vector)
    for i in range(n):
        max_fila = max(range(i, n), key=lambda k: abs(matriz[k][i]))
        matriz[i], matriz[max_fila] = matriz[max_fila], matriz[i]
        vector[i], vector[max_fila] = vector[max_fila], vector[i]
        for j in range(i + 1, n):
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            vector[j] -= factor * vector[i]
    sol = [0] * n
    for i in range(n - 1, -1, -1):
        sol[i] = (vector[i] - sum(matriz[i][j] * sol[j] for j in range(i + 1, n))) / matriz[i][i]
    return sol

def hacer_regresion():
    global regresiones, mejor_r2, mejor_index
    regresiones = []
    mejor_r2 = -1
    mejor_index = -1

    if len(x) < 2 or len(x) != len(y):
        return

    n = len(x)
    grado = 0

    while True:
        A = [[sum(xi**(i+j) for xi in x) for j in range(grado+1)] for i in range(grado+1)]
        B = [sum(yi * xi**i for xi, yi in zip(x, y)) for i in range(grado+1)]

        coef = resolver_sistema([fila[:] for fila in A], B[:])

        def f(xi, c=coef):
            return sum(c[i] * xi**i for i in range(len(c)))

        y_est = [f(xi) for xi in x]
        r2 = calcular_r2(y, y_est)

        formula = " + ".join([f"{c:.4f}x^{i}" if i > 0 else f"{c:.4f}" for i, c in enumerate(coef)])

        regresiones.append((f"Polinomial grado {grado}", coef, None, r2, f, f"y = {formula}"))

        if r2 > mejor_r2:
            mejor_r2 = r2
            mejor_index = len(regresiones) - 1

        if r2 >= 5:
            break

        grado += 1

        if grado > 20: 
            break

    mostrar_grafica()




def mostrar_grafica():
    global indice_regresion, canvas_actual
    if not regresiones:
        return
    if canvas_actual:
        canvas_actual.get_tk_widget().destroy()

    nombre, a, b, r2, funcion, desc = regresiones[indice_regresion]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.scatter(x, y, color='blue', label='Datos')
    x_vals = [min(x) + i*(max(x)-min(x))/200 for i in range(201)]
    y_vals = [funcion(xi) for xi in x_vals]
    ax.plot(x_vals, y_vals, color='red', label=nombre)
    ax.set_title(f"{desc}\nR² = {r2:.4f}")
    ax.legend()
    ax.grid(True)

    canvas_actual = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas_actual.draw()
    canvas_actual.get_tk_widget().pack()

    if indice_regresion == mejor_index:
        botonsiguiente.configure(state="disabled")
    else:
        botonsiguiente.configure(state="normal")

def siguiente_grafica():
    global indice_regresion
    if regresiones:
        indice_regresion = (indice_regresion + 1) % len(regresiones)
        mostrar_grafica()

botonborrar = ctk.CTkButton(app, text="Borrar puntos", command=borrar_puntos)
botonregresion = ctk.CTkButton(app, text="Evaluar regresión", command=hacer_regresion)
botonsiguiente = ctk.CTkButton(app, text="Siguiente gráfica", command=siguiente_grafica)

botonborrar.grid(column=1, row=1, padx=5, pady=5)
botonregresion.grid(column=1, row=0, padx=5, pady=5)
botonsiguiente.grid(column=0, row=2, columnspan=2, pady=5)

def presionar_enter(event):
    registrar_punto("x")
    registrar_punto("y")

entradax.bind("<Return>", presionar_enter)
entraday.bind("<Return>", presionar_enter)

app.mainloop()
