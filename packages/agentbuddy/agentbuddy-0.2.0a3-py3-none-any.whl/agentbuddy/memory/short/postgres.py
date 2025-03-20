class ShortPostgres(ShortMemory):
    PG_HOST = "localhost"
    PG_DB = "agent_db"
    PG_USER = "user"
    PG_PASSWORD = "password"
    PG_TABLE = "messages"

    pg_conn = psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASSWORD)
    pg_cursor = pg_conn.cursor()

    # Creazione tabella se non esiste
    pg_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {PG_TABLE} (
            session_id TEXT PRIMARY KEY,
            messages TEXT[]
        )
    """)
    pg_conn.commit()

    def load_messages(self) -> List[str]:
        ShortPostgres.pg_cursor.execute(f"SELECT messages FROM {ShortPostgres.PG_TABLE} WHERE session_id = %s", (self.session_id,))
        result = ShortPostgres.pg_cursor.fetchone()
        return result[0] if result else []

    def save_messages(self, messages: List[str]):
        ShortPostgres.pg_cursor.execute(f"""
            INSERT INTO {ShortPostgres.PG_TABLE} (session_id, messages)
            VALUES (%s, %s)
            ON CONFLICT (session_id) DO UPDATE SET messages = EXCLUDED.messages
        """, (self.session_id, messages))
        ShortPostgres.pg_conn.commit()