from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

BAD_WORDS = ['редиска', 'плохой', 'нехороший']  

@register.filter(name='censor')
@stringfilter
def censor(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Фильтр 'censor' применяется только к строке, получен {type(value)}")
    
    result = value
    for word in BAD_WORDS:
        # Для слова в нижнем регистре
        result = result.replace(word.lower(), word[0] + '*' * (len(word) - 1))
        # Для слова с заглавной первой буквой
        result = result.replace(word.capitalize(), word[0].upper() + '*' * (len(word) - 1))
    return result