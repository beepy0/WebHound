from django import forms


class QueryForm(forms.Form):
    query = forms.CharField(
        label='Trace:',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control form-placeholder',
                'id': 'query'
            }
        )
    )
