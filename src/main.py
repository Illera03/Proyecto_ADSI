from CONTROLADOR.db_manager import DbManager
from VISTA.ui_components import App
import tkinter as tk

def initialize_database():
    """Inicializa la base de datos y crea las tablas necesarias si no existen."""
    db_manager = DbManager()  # Instancia de la clase DbManager
    conn = db_manager.conn  # Usa la conexión inicializada en el constructor
    if conn is not None:
        db_manager.create_tables()  # Llama al método para crear las tablas
        conn.close()
    else:
        print("Error: No se pudo conectar a la base de datos.")

if __name__ == '__main__':
    # Inicializar la base de datos
    initialize_database()
    
    # Configurar la interfaz gráfica
    root = tk.Tk()
    root.title("Video Club - Aplicación de Escritorio")  # Título de la ventana
    root.geometry("800x800")  # Establecer tamaño de la ventana

    # Iniciar la aplicación
    app = App(root)
    root.mainloop()

