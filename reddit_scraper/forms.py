from django import forms


class PostComments(forms.Form):
    post_urls = forms.CharField(
        label="Reddit posts urls (separated by comma)", max_length=5000
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )


class UserComments(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )


class UserPosts(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
