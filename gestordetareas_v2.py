import tkinter as tk
from tkinter import messagebox
from datetime import datetime

tareas = []

# ----------- FUNCIONES DE TAREAS -----------

def mostrar_reloj():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    etiqueta_reloj.config(text=hora_actual)
    etiqueta_reloj.after(1000, mostrar_reloj)

def completar_tarea(texto_label):
    texto_label.config(fg="gray", font=("Arial", 10, "overstrike"))

def eliminar_tarea(tarea):
    if tarea in tareas:
        tareas.remove(tarea)
        mostrar_tareas()
        actualizar_menu_pomodoro()

def borrar_todas_las_tareas():
    if messagebox.askyesno("Confirmación", "¿Estás seguro que querés borrar todas las tareas?"):
        tareas.clear()
        mostrar_tareas()
        actualizar_menu_pomodoro()

def mostrar_ayuda():
    mensaje = (
        "✓: Marca la tarea como completada\n"
        "🗑: Elimina la tarea\n"
        "Podés seleccionar un día y la duración estimada al agregar una tarea."
    )
    messagebox.showinfo("¿Qué significan los íconos?", mensaje)

def agregar_tarea():
    texto = entrada_tarea.get()
    dia = variable_dia.get()
    horas = entrada_horas.get()

    if texto and dia and horas:
        tarea = f"[{dia}] {texto} ({horas}h)"
        tareas.append(tarea)
        mostrar_tareas()
        actualizar_menu_pomodoro()
        entrada_tarea.delete(0, tk.END)
        entrada_horas.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def mostrar_tareas():
    for widget in marco_tareas.winfo_children():
        widget.destroy()

    for tarea in tareas:
        tarea_frame = tk.Frame(marco_tareas, bg="#ffffff", pady=2)
        tarea_frame.pack(fill="x", padx=5, pady=2)

        texto_label = tk.Label(tarea_frame, text=tarea, font=("Arial", 10), bg="#ffffff", anchor="w")
        texto_label.pack(side="left", padx=5, fill="x", expand=True)

        tk.Button(tarea_frame, text="✓", command=lambda l=texto_label: completar_tarea(l),
                  bg="#c0f0c0", font=("Arial", 10, "bold")).pack(side="right", padx=5)

        tk.Button(tarea_frame, text="🗑", command=lambda t=tarea: eliminar_tarea(t),
                  bg="#f5a3a3", font=("Arial", 10)).pack(side="right", padx=2)

# ----------- FUNCIONES POMODORO -----------

def actualizar_menu_pomodoro():
    menu = entry_tarea_pomodoro["menu"]
    menu.delete(0, "end")
    if not tareas:
        menu.add_command(label="Seleccionar tarea", command=lambda: variable_tarea_pomodoro.set("Seleccionar tarea"))
    else:
        for tarea in tareas:
            menu.add_command(label=tarea, command=lambda v=tarea: variable_tarea_pomodoro.set(v))

def cuenta_regresiva(segundos_restantes, modo, siguiente_paso):
    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60
    temporizador_label.config(text=f"{minutos:02d}:{segundos:02d}")

    if modo == "trabajo":
        temporizador_label.config(bg="#b9fbc0")
        modo_label.config(text="Trabajando...", bg="#b9fbc0")
    else:
        temporizador_label.config(bg="#a3daff")
        modo_label.config(text="Descansando...", bg="#a3daff")

    if segundos_restantes > 0:
        ventana.after(1000, cuenta_regresiva, segundos_restantes - 1, modo, siguiente_paso)
    else:
        siguiente_paso()

def iniciar_pomodoro():
    tarea = variable_tarea_pomodoro.get()
    if tarea == "Seleccionar tarea" or tarea not in tareas:
        messagebox.showwarning("Tarea inválida", "Seleccioná una tarea válida.")
        return

    try:
        trabajo = int(entry_trabajo.get())
        descanso = int(entry_descanso.get())
        ciclos = int(entry_ciclos.get())
    except ValueError:
        messagebox.showwarning("Error", "Ingresá números válidos para los tiempos.")
        return

    def ciclo(index):
        if index >= ciclos:
            temporizador_label.config(text="¡Hecho!", bg="#edd9ee")
            modo_label.config(text="Pomodoro finalizado", bg="#edd9ee")
            messagebox.showinfo("Fin", f"Completaste {ciclos} ciclos con la tarea: {tarea}")
            return

        def comenzar_descanso():
            cuenta_regresiva(descanso * 60, "descanso", lambda: ciclo(index + 1))

        cuenta_regresiva(trabajo * 60, "trabajo", comenzar_descanso)

    ciclo(0)

# ----------- INTERFAZ GRÁFICA -----------

