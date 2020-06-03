from django import forms


class PostComments(forms.Form):
    post_urls = forms.CharField(
        label="Reddit posts urls (separated by comma)", max_length=5000
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(label="API to query", choices=(("reddit", "Reddit API"),))


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
        choices=(("reddit", "Reddit API"), ("pushshift", "Pushshift API"),),
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
        choices=(("reddit", "Reddit API"), ("pushshift", "Pushshift API"),),
    )


class SubredditPosts(forms.Form):
    terms = forms.CharField(
        label="Search terms (separated by comma, can be empty)", max_length=500
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma, can be empty)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )


class SubredditComments(forms.Form):
    terms = forms.CharField(
        label="Search terms (separated by comma, can be empty)", max_length=500
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma, can be empty)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )


class SearchComments(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma, can be empty)", max_length=500
    )
    terms = forms.CharField(
        label="Search terms (separated by comma, can be empty)", max_length=500
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma, can be empty)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )


class SearchPosts(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (separated by comma, can be empty)", max_length=500
    )
    terms = forms.CharField(
        label="Search terms (separated by comma, can be empty)", max_length=500
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma, can be empty)", max_length=500
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("csv", "Export in csv"), ("xlsx", "Export in xlsx")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )
