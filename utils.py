import sqlite3
from sqlite3 import Error

# PYTHON TO SQLITE INTERFACE
def create_connection(db_file):
    """ create a database connection to a SQLite database
    :param db_file: database local filepath string
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, sql_table):
    """ create a table from the sql_table statement
    :param conn: Connection object
    :param sql_table: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_table)
    except Error as e:
        print(e)

def insert_submission(conn, submission):
    """ insert subreddit submission into database
    :param conn: Connection object
    :param submission: (id, title, date, score) tuple
    :return:
    """
    id = submission[0]
    if select_submission(conn, id):
        update_submission(conn, submission)
    else:
        sql = ''' INSERT INTO submissions(id,title,date,score)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, submission)

def update_submission(conn, submission_update):
    """
    update submission by id with new data
    :param conn: Connection object
    :param submission_update: (id, title, date, score) tuple
    :return:
    """
    sql = """   UPDATE submissions
                    SET
                        title = ?,
                        date = ?,
                        score = ?
                    WHERE id = ?
                    ;"""
    id, title, date, score = submission_update
    submission_update = (title, date, score, id)
    cur = conn.cursor()
    cur.execute(sql, submission_update)

def delete_submission(conn, id):
    """
    delete submission by id
    :param conn:  Connection object
    :param id: submission id string
    :return:
    """
    sql = 'DELETE FROM submissions WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))

def delete_all(conn):
    """
    Delete all rows in submissions table
    :param conn: Connection object
    :return:
    """
    sql = 'DELETE FROM submissions'
    cur = conn.cursor()
    cur.execute(sql)

def select_all(conn):
    """
    Query all rows in submissions table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions")
    rows = cur.fetchall()
    return rows

def select_submission(conn, id):
    """
    Query submission by id
    :param conn: Connection object
    :param id: submission id string
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions WHERE id=?", (id,))
    row = cur.fetchall()
    return row

# DATA PREPROCESSING INTERFACE
def utc_to_std_time(utc_time):
    """
    convert utc time format to standart time format
    :param utc_time: utc time string
    :return: standard time string
    """
    from datetime import datetime
    return datetime.utcfromtimestamp(int(utc_time)).strftime('%Y-%m-%d %H:%M:%S')
