import mysql.connector
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "main")
    )
    cursor = connection.cursor(dictionary=True)  # Store the cursor with dictionary=True
    return connection, cursor
