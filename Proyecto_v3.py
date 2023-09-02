from sympy import symbols, diff, simplify
from tkinter import messagebox
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import lambdify, Symbol, symbols, simplify
import sympy as sp

ventanas_abiertas = []
entry_funcion = None
entry_learning_rate = None
entry_momentum = None
entry_epochs = None

def volver_a_inicio(ventana_actual):
    ventana_actual.destroy()
    mostrar_ventana_inicial()

def cerrar_ventanas():
    for ventana in ventanas_abiertas:
        ventana.destroy()

def borrar_datos_entrada():
    entry_funcion.delete(0, 'end')
    entry_learning_rate.delete(0, 'end')
    entry_momentum.delete(0, 'end')
    entry_epochs.delete(0, 'end')


def compute_gradient(x, funcion):
    try:
        x_symbol = symbols('x')
        funcion_symbol = simplify(funcion)
        gradient = diff(funcion_symbol, x_symbol)
        gradient_func = lambdify(x_symbol, gradient, 'numpy')
        return gradient_func(x)
    except Exception as e:
        messagebox.showerror("Error", "La función ingresada no es válida.")
        return None

def compute_simpsons_rule(a, b, n, funcion):
    try:
        x = Symbol('x')
        delta_x = (b - a) / n

        if delta_x == 0:
            messagebox.showerror("Error", "El valor de delta_x es igual a cero, lo que provocaría una división por cero.")
            return None

        suma = funcion.subs(x, a) + funcion.subs(x, b)

        for i in range(1, n):
            xi = a + i * delta_x

            if i % 2 == 0:
                suma += 2 * funcion.subs(x, xi)
            else:
                suma += 4 * funcion.subs(x, xi)

        resultado = delta_x / 3 * suma
        return resultado
    except Exception as e:
        return None

def mostrar_ventana_metodo(opcion_seleccionada, funcion):
    ventana_metodo = Toplevel()
    ventana_metodo.title("Seleccione Método")
    ventanas_abiertas.append(ventana_metodo)

    ventana_metodo.geometry("400x250")
    center_window(ventana_metodo, 400, 250)
    label_metodo = Label(ventana_metodo, text="Seleccione un método:", font=("Arial", 14))
    label_metodo.pack(pady=15)

    metodo_var = StringVar()

    if opcion_seleccionada == "Derivar":
        metodo_var.set("Descenso de Gradiente Estocástico")
        metodo_radio1 = Radiobutton(ventana_metodo, text="Descenso de Gradiente Estocástico", variable=metodo_var, value="Descenso de Gradiente Estocástico")
        metodo_radio2 = Radiobutton(ventana_metodo, text="Momentum", variable=metodo_var, value="Momentum")
    else:
        metodo_var.set("Suma de Riemann")
        metodo_radio1 = Radiobutton(ventana_metodo, text="Suma de Riemann", variable=metodo_var, value="Suma de Riemann")
        metodo_radio2 = Radiobutton(ventana_metodo, text="Simpson", variable=metodo_var, value="Simpson")

    metodo_radio1.pack()
    metodo_radio2.pack()

    def continuar():
        metodo_seleccionado = metodo_var.get()
        ventana_metodo.destroy()
        if metodo_seleccionado == "Simpson" or metodo_seleccionado == "Suma de Riemann":
            mostrar_ventana_parametros_integra(opcion_seleccionada, metodo_seleccionado, funcion)
        else:
            mostrar_ventana_parametros_deriva(opcion_seleccionada, metodo_seleccionado, funcion)
        

    frame_botones_metodo = Frame(ventana_metodo)
    frame_botones_metodo.pack()

    boton_volver = Button(frame_botones_metodo, text="Volver", font=("Arial", 14), command=lambda: volver_a_inicio(ventana_metodo))
    boton_volver.pack(side=LEFT, pady=10)

    boton_continuar = Button(frame_botones_metodo, text="Continuar", font=("Arial", 14), command=continuar)
    boton_continuar.pack(side=LEFT, pady=10, padx=5)

    boton_salir = Button(ventana_metodo, text="Salir", font=("Arial", 14), command=ventana_metodo.quit)
    boton_salir.pack(pady=15)

