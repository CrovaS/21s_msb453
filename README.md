# 2021S MSB453
This project is for `Washing Machine Remaining Time Notification Service`.  
Currently, only backend part is organized. Backend part consists of three script.

### db.py
This module is for database manipulation. We use MySQL as our DBMS. It provide wrapper for database server connection and update database tuples.

### video.py
This module is for video processing. We need to implement get_remaining_time to return current remaining time by parsing input video.

### main.py
This is our main routine run on Raspberry Pi server. It will continuously update remaining time to database server.
