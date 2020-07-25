from django import forms


class QueryForm(forms.Form):
    query = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Trace username',
                'class': 'form-control form-placeholder',
                'id': 'query'
            }
        )
    )
