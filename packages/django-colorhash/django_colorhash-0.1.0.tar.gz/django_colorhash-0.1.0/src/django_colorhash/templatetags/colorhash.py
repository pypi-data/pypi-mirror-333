from colorhash import ColorHash
from django import template

register = template.Library()


@register.filter
def colorhash_hex(
    value,
    lightness=(0.35, 0.5, 0.65),
    saturation=(0.35, 0.5, 0.65),
    min_h=None,
    max_h=None,
) -> str:
    return ColorHash(value, lightness, saturation, min_h, max_h).hex
