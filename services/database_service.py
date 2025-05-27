import sqlite3
import json
import hashlib
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen para ReflectApp - CORREGIDO"""

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

                # Si growth_tags existe pero negative_tags también, copiar datos si negative_tags está vacío
                elif 'growth_tags' in columns and 'negative_tags' in columns:
                    cursor.execute("""
                        UPDATE daily_entries 
                        SET negative_tags = growth_tags 
                        WHERE (negative_tags IS NULL OR negative_tags = '' OR negative_tags = '[]') 
                              AND growth_tags IS NOT NULL 
                              AND growth_tags != '' 
                              AND growth_tags != '[]'
                    """)
                    print("✅ Sincronización de growth_tags a negative_tags completada")

                # Tabla de interacciones con IA
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ai_interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        entry_id INTEGER,
                        interaction_type TEXT NOT NULL,
                        input_text TEXT,
                        ai_response TEXT,
                        context_data TEXT DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (entry_id) REFERENCES daily_entries (id) ON DELETE CASCADE
                    )
                """)

                # Tabla de estadísticas zen (CORREGIDA)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS zen_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        stat_date DATE NOT NULL,
                        entries_count INTEGER DEFAULT 0,
                        avg_mood_score REAL DEFAULT 0,
                        positive_tags_count INTEGER DEFAULT 0,
                        negative_tags_count INTEGER DEFAULT 0,
                        worth_it_days INTEGER DEFAULT 0,
                        reflection_words INTEGER DEFAULT 0,
                        streak_days INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        UNIQUE(user_id, stat_date)
                    )
                """)

                # Migrar growth_tags_count a negative_tags_count si es necesario
                cursor.execute("PRAGMA table_info(zen_stats)")
                stat_columns = [column[1] for column in cursor.fetchall()]

                if 'growth_tags_count' in stat_columns and 'negative_tags_count' not in stat_columns:
                    print("🔄 Migrando growth_tags_count a negative_tags_count...")
                    cursor.execute("ALTER TABLE zen_stats ADD COLUMN negative_tags_count INTEGER DEFAULT 0")
                    cursor.execute("UPDATE zen_stats SET negative_tags_count = growth_tags_count WHERE growth_tags_count IS NOT NULL")
                    print("✅ Migración de estadísticas completada")

                # Índices para rendimiento zen
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_user_date ON daily_entries(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_mood ON daily_entries(mood_score)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_zen_stats_user_date ON zen_stats(user_id, stat_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_interactions_user ON ai_interactions(user_id, created_at)")

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

    def save_daily_entry(self, user_id: int, free_reflection: str,
                         positive_tags: List = None, negative_tags: List = None,
                         worth_it: Optional[bool] = None) -> Optional[int]:
        """Guardar entrada diaria zen completa - CORREGIDO"""
        try:
            from services.ai_service import get_mood_score, get_daily_summary

            print(f"💾 Iniciando guardado para usuario {user_id}")

            # Convertir tags a formato JSON MEJORADO
            positive_tags_json = json.dumps([
                {
                    "name": getattr(tag, 'name', str(tag)),
                    "context": getattr(tag, 'context', ''),
                    "emoji": getattr(tag, 'emoji', '+')
                }
                for tag in (positive_tags or [])
            ])

            negative_tags_json = json.dumps([
                {
                    "name": getattr(tag, 'name', str(tag)),
                    "context": getattr(tag, 'context', ''),
                    "emoji": getattr(tag, 'emoji', '-')
                }
                for tag in (negative_tags or [])
            ])

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

                # CORREGIDO: Verificar si ya existe entrada para hoy
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
                            worth_it, overall_sentiment, mood_score, ai_summary, word_count
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, free_reflection, positive_tags_json, negative_tags_json,
                          worth_it_int, sentiment, mood_score, ai_summary, word_count))

                    entry_id = cursor.lastrowid

                # Actualizar estadísticas zen
                self._update_zen_stats(user_id, conn)

                print(f"🌸 Entrada zen guardada (ID: {entry_id}, Mood: {mood_score}/10)")
                return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada zen: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_user_entries(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener entradas zen del usuario - CORREGIDO"""
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

    def get_calendar_data(self, user_id: int, year: int, month: int) -> Dict[str, Any]:
        """Obtener datos para calendario zen"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Obtener entradas del mes
                cursor.execute("""
                    SELECT entry_date, worth_it, mood_score
                    FROM daily_entries 
                    WHERE user_id = ? 
                          AND strftime('%Y', entry_date) = ?
                          AND strftime('%m', entry_date) = ?
                    ORDER BY entry_date
                """, (user_id, str(year), f"{month:02d}"))

                results = cursor.fetchall()

                calendar_data = {}
                for row in results:
                    entry_date, worth_it, mood_score = row
                    calendar_data[entry_date] = {
                        "worth_it": None if worth_it is None else bool(worth_it),
                        "mood_score": mood_score,
                        "color": "green" if worth_it == 1 else "red" if worth_it == 0 else "gray"
                    }

                return calendar_data

        except Exception as e:
            print(f"❌ Error obteniendo datos de calendario: {e}")
            return {}

    def get_zen_stats(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Obtener estadísticas zen del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Estadísticas generales
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_entries,
                        AVG(mood_score) as avg_mood,
                        SUM(word_count) as total_words,
                        SUM(CASE WHEN worth_it = 1 THEN 1 ELSE 0 END) as worth_it_days,
                        COUNT(CASE WHEN worth_it = 1 THEN 1 END) * 100.0 / COUNT(*) as worth_it_percentage
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date >= date('now', '-' || ? || ' days')
                """, (user_id, days))

                general_stats = cursor.fetchone()

                # Racha actual
                current_streak = self._calculate_current_streak(user_id, conn)

                # Tags más comunes
                cursor.execute("""
                    SELECT positive_tags, negative_tags
                    FROM daily_entries 
                    WHERE user_id = ? AND entry_date >= date('now', '-' || ? || ' days')
                """, (user_id, days))

                tag_results = cursor.fetchall()
                tag_frequency = self._analyze_tag_frequency(tag_results)

                return {
                    "total_entries": general_stats[0] or 0,
                    "avg_mood": round(general_stats[1] or 0, 1),
                    "total_words": general_stats[2] or 0,
                    "worth_it_days": general_stats[3] or 0,
                    "worth_it_percentage": round(general_stats[4] or 0, 1),
                    "current_streak": current_streak,
                    "tag_frequency": tag_frequency
                }

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas zen: {e}")
            return {}

    def save_ai_interaction(self, user_id: int, interaction_type: str,
                            input_text: str, ai_response: str,
                            entry_id: Optional[int] = None, context_data: Dict = None) -> Optional[int]:
        """Guardar interacción con IA"""
        try:
            context_json = json.dumps(context_data or {})

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO ai_interactions (
                        user_id, entry_id, interaction_type, input_text, ai_response, context_data
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, entry_id, interaction_type, input_text, ai_response, context_json))

                interaction_id = cursor.lastrowid
                print(f"🤖 Interacción IA guardada (ID: {interaction_id})")
                return interaction_id

        except Exception as e:
            print(f"❌ Error guardando interacción IA: {e}")
            return None

    def _update_zen_stats(self, user_id: int, conn: sqlite3.Connection) -> None:
        """Actualizar estadísticas zen del día"""
        try:
            cursor = conn.cursor()
            today = date.today().isoformat()

            # Calcular estadísticas del día
            cursor.execute("""
                SELECT 
                    COUNT(*) as entries_count,
                    AVG(mood_score) as avg_mood,
                    SUM(json_array_length(positive_tags)) as positive_count,
                    SUM(json_array_length(negative_tags)) as negative_count,
                    SUM(CASE WHEN worth_it = 1 THEN 1 ELSE 0 END) as worth_it_count,
                    SUM(word_count) as total_words
                FROM daily_entries 
                WHERE user_id = ? AND entry_date = ?
            """, (user_id, today))

            stats = cursor.fetchone()

            # Calcular racha
            streak = self._calculate_current_streak(user_id, conn)

            # Insertar o actualizar estadísticas
            cursor.execute("""
                INSERT OR REPLACE INTO zen_stats (
                    user_id, stat_date, entries_count, avg_mood_score,
                    positive_tags_count, negative_tags_count, worth_it_days,
                    reflection_words, streak_days
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, today, stats[0], stats[1] or 0, stats[2] or 0,
                  stats[3] or 0, stats[4] or 0, stats[5] or 0, streak))

        except Exception as e:
            print(f"❌ Error actualizando estadísticas zen: {e}")

    def _calculate_current_streak(self, user_id: int, conn: sqlite3.Connection) -> int:
        """Calcular racha actual de días consecutivos"""
        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT entry_date
                FROM daily_entries 
                WHERE user_id = ?
                ORDER BY entry_date DESC
                LIMIT 30
            """, (user_id,))

            dates = [row[0] for row in cursor.fetchall()]

            if not dates:
                return 0

            # Calcular racha desde hoy hacia atrás
            today = date.today()
            streak = 0

            for i, entry_date_str in enumerate(dates):
                entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                expected_date = today - timedelta(days=i)

                if entry_date == expected_date:
                    streak += 1
                else:
                    break

            return streak

        except Exception as e:
            print(f"❌ Error calculando racha: {e}")
            return 0

    def _analyze_tag_frequency(self, tag_results: List) -> Dict[str, int]:
        """Analizar frecuencia de tags"""
        frequency = {}

        for row in tag_results:
            positive_tags_json, negative_tags_json = row

            # Procesar tags positivos
            try:
                positive_tags = json.loads(positive_tags_json or "[]")
                for tag in positive_tags:
                    name = tag.get("name", "") if isinstance(tag, dict) else str(tag)
                    frequency[f"✨ {name}"] = frequency.get(f"✨ {name}", 0) + 1
            except (json.JSONDecodeError, TypeError):
                pass

            # Procesar tags negativos
            try:
                negative_tags = json.loads(negative_tags_json or "[]")
                for tag in negative_tags:
                    name = tag.get("name", "") if isinstance(tag, dict) else str(tag)
                    frequency[f"💔 {name}"] = frequency.get(f"💔 {name}", 0) + 1
            except (json.JSONDecodeError, TypeError):
                pass

        # Retornar los 10 más frecuentes
        sorted_tags = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_tags[:10])

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

    # ====== MÉTODOS PARA CALENDARIO ======

    def get_year_summary(self, user_id: int, year: int) -> Dict[int, Dict[str, int]]:
        """Obtener resumen de todo el año por meses"""
        try:
            # Construir rango de fechas del año
            first_day = date(year, 1, 1)
            last_day = date(year, 12, 31)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Obtener todas las entradas del año
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

                    # Extraer mes de la fecha
                    entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                    month = entry_date.month

                    # Contar tags de manera segura
                    try:
                        positive_tags = json.loads(positive_tags_json or "[]")
                        positive_count = len(positive_tags)
                    except (json.JSONDecodeError, TypeError):
                        positive_count = 0

                    try:
                        negative_tags = json.loads(negative_tags_json or "[]")
                        negative_count = len(negative_tags)
                    except (json.JSONDecodeError, TypeError):
                        negative_count = 0

                    # Acumular en el mes correspondiente
                    year_data[month]["positive"] += positive_count
                    year_data[month]["negative"] += negative_count
                    year_data[month]["total"] += positive_count + negative_count

                return year_data

        except Exception as e:
            print(f"❌ Error obteniendo resumen del año {year}: {e}")
            # Retornar estructura vacía en caso de error
            year_data = {}
            for month in range(1, 13):
                year_data[month] = {"positive": 0, "negative": 0, "total": 0}
            return year_data

    def get_month_summary(self, user_id: int, year: int, month: int) -> Dict[int, Dict[str, Any]]:
        """Obtener resumen de días específicos de un mes"""
        try:
            # Construir rango de fechas del mes
            first_day = date(year, month, 1)
            if month == 12:
                last_day = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = date(year, month + 1, 1) - timedelta(days=1)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Obtener todas las entradas del mes
                cursor.execute("""
                    SELECT entry_date, positive_tags, negative_tags, worth_it
                    FROM daily_entries 
                    WHERE user_id = ? 
                          AND entry_date >= ? 
                          AND entry_date <= ?
                    ORDER BY entry_date
                """, (user_id, first_day.isoformat(), last_day.isoformat()))

                results = cursor.fetchall()

                # Procesar resultados
                month_data = {}

                for row in results:
                    entry_date_str, positive_tags_json, negative_tags_json, worth_it = row

                    # Extraer día de la fecha
                    entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                    day = entry_date.day

                    # Contar tags de manera segura
                    try:
                        positive_tags = json.loads(positive_tags_json or "[]")
                        positive_count = len(positive_tags)
                    except (json.JSONDecodeError, TypeError):
                        positive_count = 0

                    try:
                        negative_tags = json.loads(negative_tags_json or "[]")
                        negative_count = len(negative_tags)
                    except (json.JSONDecodeError, TypeError):
                        negative_count = 0

                    # Convertir worth_it
                    worth_it_bool = None
                    if worth_it == 1:
                        worth_it_bool = True
                    elif worth_it == 0:
                        worth_it_bool = False

                    month_data[day] = {
                        "positive": positive_count,
                        "negative": negative_count,
                        "submitted": True,  # Si está en BD, fue submiteado
                        "worth_it": worth_it_bool
                    }

                return month_data

        except Exception as e:
            print(f"❌ Error obteniendo resumen del mes {year}-{month}: {e}")
            return {}

    def get_day_entry(self, user_id: int, year: int, month: int, day: int) -> Optional[Dict[str, Any]]:
        """Obtener entrada completa de un día específico"""
        try:
            # Construir fecha en formato ISO
            entry_date = date(year, month, day).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Obtener la entrada del día específico
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

                # Desempaquetar resultado
                reflection, positive_tags_json, negative_tags_json, worth_it, mood_score, ai_summary = result

                # Convertir JSON a listas de manera segura
                try:
                    positive_tags = json.loads(positive_tags_json or "[]")
                except (json.JSONDecodeError, TypeError):
                    positive_tags = []

                try:
                    negative_tags = json.loads(negative_tags_json or "[]")
                except (json.JSONDecodeError, TypeError):
                    negative_tags = []

                # Convertir worth_it (puede ser 0, 1, o None)
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
            today = date.today().isoformat()  # Formato: "2024-03-15"

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Buscar si existe una entrada para hoy
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