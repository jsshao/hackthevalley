import pyodbc
server = 'valley.database.windows.net'
database = 'valley'
username = 'jason'
password = 'HackTheValley123'
driver= '{ODBC Driver 13 for SQL Server}'

def connect():
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

def insertMetric(video_id, user_id, elapsed_time, anger, contempt,
        disgust, fear, happiness, neutral, sadness, surprise):
    conn = connect()
    cursor = conn.cursor()
    query = 'INSERT INTO metrics VALUES(' + \
            "'" +  video_id + "'," + \
            str(elapsed_time) + "," + \
            str(anger) + "," + \
            str(contempt) + "," + \
            str(disgust) + "," + \
            str(fear) + "," + \
            str(happiness) + "," + \
            str(neutral) + "," + \
            str(sadness) + "," + \
            str(surprise) + "," + \
            "'" +  user_id + "'" + \
            ')'
    cursor.execute(query)
    conn.commit()

def insertUser(user_id, age, gender):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = 'INSERT INTO users VALUES(' + \
                "'" + user_id + "'," + \
                str(age) + "," + \
                "'" + gender + "')"
        cursor.execute(query)
        conn.commit()
    except:
        # Fails primary key constraint
        print "Duplicate key"

def userExists(user_id):
    cursor = connect().cursor()
    query = "SELECT user_id FROM users WHERE user_id = '" + user_id + "'"
    cursor.execute(query)
    return len(cursor.fetchall()) > 0

def deleteAll():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metrics")
    cursor.execute("DELETE FROM users")
    conn.commit() 

# Test only
if __name__ == '__main__':
    insertMetric('test', 'test', 10, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    insertUser('test_user', 22, 'male')
    #deleteAll()
    cursor = connect().cursor()
    cursor.execute("SELECT * FROM users")
    print cursor.fetchall()
    print userExists('test_user')
    print userExists('test')
   

#cursor.execute("SELECT * FROM metrics")
#for rows in cursor.tables():
#     if rows.table_type == "TABLE":  #LOCAL TABLES ONLY
#         print rows.table_name
#         for fld in cursor.columns(rows.table_name):
#             print(fld.table_name, fld.column_name)

#cursor.execute("CREATE TABLE metrics(video_id varchar(255) NOT NULL, elapsed_time int NOT NULL, anger FLOAT, contempt FLOAT, disgust FLOAT, fear FLOAT, happiness FLOAT, neutral FLOAT, sadness FLOAT, surprise FLOAT)")
#cursor.commit()
#cursor.execute("ALTER TABLE metrics ADD user_id VARCHAR(255) NOT NULL");
#cursor.commit()
#cursor.execute("CREATE TABLE users(user_id VARCHAR(255) NOT NULL, age INT NOT NULL, gender VARCHAR(16) NOT NULL, PRIMARY KEY(user_id))")
#cursor.commit()
