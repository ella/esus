from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.simple import direct_to_template

def registration(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.message_set.create(message=u"Registration successfull. You can now log in.")
            return HttpResponseRedirect(reverse('user-login'))

    return direct_to_template(request, "registration/register.html", {
        'form' : form,
    })

def profile(request):
    return direct_to_template(request, "registration/profile.html")
