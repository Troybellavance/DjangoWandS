from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import EmailingPreferencesForm
from .models import EmailingPreferences

class EmailingPreferencesUpdateView(SuccessMessageMixin, UpdateView):
    form_class = EmailingPreferencesForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = 'Your email preferences were updated.'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/login/?next=/settings/email/")
        return super(EmailingPreferencesUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EmailingPreferencesUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Emailing Preferences Settings'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = EmailingPreferences.objects.get_or_create(user=user) #getting a ForeignKey would be different
        return obj
