from django import template
from better_profanity import profanity

register = template.Library()


@register.filter(name='censor')
#
# для фильтрации английских ругательств используем библиотеку profanity
# для фильтрации русского мата можно использовать аналогичные библиотеки, например, https://github.com/PixxxeL/djantimat
#
def censor(value):
    censored_text = profanity.censor(value)
    return censored_text
