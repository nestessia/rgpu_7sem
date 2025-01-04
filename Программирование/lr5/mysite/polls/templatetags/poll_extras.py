from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def sum(value, arg):
    """
    Суммирует значения указанного поля для всех объектов в queryset
    Использование: {{ queryset|sum:'field_name' }}
    """
    try:
        return sum(float(getattr(obj, arg, 0)) for obj in value)
    except (ValueError, TypeError, AttributeError):
        return 0 