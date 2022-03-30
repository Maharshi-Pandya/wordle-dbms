# connect to the database 'wordle_dbms'

import psycopg2
from psycopg2 import Error

def connectToWordle(_user, _password, _database) -> list:
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
conn, err = connectToWordle("admin", "admin", "wordle_dbms")

if err is not None:
    print("Error ::->", err)
else:
    print("Connection successful")
    conn.close()
    print(conn)