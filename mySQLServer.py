import mysql.connector

databaseName = "ChampionsLeague"
userID = "root"
pwd = "root"


connection = mysql.connector.connect(user=userID, password=pwd,
                              host='127.0.0.1',
                              database=databaseName)

cursor = connection.cursor()

tID = "'T01'"

query = """SELECT t1.MID,t1.TID, t1.TGoals, t2.Against AS Opponent, t2.TGoals as OppenentGoals
            FROM  
            (SELECT mr.MID, ms.Team1 As TID, ms.Team2 AS Against, sum( mr.Goals) AS TGoals FROM MatchRoster mr INNER JOIN MatchSchedule ms ON ms.MID = mr.MID 
            WHERE ms.Team1 = %s AND mr.PID in (SELECT PID FROM TeamRoster WHERE TID = %s) 
            GROUP BY mr.MID, ms.Team1, ms.Team2  
            UNION 
            SELECT mr.MID,  ms.Team2 as TID, ms.Team1 AS Against, sum( mr.Goals) AS TGoals FROM MatchRoster mr INNER JOIN MatchSchedule ms ON ms.MID = mr.MID 
            WHERE ms.Team2 = %s AND mr.PID in (SELECT PID FROM TeamRoster WHERE TID = %s) 
            GROUP BY mr.MID, ms.Team2, ms.Team1 ) t1 
            LEFT JOIN   
            (SELECT mr.MID, ms.Team1 As TID, ms.Team2 AS Against, sum( mr.Goals) AS TGoals FROM MatchRoster mr INNER JOIN MatchSchedule ms ON ms.MID = mr.MID 
            WHERE ms.Team1 = %s AND mr.PID NOT in (SELECT PID FROM TeamRoster WHERE TID = %s) 
            GROUP BY mr.MID, ms.Team1, ms.Team2  
            UNION 
            SELECT mr.MID,  ms.Team2 as TID, ms.Team1 AS Against, sum( mr.Goals) AS TGoals FROM MatchRoster mr INNER JOIN MatchSchedule ms ON ms.MID = mr.MID 
            WHERE ms.Team2 = %s AND mr.PID NOT in (SELECT PID FROM TeamRoster WHERE TID = %s) 
            GROUP BY mr.MID, ms.Team2, ms.Team1) t2 ON t1.MID = t2.MID"""

cursor.execute(query,tID)

for (t1.MID, t1.TID, t1.TGoals, Opponent, OppenentGoals) in cursor:
    print("{} {} {} {} {}".format(t1.MID, t1.TID, t1.TGoals, Opponent, OppenentGoals))

cursor.close()
connection.close()