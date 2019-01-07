import sqlite3
from sqlite3 import Error
import praw
import utils
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

reddit = praw.Reddit('nbabot')
subreddit = reddit.subreddit("nba")
sia = SIA()

def metadata_extractor(submission, type):
    """ extract data (id, title, date, score) from submission
    :param submission: Submission object (sqlite3)
    :return: (id, title, date, score, sentiment) tuple
    """
    id = submission.id
    title = submission.title
    date = utils.utc_to_std_time(submission.created_utc)
    score = submission.score
    comment_data = get_comments(submission)
    sentiment = get_sentiment_intensity(comment_data)
    return (id, title, date, score, type, sentiment)

# sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
# tokens = nltk.word_tokenize(sentence)

def get_sentiment_intensity(corpus):
    scores = []
    for line in corpus:
        scores.append(sia.polarity_scores(line)['compound'])
    return sum(scores) / float(len(scores))


def get_comments(submission):
    """ get comments from submission
    :param submission: Submission object (sqlite3)
    :return: comments (string) in list
    """
    submission.comments.replace_more(limit=0)
    comment_data = [comment.body for comment in submission.comments.list()]
    return comment_data

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
                                           score integer,
                                           type text,
                                           sentiment decimal
                                       ); """
        utils.create_table(conn, submissions)
        for submission in subreddit.search("GAME THREAD", sort='new', time_filter='day'):
            submission_data = metadata_extractor(submission, "GAME THREAD")
            utils.insert_submission(conn, submission_data)

def count_vectorizer():
    corpus = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
        ]
    for submission in subreddit.hot(limit=1):
        submission.comments.replace_more(limit=0)
        corpus = [comment.body for comment in submission.comments.list()]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(X.toarray())

if __name__ == '__main__':
    main()
