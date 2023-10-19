from django import template
from tantrakazan import settings

register = template.Library()


@register.inclusion_tag('feedback/star_rating.html')
def rating(rat=4):
    print(rat)
    int_rating = int(rat)
    return {'rating': range(int_rating)}
