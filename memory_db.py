import sqlite3

DB_NAME = "assistant_memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        embedding BLOB
    )
    """)


    # User profile table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY,
        name TEXT,
        interests TEXT,
        project TEXT
    )
    """)

    conn.commit()
    conn.close()


import pickle
from sentence_transformers import SentenceTransformer

# Load embedding model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def save_chat(role, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Generate embedding
    embedding = embedder.encode(content)
    embedding_blob = pickle.dumps(embedding)

    cursor.execute(
        "INSERT INTO chat_history (role, content, embedding) VALUES (?, ?, ?)",
        (role, content, embedding_blob)
    )

    conn.commit()
    conn.close()



def get_last_chats(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]


def save_profile(name=None, interests=None, project=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user_profile")

    cursor.execute("""
    INSERT INTO user_profile (id, name, interests, project)
    VALUES (1, ?, ?, ?)
    """, (name, interests, project))

    conn.commit()
    conn.close()


def get_profile():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, interests, project FROM user_profile WHERE id=1"
    )
    row = cursor.fetchone()
    conn.close()
    return row
import numpy as np

def get_relevant_chats(query, top_k=3):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get all stored chats with embeddings
    cursor.execute("SELECT role, content, embedding FROM chat_history")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    # Encode current query
    query_embedding = embedder.encode(query)

    scored = []

    for role, content, embedding_blob in rows:
        stored_embedding = pickle.loads(embedding_blob)

        # Cosine similarity
        similarity = np.dot(query_embedding, stored_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
        )

        scored.append((similarity, role, content))

    # Sort by similarity (highest first)
    scored.sort(reverse=True, key=lambda x: x[0])

    # Return top_k
    return [(role, content) for _, role, content in scored[:top_k]]
