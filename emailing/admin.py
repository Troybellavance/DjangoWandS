from django.contrib import admin

from .models import EmailingPreferences

class EmailingPreferencesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_subscribed', 'mailchimp_message', 'timestamp', 'updated']
    class Meta:
        model = EmailingPreferences
        fields = ['user', 'subscribed', 'mailchimp_message', 'mailchimp_subscribed', 'timestamp', 'updated']

admin.site.register(EmailingPreferences, EmailingPreferencesAdmin)
