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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def create_main_buttons(self):
        """Crear botones para elegir entre registro e inicio de sesión"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Botones para registro y login
        tk.Button(self.container, text="Registrar", command=self.show_register).pack(pady=10)
        tk.Button(self.container, text="Iniciar sesión", command=self.show_login).pack(pady=10)

    def show_register(self):
        """Muestra los campos de registro en la ventana principal"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

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
        
        if user == "pendiente":
            messagebox.showwarning("Pendiente", "Tu solicitud de registro está pendiente de aceptación por un administrador.")
        elif user:
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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        tk.Label(self.container, text=f"Bienvenido, {self.logged_in_user}").pack(pady=10)

        if self.logged_in_role == "admin":
            tk.Button(self.container, text="Gestión de peticiones", command=self.admin_manage_users).pack(pady=10)
            tk.Button(self.container, text="Gestión de cuentas", command=self.admin_manage_accounts).pack(pady=10)
        
        if self.logged_in_role == "user":
            tk.Button(self.container, text="Alquilar películas", command=self.user_rent_movies).pack(pady=10)
            tk.Button(self.container, text="Ver mis alquileres", command=self.user_view_rentals).pack(pady=10)
            tk.Button(self.container, text="Actualizar datos personales", command=self.user_update_info).pack(pady=10)
            tk.Button(self.container, text="Solicitar película", command=self.user_request_movies).pack(pady=10)

        # Botón para cerrar sesión
        tk.Button(self.container, text="Cerrar sesión", command=self.logout_user).pack(pady=10)

    def admin_manage_users(self):
        """Función del administrador para gestionar peticiones de usuarios"""
        messagebox.showinfo("Admin", "Función de peticiones de registro")

    def admin_manage_accounts(self):
        """Función del administrador para gestionar cuentas (modificar y eliminar)"""
        messagebox.showinfo("Admin", "Función de gestión de cuentas")

    def user_rent_movies(self):
        """Función del usuario para alquilar películas"""
        messagebox.showinfo("Usuario", command=self.rent_user_movies).pack(pady=10)

    def user_view_rentals(self):
        """Función del usuario para ver sus alquileres"""
        messagebox.showinfo("Usuario", "Función para ver alquileres")
        
    def user_update_info(self):
        """Función del usuario para actualizar su información personal"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

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
        """Función para solicitar una película"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Etiqueta y campo de entrada para la película solicitada
        tk.Label(self.container, text="Introduce el nombre de la película:").pack(pady=10)
        film_entry = tk.Entry(self.container)
        film_entry.pack()

        # Botón para solicitar la película
        tk.Button(self.container, text="Solicitar", command=lambda: self.request_movie_from_api(film_entry.get())).pack(pady=10)

        # Botón para volver al menú de usuario
        tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)

    def request_movie_from_api(self, movie_title):
        """Función para buscar la película en OMDb API y registrar la solicitud"""
        if not movie_title:
            messagebox.showwarning("Error", "Debes introducir el nombre de una película")
            return

        # Llamar a la función para buscar la película en OMDb
        movie_data = self.user_manager.search_movie_omdb(movie_title)

        if movie_data:
            # Si se encuentra la película, se inserta en la base de datos
            self.user_manager.create_movie_request(self.logged_in_user, movie_data['Title'])

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Película '{movie_data['Title']}' solicitada correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró la película en la base de datos OMDb.")
        

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
            self.container.focus_force()  # Asegura que la ventana tenga el foco
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
    
    # Métodos del administrador
    
    def admin_manage_users(self, page=1):
        """Función del administrador para gestionar usuarios con paginación."""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Número de usuarios a mostrar por página
        items_per_page = 5

        # Obtener lista de usuarios pendientes
        pending_users = self.user_manager.get_pending_users()
        total_users = len(pending_users)

        # Calcular el rango de usuarios a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        users_to_show = pending_users[start_index:end_index]

        # Mostrar título de solicitudes pendientes
        tk.Label(self.container, text="Solicitudes pendientes de registro", font=("Arial", 14)).pack(pady=10)

        # Mostrar las solicitudes pendientes de la página actual
        if not users_to_show:
            tk.Label(self.container, text="No hay más solicitudes pendientes").pack(pady=5)
        else:
            for user in users_to_show:
                # Mostrar información del usuario
                user_label = tk.Label(self.container, text=f"Usuario: {user[0]} - Email: {user[1]}", font=("Arial", 12))
                user_label.pack(pady=5)

                # Botón para aceptar el usuario
                accept_button = tk.Button(self.container, text="Aceptar", command=lambda u=user[0]: self.accept_user(u))
                accept_button.pack(pady=2)

                # Botón para rechazar el usuario
                reject_button = tk.Button(self.container, text="Rechazar", command=lambda u=user[0]: self.reject_user(u))
                reject_button.pack(pady=2)

        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)

        # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", command=lambda: self.admin_manage_users(page-1))
            previous_button.pack(side="left", padx=5)

        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_users:
            next_button = tk.Button(nav_frame, text="Siguiente", command=lambda: self.admin_manage_users(page+1))
            next_button.pack(side="right", padx=5)

        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)



    def admin_manage_accounts(self, page=1):
        """Función del administrador para gestionar cuentas de usuario con paginación."""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Número de usuarios a mostrar por página
        items_per_page = 5

        # Obtener todas las cuentas de usuario
        all_users = self.user_manager.get_all_users()
        total_users = len(all_users)

        # Calcular el rango de usuarios a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        users_to_show = all_users[start_index:end_index]

        # Etiqueta del título
        tk.Label(self.container, text="Cuentas de usuarios", font=("Arial", 14)).pack(pady=10)

        # Mostrar las cuentas de usuario de la página actual
        for user in users_to_show:
            # Mostrar información del usuario
            user_label = tk.Label(self.container, text=f"Usuario: {user[0]} - Email: {user[1]}", font=("Arial", 12))
            user_label.pack(pady=5)

            # Botón para eliminar al usuario
            delete_button = tk.Button(self.container, text="Eliminar", command=lambda u=user[0]: self.delete_user(u))
            delete_button.pack(pady=2)

            # Botón para modificar la información del usuario
            modify_button = tk.Button(self.container, text="Modificar", command=lambda u=user[0]: self.admin_modify_user_info(u))
            modify_button.pack(pady=2)

        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)

        # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", command=lambda: self.admin_manage_accounts(page-1))
            previous_button.pack(side="left", padx=5)

        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_users:
            next_button = tk.Button(nav_frame, text="Siguiente", command=lambda: self.admin_manage_accounts(page+1))
            next_button.pack(side="right", padx=5)

        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=self.show_user_menu).pack(pady=10)



    def accept_user(self, username):
        """Aceptar solicitud de registro"""
        self.user_manager.accept_user(username)
        messagebox.showinfo("Éxito", f"Usuario {username} aceptado.")
        self.admin_manage_users()

    def reject_user(self, username):
        """Rechazar solicitud de registro"""
        self.user_manager.reject_user(username)
        messagebox.showinfo("Información", f"Usuario {username} rechazado.")
        self.admin_manage_users()
    
    def delete_user(self, username):
        """Eliminar un usuario de la base de datos"""
        self.user_manager.delete_user(username)
        messagebox.showinfo("Información", f"Usuario {username} eliminado.")
        self.admin_manage_accounts()
    
    def admin_modify_user_info(self, username):
        """Modificar los datos personales de un usuario"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Obtener la información actual del usuario desde la base de datos
        user_info = self.user_manager.get_user_info(username)

        # Mostrar campos con los datos actuales
        tk.Label(self.container, text=f"Modificar datos de {username}").pack(pady=10)

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
        tk.Button(self.container, text="Actualizar", command=lambda: self.update_user_info_admin(username, username_entry.get(), email_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(self.container, text="Volver", command=self.admin_manage_accounts).pack(pady=10)

    def update_user_info_admin(self, original_username, new_username, email, password):
        """Actualizar la información de un usuario como administrador"""
        if password:
            success = self.user_manager.update_user_info(original_username, new_username, email, password)
        else:
            success = self.user_manager.update_user_info(original_username, new_username, email)

        if success:
            messagebox.showinfo("Éxito", f"Datos de {original_username} actualizados correctamente.")
            self.admin_manage_accounts()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

