from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic.simple import direct_to_template
from django.forms.formsets import formset_factory
#from django.utils.translation import ugettext_lazy as _

from esus.phorum.models import Category, Table, Comment, TableAccess, TableAccessManager
from esus.phorum.forms import (TableCreationForm,
    CommentCreationForm, CommentControlForm,
    TableAccessForm, PublicTableAccessForm,
    NewUserForm
)
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

    comment_forms = None
    form = None

    if request.method == "POST":
        # TODO: Abstract this logic into something more sensible, some kind of
        # action dispatcher would be nice
        if request.POST.has_key(u"Odeslat"):
            
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                # posting new message
                if not access_manager.has_comment_create():
                    return HttpResponseForbidden()
                table.add_comment(
                    text = form.cleaned_data['text'],
                    author = request.user,
                )
                #TODO: Redirect to self avoid multiple posts
                form = CommentCreationForm()
        elif request.POST.has_key(u'control-action') \
            and request.POST[u'control-action']:
            comment_forms = formset_factory(CommentControlForm, can_delete=True)(request.POST)
            if comment_forms.is_valid():
                for comm_form in comment_forms.deleted_forms:
                    comment = Comment.objects.get(pk=comm_form.cleaned_data['pk'])
                    if access_manager.has_comment_delete(comment=comment):
                        comment.delete()
                    else:
                        #TODO: Display message or pass silently?
                        pass
            comment_forms = None

    comments = Comment.objects.filter(table=table).order_by('-date')

    if not comment_forms:
        comment_forms = formset_factory(CommentControlForm, can_delete=True)(
            initial = [
                {'pk' : comment.pk} for comment in comments
            ]
        )
    if not form:
        form = CommentCreationForm()

    return direct_to_template(request, "esus/table.html", {
        "category" : category,
        "table" : table,
        "form" : form,
        "formset" : comment_forms,
        "comments" : zip(comments, comment_forms.forms),
        'access' : access_manager,
    })

@login_required
def table_settings_access(request, category, table):
    category = get_object_or_404(Category, slug=category)
    table = get_object_or_404(Table, slug=table)

    access_manager = AccessManager(context={
        "user" : request.user,
        "table" : table,
        "category" : category,
    })
    if not access_manager.has_table_access_modify():
        return HttpResponseForbidden()

    new_user_form = None
    users_form = None

    if request.method == "POST":
        # found a better way to dispatch, as for table
        if request.POST.has_key(u"new_user_form"):
            new_user_form = NewUserForm(request.POST)
            if new_user_form.is_valid():
                #FIXME
                user = User.objects.get(username=new_user_form.cleaned_data['username'])
                if len(TableAccess.objects.filter(table=table, user=user)) == 0:

                    table.add_user_access(
                        user = user,
                    )
                    new_user_form = None
        elif request.POST.has_key(u"users_form"):
            users_form = formset_factory(TableAccessForm, can_delete=True, extra=0)(request.POST)
            if users_form.is_valid():
                try:
                    for access_form in users_form.deleted_forms:
                        TableAccess.objects.get(
                            user = User.objects.get(username=access_form.cleaned_data['username']),
                            table = table
                        ).delete()
                    for access_form in users_form.forms:
                        access = TableAccess.objects.get(
                            user = User.objects.get(username=access_form.cleaned_data['username']),
                            table = table
                        )
                        access.access_type = TableAccessManager.compute_named_access(
                            access_form.get_access_names()
                        )
                        access.save()

                except (TableAccess.DoesNotExist, User.DoesNotExist):
                    raise ValueError(access_form.cleaned_data['username'])
                users_form = None



    public_form = PublicTableAccessForm({
        'is_public' : table.is_public,
        'can_read' : True,
        'can_write' : True,
    })

    users_form = formset_factory(TableAccessForm, can_delete=True, extra=0)(
        initial = [
            {
                "username" : access.user.username,
                "can_read" : access.can_read(),
                "can_write" : access.can_write(),
                "can_delete" : access.can_delete(),

            }
            for access in table.get_special_accesses()
        ]
    )

    if not new_user_form:
        new_user_form = NewUserForm()

    return direct_to_template(request, "esus/table_access.html", {
        "category" : category,
        "table" : table,
        "public_form" : public_form,
        "users_form" : users_form,
        "new_user_form" : new_user_form,
        'access' : access_manager,
    })
