from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from esus.phorum.access import TableAccessManager


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

    def get_rights_for_user(self, user):
        try:
            return TableAccess.objects.get(table=self, user=user).access_type
        except TableAccess.DoesNotExist:
            return TableAccessManager.get_default_access()



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

