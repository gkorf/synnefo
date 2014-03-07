from synnefo_branding import branding_settings
from django.template.loader import render_to_string as django_render_to_string


def get_branding_dict(prepend=None):
    dct = {}
    for key in dir(branding_settings):
        if key == key.upper():
            newkey = key.lower()
            if prepend:
                newkey = '%s_%s' % (prepend, newkey)
            dct[newkey.upper()] = getattr(branding_settings, key)
    return dct


def brand_message(msg, **extra_args):
    params = get_branding_dict()
    params.update(extra_args)
    return msg % params


def render_to_string(template_name, dictionary=None, context_instance=None):
    if not dictionary:
        dictionary = {}
    if isinstance(dictionary, dict):
        newdict = get_branding_dict("BRANDING")
        newdict.update(dictionary)
    else:
        newdict = dictionary
    return django_render_to_string(template_name, newdict, context_instance)
