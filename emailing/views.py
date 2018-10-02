from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View

from .forms import EmailingPreferencesForm
from .mixins import CsrfExemptMixin
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

class MailchimpHookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
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
                status_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                status_subbed, mailchimp_subbed = (False, False)
            if status_subbed is not None and mailchimp_subbed is not None:
                qs = EmailingPreferences.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=status_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_message=str(data))
        return HttpResponse("Thanks!", status=200)
