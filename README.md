**OVERVIEW**

Djac is a double entry accounting app for Django. Included are the standalone accounts app, and many example views and templates.

**REQUIREMENTS**
    Djac uses:

- Django
- PostgreSQL
- South
- Django Debug Toolbar

PostgreSQL can usually be installed through your distro's package manager (though you can change the DB in settings.py to whatever you want). The Python dependencies are best installed through pip, as in:

`$ pip install psycopg2 south django-debug-toolbar`

I strongly recommend using virtualenv to create a separate environment.

**USAGE**

Djac has a usable web interface that runs on the Django development server. You can start it with the usual:

`$ ./manage.py runserver`

The interface can be found at http://localhost:8000/accounts. You can also use the accounts app on its own; there are a few methods on the Account model to add credits and debits, and get a running balance list. 

**AUTHORS**

Djac is written by Austin Pocus, copright 2011, under the BSD license. Details may be found in LICENSE.

