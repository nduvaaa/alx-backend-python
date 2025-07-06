# Database Streaming with Python Generators

## 📌 Overview
A Python implementation demonstrating memory-efficient streaming of database records using generators. This solution sets up a MySQL database and streams rows one-by-one to minimize memory usage.

## 🛠️ Technical Implementation

### Database Setup
```python
# seed.py - Core functionality
import csv
import uuid
import mysql.connector
from mysql.connector import Error
from typing import Generator, Tuple, Any

def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Establish connection to MySQL server"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
    except Error as e:
        print(f"Connection error: {e}")
        return None

def stream_users() -> Generator[Tuple[Any, ...], None, None]:
    """Generator that yields database rows one at a time"""
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        while (row := cursor.fetchone()) is not None:
            yield row
            
    except Error as e:
        print(f"Streaming error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
