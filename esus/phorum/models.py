from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

#from esus.phorum.access import *

# Define magic TableAccess constants
ACCESS_DICT = {
    "read" : {
        "code" : 1,
        "name" : _("Read"),
    },
    "write" : {
        "code" : 2,
        "name" : _("Write"),
    },
    "delete" : {
        "code" : 4,
        "name" : _("Delete"),
    }
}

ACCESS_TYPES = tuple([
    (ACCESS_DICT[right]['code'], ACCESS_DICT[right]["name"]) for right in ACCESS_DICT
])


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

class TableAccessManager(object):
    def __init__(self, rights):
        self.rights = rights

    def can_delete(self):
        return self.rights & 4

    def can_read(self):
        return self.rights & 1

    def can_write(self):
        return self.rights & 2

    @classmethod
    def compute_named_access(cls, names):
        return sum([
            ACCESS_DICT[val]['code'] for val in names
        ])

    @classmethod
    def get_default_access(cls):
        return cls.compute_named_access([
            "read",
            "write",
        ])

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

    def add_user_access(self, **kwargs):
        return TableAccess.objects.create(
            table = self,
            **kwargs
        )

    def get_special_accesses(self):
#        return User.tableaccess_set.filter(
#            table = self,
#            access_type = access_type
#        ).order_by('name')
        return TableAccess.objects.filter(table__exact=self).all().select_related()

class TableAccess(models.Model):
    table = models.ForeignKey(Table)
    user = models.ForeignKey(User)
    access_type = models.IntegerField(default=TableAccessManager.get_default_access())

    unique_together = (("table", "user"),)

    def can_read(self):
        return TableAccessManager(self.access_type).can_read()

    def can_write(self):
        return TableAccessManager(self.access_type).can_write()

    def can_delete(self):
        return TableAccessManager(self.access_type).can_delete()

class Comment(models.Model):
    """
    Comment from author inside table of any type.
    """
    author = models.ForeignKey(User)
    table = models.ForeignKey(Table)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
#    deleted = models.BooleanField(default=False)

