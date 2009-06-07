from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    """
    Category represents "a group of Tables". They can be nested inside each other.
    Categories with no parent are considered "root" ones.
    """
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    parent = models.ForeignKey('self', default=None, blank=True, null=True)

    unique_together = (("slug", "parent"),)


    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    def get_nested_categories(self):
        return self.category_set.all().order_by('name')

class Table(models.Model):
    """
    Table is "one discussion".
    """
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = models.TextField(_('Description'))
    creation_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category)

    unique_together = (("slug", "category"),)


    def __unicode__(self):
        return self.name


class Comment(models.Model):
    """
    Comment from author inside table of any type.
    """
    author = models.ForeignKey(User)
    table = models.ForeignKey(Table)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
