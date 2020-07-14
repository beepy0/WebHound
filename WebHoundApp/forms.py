from django import forms


class QueryForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username Trace', 'class': 'form-control form-placeholder', 'id': 'query'}
        )
    )
