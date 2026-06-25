import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jarvis.db")


def init_database():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS sys_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS web_command("
        "id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS contacts("
        "id INTEGER PRIMARY KEY, name VARCHAR(200), "
        "mobile_no VARCHAR(255), email VARCHAR(255))"
    )

    defaults = [
        ("youtube", "https://www.youtube.com/"),
        ("whatsapp", "https://web.whatsapp.com/"),
        ("google", "https://www.google.com/"),
    ]
    for name, url in defaults:
        cursor.execute("SELECT 1 FROM web_command WHERE name = ?", (name,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO web_command (name, url) VALUES (?, ?)", (name, url)
            )

    con.commit()
    con.close()
