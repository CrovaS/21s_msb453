###
### main routine
###

import db as db_module
import video
import time
import argparse

# machine id allocate for this server
MACHINE_ID = 0

# time interval between updates
TIME_INTERVAL = 5

def main(hostname, username, password):
    # Connect to DB server.
    db, cursor = db_module.db_connect(username, password, hostname, 'bookshelf')

    # Do update in every TIME_INTERVAL sec, until exception
    # (keyboard interrupt) occur.
    try:
        while True:
            remaining_time = video.get_remaining_time()
            if remaining_time >= 0:
                db_module.db_store(db, cursor, MACHINE_ID, remaining_time)
            else:
                print("failed to get remaining time. Sleep...")
            time.sleep(TIME_INTERVAL)
    except KeyboardInterrupt:
        db.close()
        print('Bye...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Real time video processing service for washing machine')
    parser.add_argument('--host', required=True, help='hostname')
    parser.add_argument('--user', required=True, help='username')
    parser.add_argument('--pw', required=True, help='password')
    args = parser.parse_args()
    main(args.host, args.user, args.pw)