def mostrar_ventana_parametros_integra(opcion_seleccionada, metodo_seleccionado, funcion):
    ventana_simpson = Toplevel()
    ventana_simpson.title("Ingrese Parámetros para Simpson")
    ventanas_abiertas.append(ventana_simpson)

    ventana_simpson.geometry("400x250")
    center_window(ventana_simpson, 400, 250)

    label_a = Label(ventana_simpson, text="Valor de a:", font=("Arial", 12))
    label_a.pack()
    entry_a = Entry(ventana_simpson, font=("Arial", 12))
    entry_a.pack()

    label_b = Label(ventana_simpson, text="Valor de b:", font=("Arial", 12))
    label_b.pack()
    entry_b = Entry(ventana_simpson, font=("Arial", 12))
    entry_b.pack()

    label_n = Label(ventana_simpson, text="Número de subintervalos (n):", font=("Arial", 12))
    label_n.pack()
    entry_n = Entry(ventana_simpson, font=("Arial", 12))
    entry_n.pack()

    def calcular_simpson():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            n = int(entry_n.get())
            resultado = compute_simpsons_rule(a, b, n, funcion)
            mostrar_resultado_simpson(resultado, ventana_simpson)
        except Exception as e:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

    boton_calcular = Button(ventana_simpson, text="Calcular", font=("Arial", 14), command=calcular_simpson)
    boton_calcular.pack(pady=10)

    boton_volver = Button(ventana_simpson, text="Volver", font=("Arial", 14), command=lambda: volver_a_inicio(ventana_simpson))
    boton_volver.pack(side=LEFT, pady=10)

    boton_salir = Button(ventana_simpson, text="Salir", font=("Arial", 14), command=ventana_simpson.quit)
    boton_salir.pack(pady=15)

def mostrar_resultado_simpson(resultado, ventana_parametros):
    resultado_label = Label(ventana_parametros, text=f"Resultado de la Regla de Simpson: {round(resultado, 2)}", font=("Arial", 16))
    resultado_label.pack(pady=10)

    boton_salir = Button(ventana_parametros, text="Cerrar", font=("Arial", 14), command=ventana_parametros.quit)
    boton_salir.pack(pady=10)

def mostrar_ventana_parametros_deriva(opcion_seleccionada, metodo_seleccionado, funcion):
    ventana_parametros = Toplevel()
    ventana_parametros.title("Ingrese Parámetros")
    ventanas_abiertas.append(ventana_parametros)

    ventana_parametros.geometry("800x800")
    center_window(ventana_parametros, 800, 800)

    global entry_funcion, entry_learning_rate, entry_momentum, entry_epochs

    label_instrucciones = Label(ventana_parametros, text="Ingrese la función de x:", font=("Arial", 15), fg="blue")
    label_instrucciones.pack(pady=10)

    entry_funcion = Entry(ventana_parametros, font=("Arial", 12))
    entry_funcion.insert(0, funcion)  # Llena la entrada con la función proporcionada
    entry_funcion.pack()

    label_learning_rate = Label(ventana_parametros, text="Learning Rate:", font=("Arial", 12))
    label_learning_rate.pack()
    entry_learning_rate = Entry(ventana_parametros, font=("Arial", 12))
    entry_learning_rate.pack()

    label_momentum = Label(ventana_parametros, text="Momentum:", font=("Arial", 12))
    label_momentum.pack()
    entry_momentum = Entry(ventana_parametros, font=("Arial", 12))
    entry_momentum.pack()

    label_epochs = Label(ventana_parametros, text="Epochs:", font=("Arial", 12))
    label_epochs.pack()
    entry_epochs = Entry(ventana_parametros, font=("Arial", 12))
    entry_epochs.pack()

    def obtener_parametros():
        funcion = entry_funcion.get()
        learning_rate = float(entry_learning_rate.get())
        momentum = float(entry_momentum.get())
        epochs = int(entry_epochs.get())

        borrar_datos_entrada()

        min_x, min_y = mostrar_resultado_derivar(funcion, learning_rate, momentum, epochs, metodo_seleccionado, ventana_parametros)

        if min_x is not None and min_y is not None:
            plt.annotate(f'Min: ({min_x:.2f}, {min_y:.2f})', xy=(min_x, min_y), xytext=(min_x + 1, min_y + 10),
                         arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='red')



    frame_botones_parametro = Frame(ventana_parametros)
    frame_botones_parametro.pack()

    boton_volver = Button(frame_botones_parametro, text="Volver", font=("Arial", 14), command=lambda: volver_a_inicio(ventana_parametros))
    boton_volver.pack(side=LEFT, pady=10)

    boton_continuar = Button(frame_botones_parametro, text="Continuar", font=("Arial", 14), command=obtener_parametros)
    boton_continuar.pack(pady=10)

    boton_salir = Button(ventana_parametros, text="Salir", font=("Arial", 14), command=ventana_parametros.quit)
    boton_salir.pack(pady=15)

