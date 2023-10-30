from django import template

register = template.Library()


@register.inclusion_tag('feedback/like_button.html')
def like_button(specialist_id, content_type_id, is_bookmarked):
    return {
        'specialist': specialist_id,
        'content_type': content_type_id,
        'is_bookmarked': is_bookmarked
    }
