from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('esus.phorum.views',
    url(r'^categories/$', 'categories', name="esus-phorum-categories"),
    url(r'^category/(?P<category>[\w-]+)$', 'category', name="esus-phorum-category"),
    url(r'^category/(?P<category>[\w-]+)/tables/create/$', 'table_create', name="esus-phorum-table-create"),
    url(r'^category/(?P<category>[\w-]+)/table/(?P<table>[\w-]+)/$', 'table', name="esus-phorum-table"),
    url(r'^category/(?P<category>[\w-]+)/table/(?P<table>[\w-]+)/settings/access/$', 'table_settings_access', name="esus-phorum-table-settings-access"),
    url(r'^markup/', include('djangomarkup.urls')),
    url(r'^$', 'root', name="esus-phorum-root"),
)