ventana = tk.Tk()
ventana.title("Gestor de tareas + Pomodoro")
ventana.geometry("800x650")
ventana.configure(bg="#edd9ee")
ventana.resizable(True, False)

# Reloj en tiempo real
etiqueta_reloj = tk.Label(ventana, font=("Arial", 12), fg="black", bg="#edd9ee")
etiqueta_reloj.pack(anchor="ne", padx=10, pady=5)
mostrar_reloj()

# Entrada de tareas
entrada_frame = tk.Frame(ventana, bg="#edd9ee")
entrada_frame.pack(pady=5)

tk.Label(entrada_frame, text="Tarea:", bg="#edd9ee").grid(row=0, column=0)
entrada_tarea = tk.Entry(entrada_frame, font=("Arial", 10), width=25)
entrada_tarea.grid(row=0, column=1, padx=5)

tk.Label(entrada_frame, text="Día:", bg="#edd9ee").grid(row=0, column=2)
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
variable_dia = tk.StringVar(value=dias[0])
tk.OptionMenu(entrada_frame, variable_dia, *dias).grid(row=0, column=3, padx=5)

tk.Label(entrada_frame, text="Horas:", bg="#edd9ee").grid(row=0, column=4)
entrada_horas = tk.Entry(entrada_frame, font=("Arial", 10), width=5)
entrada_horas.grid(row=0, column=5, padx=5)

tk.Button(entrada_frame, text="Agregar tarea", command=agregar_tarea, bg="#f0b3c6").grid(row=0, column=6, padx=10)

# Botones de ayuda y borrar
botones_frame = tk.Frame(ventana, bg="#edd9ee")
botones_frame.pack(pady=5)

tk.Button(botones_frame, text="❓ Ayuda", command=mostrar_ayuda, bg="#d9d9f3").pack(side="left", padx=10)
tk.Button(botones_frame, text="🗑️ Borrar todo", command=borrar_todas_las_tareas, bg="#f28b82").pack(side="left", padx=10)

# Lista de tareas con scroll
contenedor_canvas = tk.Frame(ventana, bg="#edd9ee")
contenedor_canvas.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(contenedor_canvas, bg="#edd9ee", highlightthickness=0)
scrollbar = tk.Scrollbar(contenedor_canvas, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

marco_tareas = tk.Frame(canvas, bg="#edd9ee")
canvas.create_window((0, 0), window=marco_tareas, anchor="nw", tags="marco_tareas")

def actualizar_scroll(event): canvas.configure(scrollregion=canvas.bbox("all"))
marco_tareas.bind("<Configure>", actualizar_scroll)
canvas.bind("<Configure>", lambda e: canvas.itemconfig("marco_tareas", width=e.width))

# Pomodoro visual
pomodoro_frame = tk.LabelFrame(ventana, text="Pomodoro", bg="#edd9ee", font=("Arial", 10, "bold"))
pomodoro_frame.pack(fill="x", padx=10, pady=10)

tk.Label(pomodoro_frame, text="Tarea:", bg="#edd9ee").grid(row=0, column=0)
variable_tarea_pomodoro = tk.StringVar(value="Seleccionar tarea")
entry_tarea_pomodoro = tk.OptionMenu(pomodoro_frame, variable_tarea_pomodoro, "Seleccionar tarea")
entry_tarea_pomodoro.grid(row=0, column=1)

tk.Label(pomodoro_frame, text="Trabajo (min):", bg="#edd9ee").grid(row=0, column=2)
entry_trabajo = tk.Entry(pomodoro_frame, width=5)
entry_trabajo.grid(row=0, column=3)

tk.Label(pomodoro_frame, text="Descanso (min):", bg="#edd9ee").grid(row=0, column=4)
entry_descanso = tk.Entry(pomodoro_frame, width=5)
entry_descanso.grid(row=0, column=5)

tk.Label(pomodoro_frame, text="Ciclos:", bg="#edd9ee").grid(row=0, column=6)
entry_ciclos = tk.Entry(pomodoro_frame, width=5)
entry_ciclos.grid(row=0, column=7)

tk.Button(pomodoro_frame, text="Iniciar Pomodoro", command=iniciar_pomodoro, bg="#b2fab4").grid(row=0, column=8, padx=10)

# Temporizador visual
temporizador_label = tk.Label(pomodoro_frame, text="", font=("Arial", 24, "bold"), bg="#edd9ee", fg="black")
temporizador_label.grid(row=1, column=0, columnspan=9, pady=10)

modo_label = tk.Label(pomodoro_frame, text="", font=("Arial", 12, "italic"), bg="#edd9ee", fg="black")
modo_label.grid(row=2, column=0, columnspan=9)

# Iniciar loop
ventana.mainloop()
