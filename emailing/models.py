from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

class EmailingPreferences(models.Model):
    user               = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed         = models.BooleanField(default=True)
    mailchimp_message  = models.TextField(null=True, blank=True)
    timestamp          = models.DateTimeField(auto_now_add=True)
    update             = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def emailing_pref_update_reciever(sender, instance, created, *args, **kwargs):
    if created:
        pass
        print("User added to mail.")

post_save.connect(emailing_pref_update_reciever, sender=EmailingPreferences)


def make_emailing_pref_reciever(sender, instance, created, *args, **kwargs):
    if created:
        EmailingPreferences.objects.get_or_create(user=instance)

post_save.connect(make_emailing_pref_reciever, sender=settings.AUTH_USER_MODEL)
