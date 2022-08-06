from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import (
    SearchComments,
    SearchPosts,
)
import pandas as pd
import time
from datetime import datetime

from .tasks import (
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


def reddit_scraper(request):
    if request.method == "POST":
        if "formposts" in request.POST:
            try:
                formposts = SearchPosts(request.POST)
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
                        filename=f"posts_{datetime.timestamp(datetime.now())}",
                    )
            except Exception as e:
                return HttpResponseNotFound(e)
        elif "formcomments" in request.POST:
            try:
                formcomments = SearchComments(request.POST)
                data = formcomments.cleaned_data
                if formcomments.is_valid():
                    response = HttpResponse(content_type="text/plain")
                    if data["api"] == "pushshift":
                        if data["url"]:
                            content = extract_comments_post_praw.delay(data["url"])
                        else:
                            content = extract_comments_psaw.delay(
                                data["username"],
                                data["subreddit"],
                                data["terms"],
                            )
                    while content.state not in ("SUCCESS", "FAILURE"):
                        time.sleep(0.5)
                    content = pd.read_json(content.get())
                    filename = f"comments_"
                    if data["url"]:
                        filename += "url_"
                    elif data["username"]:
                        filename += f"{data['username']}_"
                    elif data["subreddit"]:
                        filename += f"{data['subreddit']}_"
                    filename += f"{datetime.timestamp(datetime.now())}"

                    return format_content(
                        export_format=data["export_format"],
                        response=response,
                        content=content,
                        filename=filename,
                    )
            except Exception as e:
                return HttpResponseNotFound(e)

    # if a GET (or any other method) we'll create a blank form
    else:
        formcomments = SearchComments()
        formposts = SearchPosts()
    return render(
        request,
        "reddit_scraper/reddit_scraper.html",
        {
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
