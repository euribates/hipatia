from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Texto a buscar', max_length=180)
