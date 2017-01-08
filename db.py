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

def getVideoMetrics(video_id):
    cursor = connect().cursor()
    query = """
            SELECT elapsed_time, 
                   AVG(anger),
                   AVG(contempt),
                   AVG(disgust),
                   AVG(fear),
                   AVG(happiness),
                   AVG(neutral),
                   AVG(sadness),
                   AVG(surprise)
            FROM metrics
            WHERE video_id = '%s'
            GROUP BY elapsed_time
    """ % video_id
    cursor.execute(query)
    data = []
    for point in cursor.fetchall():
        data.append({"timestamp": point[0],
                     "anger": point[1],
                     "contempt": point[2],
                     "disgust": point[3],
                     "fear": point[4],
                     "happiness": point[5],
                     "neutral": point[6],
                     "sadness": point[7],
                     "surprise": point[8],
                     })
    return data

def getAllVideoIds():
    cursor = connect().cursor()
    query = """
            SELECT DISTINCT video_id
            FROM metrics
    """
    cursor.execute(query)
    return [video[0] for video in cursor.fetchall()]

def getDemographic(video_id):
    data = {'gender': [0, 0], 'age': [0, 0, 0, 0, 0, 0]}
    cursor = connect().cursor()
    query = """
            SELECT gender, COUNT(*)
            FROM users
            WHERE user_id IN (
	        SELECT DISTINCT user_id 
	        FROM metrics
	        WHERE video_id = '%s'
            )
            GROUP BY gender
    """ % video_id
    cursor.execute(query)
    for point in cursor.fetchall():
        if point[0] == 'male':
            data['age'][0] = point[1]
        else:
            data['age'][1] = point[1]
    query = """
            SELECT SUM(CASE WHEN age BETWEEN 13 AND 17 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN age BETWEEN 18 AND 24 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN age BETWEEN 25 AND 34 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN age BETWEEN 35 AND 44 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN age BETWEEN 45 AND 54 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN age >= 55 THEN 1 ELSE 0 END)
            FROM users
            WHERE user_id IN (
	        SELECT DISTINCT user_id 
	        FROM metrics
	        WHERE video_id = '%s'
            )
    """ % video_id
    cursor.execute(query)
    data['age'] = list(cursor.fetchall()[0])
    return data

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
    print getVideoMetrics('VEX7KhIA3bU')
    print getAllVideoIds()
    print getDemographic('VEX7KhIA3bU')

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
