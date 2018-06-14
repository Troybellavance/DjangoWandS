from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        #logged in user checkout & remembers payment 'stuff'
        if user.is_authenticated():
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        #guest user checkout & automatically reloads payment 'stuff'
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email




def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)

#Can use as plain Profile

#Could have customer_id in stripe, paypal, braintree, etc as the BillingProfile
# def billing_profile_created_receiver(sender, instasnce, created, *args, **kwargs):
#     if created:
#         print("Send to payment service (stripe/braintree/etc).")
#         instance.customer_id = newID
#         instance.save()
