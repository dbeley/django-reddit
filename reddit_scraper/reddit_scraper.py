import pandas as pd
import praw


def redditconnect():
    user_agent = "python:script:download_comments_user"

    reddit = praw.Reddit("reddit", user_agent=user_agent)
    return reddit


def extract_comments_post(url=None):
    reddit = redditconnect()
    comments = []
    urls = [x.strip() for x in url.split(",")]
    # if post_id:
    #     submission = reddit.submission(id=post_id)
    d = []
    for url in urls:
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=None)
        for index, comment in enumerate(submission.comments.list(), 1):
            comments.append(comment)
        for x in comments:
            if not x.author:
                author = "[deleted]"
            else:
                author = x.author.name
            d.append(
                {
                    "ID": x.id,
                    "Subreddit": x.subreddit.display_name,
                    "Date": x.created_utc,
                    "Author": author,
                    "Comment": x.body,
                    "Score": x.score,
                    "Length": len(x.body),
                    "Gilded": x.gilded,
                    "Parent": x.parent_id,
                    "Flair": x.author_flair_text,
                    "Post ID": submission.id,
                    "Post Permalink": f"https://reddit.com{submission.permalink}",
                    "Post Title": submission.title,
                    "Post Author": submission.author,
                    "Post URL": submission.url,
                    "Permalink": f"https://reddit.com{x.permalink}",
                }
            )

    df = pd.DataFrame(d)
    return df


def extract_comments_user(username):
    usernames = [x.strip() for x in username.split(",")]
    comments = []
    # columns = [
    #     "User",
    #     "ID",
    #     "Comment",
    #     "Permalink",
    #     "Length",
    #     "Date",
    #     "Score",
    #     "Subreddit",
    #     "Gilded",
    #     "Post ID",
    #     "Post Title",
    #     "Post URL",
    #     "Post Permalink",
    #     "Post Author",
    # ]

    reddit = redditconnect()
    d = []
    for username in usernames:
        user = reddit.redditor(username)

        for index, submission in enumerate(user.comments.new(limit=None), 1):
            comments.append(submission)

        for x in comments:
            d.append(
                {
                    "User": str(username),
                    "ID": x.id,
                    "Comment": x.body,
                    "Permalink": f"https://reddit.com{x.permalink}",
                    "Length": len(x.body),
                    "Date": x.created_utc,
                    "Score": x.score,
                    "Subreddit": x.subreddit.display_name,
                    "Gilded": x.gilded,
                    "Post ID": x.link_id,
                    "Post Title": x.link_title,
                    "Post URL": x.link_url,
                    "Post Permalink": f"https://reddit.com{submission.permalink}",
                    "Post Author": x.link_author,
                }
            )

    df = pd.DataFrame(d)
    # df = df[columns]
    return df


def extract_posts_user(username):
    usernames = [x.strip() for x in username.split(",")]
    posts = []
    # columns = [
    #     "ID",
    #     "Title",
    #     "Date",
    #     "Score",
    #     "Ratio",
    #     "Comments",
    #     "Flair",
    #     "Domain",
    #     "Text",
    #     "URL",
    #     "Permalink",
    #     "Author",
    #     "Author CSS Flair",
    #     "Author Text Flair",
    #     "Gilded",
    #     "Can Gild",
    #     "Hidden",
    #     "Archived",
    #     "Can Crosspost",
    # ]

    reddit = redditconnect()
    for username in usernames:
        user = reddit.redditor(username)

        for index, submission in enumerate(
            user.submissions.new(limit=None), 1
        ):
            posts.append(submission)

        d = []
        for submission in posts:
            d.append(
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
    df = pd.DataFrame(d)
    # df = df[columns]
    return df
