import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_file):
        """ Initialize the database manager with a database file """
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        """ Create a database connection to the SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(f"SQLite version: {sqlite3.version}")
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_tables(self):
        """ Create tables in the SQLite database """
        
        create_table1_sql = """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            gender TEXT,
            location TEXT,
            name TEXT
        );
        """
        
        create_table2_sql = """
        CREATE TABLE IF NOT EXISTS user_details (
            uuid TEXT PRIMARY KEY,
            email TEXT,
            picture TEXT,
            dob TEXT,
            login_details TEXT,
            phone TEXT,
            FOREIGN KEY (email) REFERENCES users (email)
        );
        """
        
        try:
            c = self.conn.cursor()
            c.execute(create_table1_sql)
            c.execute(create_table2_sql)
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(e)

    def check_table_exists(self, table_name):
        """
        Check if a table exists in the database
        :param table_name: Name of the table to check
        :return: True if the table exists, False otherwise
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        cur = self.conn.cursor()
        cur.execute(query, (table_name,))
        result = cur.fetchone()
        return result is not None

    # def insert_user(self, user):
    #     """
    #     Insert a new user into the users table
    #     :param user: a tuple with user data
    #     """
    #     sql = ''' INSERT INTO users(email, gender, location, name)
    #               VALUES(?,?,?,?) '''
    #     cur = self.conn.cursor()
    #     cur.execute(sql, user)
    #     self.conn.commit()
    #     return cur.lastrowid
    def insert_user(self, user):
        """
        Insert a new user into the users table
        :param user: a tuple with user data
        """
        sql = ''' INSERT OR IGNORE INTO users(email, gender, location, name)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, user)
        self.conn.commit()
        return cur.lastrowid

    def insert_user_details(self, user_details):
        """
        Insert a new user details into the user_details table
        :param user_details: a tuple with user details data
        """
        sql = ''' INSERT INTO user_details(uuid, email, picture, dob, login_details, phone)
                  VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, user_details)
        self.conn.commit()
        return cur.lastrowid

    def insert_data_from_dataframe(self, df):
        """
        Insert data from a pandas DataFrame into the SQLite database
        :param df: pandas DataFrame with user data
        """
        for index, row in df.iterrows():
            user = (row['email'], row['gender'], row['location'], row['name'])
            user_details = (row['uuid'], row['email'], row['picture'], row['dob'], row['login_details'], row['phone'])
            self.insert_user(user)
            self.insert_user_details(user_details)

    def select_all_users(self):
        """
        Query all rows in the users table
        :return: a list of users
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def select_all_user_details(self):
        """
        Query all rows in the user_details table
        :return: a list of user details
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user_details")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        """ Close the database connection """
        if self.conn:
            self.conn.close()
