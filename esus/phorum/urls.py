from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('esus.phorum.views',
    url(r'^categories/$', 'categories', name="esus-phorum-categories"),
    url(r'^category/(?P<slug>\w*)$', 'category_list', name="esus-phorum-category-list"),
    url(r'^$', 'root', name="esus-phorum-root"),
)

