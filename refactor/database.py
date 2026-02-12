import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import sys


class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)

            if self.conn.is_connected():
                print(":white_check_mark: Connected to MySQL")

            self.cursor = self.conn.cursor(dictionary=True)

        except Error as e:
            print(f":x: Database connection failed: {e}")
            sys.exit(1)

    def commit(self):
        try:
            self.conn.commit()
        except Error as e:
            print(f":x: Commit error: {e}")

    def rollback(self):
        try:
            self.conn.rollback()
        except Error as e:
            print(f":x: Rollback error: {e}")

    def close(self):
        try:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print(":lock: Database connection closed.")
        except Error as e:
            print(f":x: Closing error: {e}")