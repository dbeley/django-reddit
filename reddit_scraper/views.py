from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import PostComments, UserComments, UserPosts
import pandas as pd
import time

from .tasks import (
    extract_comments_post_praw,
    extract_comments_user_praw,
    extract_comments_user_psaw,
    extract_posts_user_praw,
    extract_posts_user_psaw,
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

    # if a GET (or any other method) we'll create a blank form
    else:
        formpostcomments = PostComments()
        formusercomments = UserComments()
        formuserposts = UserPosts()
    return render(
        request,
        "reddit_scraper/reddit_scraper.html",
        {
            "formpostcomments": formpostcomments,
            "formusercomments": formusercomments,
            "formuserposts": formuserposts,
        },
    )


def fl_redirect(request):
    try:
        url = retrieve_last_FL.delay()
        while url.state not in ("SUCCESS", "FAILURE"):
            time.sleep(0.5)
        return redirect(url.get())
    except Exception as e:
        return HttpResponseNotFound(e)
