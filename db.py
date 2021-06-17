###
### module for database operations
###

import pymysql

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

def db_store(db, cursor, machine_id, remaining_time):
    sql = "INSERT INTO washing_machine \
           VALUES ({0}, {1}) \
           ON DUPLICATE KEY UPDATE machine_id={2}, ramaining_time={3};".format(
    machine_id, remaining_time, machine_id, remaining_time)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    db.commit()

if __name__ == "__main__":
    db, cursor = db_connect('root', 'passw0rd', 'localhost', 'bookshelf')
    while (True):
        sql = input()
        if sql == "q":
            break
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        db.commit()
    db.close()


