# connect to the database 'wordle_dbms'

import psycopg2
import random

from psycopg2 import Error

# custom imports
from .errors import handle_error


# Try and connect to the wordle database
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


# Check if a word exists in a table
def check_word_exists(conn, table, word) -> tuple:
    word_id, word_content = None, None
    
    try:
        with conn.cursor() as cur:
            check_word_query = f"SELECT id, content FROM {table} WHERE content=\'{word}\';"
            
            # Execute and fetch
            cur.execute(check_word_query)
            cw_tuple = cur.fetchone()
            
            if cw_tuple is not None:
                word_id, word_content = cw_tuple
        
    except (Exception, Error) as error:
        handle_error(error)

    return (word_id, word_content)


# Fetch any random word from the table
def fetch_random_word(conn, table, max_id) -> tuple:
    word_id, word_content = None, None
    
    # random id between (1, max_id) and check if it exists
    rand_id = random.randrange(1, max_id + 1)
    
    try:
        with conn.cursor() as cur:
            rand_query = f"SELECT id, content FROM {table} WHERE id={rand_id};"
            
            # Execute and fetch
            cur.execute(rand_query)
            rq_tuple = cur.fetchone()
            
            if rq_tuple is not None:
                word_id, word_content = rq_tuple
            
    except (Exception, Error) as error:
        handle_error(error)

    return (word_id, word_content)


# Fetch the last entry's id from a table
def fetch_last_id(conn, table) -> int:
    last_id = None
    
    try:
        with conn.cursor() as cur:
            last_id_query = f"SELECT max(id) FROM {table};"
            
            # Execute and fetch
            cur.execute(last_id_query)
            li_tuple = cur.fetchone()
            
            last_id = li_tuple[0]

    except (Exception, Error) as error:
        handle_error(error)
        
    return last_id        


# Read a file line by line and insert into table
def insert_data(conn, table, datafile) -> int:
    row_id = 1
    
    try:
        with open(datafile) as file:
            for word in file:
                # word is read
                word = word.strip()
                
                with conn.cursor() as cur:
                    insert_query = f"INSERT INTO {table} (id, content) VALUES ({row_id}, \'{word}\');"
                    
                    # Execute the query and commit the changes to DB
                    cur.execute(insert_query)
                    conn.commit()
            
                row_id += 1
    
    except (Exception, Error) as error:
        handle_error(error)
                
    return row_id


# # Testing... 
# conn, err = connect_to_wordle("admin", "admin", "wordle_dbms")
# handle_error(err)

# last_id = fetch_last_id(conn, "answers")
# print("Last inserted id is:", last_id)

# check_word = check_word_exists(conn, "answers", "abbas")
# print(check_word)

# rand = fetch_random_word(conn, "answers", last_id)
# print("Random word fetched: ", rand)