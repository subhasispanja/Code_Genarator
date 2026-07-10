import sqlite3
from datetime import datetime

DB_NAME = "code_generations.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            problem TEXT,
            language TEXT,
            code_format TEXT,
            output_format TEXT,
            final_prompt TEXT,
            generated_code TEXT
        )
    """)

    conn.commit()
    conn.close()


def store_generation(
    problem,
    language,
    code_format,
    output_format,
    final_prompt,
    generated_code
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO generations (
            timestamp,
            problem,
            language,
            code_format,
            output_format,
            final_prompt,
            generated_code
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        problem,
        language,
        code_format,
        output_format,
        final_prompt,
        generated_code
    ))

    conn.commit()
    conn.close()


def get_session_history(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            language,
            final_prompt,
            generated_code
        FROM generations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "language": r[0],
            "final_prompt": r[1],
            "generated_code": r[2]
        }
        for r in rows
    ]
