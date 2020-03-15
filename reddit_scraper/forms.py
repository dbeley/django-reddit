from django import forms


class PostComments(forms.Form):
    post_urls = forms.CharField(
        label="Reddit posts urls (separated by comma)", max_length=200
    )


class UserComments(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=200
    )


class UserPosts(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=200
    )
