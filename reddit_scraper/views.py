from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import (
    PostComments,
    UserComments,
    UserPosts,
    SubredditComments,
    SubredditPosts,
    SearchComments,
    SearchPosts,
)
import pandas as pd
import time

from .tasks import (
    extract_comments_post_praw,
    extract_comments_user_praw,
    extract_comments_user_psaw,
    extract_posts_user_praw,
    extract_posts_user_psaw,
    extract_comments_subreddit_psaw,
    extract_posts_subreddit_psaw,
    extract_comments_psaw,
    extract_posts_psaw,
    retrieve_last_FL,
)
import django_tables2 as tables


def index(request):
    return render(request, "reddit_scraper/index.html")


def format_content(export_format, response, content, filename):
    if export_format == "xlsx":
        response["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
        content.to_excel(response, index=False)
    elif export_format == "csv":
        response["Content-Disposition"] = f"attachment; filename={filename}.csv"
        content.to_csv(response, index=False, sep="\t")
    return response


# Create your views here.
def reddit_scraper(request):
    if request.method == "POST":
        if "formpostcomments" in request.POST:
            try:
                formpostcomments = PostComments(request.POST)
                if formpostcomments.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    content = extract_comments_post_praw.delay(
                        formpostcomments.cleaned_data["post_urls"]
                    )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formpostcomments.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename="post_comments",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formusercomments" in request.POST:
            try:
                formusercomments = UserComments(request.POST)
                if formusercomments.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formusercomments.cleaned_data["api"] == "reddit":
                        content = extract_comments_user_praw.delay(
                            formusercomments.cleaned_data["username"]
                        )
                    elif formusercomments.cleaned_data["api"] == "pushshift":
                        content = extract_comments_user_psaw.delay(
                            formusercomments.cleaned_data["username"]
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formusercomments.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename=f"{formusercomments.cleaned_data['username']}_user_comments",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formuserposts" in request.POST:
            try:
                formuserposts = UserPosts(request.POST)
                if formuserposts.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formuserposts.cleaned_data["api"] == "reddit":
                        content = extract_posts_user_praw.delay(
                            formuserposts.cleaned_data["username"]
                        )
                    elif formuserposts.cleaned_data["api"] == "pushshift":
                        content = extract_posts_user_psaw.delay(
                            formuserposts.cleaned_data["username"]
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formuserposts.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename=f"{formuserposts.cleaned_data['username']}_user_posts",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formsubredditcomments" in request.POST:
            try:
                formsubredditcomments = SubredditComments(request.POST)
                if formsubredditcomments.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formsubredditcomments.cleaned_data["api"] == "pushshift":
                        content = extract_comments_subreddit_psaw.delay(
                            formsubredditcomments.cleaned_data["subreddit"],
                            formsubredditcomments.cleaned_data["terms"],
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formsubredditcomments.cleaned_data[
                            "export_format"
                        ],
                        response=response,
                        content=content,
                        filename=f"{formsubredditcomments.cleaned_data['subreddit']}_comments",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formsubredditposts" in request.POST:
            try:
                formsubredditposts = SubredditPosts(request.POST)
                if formsubredditposts.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formsubredditposts.cleaned_data["api"] == "pushshift":
                        content = extract_posts_subreddit_psaw.delay(
                            formsubredditcomments.cleaned_data["subreddit"],
                            formsubredditcomments.cleaned_data["terms"],
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formsubredditposts.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename=f"{formsubredditposts.cleaned_data['subreddit']}_posts",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formposts" in request.POST:
            try:
                formposts = SubredditPosts(request.POST)
                if formposts.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formposts.cleaned_data["api"] == "pushshift":
                        content = extract_posts_psaw.delay(
                            formposts.cleaned_data["username"],
                            formposts.cleaned_data["subreddit"],
                            formposts.cleaned_data["terms"],
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formposts.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename=f"{formposts.cleaned_data['subreddit']}_posts",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formcomments" in request.POST:
            try:
                formcomments = SubredditComments(request.POST)
                if formcomments.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if formcomments.cleaned_data["api"] == "pushshift":
                        content = extract_posts_psaw.delay(
                            formcomments.cleaned_data["username"],
                            formcomments.cleaned_data["subreddit"],
                            formcomments.cleaned_data["terms"],
                        )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    return format_content(
                        export_format=formcomments.cleaned_data["export_format"],
                        response=response,
                        content=content,
                        filename=f"{formcomments.cleaned_data['subreddit']}_comments",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)

    # if a GET (or any other method) we'll create a blank form
    else:
        formpostcomments = PostComments()
        formusercomments = UserComments()
        formuserposts = UserPosts()
        formsubredditcomments = SubredditComments()
        formsubredditposts = SubredditPosts()
        formcomments = SearchComments()
        formposts = SearchPosts()
    return render(
        request,
        "reddit_scraper/reddit_scraper.html",
        {
            "formpostcomments": formpostcomments,
            "formusercomments": formusercomments,
            "formuserposts": formuserposts,
            "formsubredditcomments": formsubredditcomments,
            "formsubredditposts": formsubredditposts,
            "formcomments": formcomments,
            "formposts": formposts,
        },
    )


def fl_redirect(request):
    try:
        url = retrieve_last_FL.delay()
        while url.state not in ("SUCCESS", "FAILURE"):
            time.sleep(0.5)
        return redirect(url.get().replace("www", "old") + "?sort=new")
    except Exception as e:
        return HttpResponseNotFound(e)
