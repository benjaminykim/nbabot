import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, sql_table):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_table)
    except Error as e:
        print(e)

def insert_submission(conn, submission):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
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
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
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
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM submissions WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))

def delete_all(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM submissions'
    cur = conn.cursor()
    cur.execute(sql)

def select_all(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_submission(conn, id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions WHERE id=?", (id,))

    row = cur.fetchall()
    return row

def utc_to_std_time(utc_time):
    from datetime import datetime
    return datetime.utcfromtimestamp(int(utc_time)).strftime('%Y-%m-%d %H:%M:%S')
