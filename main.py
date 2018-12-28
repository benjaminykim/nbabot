import sqlite3
from sqlite3 import Error
import praw

reddit = praw.Reddit('nbabot')
subreddit = reddit.subreddit("nba")

"""
for submission in subreddit.hot(limit=1):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("----------------------\n")

    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        print(comment.body)
"""
scores = []

# for submission in subreddit.hot(limit=1000):
#     title = submission.title
#     if "GAME THREAD:" not in title:
#         continue
#     else:
#         print(title)
#         submission.comments.replace_more(limit=0)
#         i = 0
#         for comment in submission.comments.list():
#             i += 1
#             print(comment.body)
#         print(i)

#for submission in subreddit.search("GAME THREAD", sort='new', time_filter='day'):
#    print(submission.title)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "db/pythonsqlite.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    create_connection("db/r_nba_log.db")
    main()
