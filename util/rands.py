from random import SystemRandom
import string
from django.utils.text import slugify




def random_string(len):
    return ''.join(
        SystemRandom().choices(
        string.ascii_lowercase+string.digits,
        k= len,
        )
    )

def slugfy_new(text, len = 5):

    slug = slugify(text+'-'+random_string(len))
    return slug
