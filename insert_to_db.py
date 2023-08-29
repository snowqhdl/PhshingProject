import pymysql

def insert_to_db(url, probability):
    host_name = 
    user_name = 
    password = 
    port_number = 
    database_name = 
    
    conn = pymysql.connect(host=host_name,
                           user=user_name,
                           password=password,
                           port = port_number,
                           database = database_name
                           )
    try:
        with conn.cursor() as cur:
            ## 데이터를 DB에 입력하는 SQL 쿼리
            sql = "INSERT INTO predicted_list (url, probability) VALUES (%s, %s)"
            cur.execute(sql, (url, probability))
            conn.commit()
    ## 에러 발생
    except pymysql.MySQLError:
        conn.rollback()  # 에러가 발생하면 롤백 처리
    finally:
        conn.close()
