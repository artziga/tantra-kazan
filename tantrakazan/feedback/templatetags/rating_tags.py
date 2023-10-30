from django import template
from tantrakazan import settings

register = template.Library()


@register.inclusion_tag('feedback/star_rating.html')
def rating(rat=4):
    if rat:
        int_rating = int(rat)
        return {'stars': range(int_rating),
                'o_stars': range(5-int_rating)
                }


@register.simple_tag()
def rating_class(rat):
    ratings = {
        0.5: 'star-half',
        1: 'star-one',
        1.5: 'star-one-half',
        2: 'star-two',
        2.5: 'star-two-half',
        3: 'star-three',
        3.5: 'star-three-half',
        4: 'star-four',
        4.5: 'star-four-half',
        5: 'star-five',
    }
    if rat:
        rounded_rating = round(rat * 2) / 2
        return ratings[rounded_rating]
    else:
        return 'star-null'
