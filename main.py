import sqlite3
from sqlite3 import Error
import praw
from datetime import datetime
import utils

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

def main():
    db = 'db/r_nba_log.db'
    print(db)
    # create a database connection
    conn = utils.create_connection(db)
    with conn:
        submissions = """ CREATE TABLE IF NOT EXISTS submissions (
                                           id text PRIMARY KEY,
                                           title text NOT NULL,
                                           date text,
                                           score integer
                                       ); """
        utils.create_table(conn, submissions)
        for submission in subreddit.search("GAME THREAD", sort='new', time_filter='day'):
            id = submission.id
            title = submission.title
            date = datetime.utcfromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
            score = submission.score
            submission = (id, title, date, score)
            utils.insert_submission(conn, submission)

if __name__ == '__main__':
    main()
