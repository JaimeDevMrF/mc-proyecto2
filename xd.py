import customtkinter as ctk
import matplotlib.pyplot as plt
import math

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("310x350")
app.title("xd")
app.resizable(False, False)

x = []
y = []

entradax = ctk.CTkEntry(app, placeholder_text="Ingrese punto para x")
entraday = ctk.CTkEntry(app, placeholder_text="Ingrese punto para y")
entradax.grid(column=0, row=0, padx=5, pady=5)
entraday.grid(column=0, row=1, padx=5, pady=5)


recuadro = ctk.CTkTextbox(app, height=200, width=300, state='disabled')
recuadro.grid(column=0, row=3, columnspan=3, padx=5, pady=10)


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
        if eje == "x":
            entradax.delete(0, "end")
        else:
            entraday.delete(0, "end")

def borrar_puntos():
    global x, y
    x = []
    y = []
    actualizar_recuadro()


def promedio(lista):
    return sum(lista) / len(lista)


def calcular_r2(y_real, y_pred):
    prom = promedio(y_real)
    st = sum((yi - prom)**2 for yi in y_real)
    sr = sum((yi - fi)**2 for yi, fi in zip(y_real, y_pred))
    return 1 - sr/st if st != 0 else 1


def resolver_sistema_normal(ecuaciones, terminos):
    n = len(terminos)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(ecuaciones[r][i]))
        ecuaciones[i], ecuaciones[max_row] = ecuaciones[max_row], ecuaciones[i]
        terminos[i], terminos[max_row] = terminos[max_row], terminos[i]
        for j in range(i + 1, n):
            factor = ecuaciones[j][i] / ecuaciones[i][i]
            for k in range(i, n):
                ecuaciones[j][k] -= factor * ecuaciones[i][k]
            terminos[j] -= factor * terminos[i]
    solucion = [0] * n
    for i in reversed(range(n)):
        suma = sum(ecuaciones[i][j] * solucion[j] for j in range(i+1, n))
        solucion[i] = (terminos[i] - suma) / ecuaciones[i][i]
    return solucion

import math
import matplotlib.pyplot as plt


def calcular_r2(y, y_est):
    suma_total = sum((yi - sum(y)/len(y))**2 for yi in y)
    suma_residual = sum((yi - y_est[i])**2 for i, yi in enumerate(y))
    return 1 - suma_residual / suma_total


def hacer_regresion():
    if len(x) < 2 or len(x) != len(y):
        return

    resultados = {}
    n = len(x)


    sx = sum(x)
    sy = sum(y)
    sxx = sum(xi**2 for xi in x)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    denom = n * sxx - sx**2
    if denom != 0:
        a = (n * sxy - sx * sy) / denom
        b = (sy * sxx - sx * sxy) / denom
        y_est = [a*xi + b for xi in x]
        r2 = calcular_r2(y, y_est)
        if r2 >= 0.95:
            resultados["Lineal"] = {"r2": r2, "y": lambda xi: a*xi + b, "desc": f"y = {a:.4f}x + {b:.4f}"}

 
    if all(xi > 0 for xi in x):
        lx = [math.log(xi) for xi in x]
        slx = sum(lx)
        slx2 = sum(lxi**2 for lxi in lx)
        sly = sum(y)
        slxy = sum(lxi * yi for lxi, yi in zip(lx, y))
        denom = n * slx2 - slx**2
        if denom != 0:
            a = (n * slxy - slx * sly) / denom
            b = (sly * slx2 - slx * slxy) / denom
            y_est = [a * math.log(xi) + b for xi in x]
            r2 = calcular_r2(y, y_est)
            if r2 >= 0.95:
                resultados["Logarítmica"] = {"r2": r2, "y": lambda xi: a * math.log(xi) + b, "desc": f"y = {a:.4f}ln(x) + {b:.4f}"}


    if all(yi > 0 for yi in y):
        ly = [math.log(yi) for yi in y]
        sxy = sum(xi * lyi for xi, lyi in zip(x, ly))
        sx = sum(x)
        sly = sum(ly)
        sxx = sum(xi**2 for xi in x)
        denom = n * sxx - sx**2
        if denom != 0:
            b = (n * sxy - sx * sly) / denom
            lna = (sly - b * sx) / n
            a = math.exp(lna)
            y_est = [a * math.exp(b * xi) for xi in x]
            r2 = calcular_r2(y, y_est)
            if r2 >= 0.95:
                resultados["Exponencial"] = {"r2": r2, "y": lambda xi: a * math.exp(b * xi), "desc": f"y = {a:.4f}e^({b:.4f}x)"}


    if all(xi > 0 for xi in x) and all(yi > 0 for yi in y):
        lx = [math.log(xi) for xi in x]
        ly = [math.log(yi) for yi in y]
        slx = sum(lx)
        sly = sum(ly)
        slx2 = sum(lxi**2 for lxi in lx)
        slxly = sum(lxi * lyi for lxi, lyi in zip(lx, ly))
        denom = n * slx2 - slx**2
        if denom != 0:
            b = (n * slxly - slx * sly) / denom
            lna = (sly - b * slx) / n
            a = math.exp(lna)
            y_est = [a * xi**b for xi in x]
            r2 = calcular_r2(y, y_est)
            if r2 >= 0.95:
                resultados["Potencial"] = {"r2": r2, "y": lambda xi: a * xi**b, "desc": f"y = {a:.4f}x^{b:.4f}"}


    for nombre, datos in resultados.items():
        print(f"\nRegresión con R² = {round(datos['r2'], 4)}: {nombre}")
        print("Ecuación:", datos['desc'])
        print("R²:", round(datos['r2'], 4))

        x_vals = [min(x) + i*(max(x)-min(x))/200 for i in range(201)]
        y_vals = [datos['y'](xi) for xi in x_vals]
        plt.scatter(x, y, color='blue', label='Datos')
        plt.plot(x_vals, y_vals, color='red', label=nombre)
        plt.title(f"Mejor ajuste: {nombre}\n{datos['desc']}\nR² = {datos['r2']:.4f}")
        plt.legend()
        plt.grid(True)
        plt.show()
        break


  
    for nombre, datos in resultados.items():
        if datos['r2'] >= 0.95:  
            print(f"\nRegresión con R² >= 0.95: {nombre}")
            print("Ecuación:", datos['desc'])
            print("R²:", round(datos['r2'], 4))

            x_vals = [min(x) + i*(max(x)-min(x))/200 for i in range(201)]
            y_vals = [datos['y'](xi) for xi in x_vals]
            plt.scatter(x, y, color='blue', label='Datos')
            plt.plot(x_vals, y_vals, color='red', label=nombre)
            plt.title(f"Ajuste: {nombre}\n{datos['desc']}\nR² = {datos['r2']:.4f}")
            plt.legend()
            plt.grid(True)
            plt.show()
            break


def presionar_enter(boton):
    registrar_punto("x")
    registrar_punto("y")

entradax.bind("<Return>", presionar_enter)
entraday.bind("<Return>", presionar_enter)


botonborrar = ctk.CTkButton(app, text="Borrar puntos", command=borrar_puntos)
botonregresion = ctk.CTkButton(app, text="Evaluar regresión", command=hacer_regresion)

botonborrar.grid(column=2, row=1, padx=5, pady=5)
botonregresion.grid(column=2, row=0, padx=5, pady=5)

app.mainloop()
