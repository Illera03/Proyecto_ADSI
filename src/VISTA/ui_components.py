import tkinter as tk
from tkinter import messagebox
from CONTROLADOR.user_management import UserManager
from CONTROLADOR.movie_management import MovieManager
from CONTROLADOR.review_management import ReviewManager
from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.alquiler_management import AlquilerManager
from CONTROLADOR.request_management import RequestManager
from MODELO import movie
from MODELO import review
import json

import datetime
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Club")
        # Inicializar AlquilerManager
        self.alquiler_manager = AlquilerManager()

        #Inicializar MovieManager
        self.movie_manager = MovieManager()

         #Inicializar ReviewManager
        self.review_manager = ReviewManager("data/video_club.db")

        # Inicializar UserManager
        self.user_manager = UserManager()
        
        #Inicializar RequestManager
        self.request_manager= RequestManager()

        # Inicializar GeneralManager
        self.general_manager = GeneralManager()

        # Variables para almacenar el estado del usuario
        #self.logged_in_user = None
        #self.logged_in_role = None

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
            messagebox.showerror("Error", "Credenciales incorrectas o cuenta inexistente.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        else:
            messagebox.showinfo("Éxito", f"Inicio de sesión exitoso. Rol: " + ("admin" if resul == 1 else "user"))
            #! mal self.logged_in_user = username
            if resul == 1:
                self.show_user_menu("admin")  # Enseñar el menú de administrador
            else:
                self.show_user_menu("user")
            self.container.focus_force()  # Asegura que la ventana tenga el foco

        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def show_user_menu(self, role):
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
            tk.Button(self.container, text="Crear Reseña", command=self.rented_movies_without_review).pack(pady=10)
            tk.Button(self.container, text="Modificar Reseña", command=self.rented_movies_with_review).pack(pady=10)
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
                rent_button = tk.Button(self.container, text="Alquilar", bg="grey", command=lambda movie=movie: self.rent_movie(self.logged_in_user, movie.title))
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
            if self.general_manager.rent_movie(user, movie):
                messagebox.showinfo("Éxito", f"Película '{movie}' alquilada correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo alquilar la película '{movie}'.")
            self.user_rent_movies()
            self.container.focus_force()  # Asegura que la ventana tenga el foco
 
    def user_view_rentals(self, page=1):
        """Función del usuario para ver sus alquileres"""
        self.clear_frame()
        tk.Label(self.container, text="Películas disponibles").pack(pady=10)
        # Número de películas a mostrar por página
        items_per_page = 5
        #Obtener todas las películas alquiladas
        movies = self.alquiler_manager.get_rented_movies(self.logged_in_user) # Supongamos que esta función devuelve una lista de diccionarios con las películas
        total_movies = len(movies)
         # Calcular el rango de peliculas a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        movies_to_show = movies[start_index:end_index]  # Acceso a la lista de películas
        # Etiqueta del título
        tk.Label(self.container, text="Peliculas alquiladas", font=("Arial", 14)).pack(pady=10)
        # Mostrar las peliculas de la página actual
        if not movies_to_show:
            tk.Label(self.container, text="No hay más películas disponibles", font=("Arial", 14)).pack(pady=5)
        else:
            for movie in movies_to_show:
                movie_frame = tk.Frame(self.container)  # Crea un Frame para la película y el botón
                movie_frame.pack(pady=5, fill="x")  # Empaque de la película en un Frame
                movie_label = tk.Label(movie_frame, text=f"'{movie.movie_id}'", font=("Arial", 12))
                movie_label.pack(side="left", padx=10)  # Coloca el nombre de la película a la izquierda
                # Botón ver la película
                rent_button = tk.Button(movie_frame, text="Ver", bg="grey", command=lambda movie=movie: self.view_movie(self.logged_in_user, movie.movie_id))
                rent_button.pack(side="right", padx=10)  # Coloca el botón a la derecha
        
        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)
         # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.user_view_rentals(page-1))
            previous_button.pack(side="left", padx=5)
        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_movies:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.user_view_rentals(page+1))
            next_button.pack(side="right", padx=5)     
        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def rent_movie(self, user, movie):
            """Alquilar una película"""
            if self.general_manager.rent_movie(user, movie):
                messagebox.showinfo("Éxito", f"Película '{movie}' alquilada correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo alquilar la película '{movie}'.")
            self.user_rent_movies()
            self.container.focus_force()  # Asegura que la ventana tenga el foco
    
    def view_movie(self, user, tituloPeli):
        "Ver una pelicula"
        if self.general_manager.view_movie(user, tituloPeli) == True:
            messagebox.showinfo("Éxito", f"Reproduciendo película: '{tituloPeli}'.")
        else:
            messagebox.showerror("Error", f"Se ha caducado la reserva de:'{tituloPeli}'.")
        self.user_view_rentals()
        self.container.focus_force()  # Asegura que la ventana tenga el foco
    
    def rented_movies_without_review(self, page=1):
        """Función del usuario para reseñar peliculas alquiladas"""
        self.clear_frame()
        # Limpiamos el contenedor de visualizar reseñas en caso de volver de crear/modificar reseña
        if hasattr(self, 'reviews_container'):
            self.reviews_container.destroy()  # Elimina los widgets en el contenedor
            del self.reviews_container  # Elimina la referencia al contenedor
        tk.Label(self.container, text="Películas Alquiladas Sin Reseñar").pack(pady=10)
        # Número de películas a mostrar por página
        items_per_page = 5
        #Obtener todas las películas alquiladas
        alquileres = self.general_manager.rented_movies_without_review(self.logged_in_user)
        total_movies = len(alquileres)
         # Calcular el rango de peliculas a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        movies_to_show = alquileres[start_index:end_index]  # Acceso a la lista de películas
        # Etiqueta del título
        tk.Label(self.container, text="Peliculas alquiladas", font=("Arial", 14)).pack(pady=10)
        # Mostrar las peliculas de la página actual
        if not movies_to_show:
            tk.Label(self.container, text="No hay películas para reseñar", font=("Arial", 14)).pack(pady=5)
        else:
            for alquiler in movies_to_show:
                peli = next((m for m in self.movie_manager.movieList if m.title == alquiler.get_title()), None)
                movie_frame = tk.Frame(self.container)
                movie_frame.pack(pady=5, fill="x")
                movie_label = tk.Label(movie_frame, text=f"Título : {peli.title} --> Puntuación : {peli.nota_promedio}", font=("Arial", 12))
                movie_label.pack(side="left", padx=10)
                # Botón para reseñar pelicula
                review_button = tk.Button(movie_frame, text="Crear Reseña", bg="grey", command=lambda movie=peli: self.add_review(movie.title))
                review_button.pack(side="right", padx=10)
        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)
         # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.rented_movies_without_review(page-1))
            previous_button.pack(side="left", padx=5)
        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_movies:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.rented_movies_without_review(page+1))
            next_button.pack(side="right", padx=5) 
        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco
     
    def validate_review(self, rating_entry, comment_text, save_button, event=None):
            """Habilitar el botón si ambos campos son válidos"""
            rating_text = rating_entry.get().strip()
            comment = comment_text.get("1.0", "end-1c").strip()
            try:
                if rating_text:  # Si no está vacío
                    rating = round(float(rating_text), 2)  # Intentar convertirlo a flotante
                    if 1.0 <= rating <= 10.0:
                        if comment:
                            save_button.config(state=tk.NORMAL)
                        else:
                            save_button.config(state=tk.DISABLED)
                    else:
                        save_button.config(state=tk.DISABLED)
                        messagebox.showerror("Error", "La calificacion debe estar entre 1.0 y 10.0")
                else:
                    save_button.config(state=tk.DISABLED)
            except ValueError:
                messagebox.showerror("Error", "Debe introducir un número valido.")
                save_button.config(state=tk.DISABLED)
    
    def save_review(self, movie_id, rating_entry, comment_text, modify=False):
            """Guardar la reseña"""
            rating = round(float(rating_entry.get().strip()),2)  # Extraer calificación
            comment = comment_text.get("1.0", "end-1c").strip()  # Extraer comentario
            try:
                if modify: # para modificar reseña existente
                    self.general_manager.modify_Review(self.logged_in_user, movie_id, rating, comment)
                    messagebox.showinfo("Éxito", "Reseña actualizada correctamente.")
                    self.rented_movies_with_review()  # Volver a la lista de alquileres
                else: # para crear reseña nueva
                    self.general_manager.register_Review(self.logged_in_user, movie_id, rating, comment)
                    messagebox.showinfo("Éxito", "Reseña añadida correctamente.")
                    self.rented_movies_without_review()  # Volver a la lista de peliculas a reseñar
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la reseña: {e}")
    
    def add_review(self, movie_id):
        """Función para añadir una reseña"""
        # Solicitar al usuario que ingrese el texto de la reseña
        self.clear_frame()  # Limpiar el marco de la interfaz de usuario antes de mostrar nuevos elementos
        tk.Label(self.container, text="Añadir Reseña:", font=("Arial", 11, "bold")).pack(pady=5)
        # Crear y mostrar un campo de entrada para la calificación
        tk.Label(self.container, text="Calificación (1.0 - 10.0) :").pack()
        rating_entry = tk.Entry(self.container)
        rating_entry.pack(pady=5) 
        # Crear y mostrar un campo de entrada para el comentario
        tk.Label(self.container, text="Comentario:").pack()
        comment_text = tk.Text(self.container, height=5, width=40)
        comment_text.pack(pady=5)
        # Botón para guardar la reseña, inicialmente deshabilitado
        save_button = tk.Button(self.container, text="Guardar Reseña", bg="grey", state=tk.DISABLED)
        save_button.pack(pady=10)
        # Función para habilitar o deshabilitar el botón de guardar dependiendo de la validez de los campos
        rating_entry.bind("<KeyRelease>", lambda event: self.validate_review(rating_entry, comment_text, save_button))
        comment_text.bind("<KeyRelease>", lambda event: self.validate_review(rating_entry, comment_text, save_button))
        # Función para guardar la reseña modificada
        save_button.config(command=lambda: self.save_review(movie_id, rating_entry, comment_text))
        # Mostrar reseñas de otros usuarios
        self.show_others_reviews(movie_id)
        # Botón para volver al menú anterior
        tk.Button(self.container, text="Volver", command=self.rented_movies_without_review).pack(pady=10)

    def rented_movies_with_review(self, page=1):
        """Función del usuario para modificar reseñas de peliculas alquiladas"""
        self.clear_frame()
        # Limpiamos el contenedor de visualizar reseñas en caso de volver de crear/modificar reseña
        if hasattr(self, 'reviews_container'):
            self.reviews_container.destroy()  # Elimina los widgets en el contenedor
            del self.reviews_container  # Elimina la referencia al contenedor
        tk.Label(self.container, text="Películas Alquiladas Con Reseña").pack(pady=10)
        # Número de películas a mostrar por página
        items_per_page = 5
        #Obtener todas las películas alquiladas
        alquileres = self.general_manager.rented_movies_with_review(self.logged_in_user)
        total_movies = len(alquileres)
         # Calcular el rango de peliculas a mostrar en esta página
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        movies_to_show = alquileres[start_index:end_index]  # Acceso a la lista de películas
        # Etiqueta del título
        tk.Label(self.container, text="Peliculas alquiladas", font=("Arial", 14)).pack(pady=10)
        # Mostrar las peliculas de la página actual
        if not movies_to_show:
            tk.Label(self.container, text="No hay películas para reseñar", font=("Arial", 14)).pack(pady=5)
        else:
            for alquiler in movies_to_show:
                peli = next((m for m in self.movie_manager.movieList if m.title == alquiler.get_title()), None)
                movie_frame = tk.Frame(self.container)
                movie_frame.pack(pady=5, fill="x")
                movie_label = tk.Label(movie_frame, text=f"Título : {peli.title} --> Puntuación : {peli.nota_promedio}", font=("Arial", 12))           
                movie_label.pack(side="left", padx=10)
                # Botón para reseñar pelicula
                review_button = tk.Button(movie_frame, text="Modificar Reseña", bg="grey", command=lambda movie=peli: self.modify_review(movie.title))
                review_button.pack(side="right", padx=10)
        # Navegación entre páginas
        nav_frame = tk.Frame(self.container)
        nav_frame.pack(pady=10)
         # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
        if page > 1:
            previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.rented_movies_with_review(page-1))
            previous_button.pack(side="left", padx=5)
        # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
        if end_index < total_movies:
            next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.rented_movies_with_review(page+1))
            next_button.pack(side="right", padx=5) 
        # Botón para volver al menú principal (siempre visible)
        tk.Button(self.container, text="Volver", command=lambda: self.show_user_menu("user")).pack(pady=10)
        self.container.focus_force()  # Asegura que la ventana tenga el foco
   
    def modify_review(self, movie_id):
        """Función para modificar una reseña existente"""
        # Limpiar el marco antes de mostrar nuevos elementos
        self.clear_frame()
        # Obtener la reseña actual del usuario para la película seleccionada
        review = self.general_manager.get_review_for_movie(self.logged_in_user, movie_id)
        if not review:
            messagebox.showerror("Error", "No se encontró la reseña a modificar.")
            self.rented_movies_with_review()
            return
        # Mostrar la cabecera para modificar la reseña
        tk.Label(self.container, text="Modificar Reseña").pack(pady=10)
        # Crear y mostrar un campo de entrada para la calificación, con el valor actual
        tk.Label(self.container, text="Calificación (1-10):").pack()
        rating_entry = tk.Entry(self.container)
        rating_entry.insert(0, review.get_movie_rating())  # Inserta la calificación actual
        rating_entry.pack(pady=5)
        # Crear y mostrar un campo de entrada para el comentario, con el valor actual
        tk.Label(self.container, text="Comentario:").pack()
        comment_text = tk.Text(self.container, height=5, width=40)
        comment_text.insert("1.0", review.get_movie_comment())  # Inserta el comentario actual
        comment_text.pack(pady=5)
        # Botón para guardar la reseña, inicialmente deshabilitado
        save_button = tk.Button(self.container, text="Actualizar Reseña", bg="grey", state=tk.DISABLED)
        save_button.pack(pady=10)
        # Función para habilitar o deshabilitar el botón de guardar dependiendo de la validez de los campos
        rating_entry.bind("<KeyRelease>", lambda event: self.validate_review(rating_entry, comment_text, save_button))
        comment_text.bind("<KeyRelease>", lambda event: self.validate_review(rating_entry, comment_text, save_button))
        # Función para guardar la reseña modificada
        save_button.config(command=lambda: self.save_review(movie_id, rating_entry, comment_text, modify=True))
        # Mostrar reseñas de otros usuarios
        self.show_others_reviews(movie_id)
        # Botón para volver al menú anterior
        tk.Button(self.container, text="Volver", command=self.rented_movies_with_review).pack(pady=10)

        
    def show_others_reviews(self, movie_id, page=1, sort_by_rating=False):
        """Mostrar las reseñas de otros usuarios para una película específica"""
         # Limpiar el contenedor de reseñas antes de mostrar nuevas reseñas
        if hasattr(self, 'reviews_container'):
            for widget in self.reviews_container.winfo_children():
                widget.destroy()
        # Obtener todas las reseñas de peliculas alquiladas por otros usuarios
        other_reviews = self.general_manager.get_others_reviews_for_movie(movie_id, self.logged_in_user)
        # Si no hay un contenedor de reseñas de otros usuarios, créalo
        if not hasattr(self, 'reviews_container'):
            self.reviews_container = tk.Frame(self.container)
            self.reviews_container.pack(pady=10, fill="x")
        tk.Label(self.reviews_container, text="Reseñas de otros usuarios:", font=("Arial", 11, "bold")).pack(pady=5)
        # Obtener las reseñas de otros usuarios
        if other_reviews:
            if sort_by_rating:
                other_reviews.sort(key=lambda r: r.get_movie_rating(), reverse=True)
                sort_button = tk.Button(self.reviews_container, text="Ordenar por defecto", bg="grey", command=lambda: self.show_others_reviews(movie_id, page=1, sort_by_rating=False))
            else:
                sort_button = tk.Button(self.reviews_container, text="Ordenar por Valoracion", bg="grey", command=lambda: self.show_others_reviews(movie_id, page=1, sort_by_rating=True)) 
            sort_button.pack(pady=5, anchor="center")  # Asegura que el botón esté debajo del título y alineado correctamente
            total_reviews = len(other_reviews)  
            # Número de reseñas a mostrar por página
            items_per_page = 2
            # Calcular el rango de reseñas a mostrar en esta página
            start_index = (page - 1) * items_per_page
            end_index = start_index + items_per_page
            reviews_to_show = other_reviews[start_index:end_index]  # Acceso a la lista de reseñas
            for review in reviews_to_show:
                # Crear un marco para cada reseña
                review_frame = tk.Frame(self.reviews_container, padx=10, pady=10, relief="solid", borderwidth=1)
                review_frame.pack(pady=5, fill="x")
                # Crear un sub-marco para los títulos y valores en la misma fila
                user_frame = tk.Frame(review_frame)
                user_frame.pack(fill="x", pady=2)
                # Título de usuario en negrita y valor de usuario en la misma fila
                user_label = tk.Label(user_frame, text="Usuario:", font=("Arial", 10, "bold"), fg="black")
                user_label.pack(side="left")
                user_value = tk.Label(user_frame, text=review.get_user_id(), font=("Arial", 10), fg="black")
                user_value.pack(side="left", padx=10)
                # Crear un sub-marco para puntuación
                rating_frame = tk.Frame(review_frame)
                rating_frame.pack(fill="x", pady=2)
                # Título de puntuación en negrita y valor de puntuación en la misma fila
                rating_label = tk.Label(rating_frame, text="Puntuación:", font=("Arial", 10, "bold"), fg="black")
                rating_label.pack(side="left")
                rating_value = tk.Label(rating_frame, text=f"{review.get_movie_rating()} / 10", font=("Arial", 10), fg="black")
                rating_value.pack(side="left", padx=10)
                # Título de comentario en negrita
                comment_label = tk.Label(review_frame, text="Comentario:", font=("Arial", 10, "bold"), fg="black")
                comment_label.pack(anchor="w")
                # Valor del comentario en texto normal
                comment_value = tk.Label(review_frame, text=review.get_movie_comment(), wraplength=400, justify="left", font=("Arial", 10), fg="black")
                comment_value.pack(anchor="w")
             # Navegación entre páginas
            nav_frame = tk.Frame(self.reviews_container)
            nav_frame.pack(pady=10)
            # Botón "Anterior" (sólo mostrar si no estamos en la primera página)
            if page > 1:
                previous_button = tk.Button(nav_frame, text="Anterior", bg="grey", command=lambda: self.show_others_reviews(movie_id, page-1,sort_by_rating))
                previous_button.pack(side="left", padx=5)
            # Botón "Siguiente" (sólo mostrar si hay más usuarios que mostrar)
            if end_index < total_reviews:
                next_button = tk.Button(nav_frame, text="Siguiente", bg="grey", command=lambda: self.show_others_reviews(movie_id, page+1,sort_by_rating))
                next_button.pack(side="right", padx=5) 
        else:
        # Si no hay otras reseñas, mostrar un mensaje debajo del botón de volver
            tk.Label(self.reviews_container, text="Aún no hay reseñas de otros usuarios para esta película.", font=("Arial", 10, "italic"), fg="gray").pack(pady=5)
        



    def user_update_info(self):
        """Función del usuario para actualizar su información personal"""
        self.clear_frame()
        self.container.focus_force()  # Asegura que la ventana tenga el foco

        # Obtener la información actual del usuario desde la base de datos
        user_info_json = self.general_manager.get_user_info()
        user_info = json.loads(user_info_json)

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
        movie_data = RequestManager.search_movie_omdb(movie_title)

        if movie_data:
            # Si se encuentra la película, se inserta en la base de datos
            #m = movie.Movie.new_movie(id=movie_data['imdbID'],title=movie_data['Title'],genre=movie_data['Genre'],release_year=movie_data['Year'],director=movie_data['Director'],nota_promedio=0.0,id_admin_aceptado=None)
            self.movie_manager.add_movie_from_omdb(movie_data)
            user_id = self.user_manager.get_user_id()
            self.request_manager.add_request_from_omdb(self, movie_data['omdbID'], user_id)
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Película '{movie_data['Title']}' solicitada correctamente.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        else:
            messagebox.showerror("Error", "No se encontró la película en la base de datos OMDb.")
            self.container.focus_force()  # Asegura que la ventana tenga el foco
        self.container.focus_force()  # Asegura que la ventana tenga el foco

    def logout_user(self):
        """Cerrar sesión"""
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
        pending_users_json = self.general_manager.get_pending_users()
        pending_users = json.loads(pending_users_json)
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
        all_users_json = self.general_manager.get_all_users()
        all_users = json.loads(all_users_json)
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
        user_info_json = self.general_manager.admin_get_user_info(username)
        user_info = json.loads(user_info_json)

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

