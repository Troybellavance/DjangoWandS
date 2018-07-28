from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

import stripe
stripe.api_key = "sk_test_lhe3uvwYErAh2ECdCfg6YD3C"

#Checks for user/guest status and saves payment information or reloads it for the guest user
class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated():
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
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
    customer_id = models.CharField(max_length=100, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

#Makes sure the customer doesn't have an ID already and that they have an email. No email means no stripe customer_id. Can generate new ids easily with pre_save.
def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
                email = instance.email,
        )
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)

#Can just be done through stripe, but putting the information in the backend to reduce api calls.

class CardManager(models.Manager):
    def add_new(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == "card":
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None


class CreditCard(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile)
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)

def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = CreditCard.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=CreditCard)
