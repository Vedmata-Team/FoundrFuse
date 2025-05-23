from .models import SiteSettings

def site_settings(request):
    """
    Add site settings to the context of all templates.
    """
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except Exception:
        site_settings = None
    
    return {
        'site_settings': site_settings
    }