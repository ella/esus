from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

#from esus.phorum.access import *

ACCESS_TYPES = (
    ('RA', 'Can read'),
    ('WA', 'Can write'),
    ('RB', 'Cannot read'),
    ('WB', 'Cannot write'),
    ('CA', 'Co-admin'),
)

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
        permissions = (
            ("is_administrator", "Is an administrator of this section"),
        )

    def __unicode__(self):
        return self.name

    def get_nested_categories(self):
        return self.category_set.all().order_by('name')

    def add_table(self, **kwargs):
        return Table.objects.create(
            category = self,
            **kwargs
        )

class Table(models.Model):
    """
    Table is "one discussion".
    """
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = models.TextField(_('Description'))
    creation_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, name=_('Owner'))
#    deleted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    category = models.ForeignKey(Category)

    unique_together = (("slug", "category"),)

    class Meta:
        verbose_name_plural = _('Categories')
        permissions = (
            ("is_admin", "Is selected as an administrator of this table"),
            ("is_owner", "Is owner of this table"),
        )


    def __unicode__(self):
        return self.name


    def add_comment(self, **kwargs):
        return Comment.objects.create(
            table = self,
            **kwargs
        )
    def get_privileged_users(self, access_type):
#        return User.tableaccess_set.filter(
#            table = self,
#            access_type = access_type
#        ).order_by('name')
        acc = TableAccess.objects.filter(table__exact=self, access_type__exact=access_type).all().select_related()
        return [a.user for a in acc]

class TableAccess(models.Model):
    table = models.ForeignKey(Table)
    user = models.ForeignKey(User)
    access_type = models.CharField(max_length=2, choices=ACCESS_TYPES)

class Comment(models.Model):
    """
    Comment from author inside table of any type.
    """
    author = models.ForeignKey(User)
    table = models.ForeignKey(Table)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
#    deleted = models.BooleanField(default=False)

