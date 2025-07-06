import psycopg2
from contextlib import contextmanager
from typing import Generator, List, Dict, Any, Optional

@contextmanager
def get_db_connection():
    """Context manager for database connection"""
    conn = psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        yield conn
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """Generator that yields batches of user data"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, name, email, age FROM user_data")
            while True:
                batch = cur.fetchmany(batch_size)
                if not batch:
                    return  # Explicit return to end generator
                yield [dict(zip(['user_id', 'name', 'email', 'age'], row)) for row in batch]

def batch_processing(batch_size: int, min_age: int = 25) -> Generator[Dict[str, Any], None, Optional[int]]:
    """
    Processes users in batches and yields those above min_age
    Returns count of processed users when done
    """
    processed_count = 0
    try:
        for batch in stream_users_in_batches(batch_size):
            filtered_batch = [user for user in batch if user['age'] > min_age]
            for user in filtered_batch:
                processed_count += 1
                yield user
        return processed_count  # Return total count when done
    except Exception as e:
        print(f"Processing error: {e}")
        return None  # Return None on error
