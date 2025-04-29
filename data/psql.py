import psycopg2
from psycopg2 import OperationalError
from data.queries import *

class Postgres:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=HOST,
                port=PORT,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )
            self.cursor = self.connection.cursor()
        except OperationalError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            self.connection = None
            self.cursor = None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Insert failed: {e}")

    def select_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Select failed: {e}")
            return []

    def update_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Update failed: {e}")

    def delete_query(self, query, values=None):
        try:
            print(query,values)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Delete failed: {e}")
