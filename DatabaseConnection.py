from MySQLdb import Connect, connect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector


# class to handle data base query and connect to the mysql 
class DatabaseConnection():
    
    def __init__(self):
        self.host= "localhost"

    # function to get a fresh cursor and database object 
    def getFreshConnection(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            charset='utf8mb4',
            password="",
            database="fyp"
        )

        if db.is_connected():
            print("You're connected to database!")
        else:
            print("Error Connection!")
        cursor = db.cursor()
        return cursor, db

    # close the connection using cursor and database object created
    def close_connection(self,cursor,db):
        cursor.close()
        db.close()
        if not db.is_connected():
            print("MySQL connection is closed")
        else:
            print("Connection is not closed Successfully!")

    # getter setters
    def setHost(self, host):
        self.host = host 
    def getHost(self):
        return self.host 
    def setUser(self, user):
        self.user = user 
    def getUser(self):
        return self.user 
    
    def setPassword(self, password):
        self.password = password 
    def getPassword(self):
        return self.password

    def setDb(self, db):
        self.db = db 
    def getDb(self):
        return self.db
    
    # getter setters finished


    # query and get all the results
    def queryAll(self, query, val):
        self.mysql.init_app(self.app)
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute(query, val)
        lst = cursor.fetchall()
        connection.close()
        return lst
    
    # query and get only one result
    def queryOne(self, query, val):
        self.mysql.init_app(self.app)
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute(query, val)
        lst = cursor.fetchone()
        connection.close()
        return lst
    

    # query without returning result
    def query(self, query, val):
        self.mysql.init_app(self.app)
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute(query, val)
        connection.close()
        

