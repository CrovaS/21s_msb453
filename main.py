###
### main routine
###

from db import *
from video import *

# machine id allocate for this server
MACHINE_ID = 0

# time interval between updates
TIME_INTERVAL = 5

def main():
    db, cursor = db_connect('root', 'passw0rd', 'localhost', 'bookshelf')
    try:
        while True:
            remaining_time = get_remaining_time()
            db_store(db, cursor, MACHINE_ID, remaining_time)
            time.sleep(TIME_INTERVAL)
    except:
        db.close()
        print('Bye...')

if __name__ == '__main__':
    main()
