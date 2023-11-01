from django import template

register = template.Library()


@register.filter
def years_suffix(value):
    if value % 10 == 1 and value % 100 != 11:
        suffix = "год"
    elif value % 10 in [2, 3, 4] and value % 100 not in [12, 13, 14]:
        suffix = "года"
    else:
        suffix = "лет"

    return suffix


@register.filter
def format_years(value):
    suffix = years_suffix(value)
    return f"{value} {suffix}"
