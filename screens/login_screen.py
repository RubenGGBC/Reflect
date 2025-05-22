from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
import os

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Variable para almacenar el usuario logueado
        self.current_user = None

        # VERIFICAR Y CREAR BASE DE DATOS AL INICIALIZAR
        self.setup_database()

        self.build_ui()

        # Dialog para mensajes
        self.dialog = None

    def build_ui(self):
        """Construye la interfaz de usuario"""
        # Layout principal
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )

        # Título
        title = MDLabel(
            text="ReflectApp",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(80)
        )
        layout.add_widget(title)

        # Subtítulo
        subtitle = MDLabel(
            text="Tu diario reflexivo con IA",
            theme_text_color="Secondary",
            font_style="Subtitle1",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(subtitle)

        # Espacio
        spacer = MDBoxLayout(size_hint_y=None, height=dp(40))
        layout.add_widget(spacer)

        # Campo de correo
        self.email = MDTextField(
            hint_text="Correo electrónico",
            helper_text="Introduce tu correo electrónico",
            helper_text_mode="on_focus",
            icon_right="email",
            size_hint_x=None,
            width=dp(300),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.email)

        # Campo de contraseña
        self.password = MDTextField(
            hint_text="Contraseña",
            helper_text="Introduce tu contraseña",
            helper_text_mode="on_focus",
            icon_right="eye-off",
            size_hint_x=None,
            width=dp(300),
            pos_hint={"center_x": 0.5},
            password=True
        )
        layout.add_widget(self.password)

        # Espacio
        spacer2 = MDBoxLayout(size_hint_y=None, height=dp(20))
        layout.add_widget(spacer2)

        # Botón de inicio de sesión
        login_button = MDRaisedButton(
            text="Iniciar sesión",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            on_release=self.login
        )
        layout.add_widget(login_button)

        # Botón de registro
        register_button = MDTextButton(
            text="¿No tienes cuenta? Regístrate",
            pos_hint={"center_x": 0.5},
            on_release=self.show_register
        )
        layout.add_widget(register_button)

        # Botón de usuario de prueba (para desarrollo)
        test_button = MDTextButton(
            text="Crear usuario de prueba",
            pos_hint={"center_x": 0.5},
            on_release=self.create_test_user
        )
        layout.add_widget(test_button)

        # Espacio restante
        layout.add_widget(MDBoxLayout())

        self.add_widget(layout)

    def setup_database(self):
        """
        Verifica si existe el servicio de base de datos y lo crea si es necesario
        """
        print("=== VERIFICANDO BASE DE DATOS ===")

        try:
            # Intentar importar el servicio
            from services import db
            print(f"✅ Servicio de BD encontrado: {db}")
            print(f"✅ Ruta de BD: {db.db_path}")

            # Verificar si el archivo de BD existe
            if os.path.exists(db.db_path):
                print("✅ Archivo de base de datos existe")
                self.verify_tables(db)
            else:
                print("⚠️ Archivo de BD no existe, se creará automáticamente")

        except ImportError as e:
            print(f"❌ Error importando servicio de BD: {e}")
            self.create_database_service()
        except Exception as e:
            print(f"❌ Error verificando BD: {e}")

    def verify_tables(self, db):
        """
        Verifica que las tablas necesarias existen en la base de datos
        """
        try:
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()

            # Verificar tabla users
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                print("✅ Tabla 'users' existe")
            else:
                print("⚠️ Tabla 'users' no existe, reinicializando BD")
                conn.close()
                db.init_database()
                return

            # Verificar tabla entries
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
            if cursor.fetchone():
                print("✅ Tabla 'entries' existe")
            else:
                print("⚠️ Tabla 'entries' no existe, reinicializando BD")
                conn.close()
                db.init_database()
                return

            # Ver cuántos usuarios hay
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✅ Total de usuarios en BD: {user_count}")

            conn.close()

        except Exception as e:
            print(f"❌ Error verificando tablas: {e}")
            print("🔄 Reinicializando base de datos...")
            db.init_database()

    def create_database_service(self):
        """
        Crea el archivo de servicio de base de datos si no existe
        """
        print("🔧 Creando servicio de base de datos...")

        # Crear directorio services si no existe
        services_dir = "services"
        if not os.path.exists(services_dir):
            os.makedirs(services_dir)
            print(f"✅ Directorio '{services_dir}' creado")

        # Crear __init__.py si no existe
        init_file = os.path.join(services_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Exporta funciones importantes\n")
                f.write("from .database_service import DatabaseService\n\n")
                f.write("# Instancia global de la base de datos\n")
                f.write("db = DatabaseService()\n")
            print(f"✅ Archivo '{init_file}' creado")

        # Crear database_service.py básico si no existe
        db_service_file = os.path.join(services_dir, "database_service.py")
        if not os.path.exists(db_service_file):
            self.create_basic_database_service(db_service_file)

        print("✅ Servicio de base de datos creado")

    def create_basic_database_service(self, file_path):
        """
        Crea un archivo básico de database_service.py
        """
        basic_service = """import sqlite3
import json
import hashlib
import os
from datetime import datetime

class DatabaseService:
    def __init__(self, db_path="data/reflect_app.db"):
        self.db_path = db_path
        
        # Crear directorio data si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.init_database()
    
    def init_database(self):
        \"\"\"Inicializa la base de datos y crea las tablas necesarias\"\"\"
        print("Inicializando base de datos...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de entradas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT NOT NULL,
                emotion TEXT,
                categories TEXT,
                sentiment TEXT,
                insights TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada correctamente")
    
    def create_user(self, email, password, name=None):
        \"\"\"Crea un nuevo usuario\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, name)
                VALUES (?, ?, ?)
            ''', (email, password_hash, name))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Usuario creado con ID: {user_id}")
            return user_id
            
        except sqlite3.IntegrityError:
            conn.close()
            print("⚠️ El email ya existe")
            return None
    
    def login_user(self, email, password):
        \"\"\"Autentica un usuario y devuelve su ID si es válido\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT id, name FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_data = {"id": result[0], "name": result[1], "email": email}
            print(f"✅ Login exitoso para usuario: {user_data}")
            return user_data
        else:
            print("❌ Credenciales inválidas")
            return None
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(basic_service)

        print(f"✅ Archivo '{file_path}' creado")

    def login(self, instance):
        """
        Método principal de login
        """
        print("=== INICIANDO PROCESO DE LOGIN ===")

        # Obtener datos de los campos
        email = self.email.text.strip()
        password = self.password.text

        # Validaciones
        if not email or not password:
            self.show_dialog("Error", "Por favor, completa todos los campos")
            return

        if "@" not in email:
            self.show_dialog("Error", "Introduce un email válido")
            return

        print(f"Intentando login con email: {email}")

        try:
            # Importar la instancia db
            from services import db

            # Intentar autenticación
            usuario = db.login_user(email, password)

            if usuario:
                # Login exitoso
                print(f"✅ Login exitoso: {usuario}")
                self.current_user = usuario

                # Pasar datos a la pantalla de entrada
                try:
                    entry_screen = self.manager.get_screen("entry")
                    entry_screen.current_user = usuario
                except:
                    print("⚠️ No se pudo pasar datos a entry_screen")

                # Mensaje de bienvenida
                nombre = usuario.get('name', usuario['email'])
                self.show_dialog(
                    "¡Bienvenido!",
                    f"Hola {nombre}, login exitoso",
                    auto_dismiss=True
                )

                # Cambiar pantalla
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'entry'), 1.5)

                # Limpiar campos
                self.clear_fields()

            else:
                # Login fallido
                self.show_dialog(
                    "Error de autenticación",
                    "Email o contraseña incorrectos"
                )

        except Exception as e:
            print(f"❌ Error en login: {e}")
            import traceback
            traceback.print_exc()
            self.show_dialog(
                "Error",
                f"Error en el sistema: {str(e)}"
            )

    def create_test_user(self, instance):
        """
        Crea un usuario de prueba para desarrollo
        """
        print("=== CREANDO USUARIO DE PRUEBA ===")

        test_email = "test@ejemplo.com"
        test_password = "123456"
        test_name = "Usuario de Prueba"

        try:
            # Importar la instancia db
            from services import db

            user_id = db.create_user(test_email, test_password, test_name)

            if user_id:
                # Usuario creado
                self.show_dialog(
                    "Usuario creado",
                    f"Usuario de prueba creado exitosamente\n\nEmail: {test_email}\nPassword: {test_password}"
                )

                # Autocompletar campos
                self.email.text = test_email
                self.password.text = test_password

            else:
                # Usuario ya existe
                self.show_dialog(
                    "Usuario existe",
                    f"El usuario de prueba ya existe\n\nEmail: {test_email}\nPassword: {test_password}"
                )

                # Autocompletar campos
                self.email.text = test_email
                self.password.text = test_password

        except Exception as e:
            print(f"❌ Error creando usuario de prueba: {e}")
            import traceback
            traceback.print_exc()
            self.show_dialog("Error", f"Error: {str(e)}")

    def show_register(self, instance):
        """
        Muestra la pantalla de registro
        """
        try:
            self.manager.current = "register"
        except:
            self.show_dialog(
                "Registro",
                "Pantalla de registro no disponible aún.\n\nUsa 'Crear usuario de prueba' para probar la app."
            )

    def clear_fields(self):
        """
        Limpia los campos de email y password
        """
        self.email.text = ""
        self.password.text = ""

    def show_dialog(self, title, text, auto_dismiss=False):
        """
        Muestra un diálogo con el texto proporcionado
        """
        if self.dialog:
            self.dialog.dismiss()

        ok_button = MDTextButton(
            text="OK",
            on_release=lambda x: self.dialog.dismiss()
        )

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[ok_button]
        )
        self.dialog.open()

        if auto_dismiss:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.dialog.dismiss(), 2)

    def on_enter(self):
        """
        Se ejecuta cuando entras a esta pantalla
        """
        print("Entrando a pantalla de login")

    def on_leave(self):
        """
        Se ejecuta cuando sales de esta pantalla
        """
        print("Saliendo de pantalla de login")