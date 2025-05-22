import sqlite3
import json
import hashlib
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any

class DatabaseService:
    """Servicio de base de datos zen para ReflectApp"""

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
        """Inicializar base de datos con esquema zen"""
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
                        growth_tags TEXT DEFAULT '[]',
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

                # Tabla de estadísticas zen
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS zen_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        stat_date DATE NOT NULL,
                        entries_count INTEGER DEFAULT 0,
                        avg_mood_score REAL DEFAULT 0,
                        positive_tags_count INTEGER DEFAULT 0,
                        growth_tags_count INTEGER DEFAULT 0,
                        worth_it_days INTEGER DEFAULT 0,
                        reflection_words INTEGER DEFAULT 0,
                        streak_days INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        UNIQUE(user_id, stat_date)
                    )
                """)

                # Índices para rendimiento zen
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_user_date ON daily_entries(user_id, entry_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_entries_mood ON daily_entries(mood_score)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_zen_stats_user_date ON zen_stats(user_id, stat_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_interactions_user ON ai_interactions(user_id, created_at)")

                conn.commit()
                print("✨ Base de datos zen inicializada correctamente")

        except Exception as e:
            print(f"❌ Error inicializando base de datos zen: {e}")
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
                         positive_tags: List = None, growth_tags: List = None,
                         worth_it: Optional[bool] = None) -> Optional[int]:
        """Guardar entrada diaria zen completa"""
        try:
            from services.ai_service import get_mood_score, get_daily_summary

            # Convertir tags a formato JSON
            positive_tags_json = json.dumps([
                {"name": tag.name, "context": tag.context, "emoji": tag.emoji}
                for tag in (positive_tags or [])
            ])

            growth_tags_json = json.dumps([
                {"name": tag.name, "context": tag.context, "emoji": tag.emoji}
                for tag in (growth_tags or [])
            ])

            # Calcular métricas
            word_count = len(free_reflection.split())
            mood_score = get_mood_score(free_reflection, positive_tags or [], growth_tags or [], worth_it)

            # Generar resumen con IA
            ai_summary = get_daily_summary(free_reflection, positive_tags or [], growth_tags or [], worth_it)

            # Determinar sentimiento general
            if mood_score >= 7:
                sentiment = "positive"
            elif mood_score <= 4:
                sentiment = "growth"
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

                cursor.execute("""
                    INSERT INTO daily_entries (
                        user_id, free_reflection, positive_tags, growth_tags,
                        worth_it, overall_sentiment, mood_score, ai_summary, word_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, free_reflection, positive_tags_json, growth_tags_json,
                      worth_it_int, sentiment, mood_score, ai_summary, word_count))

                entry_id = cursor.lastrowid

                # Actualizar estadísticas zen
                self._update_zen_stats(user_id, conn)

                print(f"🌸 Entrada zen guardada (ID: {entry_id}, Mood: {mood_score}/10)")
                return entry_id

        except Exception as e:
            print(f"❌ Error guardando entrada zen: {e}")
            return None

    def get_user_entries(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener entradas zen del usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, free_reflection, positive_tags, growth_tags, worth_it,
                           overall_sentiment, mood_score, ai_summary, word_count,
                           entry_date, created_at, updated_at
                    FROM daily_entries 
                    WHERE user_id = ?
                    ORDER BY entry_date DESC, created_at DESC
                    LIMIT ? OFFSET ?
                """, (user_id, limit, offset))

                results = cursor.fetchall()

                entries = []
                for row in results:
                    entry = {
                        "id": row[0],
                        "free_reflection": row[1],
                        "positive_tags": json.loads(row[2] or "[]"),
                        "growth_tags": json.loads(row[3] or "[]"),
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

                return entries

        except Exception as e:
            print(f"❌ Error obteniendo entradas zen: {e}")
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
                    SELECT positive_tags, growth_tags
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
                    SUM(json_array_length(growth_tags)) as growth_count,
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
                    positive_tags_count, growth_tags_count, worth_it_days,
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
                expected_date = today - datetime.timedelta(days=i)

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
            positive_tags_json, growth_tags_json = row

            # Procesar tags positivos
            positive_tags = json.loads(positive_tags_json or "[]")
            for tag in positive_tags:
                name = tag.get("name", "")
                frequency[f"✨ {name}"] = frequency.get(f"✨ {name}", 0) + 1

            # Procesar tags de crecimiento
            growth_tags = json.loads(growth_tags_json or "[]")
            for tag in growth_tags:
                name = tag.get("name", "")
                frequency[f"🌱 {name}"] = frequency.get(f"🌱 {name}", 0) + 1

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