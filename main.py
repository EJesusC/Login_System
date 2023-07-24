# Programa de login sencillo con sistema de registro para usuarios
# Se utiliza sql lite para la creacion de la base de datos
# Toda la escritura del codigo se encuentra en ingles
# Para la interaccion con el usuario se utiliza tkinter

# Importaciones
import tkinter as tk
import sqlite3

# Importacion de archivo para backend del programa
import system

# Clase principal para la GUI de usuario
class AuthenticationSystem:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Authentication System")
        self.master.geometry("400x400")

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack()

        self.login_frame = tk.Frame(self.master)
        self.register_frame = tk.Frame(self.master)

        self.create_menu()
        self.create_login_screen()
        self.create_register_screen()

        # Elija el nombre de la base de datos desde esta variable
        db_name  = 'users.db'

        # Utiliar extension .bd
        self.conn = sqlite3.connect(db_name)
        system.create_table(self.conn)

    def create_menu(self):
        menu_label = tk.Label(self.menu_frame, text="Auth System")
        menu_label.pack(pady=10)

        login_button = tk.Button(self.menu_frame,
                                text="Login", 
                                command=self.sh_login_screen
                                )
        login_button.pack(pady=5)

        register_button = tk.Button(self.menu_frame,
                                text="Register", 
                                command=self.sh_register_screen
                                )    
        register_button.pack(pady=5)    

    def create_login_screen(self):
        login_label = tk.Label(self.login_frame, text="Login")
        login_label.pack(pady=10)

        username_label = tk.Label(self.login_frame, text="Username:")
        username_label.pack()

        self.username2_entry = tk.Entry(self.login_frame)
        self.username2_entry.pack()

        password_label = tk.Label(self.login_frame, text="Password:")
        password_label.pack()

        self.password2_entry = tk.Entry(self.login_frame, show="*")
        self.password2_entry.pack()

        login_button = tk.Button(self.login_frame, 
                                text="Login", 
                                command=self.login)
        login_button.pack(pady=10)

        self.login_frame.pack()        

    def create_register_screen(self):
        register_label = tk.Label(self.register_frame, text="Register")
        register_label.pack(pady=10)

        name_label = tk.Label(self.register_frame, text="Nombre:")
        name_label.pack()

        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.pack()

        username_label = tk.Label(self.register_frame, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self.register_frame)
        self.username_entry.pack()

        password_label = tk.Label(self.register_frame, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self.register_frame, show="*")
        self.password_entry.pack()

        rep_password_label = tk.Label(self.register_frame, text="Repetir Password")
        rep_password_label.pack()

        self.rep_password_entry = tk.Entry(self.register_frame)
        self.rep_password_entry.pack()

        register_button = tk.Button(self.register_frame, 
                                    text="Register", 
                                    command=self.register
                                    )
        register_button.pack(pady=10)


    def sh_login_screen(self):
        self.register_frame.pack_forget()
        self.login_frame.pack()
        

    def sh_register_screen(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()
        

    def login(self):
        username = self.username2_entry.get()
        password = self.password2_entry.get()

        system.login(username, password, self.conn)

    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        rep_password = self.rep_password_entry.get()

        system.register(name, username, password, rep_password, self.conn)


# Ejecucion pricipal del codigo
if __name__ == "__main__":
    auth_system = AuthenticationSystem()
    auth_system.master.mainloop()