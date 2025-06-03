"""
📊 Database Service ACTUALIZADA - ReflectApp
✅ NUEVO: Métodos para sistema de sesiones y perfil de usuario
✅ NUEVO: Método get_user_by_email para auto-login
✅ NUEVO: Método update_user_profile para perfil
✅ NUEVO: Mejores estadísticas de usuario
"""

import sqlite3
import json
import hashlib
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen ACTUALIZADO con sistema de sesiones"""

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
        """Inicializar base de datos con esquema zen ACTUALIZADO"""
        print(f"🧘‍♀️ Inicializando base de datos zen: {self.db_path}")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # ✅ ACTUALIZADA: Tabla de usuarios con más campos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        name TEXT NOT NULL,
                        avatar_emoji TEXT DEFAULT '🦫',
                        preferences TEXT DEFAULT '{}',
                        bio TEXT DEFAULT '',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active INTEGER DEFAULT 1
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
                        mood_score INTEGER DEFAULT 5,
                        word_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        entry_date DATE DEFAULT CURRENT_DATE,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)

                # Tabla de momentos interactivos
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

                # ✅ NUEVA: Tabla de estadísticas de usuario
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        stat_date DATE DEFAULT CURRENT_DATE,
                        entries_count INTEGER DEFAULT 0,
                        positive_moments INTEGER DEFAULT 0,
                        negative_moments INTEGER DEFAULT 0,
                        total_words INTEGER DEFAULT 0,
                        avg_mood_score REAL DEFAULT 5.0,
                        streak_days INTEGER DEFAULT 0,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        UNIQUE(user_id, stat_date)
                    )
                """)

                # Índices para rendimiento zen
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_user_date ON daily_entries(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactive_moments_user_date ON interactive_moments(user_id, entry_date, is_active)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_statistics_user ON user_statistics(user_id, stat_date)")

                conn.commit()
                print("✨ Base de datos zen inicializada correctamente CON SESIONES")

        except Exception as e:
            print(f"❌ Error inicializando base de datos zen: {e}")
            import traceback
            traceback.print_exc()
            raise

    # ===============================
    # ✅ MÉTODOS DE USUARIOS ACTUALIZADOS
    # ===============================
    def create_user(self, email: str, password: str, name: str, avatar_emoji: str = "🦫") -> Optional[int]:
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

                # ✅ NUEVO: Inicializar estadísticas del usuario
                self._initialize_user_statistics(user_id)

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
                    SELECT id, name, avatar_emoji, preferences, created_at
                    FROM users 
                    WHERE email = ? AND password_hash = ? AND is_active = 1
                """, (email, password_hash))

                result = cursor.fetchone()

                if result:
                    user_id, name, avatar_emoji, preferences, created_at = result

                    # Actualizar último login zen
                    cursor.execute("""
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (user_id,))

                    user_data = {
                        "id": user_id,
                        "email": email,
                        "name": name,
                        "avatar_emoji": avatar_emoji or "🦫",
                        "preferences": json.loads(preferences or "{}"),
                        "created_at": created_at
                    }

                    print(f"🌺 Bienvenido de vuelta: {name}")
                    return user_data

                print(f"❌ Credenciales incorrectas para: {email}")
                return None

        except Exception as e:
            print(f"❌ Error en login zen: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """✅ NUEVO: Obtener usuario por email (para auto-login)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, email, name, avatar_emoji, preferences, created_at, last_login
                    FROM users 
                    WHERE email = ? AND is_active = 1
                """, (email,))

                result = cursor.fetchone()

                if result:
                    user_id, email, name, avatar_emoji, preferences, created_at, last_login = result

                    user_data = {
                        "id": user_id,
                        "email": email,
                        "name": name,
                        "avatar_emoji": avatar_emoji or "🦫",
                        "preferences": json.loads(preferences or "{}"),
                        "created_at": created_at,
                        "last_login": last_login
                    }

                    print(f"👤 Usuario encontrado: {name} ({email})")
                    return user_data

                print(f"❌ Usuario no encontrado: {email}")
                return None

        except Exception as e:
            print(f"❌ Error obteniendo usuario por email: {e}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """✅ NUEVO: Obtener usuario por ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, email, name, avatar_emoji, preferences, bio, created_at, last_login
                    FROM users 
                    WHERE id = ? AND is_active = 1
                """, (user_id,))

                result = cursor.fetchone()

                if result:
                    user_id, email, name, avatar_emoji, preferences, bio, created_at, last_login = result

                    user_data = {
                        "id": user_id,
                        "email": email,
                        "name": name,
                        "avatar_emoji": avatar_emoji or "🦫",
                        "bio": bio or "",
                        "preferences": json.loads(preferences or "{}"),
                        "created_at": created_at,
                        "last_login": last_login
                    }

                    return user_data

                return None

        except Exception as e:
            print(f"❌ Error obteniendo usuario por ID: {e}")
            return None

    def update_user_profile(self, user_id: int, name: str = None, avatar_emoji: str = None,
                            bio: str = None, preferences: Dict = None) -> bool:
        """✅ NUEVO: Actualizar perfil de usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Construir query dinámicamente según los campos proporcionados
                update_fields = []
                values = []

                if name is not None:
                    update_fields.append("name = ?")
                    values.append(name)

                if avatar_emoji is not None:
                    update_fields.append("avatar_emoji = ?")
                    values.append(avatar_emoji)

                if bio is not None:
                    update_fields.append("bio = ?")
                    values.append(bio)

                if preferences is not None:
                    update_fields.append("preferences = ?")
                    values.append(json.dumps(preferences, ensure_ascii=False))

                if not update_fields:
                    print("⚠️ No hay campos para actualizar")
                    return False

                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                values.append(user_id)

                query = f"""
                    UPDATE users 
                    SET {', '.join(update_fields)}
                    WHERE id = ?
                """

                cursor.execute(query, values)

                if cursor.rowcount > 0:
                    print(f"✅ Perfil actualizado para usuario {user_id}")
                    return True
                else:
                    print(f"❌ Usuario {user_id} no encontrado")
                    return False

        except Exception as e:
            print(f"❌ Error actualizando perfil: {e}")
            return False

    def _initialize_user_statistics(self, user_id: int) -> bool:
        """✅ NUEVO: Inicializar estadísticas para nuevo usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT OR IGNORE INTO user_statistics (user_id, stat_date)
                    VALUES (?, CURRENT_DATE)
                """, (user_id,))

                print(f"📊 Estadísticas inicializadas para usuario {user_id}")
                return True

        except Exception as e:
            print(f"❌ Error inicializando estadísticas: {e}")
            return False

    # ===============================
    # ✅ MÉTODOS DE ESTADÍSTICAS MEJORADOS
    # ===============================
    def get_user_comprehensive_statistics(self, user_id: int) -> Dict[str, Any]:
        """✅ NUEVO: Obtener estadísticas completas del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Estadísticas básicas
                cursor.execute("""
                    SELECT COUNT(*) as total_entries,
                           AVG(mood_score) as avg_mood,
                           SUM(word_count) as total_words
                    FROM daily_entries 
                    WHERE user_id = ?
                """, (user_id,))

                basic_stats = cursor.fetchone()
                total_entries, avg_mood, total_words = basic_stats if basic_stats else (0, 5.0, 0)

                # Conteo de tags positivos y negativos
                cursor.execute("""
                    SELECT positive_tags, negative_tags
                    FROM daily_entries 
                    WHERE user_id = ?
                """, (user_id,))

                entries = cursor.fetchall()
                positive_count = 0
                negative_count = 0

                for entry in entries:
                    positive_tags_json, negative_tags_json = entry
                    try:
                        positive_tags = json.loads(positive_tags_json or "[]")
                        negative_tags = json.loads(negative_tags_json or "[]")
                        positive_count += len(positive_tags)
                        negative_count += len(negative_tags)
                    except:
                        continue

                # Calcular racha de días consecutivos
                streak_days = self.calculate_current_streak(user_id)

                # Estadísticas de este mes
                current_month = date.today().replace(day=1)
                cursor.execute("""
                    SELECT COUNT(*) as entries_this_month
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date >= ?
                """, (user_id, current_month.isoformat()))

                entries_this_month = cursor.fetchone()[0] if cursor.fetchone() else 0

                # Día con mejor mood score
                cursor.execute("""
                    SELECT MAX(mood_score) as best_mood, entry_date
                    FROM daily_entries 
                    WHERE user_id = ?
                    ORDER BY mood_score DESC
                    LIMIT 1
                """, (user_id,))

                best_mood_result = cursor.fetchone()
                best_mood, best_mood_date = best_mood_result if best_mood_result else (5, None)

                return {
                    'total_entries': int(total_entries or 0),
                    'positive_count': positive_count,
                    'negative_count': negative_count,
                    'avg_mood_score': round(float(avg_mood or 5.0), 1),
                    'total_words': int(total_words or 0),
                    'streak_days': streak_days,
                    'entries_this_month': int(entries_this_month or 0),
                    'best_mood_score': int(best_mood or 5),
                    'best_mood_date': best_mood_date,
                    'total_moments': positive_count + negative_count
                }

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas completas: {e}")
            return {
                'total_entries': 0,
                'positive_count': 0,
                'negative_count': 0,
                'avg_mood_score': 5.0,
                'total_words': 0,
                'streak_days': 0,
                'entries_this_month': 0,
                'best_mood_score': 5,
                'best_mood_date': None,
                'total_moments': 0
            }

    def calculate_current_streak(self, user_id: int) -> int:
        """✅ MEJORADO: Calcular racha actual de días consecutivos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Obtener todas las fechas con entradas, ordenadas descendentemente
                cursor.execute("""
                    SELECT DISTINCT entry_date
                    FROM daily_entries 
                    WHERE user_id = ?
                    ORDER BY entry_date DESC
                """, (user_id,))

                dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in cursor.fetchall()]

                if not dates:
                    return 0

                streak = 0
                current_date = date.today()

                # Si no hay entrada para hoy, empezar desde ayer
                if dates[0] != current_date:
                    current_date = current_date - timedelta(days=1)

                # Contar días consecutivos hacia atrás
                for entry_date in dates:
                    if entry_date == current_date:
                        streak += 1
                        current_date -= timedelta(days=1)
                    else:
                        break

                return streak

        except Exception as e:
            print(f"❌ Error calculando racha: {e}")
            return 0

    # ===============================
    # MÉTODOS DE MOMENTOS INTERACTIVOS - MANTENIDOS
    # ===============================
    def save_interactive_moment(self, user_id: int, moment_data: dict) -> Optional[int]:
        """Guardar momento interactivo individual"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
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
        """Obtener momentos activos del día actual"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
                    cursor.execute("""
                        SELECT moment_id, emoji, text, moment_type, intensity, 
                               category, time_str, created_at
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ? AND is_active = 1
                        ORDER BY time_str, created_at
                    """, (user_id, today))
                else:
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

    def clear_interactive_moments_today(self, user_id: int) -> bool:
        """✅ NUEVO: Limpiar momentos del día actual"""
        try:
            today = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    DELETE FROM interactive_moments 
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                deleted_count = cursor.rowcount
                print(f"🗑️ Eliminados {deleted_count} momentos de hoy")
                return True

        except Exception as e:
            print(f"❌ Error eliminando momentos: {e}")
            return False

    def create_daily_entry_from_moments(self, user_id: int, free_reflection: str = "",
                                        worth_it: Optional[bool] = None) -> Optional[int]:
        """Crear entrada diaria desde momentos interactivos"""
        try:
            print(f"🔄 Creando entrada desde momentos para usuario {user_id}")

            moments = self.get_interactive_moments_today(user_id)

            if not moments:
                print("⚠️ No hay momentos para convertir")
                return None

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

            total_positive = len(positive_tags)
            total_negative = len(negative_tags)

            if total_positive > total_negative:
                auto_mood = 7
            elif total_negative > total_positive:
                auto_mood = 4
            else:
                auto_mood = 5

            entry_id = self.save_daily_entry(
                user_id=user_id,
                free_reflection=free_reflection or f"Reflexión del día - {total_positive + total_negative} momentos registrados",
                positive_tags=positive_tags,
                negative_tags=negative_tags,
                worth_it=worth_it,
                mood_score=auto_mood
            )

            if entry_id:
                # Eliminar momentos después de crear la entrada
                self.clear_interactive_moments_today(user_id)
                print(f"✅ Entrada creada desde momentos con ID: {entry_id}")

            return entry_id

        except Exception as e:
            print(f"❌ Error creando entrada desde momentos: {e}")
            return None

    # ===============================
    # MÉTODOS DE ENTRADAS DIARIAS - MANTENIDOS
    # ===============================
    def save_daily_entry(self, user_id: int, free_reflection: str,
                         positive_tags: List = None, negative_tags: List = None,
                         worth_it: Optional[bool] = None, mood_score: int = 5) -> Optional[int]:
        """Guardar entrada diaria"""
        try:
            print(f"💾 === GUARDANDO ENTRADA DIARIA PARA USUARIO {user_id} ===")

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

            positive_tags_json = json.dumps(positive_tags_list, ensure_ascii=False)
            negative_tags_json = json.dumps(negative_tags_list, ensure_ascii=False)

            word_count = len(free_reflection.split())

            if mood_score == 5:
                total_positive = len(positive_tags_list)
                total_negative = len(negative_tags_list)

                if total_positive > total_negative:
                    mood_score = 7 + min(2, total_positive - total_negative)
                elif total_negative > total_positive:
                    mood_score = 4 - min(2, total_negative - total_positive)

            mood_score = max(1, min(10, mood_score))

            worth_it_int = None
            if worth_it is True:
                worth_it_int = 1
            elif worth_it is False:
                worth_it_int = 0

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                today = date.today().isoformat()
                cursor.execute("""
                    SELECT id FROM daily_entries 
                    WHERE user_id = ? AND entry_date = ?
                """, (user_id, today))

                existing_entry = cursor.fetchone()

                if existing_entry:
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

    # ===============================
    # MÉTODOS DE CONSULTA - MANTENIDOS Y MEJORADOS
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

                year_data = {}
                for month in range(1, 13):
                    year_data[month] = {"positive": 0, "negative": 0, "total": 0}

                for row in results:
                    entry_date_str, positive_tags_json, negative_tags_json = row

                    entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                    month = entry_date.month

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