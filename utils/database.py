import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='online_banking',
                user='root',
                password=''
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f'Error: {e}')
            return None
        
    def query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()