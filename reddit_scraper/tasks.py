from __future__ import absolute_import, unicode_literals

from psaw import PushshiftAPI
from celery import shared_task
from .reddit_scraper import redditconnect
import pandas as pd
import os
import requests
import json

COLUMNS_POSTS = [
    "date",
    "date_utc",
    "author",
    # "author_flair_css_class",
    # "author_flair_richtext",
    # "author_flair_text",
    # "author_flair_type",
    # "brand_safe",
    # "can_mod_post",
    # "contest_mode",
    "created_utc",
    "domain",
    "full_link",
    # "gilded",
    "id",
    # "is_crosspostable",
    # "is_original_content",
    # "is_reddit_media_domain",
    # "is_self",
    # "is_video",
    # "link_flair_background_color",
    # "link_flair_css_class",
    # "link_flair_richtext",
    # "link_flair_template_id",
    "link_flair_text",
    # "link_flair_text_color",
    # "link_flair_type",
    # "locked",
    # "no_follow",
    "num_comments",
    # "num_crossposts",
    # "over_18",
    # "parent_whitelist_status",
    "permalink",
    # "pinned",
    # "post_hint",
    # "preview",
    # "retrieved_on",
    # "rte_mode",
    "score",
    "selftext",
    # "send_replies",
    # "spoiler",
    # "stickied",
    "subreddit",
    # "subreddit_id",
    "subreddit_subscribers",
    # "subreddit_type",
    "thumbnail",
    # "thumbnail_height",
    # "thumbnail_width",
    "title",
    "url",
    # "whitelist_status",
    "created",
    # "media",
    # "media_embed",
    # "secure_media",
    # "secure_media_embed",
    # "approved_at_utc",
    # "banned_at_utc",
    # "suggested_sort",
    # "view_count",
    # "author_created_utc",
    # "author_fullname",
    # "distinguished",
    # "author_flair_background_color",
    # "author_flair_template_id",
    # "author_flair_text_color",
    # "author_patreon_flair",
    # "gildings",
    # "is_meta",
    # "is_robot_indexable",
    # "media_only",
    # "pwls",
    # "wls",
    # "author_id",
    # "all_awardings",
    # "allow_live_comments",
    # "author_premium",
    # "awarders",
    # "total_awards_received",
]


COLUMNS_COMMENTS = [
    "date",
    "date_utc",
    # "all_awardings",
    # "associated_award",
    "author",
    # "author_flair_background_color",
    # "author_flair_css_class",
    # "author_flair_richtext",
    # "author_flair_template_id",
    # "author_flair_text",
    # "author_flair_text_color",
    # "author_flair_type",
    # "author_fullname",
    # "author_patreon_flair",
    # "author_premium",
    # "awarders",
    "body",
    # "collapsed_because_crowd_control",
    "created_utc",
    # "gildings",
    "id",
    # "is_submitter",
    "link_id",
    # "locked",
    # "no_follow",
    "parent_id",
    "permalink",
    # "retrieved_on",
    "score",
    # "send_replies",
    # "stickied",
    "subreddit",
    # "subreddit_id",
    # "total_awards_received",
    # "treatment_tags",
    "created",
    "edited",
    # "steward_reports",
    "updated_utc",
    # "author_created_utc",
    # "can_gild",
    # "collapsed",
    # "collapsed_reason",
    # "controversiality",
    # "distinguished",
    # "gilded",
    # "nest_level",
    # "reply_delay",
    # "subreddit_name_prefixed",
    # "subreddit_type",
    # "rte_mode",
    # "score_hidden",
]


@shared_task
def extract_comments_post_praw(url=None):
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
def extract_comments_user_praw(username):
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
def extract_posts_user_praw(username):
    usernames = [x.strip() for x in username.split(",")]
    reddit = redditconnect()
    posts = []
    for username in usernames:
        user = reddit.redditor(username)
        for index, submission in enumerate(user.submissions.new(limit=None), 1):
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
def extract_comments_user_psaw(username):
    usernames = [x.strip() for x in username.split(",")]
    api = PushshiftAPI()
    df = pd.DataFrame()
    for username in usernames:
        res = api.search_comments(author=username)
        df_new = pd.DataFrame([thing.d_ for thing in res])
        df = pd.concat([df, df_new], ignore_index=True)
    df["date_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    df["date"] = pd.to_datetime(df["created"], unit="s")
    df["permalink"] = "https://old.reddit.com" + df["permalink"].astype(str)
    df = df[df.columns.intersection(COLUMNS_COMMENTS)]
    return df.to_json()


@shared_task
def extract_posts_user_psaw(username):
    usernames = [x.strip() for x in username.split(",")]
    api = PushshiftAPI()
    df = pd.DataFrame()
    for username in usernames:
        res = api.search_submissions(author=username)
        df_new = pd.DataFrame([thing.d_ for thing in res])
        df = pd.concat([df, df_new], ignore_index=True)
    df["date_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    df["date"] = pd.to_datetime(df["created"], unit="s")
    df["permalink"] = "https://old.reddit.com" + df["permalink"].astype(str)
    df = df[df.columns.intersection(COLUMNS_POSTS)]
    return df.to_json()


@shared_task
def retrieve_last_FL():
    headers = {"User-Agent": "Reddit FL retriever"}
    url = "https://www.reddit.com/search.json?q=subreddit%3Afrance%20flair%3A%22Forum%20Libre%22%20author%3AAutoModerator%20title%3A%22Forum%20Libre*%22&sort=new"
    req = requests.get(url, headers=headers)
    return json.loads(req.content)["data"]["children"][0]["data"]["url"]
