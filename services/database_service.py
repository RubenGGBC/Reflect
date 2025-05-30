import sqlite3
import json
import hashlib
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen para ReflectApp - CORREGIDO JSON"""

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
        """Inicializar base de datos con esquema zen CORREGIDO"""
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

                # Tabla de entradas diarias zen (CORREGIDA)
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

                # MIGRACIÓN MEJORADA: growth_tags a negative_tags
                cursor.execute("PRAGMA table_info(daily_entries)")
                columns = [column[1] for column in cursor.fetchall()]

                if 'growth_tags' in columns and 'negative_tags' not in columns:
                    print("🔄 Migrando growth_tags a negative_tags...")
                    cursor.execute("ALTER TABLE daily_entries ADD COLUMN negative_tags TEXT DEFAULT '[]'")
                    cursor.execute("UPDATE daily_entries SET negative_tags = growth_tags WHERE growth_tags IS NOT NULL AND growth_tags != ''")
                    print("✅ Migración de growth_tags completada")

                # Tabla de tags temporales (NUEVA)
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

                conn.commit()
                print("✨ Base de datos zen inicializada correctamente")

        except Exception as e:
            print(f"❌ Error inicializando base de datos zen: {e}")
            import traceback
            traceback.print_exc()
            raise

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

    def save_temp_tag(self, user_id: int, tag_name: str, tag_context: str, tag_type: str, tag_emoji: str) -> Optional[int]:
        """Guardar tag temporal - NUEVO MÉTODO"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO temp_tags (user_id, tag_name, tag_context, tag_type, tag_emoji, entry_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, tag_name, tag_context, tag_type, tag_emoji, today))

                tag_id = cursor.lastrowid
                print(f"💾 Tag temporal guardado: {tag_emoji} {tag_name} (ID: {tag_id})")
                return tag_id

        except Exception as e:
            print(f"❌ Error guardando tag temporal: {e}")
            return None

    def get_temp_tags_today(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtener tags temporales del día actual - NUEVO MÉTODO"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT tag_name, tag_context, tag_type, tag_emoji
                    FROM temp_tags
                    WHERE user_id = ? AND entry_date = ?
                    ORDER BY created_at
                """, (user_id, today))

                results = cursor.fetchall()

                tags = []
                for row in results:
                    tag = {
                        "name": row[0],
                        "context": row[1],
                        "type": row[2],
                        "emoji": row[3]
                    }
                    tags.append(tag)

                print(f"📋 Tags temporales encontrados: {len(tags)}")
                return tags

        except Exception as e:
            print(f"❌ Error obteniendo tags temporales: {e}")
            return []

    def clear_temp_tags_today(self, user_id: int) -> None:
        """Limpiar tags temporales del día - NUEVO MÉTODO"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    DELETE FROM temp_tags
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                deleted_count = cursor.rowcount
                print(f"🧹 Tags temporales eliminados: {deleted_count}")

        except Exception as e:
            print(f"❌ Error limpiando tags temporales: {e}")

    def save_daily_entry(self, user_id: int, free_reflection: str,
                         positive_tags: List = None, negative_tags: List = None,
                         worth_it: Optional[bool] = None) -> Optional[int]:
        """Guardar entrada diaria zen completa - CORREGIDO JSON"""
        try:
            from services.ai_service import get_mood_score, get_daily_summary

            print(f"💾 === INICIANDO GUARDADO PARA USUARIO {user_id} ===")

            # Convertir tags a formato JSON SEGURO
            def tag_to_dict(tag):
                """Convertir tag a diccionario de forma segura"""
                if hasattr(tag, '__dict__'):
                    # Es un objeto con atributos
                    return {
                        "name": getattr(tag, 'name', str(tag)),
                        "context": getattr(tag, 'context', ''),
                        "emoji": getattr(tag, 'emoji', '+' if getattr(tag, 'type', 'positive') == 'positive' else '-')
                    }
                elif isinstance(tag, dict):
                    # Ya es un diccionario
                    return {
                        "name": tag.get('name', ''),
                        "context": tag.get('context', ''),
                        "emoji": tag.get('emoji', '+')
                    }
                else:
                    # Es un string u otro tipo
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

            print(f"📝 Positive tags JSON: {positive_tags_json}")
            print(f"📝 Negative tags JSON: {negative_tags_json}")

            # Calcular métricas
            word_count = len(free_reflection.split())
            mood_score = get_mood_score(free_reflection, positive_tags or [], negative_tags or [], worth_it)

            # Generar resumen con IA
            ai_summary = get_daily_summary(free_reflection, positive_tags or [], negative_tags or [], worth_it)

            # Determinar sentimiento general
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
                          worth_it_int, sentiment, mood_score, ai_summary, word_count, entry_id))
                else:
                    # CREAR nueva entrada
                    print(f"✨ Creando nueva entrada")

                    cursor.execute("""
                        INSERT INTO daily_entries (
                            user_id, free_reflection, positive_tags, negative_tags,
                            worth_it, overall_sentiment, mood_score, ai_summary, word_count, entry_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, sentiment, mood_score, ai_summary, word_count, today))

                    entry_id = cursor.lastrowid

                # Limpiar tags temporales después de guardar
                self.clear_temp_tags_today(user_id)

                print(f"🌸 Entrada zen guardada (ID: {entry_id}, Mood: {mood_score}/10)")
                return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada zen: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_user_entries(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener entradas zen del usuario - CORREGIDO JSON"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, free_reflection, positive_tags, negative_tags, worth_it,
                           overall_sentiment, mood_score, ai_summary, word_count,
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
                        print(f"⚠️ Error parseando positive_tags: {row[2]}")
                        positive_tags = []

                    try:
                        negative_tags = json.loads(row[3] or "[]")
                    except (json.JSONDecodeError, TypeError):
                        print(f"⚠️ Error parseando negative_tags: {row[3]}")
                        negative_tags = []

                    entry = {
                        "id": row[0],
                        "free_reflection": row[1],
                        "positive_tags": positive_tags,
                        "negative_tags": negative_tags,
                        "worth_it": None if row[4] is None else bool(row[4]),
                        "overall_sentiment": row[5],
                        "mood_score": row[6],
                        "ai_summary": row[7],
                        "word_count": row[8],
                        "entry_date": row[9],
                        "created_at": row[10],
                        "updated_at": row[11]
                    }
                    entries.append(entry)

                    print(f"  📄 Entrada {row[9]}: {len(positive_tags)} positivos, {len(negative_tags)} negativos")

                return entries

        except Exception as e:
            print(f"❌ Error obteniendo entradas zen: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_today_entry_with_temp_tags(self, user_id: int) -> Dict[str, Any]:
        """Obtener entrada de hoy combinando datos guardados y tags temporales - NUEVO MÉTODO"""
        try:
            print(f"🔍 === OBTENIENDO ENTRADA DE HOY PARA USUARIO {user_id} ===")

            today = date.today().isoformat()

            # Buscar entrada guardada
            entries = self.get_user_entries(user_id, limit=1, offset=0)
            saved_entry = None

            if entries and entries[0].get('entry_date') == today:
                saved_entry = entries[0]
                print(f"📄 Entrada guardada encontrada: ID {saved_entry.get('id')}")
            else:
                print("📄 No hay entrada guardada para hoy")

            # Obtener tags temporales
            temp_tags = self.get_temp_tags_today(user_id)
            temp_positive = [tag for tag in temp_tags if tag['type'] == 'positive']
            temp_negative = [tag for tag in temp_tags if tag['type'] == 'negative']

            print(f"📋 Tags temporales: {len(temp_positive)} positivos, {len(temp_negative)} negativos")

            # Combinar datos
            result = {
                "reflection": saved_entry.get('free_reflection', '') if saved_entry else '',
                "positive_tags": (saved_entry.get('positive_tags', []) if saved_entry else []) + temp_positive,
                "negative_tags": (saved_entry.get('negative_tags', []) if saved_entry else []) + temp_negative,
                "worth_it": saved_entry.get('worth_it') if saved_entry else None,
                "mood_score": saved_entry.get('mood_score', 5) if saved_entry else 5,
                "has_saved_entry": saved_entry is not None,
                "has_temp_tags": len(temp_tags) > 0
            }

            print(f"📊 Resultado combinado:")
            print(f"   Reflexión: {'Sí' if result['reflection'] else 'No'}")
            print(f"   Tags positivos: {len(result['positive_tags'])}")
            print(f"   Tags negativos: {len(result['negative_tags'])}")
            print(f"   Worth it: {result['worth_it']}")
            print(f"   Entrada guardada: {result['has_saved_entry']}")
            print(f"   Tags temporales: {result['has_temp_tags']}")

            return result

        except Exception as e:
            print(f"❌ Error obteniendo entrada de hoy: {e}")
            import traceback
            traceback.print_exc()
            return {
                "reflection": "",
                "positive_tags": [],
                "negative_tags": [],
                "worth_it": None,
                "mood_score": 5,
                "has_saved_entry": False,
                "has_temp_tags": False
            }

    def get_year_summary(self, user_id: int, year: int) -> Dict[int, Dict[str, int]]:
        """Obtener resumen de todo el año por meses - CORREGIDO SIN JSON FUNCTIONS"""
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

                # Procesar resultados SIN usar funciones JSON de SQLite
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
        """Obtener resumen de días específicos de un mes - CORREGIDO SIN JSON FUNCTIONS"""
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
                           worth_it, mood_score, ai_summary
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (user_id, entry_date))

                result = cursor.fetchone()

                if not result:
                    return None

                reflection, positive_tags_json, negative_tags_json, worth_it, mood_score, ai_summary = result

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
                    "mood_score": mood_score or 5,
                    "ai_summary": ai_summary or ""
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


    # En tu database_service.py - NUEVA TABLA
def create_memory_table(self):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            contenido TEXT NOT NULL,  -- JSON
            contexto_original TEXT,
            importancia REAL,
            frecuencia INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
