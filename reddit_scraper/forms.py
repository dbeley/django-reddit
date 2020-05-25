from django import forms


class PostComments(forms.Form):
    post_urls = forms.CharField(
        label="Reddit posts urls (separated by comma)", max_length=5000
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(label="API to query", choices=(("reddit", "reddit API"),))


class UserComments(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(
        label="API to query",
        choices=(("reddit", "reddit API"), ("pushshift", "pushshift API"),),
    )


class UserPosts(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )

    api = forms.ChoiceField(
        label="API to query",
        choices=(("reddit", "reddit API"), ("pushshift", "pushshift API"),),
    )
