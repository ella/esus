from django.core.urlresolvers import reverse
#from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.views.generic.simple import direct_to_template

from esus.phorum.models import Category

def root(request):
    """
    Root of esus. Probably, a dashboard will be here; for now, we're just redirecting.
    Feel free to override this if you want to display "welcome" page.
    """
    return HttpResponseRedirect(reverse("esus-phorum-categories"))

def categories(request):
    categories = Category.objects.all().order_by('name')
#    raise ValueError(request.user.is_authenticated())
    return direct_to_template(request, "esus/categories.html", {
        'categories' : categories,
    })

def category_list(request, slug=None):
    """
    """
    pass
#    if name:
#        category = get_object_or_404(Category, slug=slug)
#    else:
#        category = Category.objecs.all().order_by('name')
#
#    return direct_to_template(request, "esus/category", {
#    })
