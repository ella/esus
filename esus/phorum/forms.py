from django import forms

class TableCreationForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea())

class ArticleCreationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

