import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Crea la tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Base de datos inicializada correctamente.")
