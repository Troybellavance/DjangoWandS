from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import EmailingPreferencesForm
from .models import EmailingPreferences

class EmailingPreferencesUpdateView(UpdateView):
    form_class = EmailingPreferencesForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'

    def get_context_data(self, *args, **kwargs):
        context = super(EmailingPreferencesUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Emailing Preferences Settings'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = EmailingPreferences.objects.get_or_create(user=user) #getting a ForeignKey would be different
        return obj
