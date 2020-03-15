import pandas as pd
import praw
import os


def redditconnect():
    try:
        user_agent = "python:django-reddit:selfhost"
        reddit = praw.Reddit("reddit", user_agent=user_agent)
    except Exception as e:
        print(e)
        user_agent = "python:django-reddit:heroku"
        reddit = praw.Reddit(
            client_id=os.environ("PRAW_CLIENT_ID"),
            client_secret=os.environ("PRAW_CLIENT_SECRET"),
            password=os.environ("PRAW_PASSWORD"),
            user_agent=user_agent,
            username=os.environ("PRAW_USERNAME"),
        )
    return reddit


def extract_comments_post(url=None):
    reddit = redditconnect()
    comments = []
    urls = [x.strip() for x in url.split(",")]
    for url in urls:
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=None)
        for index, comment in enumerate(submission.comments.list(), 1):
            if not comment.author:
                author = "[deleted]"
            else:
                author = comment.author.name
            comments.append(
                {
                    "ID": comment.id,
                    "Subreddit": comment.subreddit.display_name,
                    "Date": comment.created_utc,
                    "Author": author,
                    "Comment": comment.body,
                    "Score": comment.score,
                    "Length": len(comment.body),
                    "Gilded": comment.gilded,
                    "Parent": comment.parent_id,
                    "Flair": comment.author_flair_text,
                    "Post ID": submission.id,
                    "Post Permalink": f"https://reddit.com{submission.permalink}",
                    "Post Title": submission.title,
                    "Post Author": submission.author,
                    "Post URL": submission.url,
                    "Permalink": f"https://reddit.com{comment.permalink}",
                }
            )

    df = pd.DataFrame(comments)
    return df


def extract_comments_user(username):
    usernames = [x.strip() for x in username.split(",")]
    comments = []
    reddit = redditconnect()
    for username in usernames:
        user = reddit.redditor(username)
        for index, comment in enumerate(user.comments.new(limit=None), 1):
            comments.append(
                {
                    "User": str(username),
                    "ID": comment.id,
                    "Comment": comment.body,
                    "Permalink": f"https://reddit.com{comment.permalink}",
                    "Length": len(comment.body),
                    "Date": comment.created_utc,
                    "Score": comment.score,
                    "Subreddit": comment.subreddit.display_name,
                    "Gilded": comment.gilded,
                    "Post ID": comment.link_id,
                    "Post Title": comment.link_title,
                    "Post URL": comment.link_url,
                    "Post Author": comment.link_author,
                }
            )
    df = pd.DataFrame(comments)
    return df


def extract_posts_user(username):
    usernames = [x.strip() for x in username.split(",")]
    reddit = redditconnect()
    posts = []
    for username in usernames:
        user = reddit.redditor(username)
        for index, submission in enumerate(
            user.submissions.new(limit=None), 1
        ):
            posts.append(
                {
                    "ID": submission.name,
                    "Title": submission.title,
                    "URL": submission.url,
                    "Comments": submission.num_comments,
                    "Score": submission.score,
                    "Ratio": submission.upvote_ratio,
                    "Author": str(submission.author),
                    "Author CSS Flair": str(submission.author_flair_css_class),
                    "Author Text Flair": str(submission.author_flair_text),
                    "Permalink": f"https://reddit.com{submission.permalink}",
                    "Date": submission.created_utc,
                    "Flair": str(submission.link_flair_text),
                    "Text": str(submission.selftext),
                    "Domain": submission.domain,
                    "Gilded": submission.gilded,
                    "Hidden": submission.hidden,
                    "Archived": submission.archived,
                    "Can Gild": submission.can_gild,
                    "Can Crosspost": submission.is_crosspostable,
                }
            )
    df = pd.DataFrame(posts)
    return df
