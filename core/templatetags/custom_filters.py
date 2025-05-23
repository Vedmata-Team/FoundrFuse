from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='getattribute')
def getattribute(obj, attr):
    """
    Gets an attribute of an object dynamically from a string name.
    Used in the PDF export template to get field values.
    """
    if hasattr(obj, str(attr)):
        try:
            # Handle foreign key relationships
            if '__' in attr:
                attrs = attr.split('__')
                result = obj
                for a in attrs:
                    result = getattr(result, a)
                return result
            return getattr(obj, attr)
        except:
            return ""
    elif hasattr(obj, 'get'):
        try:
            return obj.get(attr)
        except:
            return ""
    else:
        return ""