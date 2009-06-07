from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.views.generic.simple import direct_to_template

from esus.phorum.models import Category, Table, Comment
from django.template.defaultfilters import slugify
from esus.phorum.forms import TableCreationForm, CommentCreationForm

def root(request):
    """
    Root of esus. Probably, a dashboard will be here; for now, we're just redirecting.
    Feel free to override this if you want to display "welcome" page.
    """
    return HttpResponseRedirect(reverse("esus-phorum-categories"))

def categories(request):
    categories = Category.objects.all().order_by('name')

    return direct_to_template(request, "esus/categories.html", {
        'categories' : categories,
    })

def category(request, category):
    category = get_object_or_404(Category, slug=category)
    tables = category.table_set.order_by('-name')

    return direct_to_template(request, "esus/category.html", {
        "category" : category,
        "tables" : tables,
    })

def table_create(request, category):
    category = get_object_or_404(Category, slug=category)
    if request.method == "POST":
        form = TableCreationForm(request.POST)
        if form.is_valid():
            table = Table.objects.create(
                category = category,
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

def table(request, category, table):
    category = get_object_or_404(Category, slug=category)
    table = get_object_or_404(Table, slug=table)

    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                table = table,
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
    })



