import sqlite3
from flask import g
from chanchan_work import app

# Función para obtener la conexión a la base de datos de tareas del usuario actual
def get_connection():
    conn = sqlite3.connect('chan.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
                        username TEXT NOT NULL,
                        PASSWORD TEXT NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0
                      )''')
    cursor.close()
    conn.close()
    return sqlite3.connect('chan.db', check_same_thread=False)

def create_task_db(username):
    conn = sqlite3.connect('chan.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {username}_tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0
                      )''')
    conn.commit()
    cursor.close()
    conn.close()
