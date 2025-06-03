import sqlite3
import json
import hashlib
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen para ReflectApp - CORREGIDO SIN IA"""

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

                # Tabla de entradas diarias zen - SIMPLIFICADA SIN IA
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS daily_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        free_reflection TEXT NOT NULL,
                        positive_tags TEXT DEFAULT '[]',
                        negative_tags TEXT DEFAULT '[]',
                        worth_it INTEGER,
                        mood_score INTEGER DEFAULT 5,
                        word_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # ✅ Tabla de momentos interactivos - MEJORADA
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS interactive_moments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        moment_id TEXT NOT NULL,
                        emoji TEXT NOT NULL,
                        text TEXT NOT NULL,
                        moment_type TEXT NOT NULL CHECK (moment_type IN ('positive', 'negative')),
                        intensity INTEGER NOT NULL CHECK (intensity >= 1 AND intensity <= 10),
                        category TEXT NOT NULL DEFAULT 'general',
                        time_str TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        is_active INTEGER DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # Índices para rendimiento zen
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_user_date ON daily_entries(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactive_moments_user_date ON interactive_moments(user_id, entry_date, is_active)")

                conn.commit()
                print("✨ Base de datos zen inicializada correctamente SIN IA")

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
        """✅ CORREGIDO: Guardar momento interactivo individual con persistencia"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # ✅ VERIFICAR PRIMERO que la columna is_active existe
                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
                    # Versión con is_active
                    cursor.execute("""
                        INSERT INTO interactive_moments (
                            user_id, moment_id, emoji, text, moment_type, 
                            intensity, category, time_str, entry_date, is_active
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """, (
                        user_id,
                        moment_data.get('id', str(int(datetime.now().timestamp() * 1000))),
                        moment_data.get('emoji', ''),
                        moment_data.get('text', ''),
                        moment_data.get('type', 'positive'),
                        moment_data.get('intensity', 5),
                        moment_data.get('category', 'general'),
                        moment_data.get('time', datetime.now().strftime("%H:%M")),
                        today
                    ))
                else:
                    # Versión sin is_active (para compatibilidad)
                    cursor.execute("""
                        INSERT INTO interactive_moments (
                            user_id, moment_id, emoji, text, moment_type, 
                            intensity, category, time_str, entry_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        moment_data.get('id', str(int(datetime.now().timestamp() * 1000))),
                        moment_data.get('emoji', ''),
                        moment_data.get('text', ''),
                        moment_data.get('type', 'positive'),
                        moment_data.get('intensity', 5),
                        moment_data.get('category', 'general'),
                        moment_data.get('time', datetime.now().strftime("%H:%M")),
                        today
                    ))

                moment_id = cursor.lastrowid
                print(f"💾 Momento guardado: {moment_data.get('emoji')} {moment_data.get('text')} (ID: {moment_id})")
                return moment_id

        except Exception as e:
            print(f"❌ Error guardando momento interactivo: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_interactive_moments_today(self, user_id: int) -> List[Dict[str, Any]]:
        """✅ CORREGIDO: Obtener momentos activos del día actual"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # ✅ VERIFICAR si existe la columna is_active
                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
                    # Versión con is_active
                    cursor.execute("""
                        SELECT moment_id, emoji, text, moment_type, intensity, 
                               category, time_str, created_at
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ? AND is_active = 1
                        ORDER BY time_str, created_at
                    """, (user_id, today))
                else:
                    # Versión sin is_active (obtener todos)
                    cursor.execute("""
                        SELECT moment_id, emoji, text, moment_type, intensity, 
                               category, time_str, created_at
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
                        'created_at': row[7]
                    }
                    moments.append(moment_dict)

                print(f"📚 Cargados {len(moments)} momentos de hoy")
                return moments

        except Exception as e:
            print(f"❌ Error obteniendo momentos interactivos: {e}")
            return []

    def deactivate_interactive_moments_today(self, user_id: int) -> bool:
        """✅ NUEVO: Desactivar momentos del día (no eliminar)"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE interactive_moments 
                    SET is_active = 0 
                    WHERE user_id = ? AND entry_date = ? AND is_active = 1
                """, (user_id, today))

                updated_count = cursor.rowcount
                print(f"✅ Desactivados {updated_count} momentos de hoy")
                return True

        except Exception as e:
            print(f"❌ Error desactivando momentos: {e}")
            return False

    def count_moments_today(self, user_id: int) -> Dict[str, int]:
        """✅ NUEVO: Contar momentos activos del día"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT moment_type, COUNT(*) 
                    FROM interactive_moments 
                    WHERE user_id = ? AND entry_date = ? AND is_active = 1
                    GROUP BY moment_type
                """, (user_id, today))

                results = cursor.fetchall()
                counts = {"positive": 0, "negative": 0, "total": 0}

                for moment_type, count in results:
                    counts[moment_type] = count
                    counts["total"] += count

                return counts

        except Exception as e:
            print(f"❌ Error contando momentos: {e}")
            return {"positive": 0, "negative": 0, "total": 0}

    # ===============================
    # MÉTODOS DE ENTRADAS DIARIAS - SIMPLIFICADO SIN IA
    # ===============================
    def save_daily_entry(self, user_id: int, free_reflection: str,
                         positive_tags: List = None, negative_tags: List = None,
                         worth_it: Optional[bool] = None, mood_score: int = 5) -> Optional[int]:
        """✅ Guardar entrada diaria SIMPLIFICADA SIN IA"""
        try:
            print(f"💾 === GUARDANDO ENTRADA DIARIA PARA USUARIO {user_id} ===")

            # Procesar tags de manera segura
            def process_tags(tags):
                if not tags:
                    return []

                processed = []
                for tag in tags:
                    if isinstance(tag, dict):
                        processed.append({
                            "name": tag.get('name', ''),
                            "context": tag.get('context', ''),
                            "emoji": tag.get('emoji', '✨')
                        })
                    else:
                        processed.append({
                            "name": str(tag),
                            "context": '',
                            "emoji": '✨'
                        })
                return processed

            positive_tags_list = process_tags(positive_tags)
            negative_tags_list = process_tags(negative_tags)

            # Convertir a JSON
            positive_tags_json = json.dumps(positive_tags_list, ensure_ascii=False)
            negative_tags_json = json.dumps(negative_tags_list, ensure_ascii=False)

            # Calcular métricas simples
            word_count = len(free_reflection.split())

            # Mood score basado en balance si no se proporciona
            if mood_score == 5:  # Valor por defecto
                total_positive = len(positive_tags_list)
                total_negative = len(negative_tags_list)

                if total_positive > total_negative:
                    mood_score = 7 + min(2, total_positive - total_negative)
                elif total_negative > total_positive:
                    mood_score = 4 - min(2, total_negative - total_positive)

            mood_score = max(1, min(10, mood_score))

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
                            mood_score = ?,
                            word_count = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, mood_score, word_count, entry_id))
                else:
                    # CREAR nueva entrada
                    print(f"✨ Creando nueva entrada")

                    cursor.execute("""
                        INSERT INTO daily_entries (
                            user_id, free_reflection, positive_tags, negative_tags,
                            worth_it, mood_score, word_count, entry_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, mood_score, word_count, today))

                    entry_id = cursor.lastrowid

                print(f"🌸 Entrada zen guardada (ID: {entry_id}, Mood: {mood_score}/10)")
                return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada zen: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_daily_entry_from_moments(self, user_id: int, free_reflection: str = "",
                                        worth_it: Optional[bool] = None) -> Optional[int]:
        """✅ NUEVO: Crear entrada diaria desde momentos interactivos"""
        try:
            print(f"🔄 Creando entrada desde momentos para usuario {user_id}")

            # Obtener momentos activos del día
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
                    "context": f"Momento {moment['category']} a las {moment['time']}",
                    "emoji": moment['emoji']
                }

                if moment['type'] == 'positive':
                    positive_tags.append(tag_dict)
                else:
                    negative_tags.append(tag_dict)

            # Calcular mood automático basado en momentos
            total_positive = len(positive_tags)
            total_negative = len(negative_tags)

            if total_positive > total_negative:
                auto_mood = 7
            elif total_negative > total_positive:
                auto_mood = 4
            else:
                auto_mood = 5

            # Crear entrada
            entry_id = self.save_daily_entry(
                user_id=user_id,
                free_reflection=free_reflection or f"Reflexión del día - {total_positive + total_negative} momentos registrados",
                positive_tags=positive_tags,
                negative_tags=negative_tags,
                worth_it=worth_it,
                mood_score=auto_mood
            )

            if entry_id:
                # Desactivar momentos (no eliminar)
                self.deactivate_interactive_moments_today(user_id)
                print(f"✅ Entrada creada desde momentos con ID: {entry_id}")

            return entry_id

        except Exception as e:
            print(f"❌ Error creando entrada desde momentos: {e}")
            return None

    # ===============================
    # MÉTODOS DE CONSULTA - SIMPLIFICADOS
    # ===============================
    def get_user_entries(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener entradas zen del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, free_reflection, positive_tags, negative_tags, worth_it,
                           mood_score, word_count, entry_date, created_at, updated_at
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
                    except:
                        positive_tags = []

                    try:
                        negative_tags = json.loads(row[3] or "[]")
                    except:
                        negative_tags = []

                    entry = {
                        "id": row[0],
                        "free_reflection": row[1],
                        "positive_tags": positive_tags,
                        "negative_tags": negative_tags,
                        "worth_it": None if row[4] is None else bool(row[4]),
                        "mood_score": row[5],
                        "word_count": row[6],
                        "entry_date": row[7],
                        "created_at": row[8],
                        "updated_at": row[9]
                    }
                    entries.append(entry)

                return entries

        except Exception as e:
            print(f"❌ Error obteniendo entradas zen: {e}")
            return []

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

                    # Contar tags
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

                    # Contar tags
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