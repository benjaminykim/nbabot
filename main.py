import sqlite3
from sqlite3 import Error
import praw
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


def metadata_extractor(submission):
    """ extract data (id, title, date, score) from submission
    :param submission: Submission object (sqlite3)
    :return: (id, title, date, score) tuple
    """
    id = submission.id
    title = submission.title
    date = utils.utc_to_std_time(submission.created_utc)
    score = submission.score
    return (id, title, date, score)

def main():
    # r/nba logs database filepath
    db = 'db/r_nba_log.db'

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
            submission_data = metadata_extractor(submission)
            utils.insert_submission(conn, submission_data)

if __name__ == '__main__':
    main()
