import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        yield conn
    finally:
        conn.close()

def stream_users_in_batches(batch_size):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, name, email, age FROM user_data")
            while True:
                batch = cur.fetchmany(batch_size)
                if not batch:
                    break
                yield [dict(zip(['user_id', 'name', 'email', 'age'], row)) for row in batch]

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = [user for user in batch if user['age'] > 25]
        for user in filtered_batch:
            yield user
