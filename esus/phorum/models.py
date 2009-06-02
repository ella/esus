from django.db import models

from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)


    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name
