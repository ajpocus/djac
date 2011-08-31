**DISCLAIMER**: I am not an accountant, and this is not professional accounting software. A full disclaimer can be found in LICENSE.

**OVERVIEW**

Djac is a double entry accounting app for Django. Included are the standalone accounts app, and many usable example views and templates.

**REQUIREMENTS**
    Djac uses:

- Django
- PostgreSQL
- South
- Django Debug Toolbar

Postgres can usually be installed through your distro's package manager (though you can change the DB in settings.py to whatever you want). The Python dependencies are best installed through pip, as in:

`$ pip install psycopg2 south django-debug-toolbar`

I strongly recommend using virtualenv to create a separate environment.

**USAGE**

Djac has a usable web interface (though not the best-looking). It can be activated with the Django development server, from the project root:

`$ ./manage.py runserver`

The interface can be found at http://localhost:8000/accounts. You can also use the accounts app on its own; there are a few methods on the Account model to add credits and debits, and get a running balance list. 

**AUTHORS**

Djac is written by Austin Pocus, copright 2011, under the BSD license. Details may be found in LICENSE. Djac wouldn't exist without the help of this great software:

- Django
- PostgreSQL
- South
- Django Debug Toolbar
- jQuery
- jQuery UI
