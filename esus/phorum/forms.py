from django.forms.util import ValidationError
from django import forms
from django.contrib.auth.models import User

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

class CommaSeparatedUsernamesField(forms.CharField):
    def clean(self, value):
        # we must also be valid as CharField
        value = super(CommaSeparatedUsernamesField, self).clean(value)

        if value:
            usernames = value.split(",")
            for username in usernames:
                try:
                    User.objects.get(username=username.strip())
                except User.DoesNotExists:
                    raise ValidationError(u"Given username %s not found" % username)
        return value

class CommentControlForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class TableAccessForm(forms.Form):
    is_public = forms.BooleanField()
    can_read = CommaSeparatedUsernamesField(required=False)
    can_write = CommaSeparatedUsernamesField(required=False)
    cannot_write = CommaSeparatedUsernamesField(required=False)
    cannot_read = CommaSeparatedUsernamesField(required=False)

