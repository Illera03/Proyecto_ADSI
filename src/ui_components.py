import tkinter as tk
from tkinter import messagebox
from user_management import UserManager  # Importar la clase UserManager

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Club")

        # Inicializar UserManager
        self.user_manager = UserManager("data/video_club.db")

        # Crear elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Etiquetas y campos de entrada
        tk.Label(self.master, text="Nombre de usuario").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Contraseña").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Label(self.master, text="Correo electrónico").pack()
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack()

        # Botones
        tk.Button(self.master, text="Registrar", command=self.register_user).pack()
        tk.Button(self.master, text="Iniciar sesión", command=self.login_user).pack()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        self.user_manager.register_user(username, password, email)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_manager.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
