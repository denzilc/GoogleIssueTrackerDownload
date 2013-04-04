import MySQLdb as mysql

''' This class defines all the required methods and data for a mysql connection. '''
class MySQL:

    ''' Initialize the MySql connection paramters '''
    def __init__(self, host, username, passwd, db, port):
        self.host = host
        self.username = username
        self.passwd = passwd
        self.db = db
        self.port = port

    ''' Creates a MySQL connection and returns the cursor '''
    def create_connection(self):
        connection = mysql.connect(self.host, self.username, self.passwd, self.db, self.port)
        cursor = connection.cursor()
        return connection, cursor


    ''' Close the connection on the MySQL host '''
    def close_connection(self,cursor, connection):
        cursor.close()
        connection.commit()
        connection.close()