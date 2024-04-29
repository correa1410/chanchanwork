from flask import render_template, request, redirect, url_for, session
from chanchan_work import app 
from .db import get_connection, create_task_db # type: ignore

@app.route('/')
def login_page():
    return render_template('login.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    login_id = request.form['login_id']
    login_ps = request.form['login_ps']
    
    # Verificar si el nombre de usuario y la contraseña coinciden con los datos de la base de datos
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (login_id, login_ps))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        # Si las credenciales son correctas, redirigir al usuario a la página principal
        session['username'] = login_id
        return redirect(url_for('index'))
    else:
        # Si las credenciales son incorrectas, volver a la página de inicio de sesión con un mensaje de error
        return render_template('login.html', error_message="Nombre de usuario o contraseña incorrectos")

# Ruta para la página principal
@app.route('/index')
def index():
    username = session.get('username')
    # Obtener todas las tareas del usuario actual de la base de datos
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name, completed FROM {username}_tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Ruta para agregar una nueva tarea
@app.route('/add_task', methods=['POST'])
def add_task():
    username = session.get('username')
    task_name = request.form['task_name']
    conn = get_connection()
    cursor = conn.cursor()
    # Insertar la nueva tarea en la base de datos del usuario actual
    cursor.execute(f"INSERT INTO {username}_tasks (name) VALUES (?)", (task_name,))
    conn.commit()
    cursor.close()
    conn.close()
    # Redirigir de vuelta a la página principal después de agregar la tarea
    return redirect(url_for('index', username=username))

# Ruta para eliminar tareas seleccionadas
@app.route('/delete_selected_tasks', methods=['POST'])
def delete_selected_tasks():
    username = session.get('username')
    task_ids = request.form.getlist('task_ids')
    if task_ids:
        conn = get_connection()
        cursor = conn.cursor()
        # Eliminar las tareas seleccionadas del usuario actual de la base de datos
        for task_id in task_ids:
            cursor.execute(f"DELETE FROM {username}_tasks WHERE id = ?", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index', username=username))

# Ruta para registrar nuevos usuarios
@app.route('/chan_in', methods=['POST'])
def chan_in():
    username = request.form['chan_id']
    password = request.form['chan_ps']
    
    # Establecer conexión a la base de datos de usuarios
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el nombre de usuario ya existe
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return render_template('login.html', error_message="El nombre de usuario ya está en uso")
    else:
        # Insertar el nuevo usuario en la tabla "users"
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        # Crear una nueva base de datos de tareas para el usuario
        create_task_db(username)
        return render_template('login.html', success_message="¡Usuario registrado con éxito! Ahora puede iniciar sesión.")
       
@app.route('/chan_sin', methods=['POST'])
def chan_sin():
    return render_template('chan_in.html')