from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PostComments, UserComments, UserPosts
from .reddit_scraper import (
    extract_comments_post,
    extract_comments_user,
    extract_posts_user,
    retrieve_last_FL,
)
import django_tables2 as tables


def index(request):
    return render(request, "reddit_scraper/index.html")


# Create your views here.
def reddit_scraper(request):
    if request.method == "POST":
        if "formpostcomments" in request.POST:
            try:
                formpostcomments = PostComments(request.POST)
            except Exception as e:
                print(e)
                return HttpResponse(content=e, status=400)
            if formpostcomments.is_valid():
                response = HttpResponse(content_type="text/plain")
                content = extract_comments_post(
                    formpostcomments.cleaned_data["post_urls"],
                )
                if formpostcomments.cleaned_data["export_format"] == "csv":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename=post_comments.csv"
                    content.to_csv(response, index=False, sep="\t")
                elif formpostcomments.cleaned_data["export_format"] == "xlsx":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename=post_comments.xlsx"
                    content.to_excel(response, index=False)
                return response
        elif "formusercomments" in request.POST:
            try:
                formusercomments = UserComments(request.POST)
            except Exception as e:
                print(e)
                return HttpResponse(content=e, status=400)
            if formusercomments.is_valid():
                response = HttpResponse(content_type="text/plain")
                content = extract_comments_user(
                    formusercomments.cleaned_data["username"],
                )
                if formusercomments.cleaned_data["export_format"] == "csv":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename={formusercomments.cleaned_data['username']}_user_comments.csv"
                    content.to_csv(response, index=False, sep="\t")
                elif formusercomments.cleaned_data["export_format"] == "xlsx":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename={formusercomments.cleaned_data['username']}_user_comments.xlsx"
                    content.to_excel(response, index=False)
                return response
        elif "formuserposts" in request.POST:
            try:
                formuserposts = UserPosts(request.POST)
            except Exception as e:
                print(e)
                return HttpResponse(content=e, status=400)
            if formuserposts.is_valid():
                response = HttpResponse(content_type="text/plain")
                content = extract_posts_user(
                    formuserposts.cleaned_data["username"],
                )
                if formuserposts.cleaned_data["export_format"] == "csv":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename={formuserposts.cleaned_data['username']}_user_posts.csv"
                    content.to_csv(response, index=False, sep="\t")
                elif formuserposts.cleaned_data["export_format"] == "xlsx":
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename={formuserposts.cleaned_data['username']}_user_posts.xlsx"
                    content.to_excel(response, index=False)
                return response

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
        url = retrieve_last_FL()
        return redirect(url)
    except Exception as e:
        print(e)
        return HttpResponse(content=e, status=400)
