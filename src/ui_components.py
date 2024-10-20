import tkinter as tk
from tkinter import messagebox
from user_management import UserManager

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Club")

        # Inicializar UserManager
        self.user_manager = UserManager("data/video_club.db")

        # Crear contenedor principal
        self.container = tk.Frame(self.master)
        self.container.pack()

        # Crear botones principales
        self.create_main_buttons()

    def create_main_buttons(self):
        """Crear botones para elegir entre registro e inicio de sesión"""
        # Limpiar el contenedor
        self.clear_frame()

        # Crear botones
        tk.Button(self.container, text="Registrar", command=self.show_register).pack(pady=10)
        tk.Button(self.container, text="Iniciar sesión", command=self.show_login).pack(pady=10)

    def show_register(self):
        """Muestra los campos de registro en la ventana principal"""
        self.clear_frame()

        # Etiquetas y campos de entrada
        tk.Label(self.container, text="Nombre de usuario").pack()
        username_entry = tk.Entry(self.container)
        username_entry.pack()

        tk.Label(self.container, text="Contraseña").pack()
        password_entry = tk.Entry(self.container, show="*")
        password_entry.pack()

        tk.Label(self.container, text="Correo electrónico").pack()
        email_entry = tk.Entry(self.container)
        email_entry.pack()

        # Botón para registrar
        tk.Button(self.container, text="Registrar", command=lambda: self.register_user(username_entry.get(), password_entry.get(), email_entry.get())).pack(pady=10)

        # Botón para volver
        tk.Button(self.container, text="Volver", command=self.create_main_buttons).pack(pady=10)

    def register_user(self, username, password, email):
        """Registra el usuario"""
        reg = self.user_manager.register_user(username, password, email)
        if reg:
            messagebox.showinfo("Éxito", "Registro exitoso")
            self.create_main_buttons()  # Volver a la pantalla principal
        else:
            messagebox.showerror("Error", "Registro incorrecto")

    def show_login(self):
        """Muestra los campos de inicio de sesión en la ventana principal"""
        self.clear_frame()

        # Etiquetas y campos de entrada
        tk.Label(self.container, text="Nombre de usuario").pack()
        username_entry = tk.Entry(self.container)
        username_entry.pack()

        tk.Label(self.container, text="Contraseña").pack()
        password_entry = tk.Entry(self.container, show="*")
        password_entry.pack()

        # Botón para iniciar sesión
        tk.Button(self.container, text="Iniciar sesión", command=lambda: self.login_user(username_entry.get(), password_entry.get())).pack(pady=10)

        # Botón para volver
        tk.Button(self.container, text="Volver", command=self.create_main_buttons).pack(pady=10)

    def login_user(self, username, password):
        """Inicia sesión"""
        user = self.user_manager.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.create_main_buttons()  # Volver a la pantalla principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def clear_frame(self):
        """Eliminar todos los widgets actuales del contenedor"""
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
