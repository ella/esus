from django import forms

from djangomarkup.fields import RichTextField
from esus.phorum.models import Comment

__all__ = ("TableCreationForm", "CommentCreationForm", "CommentControlForm")

class TableCreationForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea())

class CommentCreationForm(forms.Form):
    text = RichTextField(
        instance=None,
        model = Comment,
        syntax_processor_name="czechtile",
        field_name="text",
    )

#FIXME: Hacky, see if we cannot have dynamic forms instead
#def get_article_form_class(instance=None):
#return ArticleForm

class CommentControlForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)


