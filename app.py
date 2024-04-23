import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configurar la conexión a la base de datos SQLite
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Crear la tabla de tareas si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             completed INTEGER NOT NULL DEFAULT 0)''')

# Crear la tabla de usuarios si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             password TEXT NOT NULL)''')
conn.commit()

# Ruta para la página de inicio de sesión
@app.route('/')
def login_page():
    return render_template('login.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    login_id = request.form['login_id']
    login_ps = request.form['login_ps']
    cursor = conn.cursor()
    # Verificar si el nombre de usuario y la contraseña coinciden con los datos de la base de datos
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (login_id, login_ps))
    user = cursor.fetchone()
    cursor.close()
    if user:
        # Si las credenciales son correctas, redirigir al usuario a la página principal
        return redirect(url_for('index'))
    else:
        # Si las credenciales son incorrectas, volver a la página de inicio de sesión con un mensaje de error
        return render_template('login.html', error_message="Nombre de usuario o contraseña incorrectos")

# En app.py
@app.route('/chan_sin', methods=['POST'])
def chan_sin():
    return render_template('chan_in.html')


@app.route('/chan_in', methods=['POST'])
def chan_in():
    chan_id = request.form['chan_id']
    chan_ps = request.form['chan_ps']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (chan_id, chan_ps))
    existing_user = cursor.fetchone()
    if existing_user:
        return render_template('login.html', error_message="El nombre de usuario ya está en uso")
    else:
        # Insertar el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (chan_id, chan_ps))
        conn.commit()
        cursor.close()
        return render_template('login.html', success_message="¡Usuario registrado con éxito! Ahora puede iniciar sesión.")
        

# Ruta para la página principal
@app.route('/index')
def index():
    cursor = conn.cursor()
    # Obtener todas las tareas de la base de datos
    cursor.execute("SELECT id, name, completed FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)

# Ruta para agregar una nueva tarea
@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    cursor = conn.cursor()
    # Insertar la nueva tarea en la base de datos
    cursor.execute("INSERT INTO tasks (name) VALUES (?)", (task_name,))
    conn.commit()
    cursor.close()
    # Redirigir de vuelta a la página principal después de agregar la tarea
    return redirect(url_for('index'))

# Ruta para eliminar tareas seleccionadas
@app.route('/delete_selected_tasks', methods=['POST'])
def delete_selected_tasks():
    task_ids = request.form.getlist('task_ids')
    if task_ids:
        cursor = conn.cursor()
        # Eliminar las tareas seleccionadas de la base de datos
        for task_id in task_ids:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        cursor.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
