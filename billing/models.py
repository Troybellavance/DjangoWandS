from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

import stripe
stripe.api_key = "sk_test_niKU6xKa1ICCmh61JOLqkqft"

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
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    # customer_id in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def billing_charge(self, order_obj, card=None):
        return ChargeOrder.objects.create_charge(self, order_obj, card)

    def get_cards(self):
        return self.creditcard_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):
        creditcard_qs = self.get_cards()
        return creditcard_qs.exists()

    @property
    def default_card(self):
        creditcards = self.get_cards().filter(active=True, default=True)
        if creditcards.exists():
            return creditcards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

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
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new_stripe(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_stripe_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_stripe_card.save()
            print(new_stripe_card)
            return new_stripe_card
        return None


class CreditCard(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile)
    stripe_id               = models.CharField(max_length=100)
    brand                   = models.CharField(max_length=100, null=True, blank=True)
    country                 = models.CharField(max_length=30, null=True, blank=True)
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

class ChargeManager(models.Manager):
    def create_charge(self, billing_profile, order_obj, card=None): # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.creditcard_set.filter(default=True) # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"

        charge = stripe.Charge.create(
              amount = int(order_obj.total * 100),
              currency = "usd",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
            )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = charge.id,
                paid = charge.paid,
                refunded = charge.refunded,
                outcome = charge.outcome,
                outcome_type = charge.outcome['type'],
                seller_message = charge.outcome.get('seller_message'),
                risk_level = charge.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message

class ChargeOrder(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile)
    stripe_id               = models.CharField(max_length=100)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=100, null=True, blank=True)
    seller_message          = models.CharField(max_length=160, null=True, blank=True)
    risk_level              = models.CharField(max_length=100, null=True, blank=True)

    objects = ChargeManager()
