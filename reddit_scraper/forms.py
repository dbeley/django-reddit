from django import forms


class SearchComments(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (use ! to negate, separated by comma)",
        max_length=500,
        required=False,
    )
    terms = forms.CharField(
        label="Search terms (separated by comma, use | for OR)",
        max_length=500,
        required=False,
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma)",
        max_length=500,
        required=False,
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("xlsx", "Export in xlsx"), ("csv", "Export in csv")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )


class SearchPosts(forms.Form):
    username = forms.CharField(
        label="Reddit usernames (use ! to negate, separated by comma)",
        max_length=500,
        required=False,
    )
    terms = forms.CharField(
        label="Search terms (separated by comma, use | for OR)",
        max_length=500,
        required=False,
    )
    subreddit = forms.CharField(
        label="Subreddit (separated by comma)",
        max_length=500,
        required=False,
    )
    url = forms.CharField(
        label="Post URL (will render above fields inactive)",
        max_length=500,
        required=False,
    )
    export_format = forms.ChoiceField(
        label="Export format",
        choices=(("xlsx", "Export in xlsx"), ("csv", "Export in csv")),
    )
    api = forms.ChoiceField(
        label="API to query", choices=(("pushshift", "Pushshift API"),)
    )
