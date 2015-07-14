django-teamgroups
===================

django-teamgroups is a simple Django app to enable sites to have teams of users.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "teamgroups" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'teamgroups',
    )

2. Include the teamgroups URLconf in your project urls.py like this::

    url(r'^teamgroups/', include('teamgroups.urls')),

3. Run `python manage.py migrate` to create the teamgroups models.
