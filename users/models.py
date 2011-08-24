from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.contrib import auth

from accounts.models import Account
from budget.models import Budget

class UserProfile(models.Model):
    user = models.OneToOneField(auth.models.User)
    accounts = models.ManyToManyField(Account, null=True)
    budgets = models.ManyToManyField(Budget, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def get_total_balance(self):
        return self.accounts.aggregate(Sum('balance'))['balance__sum']

    def __unicode__(self):
	return self.user.username

def user_profile_create(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(user_profile_create, sender=auth.models.User)


