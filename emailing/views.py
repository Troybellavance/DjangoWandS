from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import EmailingPreferencesForm
from .models import EmailingPreferences
from .utilities import MailchimpEmailing

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

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
        obj, created = EmailingPreferences.objects.get_or_create(user=user)
        return obj


def mailchimp_hook_view(request):
    data = request.POST
    list_id = data.get('data[list_id]')
    if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
        email = data.get('data[email]')
        hook_type = data.get('type')
        response_status, response = MailchimpEmailing().check_sub_status(email)
        sub_status = response['status']
        status_subbed = None
        mailchimp_subbed = None
        if sub_status == 'subscribed':
            qs = EmailingPreferences.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(subscribed=True, mailchimp_subscribed=False, str(data))
        elif sub_status == 'unsubscribed':
            qs = EmailingPreferences.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(subscribed=False, mailchimp_subscribed=False, str(data))
        if status_subbed and mailchimp_subbed:
            qs = EmailingPreferences.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(subscribed=status_subbed, mailchimp_subscribed=mailchimp_subbed, str(data))
    return
