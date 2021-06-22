# Backend part
This part is for video processing and db updating, run on Raspberry Pi server.  
It consists of three scripts.

### [db.py](./db.py)
This module is for database manipulation.
We use MySQL as our DBMS, using pymysql module.
It provide wrapper for database server connection and update database tuples.

### [video.py](./video.py)
This module is for video processing.
Main routine is `get_remaining_time`, which will return current remaining time.
It will capture image with Raspberry Pi camera module, preprocess and recognize remaining time using OpenCV library. 

### [main.py](./main.py)
This is our main routine run on Raspberry Pi server. It will continuously update remaining time to database server.
