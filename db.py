import pyodbc
server = 'valley.database.windows.net'
database = 'valley'
username = 'jason'
password = 'HackTheValley123'
driver= '{ODBC Driver 13 for SQL Server}'

def connect():
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn.cursor()

def insertMetric(video_id, user_id, elapsed_time, anger, contempt,
        disgust, fear, happiness, neutral, sadness, surprise):
    cursor = connect()
    cursor.execute('INSERT INTO metrics VALUES(' +
            "'" +  video_id + "'," +
            "'" +  user_id + "'," +
            elapsed_time + "," +
            anger + "," +
            contempt + "," +
            disgust + "," +
            fear + "," +
            happiness + "," +
            neutral + "," +
            sadness + "," +
            surprise +
            ')') 
    cursor.commit()

#def insertUser(video

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
#row = cursor.fetchone()
#if row:
#    print row
