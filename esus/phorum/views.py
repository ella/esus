from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic.simple import direct_to_template

from esus.phorum.models import Category, Table, Comment
from esus.phorum.forms import TableCreationForm, CommentCreationForm
from esus.phorum.access import AccessManager

def root(request):
    """
    Root of esus. Probably, a dashboard will be here; for now, we're just redirecting.
    Feel free to override this if you want to display "welcome" page.
    """
    return HttpResponseRedirect(reverse("esus-phorum-categories"))

@login_required
def categories(request):
    categories = Category.objects.all().order_by('name')

    return direct_to_template(request, "esus/categories.html", {
        'categories' : categories,
    })

@login_required
def category(request, category):
    category = get_object_or_404(Category, slug=category)
    tables = category.table_set.order_by('-name')

    return direct_to_template(request, "esus/category.html", {
        "category" : category,
        "tables" : tables,
    })

@login_required
def table_create(request, category):
    category = get_object_or_404(Category, slug=category)
    if request.method == "POST":
        form = TableCreationForm(request.POST)
        if form.is_valid():
            table = category.add_table(
                owner = request.user,
                name = form.cleaned_data['name'],
                slug = slugify(form.cleaned_data['name']),
                description = form.cleaned_data['description'],
            )
            return HttpResponseRedirect(reverse("esus-phorum-table", kwargs={
                "category" : category.slug,
                "table" : table.slug,
            }))
    else:
        form = TableCreationForm()
    return direct_to_template(request, "esus/table_create.html", {
        "category" : category,
        "form" : form,
    })

@login_required
def table(request, category, table):
    category = get_object_or_404(Category, slug=category)
    table = get_object_or_404(Table, slug=table)

    access_manager = AccessManager(context={
        "user" : request.user,
        "table" : table,
        "category" : category,
    })

    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            # posting new message
            if not access_manager.has_comment_create():
                return HttpResponseForbidden()
            table.add_comment(
                text = form.cleaned_data['text'],
                author = request.user,
            )
            form = CommentCreationForm()
    else:
        form = CommentCreationForm()

    comments = Comment.objects.filter(table=table).order_by('-date')

    return direct_to_template(request, "esus/table.html", {
        "category" : category,
        "table" : table,
        "form" : form,
        "comments" : comments,
        'access' : access_manager,
    })
