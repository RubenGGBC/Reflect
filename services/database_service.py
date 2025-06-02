import sqlite3
import json
import hashlib
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen para ReflectApp - CORREGIDO COMPLETO"""

    def __init__(self, db_path: str = "data/reflect_zen.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._initialize_database()

    def _ensure_directory(self) -> None:
        """Crear directorio de datos si no existe"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"🗂️ Directorio zen creado: {db_dir}")

    def _initialize_database(self) -> None:
        """Inicializar base de datos con esquema zen COMPLETO"""
        print(f"🧘‍♀️ Inicializando base de datos zen: {self.db_path}")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabla de usuarios zen
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        name TEXT NOT NULL,
                        avatar_emoji TEXT DEFAULT '🧘‍♀️',
                        preferences TEXT DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                """)

                # Tabla de entradas diarias zen
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS daily_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        free_reflection TEXT NOT NULL,
                        positive_tags TEXT DEFAULT '[]',
                        negative_tags TEXT DEFAULT '[]',
                        worth_it INTEGER,
                        overall_sentiment TEXT,
                        mood_score INTEGER,
                        ai_summary TEXT,
                        word_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # ✅ NUEVA: Tabla de momentos interactivos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS interactive_moments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        moment_id TEXT NOT NULL,
                        emoji TEXT NOT NULL,
                        text TEXT NOT NULL,
                        moment_type TEXT NOT NULL CHECK (moment_type IN ('positive', 'negative')),
                        intensity INTEGER NOT NULL CHECK (intensity >= 1 AND intensity <= 10),
                        category TEXT NOT NULL,
                        time_str TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        timestamp_data TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # ✅ NUEVA: Tabla de tags temporales
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS temp_tags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        tag_name TEXT NOT NULL,
                        tag_context TEXT NOT NULL,
                        tag_type TEXT NOT NULL,
                        tag_emoji TEXT NOT NULL,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # Índices para rendimiento zen
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_user_date ON daily_entries(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_temp_tags_user_date ON temp_tags(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactive_moments_user_date ON interactive_moments(user_id, entry_date)")

                conn.commit()
                print("✨ Base de datos zen inicializada correctamente")

        except Exception as e:
            print(f"❌ Error inicializando base de datos zen: {e}")
            import traceback
            traceback.print_exc()
            raise

    # ===============================
    # MÉTODOS DE USUARIOS
    # ===============================
    def create_user(self, email: str, password: str, name: str, avatar_emoji: str = "🧘‍♀️") -> Optional[int]:
        """Crear nuevo usuario zen"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (email, password_hash, name, avatar_emoji)
                    VALUES (?, ?, ?, ?)
                """, (email, password_hash, name, avatar_emoji))

                user_id = cursor.lastrowid
                print(f"🌸 Usuario zen creado: {email} (ID: {user_id})")
                return user_id

        except sqlite3.IntegrityError:
            print(f"⚠️ El email {email} ya existe en el santuario")
            return None
        except Exception as e:
            print(f"❌ Error creando usuario zen: {e}")
            return None

    def login_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar usuario zen"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, name, avatar_emoji, preferences 
                    FROM users 
                    WHERE email = ? AND password_hash = ?
                """, (email, password_hash))

                result = cursor.fetchone()

                if result:
                    user_id, name, avatar_emoji, preferences = result

                    # Actualizar último login zen
                    cursor.execute("""
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (user_id,))

                    user_data = {
                        "id": user_id,
                        "email": email,
                        "name": name,
                        "avatar_emoji": avatar_emoji or "🧘‍♀️",
                        "preferences": json.loads(preferences or "{}")
                    }

                    print(f"🌺 Bienvenido de vuelta: {name}")
                    return user_data

                print(f"❌ Credenciales incorrectas para: {email}")
                return None

        except Exception as e:
            print(f"❌ Error en login zen: {e}")
            return None

    # ===============================
    # MÉTODOS DE MOMENTOS INTERACTIVOS - CORREGIDOS
    # ===============================
    def save_interactive_moment(self, user_id: int, moment_data: dict) -> Optional[int]:
        """
        ✅ CORREGIDO: Guardar momento interactivo individual
        """
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO interactive_moments (
                        user_id, moment_id, emoji, text, moment_type, 
                        intensity, category, time_str, entry_date, timestamp_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    moment_data.get('id', 0),
                    moment_data.get('emoji', ''),
                    moment_data.get('text', ''),
                    moment_data.get('type', 'positive'),
                    moment_data.get('intensity', 5),
                    moment_data.get('category', 'general'),
                    moment_data.get('time', '00:00'),
                    today,
                    moment_data.get('timestamp', '')
                ))

                moment_id = cursor.lastrowid
                print(f"💾 Momento interactivo guardado: {moment_data.get('emoji')} {moment_data.get('text')} (ID: {moment_id})")
                return moment_id

        except Exception as e:
            print(f"❌ Error guardando momento interactivo: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_interactive_moments_today(self, user_id: int) -> List[Dict[str, Any]]:
        """
        ✅ CORREGIDO: Obtener momentos interactivos del día actual
        """
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT moment_id, emoji, text, moment_type, intensity, 
                           category, time_str, timestamp_data, created_at
                    FROM interactive_moments 
                    WHERE user_id = ? AND entry_date = ?
                    ORDER BY time_str, created_at
                """, (user_id, today))

                results = cursor.fetchall()

                moments = []
                for row in results:
                    moment_dict = {
                        'id': row[0],
                        'emoji': row[1],
                        'text': row[2],
                        'type': row[3],
                        'intensity': row[4],
                        'category': row[5],
                        'time': row[6],
                        'timestamp': row[7] or '',
                        'created_at': row[8]
                    }
                    moments.append(moment_dict)

                print(f"📚 Cargados {len(moments)} momentos interactivos de hoy")
                return moments

        except Exception as e:
            print(f"❌ Error obteniendo momentos interactivos: {e}")
            return []

    def clear_interactive_moments_today(self, user_id: int) -> bool:
        """
        ✅ CORREGIDO: Eliminar todos los momentos interactivos del día
        """
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    DELETE FROM interactive_moments 
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                deleted_count = cursor.rowcount
                print(f"🗑️ Eliminados {deleted_count} momentos interactivos de hoy")
                return True

        except Exception as e:
            print(f"❌ Error eliminando momentos interactivos: {e}")
            return False

    def save_interactive_moments_as_entry(self, user_id: int, reflection: str = "", worth_it: Optional[bool] = None) -> Optional[int]:
        """
        ✅ NUEVO: Convertir momentos interactivos del día en entrada diaria
        """
        try:
            print(f"🔄 Convirtiendo momentos interactivos en entrada diaria para usuario {user_id}")

            # Obtener momentos del día
            moments = self.get_interactive_moments_today(user_id)

            if not moments:
                print("⚠️ No hay momentos para convertir")
                return None

            # Separar por tipo
            positive_tags = []
            negative_tags = []

            for moment in moments:
                tag_dict = {
                    "name": moment['text'],
                    "context": f"Momento {moment['category']} de intensidad {moment['intensity']} a las {moment['time']}",
                    "emoji": moment['emoji']
                }

                if moment['type'] == 'positive':
                    positive_tags.append(tag_dict)
                else:
                    negative_tags.append(tag_dict)

            print(f"📊 Convertidos: {len(positive_tags)} positivos, {len(negative_tags)} negativos")

            # Usar el método existente para guardar entrada
            entry_id = self.save_daily_entry(
                user_id=user_id,
                free_reflection=reflection or "Entrada creada desde Momentos Interactivos",
                positive_tags=positive_tags,
                negative_tags=negative_tags,
                worth_it=worth_it
            )

            if entry_id:
                print(f"✅ Entrada diaria creada con ID: {entry_id}")
                # NO eliminar los momentos, dejarlos para referencia
                return entry_id
            else:
                print("❌ Error creando entrada diaria")
                return None

        except Exception as e:
            print(f"❌ Error convirtiendo momentos a entrada: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ===============================
    # MÉTODOS DE ENTRADAS DIARIAS - SIN IA
    # ===============================
    def save_daily_entry(self, user_id: int, free_reflection: str,
                         positive_tags: List = None, negative_tags: List = None,
                         worth_it: Optional[bool] = None) -> Optional[int]:
        """Guardar entrada diaria zen completa - SIN IA"""
        try:
            print(f"💾 === INICIANDO GUARDADO PARA USUARIO {user_id} ===")

            # Convertir tags a formato JSON SEGURO
            def tag_to_dict(tag):
                if hasattr(tag, '__dict__'):
                    return {
                        "name": getattr(tag, 'name', str(tag)),
                        "context": getattr(tag, 'context', ''),
                        "emoji": getattr(tag, 'emoji', '+' if getattr(tag, 'type', 'positive') == 'positive' else '-')
                    }
                elif isinstance(tag, dict):
                    return {
                        "name": tag.get('name', ''),
                        "context": tag.get('context', ''),
                        "emoji": tag.get('emoji', '+')
                    }
                else:
                    return {
                        "name": str(tag),
                        "context": '',
                        "emoji": '+'
                    }

            positive_tags_list = []
            if positive_tags:
                for tag in positive_tags:
                    tag_dict = tag_to_dict(tag)
                    positive_tags_list.append(tag_dict)

            negative_tags_list = []
            if negative_tags:
                for tag in negative_tags:
                    tag_dict = tag_to_dict(tag)
                    negative_tags_list.append(tag_dict)

            # Convertir a JSON
            positive_tags_json = json.dumps(positive_tags_list, ensure_ascii=False)
            negative_tags_json = json.dumps(negative_tags_list, ensure_ascii=False)

            # Calcular métricas básicas
            word_count = len(free_reflection.split())

            # Mood score simple basado en balance
            total_positive = len(positive_tags_list)
            total_negative = len(negative_tags_list)

            if total_positive > total_negative:
                mood_score = 7 + min(3, total_positive - total_negative)
            elif total_negative > total_positive:
                mood_score = 5 - min(3, total_negative - total_positive)
            else:
                mood_score = 5

            mood_score = max(1, min(10, mood_score))

            # Sentimiento general
            if mood_score >= 7:
                sentiment = "positive"
            elif mood_score <= 4:
                sentiment = "negative"
            else:
                sentiment = "balanced"

            # Convertir worth_it a entero para SQLite
            worth_it_int = None
            if worth_it is True:
                worth_it_int = 1
            elif worth_it is False:
                worth_it_int = 0

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Verificar si ya existe entrada para hoy
                today = date.today().isoformat()
                cursor.execute("""
                    SELECT id FROM daily_entries 
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                existing_entry = cursor.fetchone()

                if existing_entry:
                    # ACTUALIZAR entrada existente
                    entry_id = existing_entry[0]
                    print(f"🔄 Actualizando entrada existente {entry_id}")

                    cursor.execute("""
                        UPDATE daily_entries SET
                            free_reflection = ?,
                            positive_tags = ?,
                            negative_tags = ?,
                            worth_it = ?,
                            overall_sentiment = ?,
                            mood_score = ?,
                            ai_summary = ?,
                            word_count = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, sentiment, mood_score, "", word_count, entry_id))
                else:
                    # CREAR nueva entrada
                    print(f"✨ Creando nueva entrada")

                    cursor.execute("""
                        INSERT INTO daily_entries (
                            user_id, free_reflection, positive_tags, negative_tags,
                            worth_it, overall_sentiment, mood_score, ai_summary, word_count, entry_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, sentiment, mood_score, "", word_count, today))

                    entry_id = cursor.lastrowid

                print(f"🌸 Entrada zen guardada (ID: {entry_id}, Mood: {mood_score}/10)")
                return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada zen: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ===============================
    # MÉTODOS DE CONSULTA
    # ===============================
    def get_user_entries(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener entradas zen del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, free_reflection, positive_tags, negative_tags, worth_it,
                           overall_sentiment, mood_score, word_count,
                           entry_date, created_at, updated_at
                    FROM daily_entries 
                    WHERE user_id = ?
                    ORDER BY entry_date DESC, created_at DESC
                    LIMIT ? OFFSET ?
                """, (user_id, limit, offset))

                results = cursor.fetchall()
                print(f"🔍 Encontradas {len(results)} entradas para usuario {user_id}")

                entries = []
                for row in results:
                    # Parsear JSON de manera segura
                    try:
                        positive_tags = json.loads(row[2] or "[]")
                    except (json.JSONDecodeError, TypeError):
                        positive_tags = []

                    try:
                        negative_tags = json.loads(row[3] or "[]")
                    except (json.JSONDecodeError, TypeError):
                        negative_tags = []

                    entry = {
                        "id": row[0],
                        "free_reflection": row[1],
                        "positive_tags": positive_tags,
                        "negative_tags": negative_tags,
                        "worth_it": None if row[4] is None else bool(row[4]),
                        "overall_sentiment": row[5],
                        "mood_score": row[6],
                        "word_count": row[7],
                        "entry_date": row[8],
                        "created_at": row[9],
                        "updated_at": row[10]
                    }
                    entries.append(entry)

                return entries

        except Exception as e:
            print(f"❌ Error obteniendo entradas zen: {e}")
            return []

    def get_year_summary(self, user_id: int, year: int) -> Dict[int, Dict[str, int]]:
        """Obtener resumen de todo el año por meses"""
        try:
            first_day = date(year, 1, 1)
            last_day = date(year, 12, 31)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT entry_date, positive_tags, negative_tags
                    FROM daily_entries 
                    WHERE user_id = ? 
                          AND entry_date >= ? 
                          AND entry_date <= ?
                    ORDER BY entry_date
                """, (user_id, first_day.isoformat(), last_day.isoformat()))

                results = cursor.fetchall()

                # Inicializar datos para todos los meses
                year_data = {}
                for month in range(1, 13):
                    year_data[month] = {"positive": 0, "negative": 0, "total": 0}

                # Procesar resultados
                for row in results:
                    entry_date_str, positive_tags_json, negative_tags_json = row

                    entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                    month = entry_date.month

                    # Contar tags manualmente
                    try:
                        positive_tags = json.loads(positive_tags_json or "[]")
                        positive_count = len(positive_tags)
                    except:
                        positive_count = 0

                    try:
                        negative_tags = json.loads(negative_tags_json or "[]")
                        negative_count = len(negative_tags)
                    except:
                        negative_count = 0

                    year_data[month]["positive"] += positive_count
                    year_data[month]["negative"] += negative_count
                    year_data[month]["total"] += positive_count + negative_count

                return year_data

        except Exception as e:
            print(f"❌ Error obteniendo resumen del año {year}: {e}")
            year_data = {}
            for month in range(1, 13):
                year_data[month] = {"positive": 0, "negative": 0, "total": 0}
            return year_data

    def get_month_summary(self, user_id: int, year: int, month: int) -> Dict[int, Dict[str, Any]]:
        """Obtener resumen de días específicos de un mes"""
        try:
            first_day = date(year, month, 1)
            if month == 12:
                last_day = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = date(year, month + 1, 1) - timedelta(days=1)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT entry_date, positive_tags, negative_tags, worth_it
                    FROM daily_entries 
                    WHERE user_id = ? 
                          AND entry_date >= ? 
                          AND entry_date <= ?
                    ORDER BY entry_date
                """, (user_id, first_day.isoformat(), last_day.isoformat()))

                results = cursor.fetchall()
                month_data = {}

                for row in results:
                    entry_date_str, positive_tags_json, negative_tags_json, worth_it = row

                    entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                    day = entry_date.day

                    # Contar tags manualmente
                    try:
                        positive_tags = json.loads(positive_tags_json or "[]")
                        positive_count = len(positive_tags)
                    except:
                        positive_count = 0

                    try:
                        negative_tags = json.loads(negative_tags_json or "[]")
                        negative_count = len(negative_tags)
                    except:
                        negative_count = 0

                    worth_it_bool = None
                    if worth_it == 1:
                        worth_it_bool = True
                    elif worth_it == 0:
                        worth_it_bool = False

                    month_data[day] = {
                        "positive": positive_count,
                        "negative": negative_count,
                        "submitted": True,
                        "worth_it": worth_it_bool
                    }

                return month_data

        except Exception as e:
            print(f"❌ Error obteniendo resumen del mes {year}-{month}: {e}")
            return {}

    def get_day_entry(self, user_id: int, year: int, month: int, day: int) -> Optional[Dict[str, Any]]:
        """Obtener entrada completa de un día específico"""
        try:
            entry_date = date(year, month, day).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT free_reflection, positive_tags, negative_tags, 
                           worth_it, mood_score
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (user_id, entry_date))

                result = cursor.fetchone()

                if not result:
                    return None

                reflection, positive_tags_json, negative_tags_json, worth_it, mood_score = result

                # Convertir JSON a listas de manera segura
                try:
                    positive_tags = json.loads(positive_tags_json or "[]")
                except:
                    positive_tags = []

                try:
                    negative_tags = json.loads(negative_tags_json or "[]")
                except:
                    negative_tags = []

                worth_it_bool = None
                if worth_it == 1:
                    worth_it_bool = True
                elif worth_it == 0:
                    worth_it_bool = False

                return {
                    "reflection": reflection or "",
                    "positive_tags": positive_tags,
                    "negative_tags": negative_tags,
                    "worth_it": worth_it_bool,
                    "mood_score": mood_score or 5
                }

        except Exception as e:
            print(f"❌ Error obteniendo entrada del día {year}-{month}-{day}: {e}")
            return None

    def has_submitted_today(self, user_id: int) -> bool:
        """Verificar si el usuario ya submiteó una entrada hoy"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                count = cursor.fetchone()[0]
                return count > 0

        except Exception as e:
            print(f"❌ Error verificando entrada de hoy: {e}")
            return False

    def get_entry_count(self, user_id: int) -> int:
        """Obtener total de entradas del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM daily_entries WHERE user_id = ?", (user_id,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Error obteniendo contador zen: {e}")
            return 0