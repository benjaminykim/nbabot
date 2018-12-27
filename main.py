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

for submission in subreddit.hot(limit=1000):
    title = submission.title
    if "GAME THREAD:" not in title:
        continue
    else:
        print(title)
        submission.comments.replace_more(limit=0)
        i = 0
        for comment in submission.comments.list():
            i += 1
            print(comment.body)
        print(i)
