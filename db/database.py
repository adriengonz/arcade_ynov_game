import sqlite3

def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS joueurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT,
        vitesse_rotation REAL,
        vitesse_deplacement REAL,
        points_vie INTEGER,
        puissance_tir REAL,
        delai_tir REAL,
        vitesse_projectile REAL
    );

    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT,
        score INTEGER
    );
    """)
    conn.commit()
    return conn, cursor