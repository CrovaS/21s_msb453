###
### module for database operations
###
### DB schema
### CREATE TABLE realtime(
### realTimeID INT NOT NULL AUTO_INCREMENT,
### washingID INT,
### realTimeHour INT,
### realTimeMinute INT,
### PRIMARY KEY(realTimeID));

import pymysql


# Connect MySQL DB server with given information.
# DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE
def db_connect(db_user, db_password, db_host, db_database):
    db = pymysql.connect(
        user = db_user,
        password = db_password,
        host = db_host,
        db = db_database,
        charset = 'utf8'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


# Send Query to DB server with MACHINE_ID and REMAINING_TIME.
def db_store(db, cursor, machine_id, remaining_time):
    remaining_hour = remaining_time // 60
    remaining_minute = remaining_time % 60
    sql = "INSERT INTO realtime(washingID, realTimeHour, realTimeMinute) \
           VALUES ({0}, {1}, {2});".format(
           machine_id, remaining_hour, remaining_minute)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    db.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Real time video processing service for washing machine')
    parser.add_argument('--host', required=True, help='hostname')
    parser.add_argument('--user', required=True, help='username')
    parser.add_argument('--pw', required=True, help='password')
    args = parser.parse_args()
    db, cursor = db_connect(args.user, args.pw, args.host, 'bookshelf')
    while True:
        sql = input()
        if sql == "q":
            break
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        db.commit()
    db.close()


