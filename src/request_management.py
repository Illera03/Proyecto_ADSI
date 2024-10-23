import sqlite3
from tkinter import messagebox
from db_manager import create_connection

class RequestManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = create_connection(db_file)

   # def create_request():