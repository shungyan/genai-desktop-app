import psycopg2

# === Database connection settings ===
DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",
    "user": "postgres",     # or your user, e.g., "myuser"
    "password": "postgres"  # change if you set a different password
}

def fetch_conversation_history():
    """Fetch all chat messages from the PostgreSQL conversations table."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Retrieve messages ordered by insertion time
        cursor.execute("""
            SELECT sender, message, created_at
            FROM conversations
            ORDER BY created_at ASC;
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    except Exception as e:
        print("Error connecting to database:", e)
        return []

def format_history(messages):
    """Format chat messages into readable text for summarization."""
    formatted = []
    for sender, message, created_at in messages:
        formatted.append(f"[{created_at}] {sender.upper()}: {message}")
    return "\n".join(formatted)

def save_to_file(text, filename="chat_history.txt"):
    """Save formatted chat history to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Chat history exported to {filename}")

if __name__ == "__main__":
    messages = fetch_conversation_history()
    if messages:
        formatted = format_history(messages)
        save_to_file(formatted)
    else:
        print("No messages found in database.")
