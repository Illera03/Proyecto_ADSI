from db_manager import create_connection, create_tables
from ui_components import App
import tkinter as tk

def db():
    database = "data/video_club.db"
    # Crear conexión y crear tablas si no existen
    conn = create_connection(database)
    if conn is not None:
        create_tables(conn)
        conn.close()

if __name__ == '__main__': # __name__ es una variable especial que se asigna el valor "__main__" si el script se ejecuta directamente
    db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()




