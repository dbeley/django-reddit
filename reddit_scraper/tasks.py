from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .reddit_scraper import redditconnect
import pandas as pd
import os
import requests
import json


@shared_task
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
                    "id": str(comment.id),
                    "subreddit": str(comment.subreddit.display_name),
                    "timestamp": int(comment.created_utc),
                    "author": str(author),
                    "comment": str(comment.body),
                    "score": str(comment.score),
                    "length": len(comment.body),
                    "gilded": int(comment.gilded),
                    "parent": str(comment.parent_id),
                    "flair": str(comment.author_flair_text),
                    "post_id": str(submission.id),
                    "post_permalink": f"https://reddit.com{submission.permalink}",
                    "post_title": str(submission.title),
                    "post_author": str(submission.author),
                    "post_url": str(submission.url),
                    "permalink": f"https://reddit.com{comment.permalink}",
                }
            )

    df = pd.DataFrame(comments)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.to_json()


@shared_task
def extract_comments_user(username):
    usernames = [x.strip() for x in username.split(",")]
    comments = []
    reddit = redditconnect()
    for username in usernames:
        user = reddit.redditor(username)
        for index, comment in enumerate(user.comments.new(limit=None), 1):
            comments.append(
                {
                    "user": str(username),
                    "id": comment.id,
                    "comment": comment.body,
                    "permalink": f"https://reddit.com{comment.permalink}",
                    "length": len(comment.body),
                    "timestamp": int(comment.created_utc),
                    "score": comment.score,
                    "subreddit": comment.subreddit.display_name,
                    "gilded": comment.gilded,
                    "post_id": comment.link_id,
                    "post_title": comment.link_title,
                    "post_url": comment.link_url,
                    "post_author": comment.link_author,
                }
            )
    df = pd.DataFrame(comments)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.to_json()


@shared_task
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
                    "id": submission.name,
                    "title": submission.title,
                    "url": submission.url,
                    "comments": submission.num_comments,
                    "score": submission.score,
                    "ratio": submission.upvote_ratio,
                    "author": str(submission.author),
                    "author_css_flair": str(submission.author_flair_css_class),
                    "author_text_flair": str(submission.author_flair_text),
                    "permalink": f"https://reddit.com{submission.permalink}",
                    "timestamp": int(submission.created_utc),
                    "flair": str(submission.link_flair_text),
                    "text": str(submission.selftext),
                    "domain": submission.domain,
                    "gilded": submission.gilded,
                    "hidden": submission.hidden,
                    "archived": submission.archived,
                    "can_gild": submission.can_gild,
                    "can_crosspost": submission.is_crosspostable,
                }
            )
    df = pd.DataFrame(posts)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    return df.to_json()


@shared_task
def retrieve_last_FL():
    headers = {"User-Agent": "Reddit FL retriever"}
    url = "https://www.reddit.com/search.json?q=subreddit%3Afrance%20flair%3A%22Forum%20Libre%22%20author%3AAutoModerator%20title%3A%22Forum%20Libre*%22&sort=new"
    req = requests.get(url, headers=headers)
    return json.loads(req.content)["data"]["children"][0]["data"]["url"]
