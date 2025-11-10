import psycopg2

class Database:
    def __init__(self):
        '''us=input("User for postgres: ")
        pa=input("Password for postgres: ")
        ho=input("Host for postgres: ")'''
        self.conn1 = psycopg2.connect(
            dbname="postgres",
            user='postgres',
            password='12345',
            host='localhost')
        
        self.conn1.autocommit = True
        self.cursor1 = self.conn1.cursor()
        
        #Create Database chess
        self.cursor1.execute("SELECT datname FROM pg_database;")
        
        self.databases = [db[0] for db in self.cursor1.fetchall()]
        
        if "chess" not in self.databases:
            self.cursor1.execute("CREATE DATABASE chess")
            self.conn1.commit()
            print('Database Created')
        elif "chess" in self.databases:
            print("Database Exists")
        self.cursor1.close()
        self.conn1.close()
        
        #=============================================================================#
        
        # Establish connection
        self.conn = psycopg2.connect(
            dbname="chess",
            user='postgres',
            password='12345',
            host='localhost',
            port="5432")
                
        # Create cursor
        self.cur = self.conn.cursor()
        
        self.table_name = 'chess_user'
        
        self.cur.execute("""SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s);""", (self.table_name,))
        
        self.exists = self.cur.fetchone()[0]
        if self.exists:
            print('Table Exists')
        else:
            self.cur.execute("""CREATE TABLE chess_user(username varchar(30) PRIMARY KEY, password varchar(30), wins int, lost int)""")
            self.conn.commit()
            print('Table Created')
        
    
    def insert_data(self,username,pin):
        try:
            self.cur.execute("insert into chess_user values(%s,%s,%s,%s,%s);",(username,pin,0,0))
            self.conn.commit()
            
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
    def password_reset(self,npin,usn):
        self.cur.execute("update chess_user set password=%s where username = %s;",(npin,usn))
    def username_check(self,usn):  
        self.cur.execute("SELECT username FROM chess_user where username = %s;",(usn,))
        self.data = self.cur.fetchall()
        if self.data!=[]:
            return True
        return False
    
