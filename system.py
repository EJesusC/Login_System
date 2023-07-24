# Systema backend para funcionamiento del programa
# Todo el codigo es programacion modular para reutilizacion de codigo

# Importaciones
import hashlib
from cryptography.fernet import Fernet, base64
from getpass import getpass
import sqlite3
from tkinter import messagebox

# Creacion de base de datos en caso de que no exista
def create_table(conn):
    print("conectando db")
    
    # Consulta
    query = ("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
            );""")

    conn.execute(query)
    conn.commit()

    print("db conectada")
    return conn

# Generacion de llaves por hash utilizando username como seguro - 
# - para generar siempre la misma llave por usuario
def generate_secret_key( username):
    master_key = 'Codigo por mrLowhi'
    dk = hashlib.pbkdf2_hmac('sha256', username.encode(), master_key.encode(), 100000)
    
    return base64.urlsafe_b64encode(dk)


# Encriptacion de la llave para guardar en la base
def encrypt_password(username, password):
    key = generate_secret_key(username)
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    
    return base64.urlsafe_b64encode(encrypted_password).decode()


# Decencriptacion de la contraseña almacenada para comparacion con contraseña que se -
# - encuentra en la base de datos
def check_password(username, input_password, encrypted_password):
    # Usando el generador de llaves para crear la base del programa
    key = generate_secret_key(username)
    cipher_suite = Fernet(key)

    # Asegurando la longitud de la contraseña
    encrypted_password = base64.urlsafe_b64decode(encrypted_password.encode())
    
    # Decriptando la contraseña guardada
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    print('decry',decrypted_password)
    
    return input_password == decrypted_password


# Sistema de login principal
def login(username, password, conn):
    print("Ejecutando login")


    # Conexion y consulta a la base de datos
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=?;"
    print('user',username)
    print('pass',password)
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    print('consulta',user)

    # Validacion de usuario
    if user:
        encrypted_password = user[3]
        
        # Validacion de contraseña
        if check_password(username, password, encrypted_password):
            messagebox.showinfo(message="Login correcto", title="Auth System")
        else:
            messagebox.showerror(message="Usuario o password incorrectos", title="Auth System")
    else:
        messagebox.showerror(message="Usuario o password incorrectos", title="Auth System")

    print("Login ejecutado")

def register(name, username, password, rep_password, conn):
    print("Ejecutando register")

    if password != rep_password:
        messagebox.showwarning(message="Las passwords no coinciden", title="Auth System")
        
        return

    if not is_username_available(username,conn):
        messagebox.showwarning(message="El usuario ya se esta utilizando \nPor favor utilice otro", 
                                title="Auth System"
                                )
        
        return
    
    encrypted_password = encrypt_password(username, password)

    # Conexion y consulta a la base de datos
    query = "INSERT INTO users (name, username, password) VALUES (?, ?, ?);"
    conn.execute(query, (name, username, encrypted_password))
    conn.commit()

    messagebox.showinfo(message='Registro realizado', title='Auth System')    
    print("Register ejecutado")


# Validacion de disponibilidad de usuario
def is_username_available(username,conn):
    query = "SELECT COUNT(*) FROM users WHERE username=?;"
    cursor = conn.execute(query, (username,))
    count = cursor.fetchone()[0]

    return count == 0
