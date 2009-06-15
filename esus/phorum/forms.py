from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from djangomarkup.fields import RichTextField
from esus.phorum.models import Comment

__all__ = ("TableCreationForm", "CommentCreationForm", "CommentControlForm")

# MutlipleSubmit snippet from http://www.djangosnippets.org/snippets/951s/
class SubmitButton(forms.Widget):
    """
    A widget that handles a submit button.
    """
    def __init__(self, name, value, label, attrs):
        self.name, self.value, self.label = name, value, label
        self.attrs = attrs

    def __unicode__(self):
        final_attrs = self.build_attrs(
            self.attrs,
            type="submit",
            name=self.name,
            value=self.value,
            )
        return mark_safe(u'<button%s>%s</button>' % (
            forms.widgets.flatatt(final_attrs),
            self.label,
            ))

class MultipleSubmitButton(forms.Select):
    """
    A widget that handles a list of submit buttons.
    """
    def __init__(self, attrs={}, choices=()):
        self.attrs = attrs
        self.choices = choices

    def __iter__(self):
        for value, label in self.choices:
            yield SubmitButton(self.name, value, label, self.attrs.copy())

    def __unicode__(self):
        return '<button type="submit" />'

    def render(self, name, value, attrs=None, choices=()):
        """Outputs a <ul> for this set of submit buttons."""
        self.name = name
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join(
            [u'<li>%s</li>' % force_unicode(w) for w in self],
            ))
    def value_from_datadict(self, data, files, name):
        """
        returns the value of the widget: IE posts inner HTML of the button
        instead of the value.
        """
        value = data.get(name, None)
        if value in dict(self.choices):
            return value
        else:
            inside_out_choices = dict([(v, k) for (k, v) in self.choices])
            if value in inside_out_choices:
                return inside_out_choices[value]
        return None


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



