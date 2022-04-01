# connect to the database 'wordle_dbms'

import sys
import psycopg2

from psycopg2 import Error

# custom imports
from errors import handle_error


def connect_to_wordle(_user, _password, _database) -> list:
    # First element is the connection, Second is the error
    # If connection is successful, we return [conn, None]
    # Else we return [None, error]
    retList = [None, None]
    
    try:
        conn = psycopg2.connect(
            user=_user,
            password=_password,
            host="127.0.0.1",
            port="5432",
            database=_database
        )
        retList[0] = conn

    # catch!
    except (Exception, Error) as error:
        retList[1] = error
            
    return retList


# Example: kinda Go syntax hehe 
conn, err = connect_to_wordle("admin", "admin", "wordle_dbms")
handle_error(err)

print("Connection successful")
conn.close()
print(conn)