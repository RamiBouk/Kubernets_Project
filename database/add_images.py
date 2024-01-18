# add_images.py
import os
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

def add_image_to_database(category, filename, filepath):
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    # Insert image information into the database
    cursor.execute('''
        INSERT INTO images (category, filename, filepath)
        VALUES (?, ?, ?)
    ''', (category, filename, filepath))

    conn.commit()
    conn.close()

def add_images_from_directory(directory):
    added=0
    for category in os.listdir(directory):
        category_path = os.path.join(directory, category)
        
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    filepath = os.path.join(category_path, filename)
                    add_image_to_database(category, filename, filepath)
                    print(f'{added}')

if __name__ == '__main__':
    create_database()  # Ensure the database and table are created
    image_directory = 'Images'
    add_images_from_directory(image_directory)

