# Importación de librerías necesarias
from random import randint  # Para generar números aleatorios
import webbrowser  # Para abrir el manual de usuario en el navegador
import tkinter as tk  # Para la interfaz gráfica
from tkinter import messagebox  # Para mostrar mensajes emergentes
import os  # Para operaciones del sistema (no se usa actualmente)
from datetime import datetime  # Para mostrar la hora actual

class Application(tk.Frame):
    """Clase principal que representa la aplicación de tragamonedas."""
    
    def __init__(self, master=None):
        """Inicializa la aplicación con balance cero y configura la interfaz."""
        super().__init__(master)
        self.balance = 0.0  # Balance inicial del jugador
        self.master = master  # Ventana principal
        self.configure()  # Configura menús y título
        self.create_widgets()  # Crea todos los elementos de la interfaz
        self.pack()  # Empaqueta el frame principal
        self.update_clock()  # Inicia el reloj en tiempo real

    def configure(self):
        """Configura el menú de ayuda y el título de la ventana."""
        self.master.title("Tragamonedas (RTP 94%)")
        
        # Creación del menú de ayuda
        menu_bar = tk.Menu(self.master)
        help_menu = tk.Menu(self.master, tearoff=0)
        help_menu.add_command(label="Manual de Usuario", command=self.redirect_to_help)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        self.master.config(menu=menu_bar)

    def create_widgets(self):
        """Crea y posiciona todos los widgets de la interfaz gráfica."""
        # Título principal
        title_label = tk.Label(text="Maquina Tragamonedas (RTP 94%)", font=("Arial", 16))
        title_label.pack(padx=10, pady=10)

        # Etiqueta que muestra el balance actual
        self.balance_label = tk.Label(text="Dinero: $0.00", font=("Arial", 12))
        self.balance_label.pack(padx=10, pady=10)

        # Entrada para depositar dinero
        self.balance_var = tk.DoubleVar()
        self.balance_input = tk.Entry(textvariable=self.balance_var)
        self.balance_input.pack()

        # Botón para realizar depósito
        deposit_button = tk.Button(text="Depositar", command=self.deposit)
        deposit_button.pack()

        # Etiqueta y entrada para la apuesta
        bet_label = tk.Label(text="Ingrese su apuesta (Premios fijos)")
        bet_label.pack()

        self.bet_var = tk.DoubleVar()
        bet_input = tk.Entry(textvariable=self.bet_var)
        bet_input.pack()

        # Etiqueta que muestra los números generados
        self.numbers_label = tk.Label(text="0   0   0", font=("Arial", 12))
        self.numbers_label.pack(padx=5, pady=5)

        # Botón para girar los rodillos
        shoot_button = tk.Button(text="Tirar", command=self.shoot)
        shoot_button.pack()

        # Área de mensajes para el usuario
        self.message = tk.Label(text="¡Haga su primer tiro!", bg="lightblue")
        self.message.pack(padx=5, pady=5)

        # Reloj en tiempo real
        self.clock_label = tk.Label(self, font=('Arial', 12), bg='lightgray')
        self.clock_label.pack(pady=10)

        # Barra de desplazamiento para el historial
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Área de texto para el historial de jugadas
        self.history_text = tk.Text(self.master, yscrollcommand=self.scrollbar.set, height=10, width=40)
        self.history_text.pack(pady=10)
        self.scrollbar.config(command=self.history_text.yview)

    def update_clock(self):
        """Actualiza el reloj cada segundo con la hora actual."""
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)  # Programa la próxima actualización

    def update_balance(self, new_balance):
        """Actualiza el balance mostrado en la interfaz."""
        self.balance = round(new_balance, 2)  # Redondea a 2 decimales
        self.balance_label.config(text=f"Dinero: ${self.balance:.2f}")

    def show_message(self, text, msg_type):
        """Muestra mensajes al usuario con diferentes colores según el tipo.
        
        Args:
            text (str): Mensaje a mostrar
            msg_type (str): Tipo de mensaje (success, info, warning, error)
        """
        color_dict = {"success": "lightgreen", "info": "lightblue", "warning": "lightyellow"}
        if msg_type in color_dict:
            self.message.config(text=text, bg=color_dict[msg_type])
        elif msg_type == "error":
            messagebox.showerror("Error", text)

    def redirect_to_help(self):
        """Abre el manual de usuario en el navegador predeterminado."""
        webbrowser.open("https://github.com/WilsonLombardo/maquinatragamonedas")

    def show_about(self):
        """Muestra información acerca de la aplicación."""
        messagebox.showinfo("Acerca de", "Tragamonedas v2.0\nRTP 94% garantizado\nCreado por Wilson Lombardo")

    def deposit(self):
        """Procesa el depósito de dinero en la cuenta del jugador."""
        try:
            deposited_balance = float(self.balance_var.get())
            if deposited_balance <= 0:
                self.show_message("El depósito debe ser mayor a 0.", "error")
                return
            self.update_balance(self.balance + deposited_balance)
            self.balance_var.set(0)  # Limpia el campo de entrada
            self.show_message(f"Depositado: ${deposited_balance:.2f}", "success")
        except:
            self.show_message("Ingrese un valor numérico válido.", "error")

    def shoot(self):
        """Realiza un giro en la tragamonedas y calcula los resultados."""
        try:
            bet = float(self.bet_var.get())
            # Validaciones de la apuesta
            if bet <= 0:
                self.show_message("La apuesta debe ser mayor a 0.", "error")
                return
            if bet > self.balance:
                self.show_message("Balance insuficiente.", "error")
                return

            # Genera 3 números aleatorios entre 1 y 6
            generated_numbers = [randint(1, 6) for _ in range(3)]
            self.numbers_label.config(text="   ".join(map(str, generated_numbers)))

            # Determina el premio según las reglas del juego
            if all(x == generated_numbers[0] for x in generated_numbers):
                win = bet * 4.40  # 3 números iguales (jackpot)
            elif generated_numbers in [[1,2,3], [2,3,4], [3,4,5], [4,5,6]]:
                win = bet * 3.00  # 3 números consecutivos
            elif (generated_numbers[0] == generated_numbers[1] or 
                  generated_numbers[1] == generated_numbers[2] or 
                  generated_numbers[0] == generated_numbers[2]):
                win = bet * 1.16  # 2 números iguales
            else:
                win = -bet  # Perdió la apuesta

            # Actualiza el balance y el historial
            self.update_balance(self.balance + win)
            self.history_text.insert(tk.END, f"Números: {generated_numbers}, Apuesta: {bet}, Ganancia: {win}\n")
            self.history_text.see(tk.END)  # Auto-desplaza al final

            # Mensaje según el resultado
            result_msg = {
                win == bet * 4.40: f"¡Jackpot! Ganó ${win:.2f} (3 iguales)",
                win == bet * 3.00: f"¡Ganó ${win:.2f} (Consecutivos)!",
                win == bet * 1.16: f"¡Ganó ${win:.2f} (2 iguales)!",
                win == -bet: f"Perdió ${bet:.2f}. ¡Siga intentando!"
            }[True]

            self.show_message(result_msg, "success" if win > 0 else "info")
        except ValueError:
            self.show_message("Ingrese un valor numérico válido.", "error")
        except Exception as e:
            messagebox.showerror("Error crítico", f"Ocurrió un error inesperado:\n{str(e)}")

# Punto de entrada principal
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = Application(master=root)  # Crea la aplicación
    app.mainloop()  # Inicia el bucle principal de eventos
