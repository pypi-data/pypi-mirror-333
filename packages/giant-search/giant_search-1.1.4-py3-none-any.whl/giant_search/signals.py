from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from giant_search.utils import register_for_search

DB_ENGINE = settings.DATABASES['default']['ENGINE']

db_backend = import_module(DB_ENGINE + ".base")


@receiver(connection_created, sender=db_backend.DatabaseWrapper)
def initial_connection_to_db(sender, **kwargs):
    # Get a list of all models that implement the SearchableMixin?
    for app in apps.all_models.values():
        for model in app.values():
            if hasattr(model, "is_searchable"):
                # We have search_fields, try to register the model.
                register_kwargs = {"model": model.get_search_queryset()}

                # If the model defines which fields should be searchable,
                #   pass them to the register() call.
                try:
                    search_fields = model.get_search_fields()
                    if search_fields:
                        register_kwargs["fields"] = search_fields
                except AttributeError:
                    pass

                # Now we register this Model with the kwargs built up from above.
                register_for_search(**register_kwargs)

    # Register Page Titles / PageContents
    try:
        from cms.models import Title
    except ImportError:
        from cms.models import PageContent
        # from cms.utils import get_current_site
        from cms.utils.i18n import get_public_languages

        # site = get_current_site()
        languages = get_public_languages(site_id=settings)
        register_for_search(PageContent.objects.filter(language__in=languages))
    else:
        register_for_search(
            Title.objects.filter(published=True, publisher_is_draft=False)
        )

