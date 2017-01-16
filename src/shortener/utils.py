import random
import string
from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)


def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    """randomly generate shortcode"""
    # new code = ''
    # for _ in range(size): # _ just a placeholder, shorthand method used often
    #         new_code += random.choice(chars)
    # return new_code
    return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode(instance, size=SHORTCODE_MIN):
    """ """

    new_code = code_generator(size=size)
    #cannot import from models.py (circular import problem)
    #another way of
    # print(instance)
    # print(instance.__class__)
    # print(instance.__class__.__name__)
    #importing the class without importing the class
    Klass = instance.__class__
    #qs = query set
    qs_exists = Klass.objects.filter(shortcode=new_code).exists()
    if qs_exists:
        return create_shortcode(size=size)
    return new_code
