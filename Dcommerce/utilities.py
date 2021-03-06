import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance, new_slug=None):
    """
    Generator for a Django project to make a unique order id for an order_id field.
    """
    order_id_new = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id_new).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_id_new

def slug_generator(instance, new_slug=None):
    """
    Django project slug generator that assumes the instance
    has a model with at least a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return slug_generator(instance, new_slug=new_slug)
    return slug
