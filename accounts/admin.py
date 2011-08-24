from django.contrib import admin
from accounts.models import Account, Journal, Posting

admin.site.register(Account)
admin.site.register(Journal)
admin.site.register(Posting)

