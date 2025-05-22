import sqlite3
import json
import hashlib
import os
from datetime import datetime

class DatabaseService:
    def __init__(self, db_path="data/reflect_app.db"):
        self.db_path = db_path

        # CREAR DIRECTORIO ANTES DE CONECTAR A LA BD
        self.ensure_data_directory()

        self.init_database()

    def ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        try:
            # Obtener el directorio del archivo de BD
            db_dir = os.path.dirname(self.db_path)

            # Si la ruta está vacía, usar directorio actual
            if not db_dir:
                db_dir = "."

            # Crear directorio si no existe
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"✅ Directorio creado: {db_dir}")
            else:
                print(f"✅ Directorio existe: {db_dir}")

            # Verificar que se puede escribir en el directorio
            test_file = os.path.join(db_dir, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ Permisos de escritura OK en: {db_dir}")
            except Exception as e:
                print(f"❌ No se puede escribir en: {db_dir} - Error: {e}")
                # Cambiar a directorio actual como fallback
                self.db_path = "reflect_app.db"
                print(f"🔄 Usando ruta alternativa: {self.db_path}")

        except Exception as e:
            print(f"❌ Error creando directorio: {e}")
            # Usar directorio actual como fallback
            self.db_path = "reflect_app.db"
            print(f"🔄 Usando ruta alternativa: {self.db_path}")

    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        print(f"Inicializando base de datos en: {self.db_path}")

        try:
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

        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            raise

    def create_user(self, email, password, name=None):
        """Crea un nuevo usuario"""
        print(f"Creando usuario: {email}")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

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
            print("⚠️ El email ya existe")
            return None
        except Exception as e:
            print(f"❌ Error creando usuario: {e}")
            return None

    def login_user(self, email, password):
        """Autentica un usuario y devuelve sus datos si es válido"""
        print(f"Intentando login para: {email}")

        try:
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

        except Exception as e:
            print(f"❌ Error en login: {e}")
            return None

    def save_entry(self, user_id, text, emotion=None, categories=None, sentiment=None, insights=None):
        """Guarda una nueva entrada en el diario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Convertir categorías a JSON
            categories_json = json.dumps(categories) if categories else None

            cursor.execute('''
                INSERT INTO entries (user_id, text, emotion, categories, sentiment, insights)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, text, emotion, categories_json, sentiment, insights))

            entry_id = cursor.lastrowid
            conn.commit()
            conn.close()

            print(f"✅ Entrada guardada con ID: {entry_id}")
            return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada: {e}")
            return None

    def get_user_entries(self, user_id, limit=10):
        """Obtiene las entradas de un usuario (más recientes primero)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, text, emotion, categories, sentiment, insights, created_at
                FROM entries 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))

            results = cursor.fetchall()
            conn.close()

            entries = []
            for row in results:
                categories = json.loads(row[3]) if row[3] else []
                entries.append({
                    "id": row[0],
                    "text": row[1],
                    "emotion": row[2],
                    "categories": categories,
                    "sentiment": row[4],
                    "insights": row[5],
                    "created_at": row[6]
                })

            return entries

        except Exception as e:
            print(f"❌ Error obteniendo entradas: {e}")
            return []