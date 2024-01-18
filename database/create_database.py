# database.py
import sqlite3

def create_database():
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    # Create a table to store image information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()