def mostrar_resultado_derivar(funcion, learning_rate, momentum, epochs, metodo_seleccionado, ventana_parametros):
    resultado_label = Label(ventana_parametros, text="Resultado del Descenso de Gradiente", font=("Arial", 16))
    resultado_label.pack(pady=10)

    Funcion_label = Label(ventana_parametros, text=f"Función: {funcion}", font=("Arial", 16))
    Funcion_label.pack(pady=10)
    # Parsea la función ingresada por el usuario a una función Python
    def parse_func(x):
        try:
            return eval(funcion.replace("^", "**"))
        except:
            messagebox.showerror("Error", "La función ingresada no es válida.")
            return None

    # Inicializa theta y v
    theta = np.random.rand()  # Puedes cambiar esto a un valor inicial ingresado por el usuario
    v = np.zeros_like(theta)

    theta_history = []

    min_x = None
    min_y = None

    # Itera a través de las épocas
    for epoch in range(epochs):
        gradient = compute_gradient(theta, funcion)  # Calcula el gradiente en el punto actual
        v = momentum * v + learning_rate * gradient  # Actualiza la velocidad con momentum
        theta = theta - v  # Actualiza theta
        theta_history.append(theta)

        if min_x is None or parse_func(theta) < min_y:
            min_x = theta
            min_y = parse_func(theta)

    # Crea un conjunto de valores x para graficar la función
    x_values = np.linspace(-5, 5, 400)
    # Calcula los valores correspondientes de la función
    y_values = [parse_func(x) for x in x_values]

    # Grafica la función
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label='Función')
    plt.scatter(theta_history, [parse_func(theta) for theta in theta_history], c='red', label='Optimización')
    plt.xlabel('Theta')
    plt.ylabel('f(Theta)')
    plt.legend()

    # Muestra la gráfica en la misma ventana de parámetros
    canvas = FigureCanvasTkAgg(plt.gcf(), master=ventana_parametros)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    boton_salir = Button(ventana_parametros, text="Cerrar", font=("Arial", 14), command=ventana_parametros.quit)
    boton_salir.pack(pady=10)

    return min_x, min_y

def center_window(window, width, height): 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def mostrar_ventana_inicial():
    ventana = Tk()
    ventana.title("Calculadora para Derivar o Integrar")

    ventana.geometry("400x200")
    center_window(ventana, 400, 200)
    ventanas_abiertas.append(ventana) 

    label_instrucciones = Label(ventana, text="Seleccione si desea derivar o integrar:", font=("Arial", 14))
    label_instrucciones.pack(pady=15)

    frame_botones = Frame(ventana)
    frame_botones.pack()

    boton_derivacion = Button(frame_botones, text="Derivar", font=("Arial", 14), command=lambda: mostrar_ventana_metodo("Derivar", ""))
    boton_derivacion.pack(side=LEFT, padx=10)

    boton_integracion = Button(frame_botones, text="Integrar", font=("Arial", 14), command=lambda: mostrar_ventana_metodo("Integrar", ""))
    boton_integracion.pack(side=LEFT, padx=10)

    boton_salir = Button(ventana, text="Salir", font=("Arial", 14), command=ventana.quit)
    boton_salir.pack(pady=15)

    for ventana in ventanas_abiertas:
        ventana.protocol("WM_DELETE_WINDOW", ventana.quit)

    ventana.mainloop() 

mostrar_ventana_inicial()

