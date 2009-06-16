from django.forms.util import ValidationError
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangomarkup.fields import RichTextField
from esus.phorum.models import Comment

__all__ = (
    "TableCreationForm", "CommentCreationForm", "CommentControlForm",
    "TableAccessForm", "PublicTableAccessForm",
)

class UserField(forms.CharField):
    def clean(self, value):
        if value:
            try:
                value = User.objects.get(username=value.strip()).username
            except User.DoesNotExist:
                raise ValidationError(u"Username %s not found" % value)
        return value

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

class CommentControlForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class AccessForm(forms.Form):
    can_read = forms.BooleanField(label=_(u"Can read?"), required=False,
        help_text=_(u"Can see comments in this table"))
    can_write = forms.BooleanField(label=_(u"Can write?"), required=False,
        help_text=_(u"Can write new comments to this table"))
    can_delete = forms.BooleanField(label=_(u"Can delete?"), required=False,
        help_text=_(u"Can hide comments from this table"))

    def get_access_names(self):
        return [
            name for name in ["read", "write", "delete"]
            if self.cleaned_data["can_%s" % name]
        ]

class TableAccessForm(AccessForm):
#    username = UserField(widget=widgets.TextInput(attrs={"disabled" : "disabled"}))
    username = UserField(widget=widgets.TextInput())
    
class PublicTableAccessForm(AccessForm):
    is_public = forms.BooleanField(label=_(u"Is public?"), help_text=_(u"If table is public, it's content is available for Google and friends"))

class NewUserForm(forms.Form):
    username = UserField(label=_(u"Username"))
