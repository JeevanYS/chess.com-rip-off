import mysql.connector

class Database:
    def __init__(self):
        us=input("User for mySQL: ")
        pa=input("Password for mySQL: ")
        ho=input("Host for muSQL: ")
        self.conn1 = mysql.connector.connect(
            host=ho,
            user=us,
            password=pa
        )
        self.conn1.autocommit = True
        self.cursor1 = self.conn1.cursor()
        
        self.cursor1.execute("SHOW DATABASES")
        
        self.databases = [db[0] for db in self.cursor1.fetchall()]
        
        if "chess" not in self.databases:
            self.cursor1.execute("CREATE DATABASE chess")
            print('Database Created')
        else:
            print("Databse Exists")
        self.cursor1.close()
        self.conn1.close()
        #=============================================================================#
        self.conn = mysql.connector.connect(
            database="chess",
            user=us,
            password=pa,
            host=ho,
            port=3306
        )
        
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        
        table_name = 'chess_user'
        
        self.cur.execute("SHOW TABLES LIKE %s", (table_name,))
        self.result = self.cur.fetchone()
        
        if self.result:
            print(f"Table '{table_name}' exists.")
        else:
            self.cur.execute("""CREATE TABLE chess_user(username varchar(30) PRIMARY KEY, password varchar(30), wins int, lost int)""")
            print('Table Created')
    
    def insert_data(self,username,pin):
        try:
            self.cur.execute("insert into chess_user values(%s,%s,%s,%s);",(username,pin,0,0))
            
        except Exception as a:
            print("Insert Record Error",a)
            self.conn.rollback()
            
    def password_check(self,pin,usn):
        self.cur.execute("SELECT password FROM chess_user where username = %s;",(usn,))
        self.data = self.cur.fetchall()
        self.passwrd=pin.get_text()
        if self.data[0][0]==self.passwrd:
            return True
        return False
        
    def username_check(self,usn):
        self.cur.execute("SELECT username FROM chess_user where username = %s;",(usn,))
        self.data = self.cur.fetchall()
        if self.data!=[]:
            return True
        return False

