import sqlite3
import uuid

# In-memory database (SQLite) setup
conn = sqlite3.connect('image_classification.db', check_same_thread=False)
cursor = conn.cursor()

# Create table for storing image, id, and result
cursor.execute('''CREATE TABLE IF NOT EXISTS classification_results (
    id TEXT PRIMARY KEY, 
    image BLOB,
    result TEXT
)''')
conn.commit()

def insert_image(image_data: bytes) -> str:
    """Insert image into the database and return the image ID."""
    # Generate unique ID for the image
    image_id = str(uuid.uuid4())
    
    # Insert the image and an empty result into the database
    cursor.execute("INSERT INTO classification_results (id, image, result) VALUES (?, ?, ?)", (image_id, image_data, None))
    conn.commit()
    
    return image_id

def update_result(image_id: str, result: str):
    """Update classification result in the database."""
    cursor.execute("UPDATE classification_results SET result = ? WHERE id = ?", (result, image_id))
    conn.commit()

def get_result(image_id: str):
    """Retrieve result and image data from the database."""
    cursor.execute("SELECT result, image FROM classification_results WHERE id = ?", (image_id,))
    return cursor.fetchone()

def close_connection():
    """Close the database connection."""
    conn.close()
