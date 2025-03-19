__version__ = '0.17'

# set default_app_config when using django earlier than 3.2
try:
    import django

    if django.VERSION < (3, 2):
        default_app_config = 'dkron.apps.DkronConfig'
except ImportError:
    pass
