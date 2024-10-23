import tkinter as tk
from tkinter import messagebox
from user_management import UserManager

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Club")

        # Inicializar UserManager
        self.user_manager = UserManager("data/video_club.db")

        # Variables para almacenar el estado del usuario
        self.logged_in_user = None
        self.logged_in_role = None

        # Crear contenedor principal
        self.container = tk.Frame(self.master)
        self.container.pack()

        # Crear botones principales
        self.create_main_buttons()

    def create_main_buttons(self):
        """Crear botones para elegir entre registro e inicio de sesión"""
        self.clear_frame()

        # Botones para registro y login
        tk.Button(self.container, text="Registrar", command=self.show_register).pack(pady=10)
        tk.Button(self.container, text="Iniciar sesión", command=self.show_login).pack(pady=10)

    def show_register(self):
        """Muestra los campos de registro en la ventana principal"""
        self.clear_frame()

        tk.Label(self.container, text="Nombre de usuario").pack()
        username_entry = tk.Entry(self.container)
        username_entry.pack()

        tk.Label(self.container, text="Contraseña").pack()
        password_entry = tk.Entry(self.container, show="*")
        password_entry.pack()

        tk.Label(self.container, text="Correo electrónico").pack()
        email_entry = tk.Entry(self.container)
        email_entry.pack()

        tk.Button(self.container, text="Registrar", command=lambda: self.register_user(username_entry.get(), password_entry.get(), email_entry.get())).pack(pady=10)
        tk.Button(self.container, text="Volver", command=self.create_main_buttons).pack(pady=10)

    def register_user(self, username, password, email):
        """Registra el usuario"""
        reg = self.user_manager.register_user(username, password, email)
        if reg:
            messagebox.showinfo("Éxito", "Registro exitoso")
            self.create_main_buttons()
        else:
            messagebox.showerror("Error", "Registro incorrecto")

    def show_login(self):
        """Muestra los campos de inicio de sesión en la ventana principal"""
        self.clear_frame()

        tk.Label(self.container, text="Nombre de usuario").pack()
        username_entry = tk.Entry(self.container)
        username_entry.pack()

        tk.Label(self.container, text="Contraseña").pack()
        password_entry = tk.Entry(self.container, show="*")
        password_entry.pack()

        tk.Button(self.container, text="Iniciar sesión", command=lambda: self.login_user(username_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.container, text="Volver", command=self.create_main_buttons).pack(pady=10)

    def login_user(self, username, password):
        """Inicia sesión"""
        user = self.user_manager.authenticate_user(username, password)
        if user:
            # Guardar el usuario y su rol
            self.logged_in_user = user['username']
            self.logged_in_role = user['role']  # Supongamos que el rol está en la columna 'role'

            messagebox.showinfo("Éxito", f"Inicio de sesión exitoso. Rol: {self.logged_in_role}")
            self.show_user_menu()  # Mostrar las opciones dependiendo del rol
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def show_user_menu(self):
        """Muestra el menú de opciones según el rol"""
        self.clear_frame()

        tk.Label(self.container, text=f"Bienvenido, {self.logged_in_user}").pack(pady=10)

        if self.logged_in_role == "admin":
            tk.Button(self.container, text="Gestión de usuarios", command=self.admin_manage_users).pack(pady=10)
            tk.Button(self.container, text="Gestión de películas", command=self.admin_manage_movies).pack(pady=10)
        
        if self.logged_in_role == "user":
            tk.Button(self.container, text="Alquilar películas", command=self.user_rent_movies).pack(pady=10)
            tk.Button(self.container, text="Ver mis alquileres", command=self.user_view_rentals).pack(pady=10)
            tk.Button(self.container, text="Actualizar datos personales", command=self.user_update_info).pack(pady=10)
            tk.Button(self.container, text="Solicitar película", command=self.user_request_movies).pack(pady=10)

        # Botón para cerrar sesión
        tk.Button(self.container, text="Cerrar sesión", command=self.logout_user).pack(pady=10)

    def admin_manage_users(self):
        """Función del administrador para gestionar usuarios"""
        messagebox.showinfo("Admin", "Función de gestión de usuarios")

    def admin_manage_movies(self):
        """Función del administrador para gestionar películas"""
        messagebox.showinfo("Admin", "Función de gestión de películas")

    def user_rent_movies(self):
        """Función del usuario para alquilar películas"""
        messagebox.showinfo("Usuario", command=self.rent_user_movies).pack(pady=10)

    def user_view_rentals(self):
        """Función del usuario para ver sus alquileres"""
        messagebox.showinfo("Usuario", "Función para ver alquileres")
        
    def user_update_info(self):
        """Función del usuario para actualizar su información personal"""
        self.clear_frame()

        # Obtener la información actual del usuario desde la base de datos
        user_info = self.user_manager.get_user_info(self.logged_in_user)

        # Mostrar campos con los datos actuales
        tk.Label(self.container, text="Actualizar información personal").pack(pady=10)

        tk.Label(self.container, text="Nombre de usuario").pack()
        username_entry = tk.Entry(self.container)
        username_entry.insert(0, user_info['username'])  # Mostrar el nombre actual
        username_entry.pack()

        tk.Label(self.container, text="Correo electrónico").pack()
        email_entry = tk.Entry(self.container)
        email_entry.insert(0, user_info['email'])  # Mostrar el email actual
        email_entry.pack()

        tk.Label(self.container, text="Nueva contraseña (opcional)").pack()
        password_entry = tk.Entry(self.container, show="*")  # Campo de nueva contraseña (opcional)
        password_entry.pack()

        # Botón para guardar los cambios
        tk.Button(self.container, text="Actualizar", command=lambda: self.update_user_info(username_entry.get(), email_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)

    def update_user_info(self, username, email, password):
        """Actualizar la información del usuario en la base de datos"""
        if password:
            success = self.user_manager.update_user_info(self.logged_in_user, username, email, password)
        else:
            success = self.user_manager.update_user_info(self.logged_in_user, username, email)

        if success:
            messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
            self.show_user_menu()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información.")
    
    def user_request_movies(self):
        self.clear_frame()
        tk.Label(self.container, text="Nombre de la pelcula").pack()
        film_entry = tk.Entry(self.container)
        film_entry.pack()
        tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)
        

    def logout_user(self):
        """Cerrar sesión"""
        self.logged_in_user = None
        self.logged_in_role = None
        messagebox.showinfo("Cerrar sesión", "Has cerrado sesión")
        self.create_main_buttons()

    def clear_frame(self):
        """Eliminar todos los widgets actuales del contenedor"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def rent_user_movies(self):
            """Función para ver las películas disponibles"""
            self.clear_frame()
            tk.Label(self.container, text="Películas disponibles").pack(pady=10)

            movies = self.user_manager.get_all_movies() # Supongamos que esta función devuelve una lista de diccionarios con las películas


            for movie in movies:
                movie_info = f"ID: {movie['id']} - Título: {movie['title']} - Año: {movie['year']}"
                tk.Label(self.container, text=movie_info).pack()

            tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)

    def get_all_movies(self):
        """Obtener todas las películas de la base de datos"""
        cursor = self.user_manager.connection.cursor()
        cursor.execute("SELECT id, title, year FROM Movies")
        movies = cursor.fetchall()

        movie_list = []
        for movie in movies:
            movie_list.append({'id': movie[0], 'title': movie[1], 'year': movie[2]})

        return movie_list
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

