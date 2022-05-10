from django import template
import datetime

register = template.Library()


def month_word(month):
    if month == 1:
        return 'Января'
    elif month == 2:
        return 'Февраля'
    elif month == 3:
        return 'Марта'
    elif month == 4:
        return 'Апреля'
    elif month == 5:
        return 'Мая'
    elif month == 6:
        return 'Июня'
    elif month == 7:
        return 'Июля'
    elif month == 8:
        return 'Августа'
    elif month == 9:
        return 'Сентября'
    elif month == 10:
        return 'Октября'
    elif month == 11:
        return 'Ноября'
    elif month == 12:
        return 'Декабря'
    return month

register.filter('month_word', month_word)