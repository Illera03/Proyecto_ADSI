import tkinter as tk
from tkinter import messagebox
from CONTROLADOR.user_management import UserManager
from CONTROLADOR.movie_management import MovieManager
from review_management import ReviewManager
from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.alquiler_management import AlquilerManager
import datetime
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Club")
        
        #Inicializar MovieManager
        self.movie_manager = MovieManager()

         #Inicializar ReviewManager
        self.review_manager = ReviewManager("data/video_club.db")

        # Inicializar UserManager
        self.user_manager = UserManager()
        
        # Inicializar GeneralManager
        self.general_manager = GeneralManager()

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
        # Botones para registro y login
        tk.Button(self.container, text="Registrar", command=self.show_register).pack(pady=10)
        tk.Button(self.container, text="Iniciar sesión", command=self.show_login).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco
 
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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def register_user(self, username, password, email):
        """Registra el usuario"""
        reg = self.general_manager.register_user(username, password, email)
        if reg:
            messagebox.showinfo("Éxito", "Registro exitoso")
            self.create_main_buttons()
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        else:
            messagebox.showerror("Error", "Registro incorrecto")
            self.container.focus_force()  # Asegura que la ventana tenga el foco

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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def login_user(self, username, password):
        """Inicia sesión"""
        resul = self.general_manager.authenticate_user(username, password)
        
        if resul == 4:
            messagebox.showerror("Error", "Tu solicitud de registro ha sido rechazada.")
            self.container.focus_force()
        elif resul == 3:
            messagebox.showwarning("Pendiente", "Tu solicitud de registro está pendiente de aceptación por un administrador.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        elif resul == 2:
            messagebox.showerror("Error", "Credenciales incorrectas")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        else:
            messagebox.showinfo("Éxito", f"Inicio de sesión exitoso. Rol: " + ("admin" if resul == 1 else "user"))

            if resul == 1:
                self.show_user_menu("admin")  # Enseñar el menú de administrador
            else:
                self.show_user_menu("user")
            self.container.focus_force()  # Asegura que la ventana tenga el foco

        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def show_user_menu(self, role):
        #TODO CAMBIAR
        """Muestra el menú de opciones según el rol"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        tk.Label(self.container, text=f"Bienvenido").pack(pady=10)

        if role == "admin":
            tk.Button(self.container, text="Gestión de peticiones", command=self.admin_manage_users).pack(pady=10)
            tk.Button(self.container, text="Gestión de cuentas", command=self.admin_manage_accounts).pack(pady=10)
        
        if role == "user":
            tk.Button(self.container, text="Alquilar películas", command=self.user_rent_movies).pack(pady=10)
            tk.Button(self.container, text="Ver mis alquileres", command=self.user_view_rentals).pack(pady=10)
            tk.Button(self.container, text="Actualizar datos personales", command=self.user_update_info).pack(pady=10)
            tk.Button(self.container, text="Solicitar película", command=self.user_request_movies).pack(pady=10)

        # Botón para cerrar sesión
        tk.Button(self.container, text="Cerrar sesión", command=self.logout_user).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def admin_manage_users(self):
        """Función del administrador para gestionar peticiones de usuarios"""
        messagebox.showinfo("Admin", "Función de peticiones de registro")
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def admin_manage_accounts(self):
        """Función del administrador para gestionar cuentas (modificar y eliminar)"""
        messagebox.showinfo("Admin", "Función de gestión de cuentas")
        self.container.focus_force()  # Asegura que la ventana tenga el foco  
    
   
    
   
 
    def user_rent_movies(self, page=1):
        """Función del usuario para alquilar las películas disponibles"""
       #  messagebox.showinfo(text="Alquilar pelicula", command=self.user_rent_movies).pack(pady=10)
       # self.container.focus_force()  # Asegura que la ventana tenga el foco
        self.clear_frame()
        tk.Label(self.container, text="Películas disponibles").pack(pady=10)
        # Número de películas a mostrar por página
        items_per_page = 5
        #Obtener todas las películas
        movies = self.movie_manager.get_all_movies() # Supongamos que esta función devuelve una lista de diccionarios con las películas
        total_movies = len(movies)
        
         # Calcular el rango de peliculas a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        movies_to_show = movies[start_index:end_index]  # Acceso a la lista de películas

        # Etiqueta del título
        tk.Label(self.container, text="Peliculas para alquilar", font=("Arial", 14)).pack(pady=10)

        # Mostrar las peliculas de la página actual
        if not movies_to_show:
            tk.Label(self.container, text="No hay más películas disponibles", font=("Arial", 14)).pack(pady=5)
        else:
            for movie in movies_to_show:
                movie_label = tk.Label(self.container, text=f"{movie.title}", font=("Arial", 12))
                movie_label.pack(pady=5)

             # Botón alquilar la película
                rent_button = tk.Button(self.container, text="Alquilar", bg="grey", command=lambda m=movie: self.rent_movie(self.logged_in_user,m))
                rent_button.pack(pady=2)

        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)

         # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.user_rent_movies(page-1))
            previous_button.pack(side="left", padx=5)

        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_movies:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.user_rent_movies(page+1))
            next_button.pack(side="right", padx=5)
            
        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def rent_movie(self, user, movie):
            """Alquilar una película"""
            if self.general_manager.rent_movie(user, movie, datetime.date.today()):
                messagebox.showinfo("Éxito", f"Película '{movie}' alquilada correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo alquilar la película '{movie}'.")
            self.user_rent_movies()
            self.container.focus_force()  # Asegura que la ventana tenga el foco
 
    def user_view_rentals(self):
        """Función del usuario para ver sus alquileres"""
        #messagebox.showinfo("Usuario", "Función para ver alquileres")
        #self.container.focus_force()  # Asegura que la ventana tenga el foco
        self.clear_frame()
        tk.Label(self.container, text="Mis Alquileres").pack(pady=10)

        # Obtener los alquileres del usuario ordenador por valoracion
        cursor = self.movie_manager.connection.cursor()
        cursor.execute("""
            SELECT P.movie_id, P.title, P.genre, P.release_year, P.director, P.notaPromedio
            FROM Alquileres A JOIN Películas P ON A.movie_id = P.movie_id
            WHERE A.user_id = ? ORDER BY notaPromedio DESC
        """, (self.logged_in_user,))  # Suponiendo que self.logged_in_user contiene el ID del usuario
        rentals = cursor.fetchall()

        if not rentals:
            # Si no hay alquileres, mostrar un mensaje
            tk.Label(self.container, text="No tienes alquileres aun", font=("Arial", 14)).pack(pady=10)
        else:
            # Mostrar las películas alquiladas
            for rental in rentals:
                movie_info = f"ID: {rental[0]} - Título: {rental[1]} - Año: {rental[3]} - Género: {rental[2]} - Director: {rental[4]} - notaPromedio: {rental[5]}"
                tk.Label(self.container, text=movie_info).pack()
                # Verificar si el usuario ya tiene una reseña para esta película
                review = self.review_manager.get_review_for_movie(self.logged_in_user, rental[0])  # Obtener la reseña actual
                if review:
                    # Si ya existe la reseña, mostrar botón para modificarla
                    modify_button = tk.Button(self.container, text="Modificar Reseña", bg="blue", command=lambda m=rental[0]: self.modify_review(m))
                    modify_button.pack(pady=5)
                else:
                    # Si no existe la reseña, mostrar botón para añadirla
                    add_button = tk.Button(self.container, text="Añadir Reseña", bg="green", command=lambda m=rental[0]: self.add_review(m))
                    add_button.pack(pady=5)

                    # Botón para ver reseñas de otros usuarios
                view_reviews_button = tk.Button(self.container, text="Ver Reseñas", bg="orange", command=lambda m=rental[0]: self.show_others_reviews(m))
                view_reviews_button.pack(pady=5)
        
        self.container.focus_force()  # Asegura que la ventana tenga el foco
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)

    def add_review(self, movie_id):
        """Función para añadir una reseña"""
        # Solicitar al usuario que ingrese el texto de la reseña
        self.clear_frame()  # Limpiar el marco de la interfaz de usuario antes de mostrar nuevos elementos
        tk.Label(self.container, text="Añadir Reseña").pack(pady=10)
        # Crear y mostrar un campo de entrada para la calificación
        tk.Label(self.container, text="Calificación (1-10):").pack()
        rating_entry = tk.Entry(self.container)
        rating_entry.pack(pady=5) 
        # Crear y mostrar un campo de entrada para el comentario
        tk.Label(self.container, text="Comentario:").pack()
        comment_text = tk.Text(self.container, height=5, width=40)
        comment_text.pack(pady=5)
        # Botón para guardar la reseña, inicialmente deshabilitado
        save_button = tk.Button(self.container, text="Guardar Reseña", bg="grey", state=tk.DISABLED)
        save_button.pack(pady=10)

        def validate_review(event=None):
            """Habilitar el botón si ambos campos son válidos"""
            rating = float(rating_entry.get().strip())
            comment = comment_text.get("1.0", "end-1c").strip()
            if 1.0 <= rating <= 10.0 and comment:
                save_button.config(state=tk.NORMAL)
            else:
                save_button.config(state=tk.DISABLED)
        # Asociar validación dinámica a los eventos de los widgets
        rating_entry.bind("<KeyRelease>", validate_review)
        comment_text.bind("<KeyRelease>", validate_review)

        def save_review():
            """Guardar la reseña en la base de datos"""
            rating = float(rating_entry.get().strip())  # Extraer calificación
            comment = comment_text.get("1.0", "end-1c").strip()  # Extraer comentario
            try:
                self.review_manager.add_review(self.logged_in_user, movie_id, rating, comment)
                messagebox.showinfo("Éxito", "Reseña añadida correctamente.")
                self.user_view_rentals()  # Volver a la lista de alquileres
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la reseña: {e}")

        # Conectar el botón de guardar al evento de guardar reseña
        save_button.config(command=save_review)
        # Botón para volver al menú anterior
        tk.Button(self.container, text="Volver", command=self.user_view_rentals).pack(pady=10)

    def modify_review(self, movie_id):
        """Función para modificar una reseña existente"""
        # Limpiar el marco antes de mostrar nuevos elementos
        self.clear_frame()
        # Obtener la reseña actual del usuario para la película seleccionada
        review = self.movie_manager.get_review_for_movie(self.logged_in_user, movie_id)

        # Mostrar la cabecera para modificar la reseña
        tk.Label(self.container, text="Modificar Reseña").pack(pady=10)

        # Crear y mostrar un campo de entrada para la calificación, con el valor actual
        tk.Label(self.container, text="Calificación (1-10):").pack()
        rating_entry = tk.Entry(self.container)
        rating_entry.insert(0, review[0])  # Inserta la calificación actual
        rating_entry.pack(pady=5)

        # Crear y mostrar un campo de entrada para el comentario, con el valor actual
        tk.Label(self.container, text="Comentario:").pack()
        comment_text = tk.Text(self.container, height=5, width=40)
        comment_text.insert("1.0", review[1])  # Inserta el comentario actual
        comment_text.pack(pady=5)

        # Botón para guardar la reseña, inicialmente deshabilitado
        save_button = tk.Button(self.container, text="Actualizar Reseña", bg="grey", state=tk.DISABLED)
        save_button.pack(pady=10)

        # Función para habilitar o deshabilitar el botón de guardar dependiendo de la validez de los campos
        def validate_review(event=None):
            """Habilitar el botón si ambos campos son válidos"""
            rating = float(rating_entry.get().strip())
            comment = comment_text.get("1.0", "end-1c").strip()
            if 1.0 <= float(rating) <= 10.0 and comment:
                save_button.config(state=tk.NORMAL)
            else:
                save_button.config(state=tk.DISABLED)

        # Asociar validación dinámica a los eventos de los widgets
        rating_entry.bind("<KeyRelease>", validate_review)
        comment_text.bind("<KeyRelease>", validate_review)

        # Función para guardar la reseña modificada en la base de datos
        def save_review():
            """Guardar la reseña modificada en la base de datos"""
            rating = float(rating_entry.get().strip())  # Extraer calificación
            comment = comment_text.get("1.0", "end-1c").strip()  # Extraer comentario
            print(f"Rating: {rating}, Comment: {comment}")  # Verifica los valores
            try:
                # Llamar a modify_review para actualizar la reseña en la base de datos
                self.movie_manager.modify_review(self.logged_in_user, movie_id, rating, comment)
                messagebox.showinfo("Éxito", "Reseña actualizada correctamente.")
                self.user_view_rentals()  # Volver a la lista de alquileres
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la reseña: {e}")

        # Conectar el botón de guardar al evento de guardar reseña
        save_button.config(command=save_review)

        # Botón para volver al menú anterior
        tk.Button(self.container, text="Volver", command=self.user_view_rentals).pack(pady=10)

    def show_others_reviews(self, movie_id):
        """Mostrar las reseñas de otros usuarios para una película específica"""
        self.clear_frame()
        tk.Label(self.container, text="Reseñas de Otros Usuarios").pack(pady=10)

        # Obtener las reseñas de otros usuarios
        other_reviews = self.review_manager.get_all_reviews_of_a_movie(movie_id, self.logged_in_user)

        if other_reviews:
            for user, rating, comment in other_reviews:
                tk.Label(self.container, text=f"Usuario: {user} - Calificación: {rating}", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=2)
                tk.Label(self.container, text=f"Comentario: {comment}", wraplength=400, justify="left").pack(anchor="w", padx=20, pady=2)
        else:
            tk.Label(self.container, text="No hay reseñas de otros usuarios para esta película.", fg="gray").pack(pady=10)

        # Botón para volver al menú anterior
        tk.Button(self.container, text="Volver", command=self.user_view_rentals).pack(pady=10)

    def user_update_info(self):
        """Función del usuario para actualizar su información personal"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Obtener la información actual del usuario desde la base de datos
        user_info = self.general_manager.get_user_info()

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
        tk.Button(self.container, text="Actualizar", command=lambda: self.update_user_info(username_entry.get(), email_entry.get(), password_entry.get(), "user")).pack(pady=10)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def update_user_info(self, username, email, password, who):
        """Actualizar la información del usuario en la base de datos"""
        if password:
            success = self.general_manager.update_user_info(username, email, password)
        else:
            success = self.general_manager.update_user_info(username, email)

        if success:
            messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
            self.show_user_menu(who)
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        self.container.focus_force()  # Asegura que la ventana tenga el foco
    
    def user_request_movies(self):
        """Función para solicitar una película"""
        self.clear_frame()

        # Etiqueta y campo de entrada para la película solicitada
        tk.Label(self.container, text="Introduce el nombre de la película:").pack(pady=10)
        film_entry = tk.Entry(self.container)
        film_entry.pack()

        # Botón para solicitar la película
        tk.Button(self.container, text="Solicitar", command=lambda: self.request_movie_from_api(film_entry.get())).pack(pady=10)

        # Botón para volver al menú de usuario
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def request_movie_from_api(self, movie_title):
        """Función para buscar la película en OMDb API y registrar la solicitud"""
        if not movie_title:
            messagebox.showwarning("Error", "Debes introducir el nombre de una película")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
            return

        # Llamar a la función para buscar la película en OMDb
        movie_data = self.user_manager.search_movie_omdb(movie_title)

        if movie_data:
            # Si se encuentra la película, se inserta en la base de datos
            self.user_manager.create_movie_request(self.logged_in_user, movie_data['Title'])

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Película '{movie_data['Title']}' solicitada correctamente.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        else:
            messagebox.showerror("Error", "No se encontró la película en la base de datos OMDb.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def logout_user(self):
        """Cerrar sesión"""
        self.logged_in_user = None
        self.logged_in_role = None
        messagebox.showinfo("Cerrar sesión", "Has cerrado sesión")
        self.create_main_buttons()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def clear_frame(self):
        """Eliminar todos los widgets actuales del contenedor"""
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    # Métodos del administrador
    
    def admin_manage_users(self, page=1):
        """Función del administrador para gestionar usuarios con paginación."""
        self.clear_frame()

        # Número de usuarios a mostrar por página
        items_per_page = 5

        # Obtener lista de usuarios pendientes
        pending_users = self.general_manager.get_pending_users()
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
                # Mostrar el nombre del usuario
                user_label = tk.Label(self.container, text=f"Usuario: {user}", font=("Arial", 12))
                user_label.pack(pady=5)

                # Botón para aceptar el usuario
                accept_button = tk.Button(self.container, text="Aceptar", bg="green", command=lambda u=user: self.accept_user(u))
                accept_button.pack(pady=2)

                # Botón para rechazar el usuario
                reject_button = tk.Button(self.container, text="Rechazar", bg="red", command=lambda u=user: self.reject_user(u))
                reject_button.pack(pady=2)

        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)

        # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.admin_manage_users(page-1))
            previous_button.pack(side="left", padx=5)

        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_users:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.admin_manage_users(page+1))
            next_button.pack(side="right", padx=5)

        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("admin")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def admin_manage_accounts(self, page=1):
        """Función del administrador para gestionar cuentas de usuario con paginación."""
        self.clear_frame()

        # Número de usuarios a mostrar por página
        items_per_page = 5

        # Obtener todas las cuentas de usuario (lista de nombres de usuario)
        all_users = self.general_manager.get_all_users()
        total_users = len(all_users)

        # Calcular el rango de usuarios a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        # Obtener los usuarios que se mostrarán en esta página
        users_to_show = all_users[start_index:end_index]

        # Etiqueta del título
        tk.Label(self.container, text="Cuentas de usuarios", font=("Arial", 14)).pack(pady=10)

        # Mostrar las cuentas de usuario de la página actual
        for user in users_to_show:
            # Mostrar el nombre del usuario
            user_label = tk.Label(self.container, text=f"Usuario: {user}", font=("Arial", 12))
            user_label.pack(pady=5)

            # Botón para eliminar al usuario
            delete_button = tk.Button(self.container, text="Eliminar", bg="red", command=lambda u=user: self.delete_user(u))
            delete_button.pack(pady=2)

            # Botón para modificar la información del usuario
            modify_button = tk.Button(self.container, text="Modificar", bg="green", command=lambda u=user: self.admin_modify_user_info(u))
            modify_button.pack(pady=2)

        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)

        # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.admin_manage_accounts(page-1))
            previous_button.pack(side="left", padx=5)

        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_users:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.admin_manage_accounts(page+1))
            next_button.pack(side="right", padx=5)

        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("admin")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco



    def accept_user(self, username):
        """Aceptar solicitud de registro"""
        self.general_manager.accept_user(username)
        messagebox.showinfo("Éxito", f"Usuario {username} aceptado.")
        self.admin_manage_users()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def reject_user(self, username):
        """Rechazar solicitud de registro"""
        self.general_manager.reject_user(username)
        messagebox.showinfo("Información", f"Usuario {username} rechazado.")
        self.admin_manage_users()
        self.container.focus_force()  # Asegura que la ventana tenga el foco
    
    def delete_user(self, username):
        """Eliminar un usuario de la base de datos"""
        if self.general_manager.delete_user(username):
            messagebox.showinfo("Información", f"Usuario {username} eliminado.")
        else:
            messagebox.showerror("Error", f"No se pudo eliminar al usuario {username}.")
        self.admin_manage_accounts()
        self.container.focus_force()  # Asegura que la ventana tenga el foco
    
    def admin_modify_user_info(self, username):
        """Modificar los datos personales de un usuario"""
        self.clear_frame()

        # Obtener la información actual del usuario desde la base de datos
        user_info = self.general_manager.admin_get_user_info(username)

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
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def update_user_info_admin(self, original_username, new_username, email, password):
        """Actualizar la información de un usuario como administrador"""
        if password:
            success = self.general_manager.admin_update_user_info(original_username, new_username, email, password)
        else:
            success = self.general_manager.admin_update_user_info(original_username, new_username, email)

        if success:
            messagebox.showinfo("Éxito", f"Datos de {original_username} actualizados correctamente.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
            self.admin_manage_accounts()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
            
        self.container.focus_force()  # Asegura que la ventana tenga el foco

   
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

