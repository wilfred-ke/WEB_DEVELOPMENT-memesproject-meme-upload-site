from django import template

register = template.Library()


@register.filter
def is_image(file_url):
    if file_url is None:
        return False
    return file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))


@register.filter
def is_video(file_url):
    if file_url is None:
        return False
    return file_url.lower().endswith(('.mp4', '.avi', '.mov', '.webm', '.mkv', '.ogg', '.3gp'))
