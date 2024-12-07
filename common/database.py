import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

class ClientQueries:
    @staticmethod
    def get_by_id(cursor, client_id: int, fields: list = None) -> dict:
        fields_str = ", ".join(fields) if fields else "*"
        query = f"""
        SELECT {fields_str}
        FROM Persons p
        LEFT JOIN PersonsProfile pp ON p.Person_id = pp.Person_id
        WHERE p.Person_id = %s
        """
        cursor.execute(query, (client_id,))
        return cursor.fetchone()

    @staticmethod
    def search_by_criteria(cursor, criteria: dict) -> list:
        conditions = []
        params = []
        
        # Build WHERE clause dynamically
        for key, value in criteria.items():
            if key == 'city':
                conditions.append("a.City = %s")
                params.append(value)
            elif key == 'gender':
                conditions.append("p.Gender = %s")
                params.append(value)
            # Add more criteria mappings as needed
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"""
        SELECT DISTINCT
            p.Person_id,
            p.FirstName,
            p.LastName,
            p.Gender,
            a.City,
            a.State
        FROM Persons p
        LEFT JOIN Addresses a ON p.Person_id = a.Person_id
        WHERE {where_clause}
        """
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        # Validate config
        missing = [k for k, v in self.config.items() if not v and k != 'port']
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

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

    def get_client(self, client_id: int, fields: list = None) -> dict:
        with self as cursor:
            return ClientQueries.get_by_id(cursor, client_id, fields)

    def search_clients(self, criteria: dict) -> list:
        with self as cursor:
            return ClientQueries.search_by_criteria(cursor, criteria)

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
