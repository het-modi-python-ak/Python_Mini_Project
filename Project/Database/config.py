import os 

DB_CONFIG = {
   "host": os.environ.get('HOST'),
   "user": os.environ.get('USER'),
   "password": os.environ.get('PASSWORD'),
   "database": os.environ.get('DATABASE')
}