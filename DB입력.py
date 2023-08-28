import pymysql
import csv
'''
url : db-i9ss7.pub-cdb.ntruss.com
username : owen
password : ow980916@
port : 13306
'''
host_name = "db-i9ss7.pub-cdb.ntruss.com"
user_name = "owen"
password = "ow980916@"
port_number = 13306
database_name = "PhishNetter"

conn = pymysql.connect(
    host=host_name,
    user=user_name,
    password=password,
    port = port_number,
    database = database_name
)

cur = conn.cursor()
##67501
conn.begin()
with open("verified_online_20230825.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        try:
            print(len(row[1]))
            qur = "INSERT INTO black_list (url) VALUES(%s);"
            cur.execute(qur, (row[1]))
            conn.commit()
        except:
            pass

cur.close()
conn.close()
