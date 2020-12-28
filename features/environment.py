from django.conf import settings

from splinter import Browser


def django_ready(context):  # noqa: D103
    context.browser = Browser(getattr(settings, 'SPLINTER_BROWSER', 'django'))
    context.django = True
