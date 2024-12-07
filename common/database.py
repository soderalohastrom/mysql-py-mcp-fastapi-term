import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT')
        }

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.cursor
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

class CRUDOperations:
    @staticmethod
    def create(table: str, data: dict):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, tuple(data.values()))
            cursor.connection.commit()
            return cursor.lastrowid

    @staticmethod
    def read(table: str, conditions: dict = None):
        query = f"SELECT * FROM {table}"
        params = []
        
        if conditions:
            where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = list(conditions.values())

        with DatabaseConnection() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def update(table: str, data: dict, conditions: dict):
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = list(data.values()) + list(conditions.values())
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, params)
            cursor.connection.commit()
            return cursor.rowcount

    @staticmethod
    def delete(table: str, conditions: dict):
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        with DatabaseConnection() as cursor:
            cursor.execute(query, tuple(conditions.values()))
            cursor.connection.commit()
            return cursor.rowcount
