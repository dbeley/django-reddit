import praw


def redditconnect():
    try:
        user_agent = "python:django-reddit:selfhost"
        reddit = praw.Reddit("reddit", user_agent=user_agent)
    except Exception as e:
        print(e)
        user_agent = "python:django-reddit:heroku"
        reddit = praw.Reddit(
            client_id=os.environ["PRAW_CLIENT_ID"],
            client_secret=os.environ["PRAW_CLIENT_SECRET"],
            password=os.environ["PRAW_PASSWORD"],
            user_agent=user_agent,
            username=os.environ["PRAW_USERNAME"],
        )
    return reddit
