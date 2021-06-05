from django import template
import requests
import decimal

from requests.models import DecodeError
register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price

