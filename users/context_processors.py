from django.contrib.auth.decorators import login_required

@login_required
def user_context(request):
    profile = request.user.get_profile()
    total = profile.get_total_balance()
    start_date = profile.start_date.strftime("%m/%d/%Y")
    end_date = profile.end_date.strftime("%m/%d/%Y")

    return {
	'total': total,
	'start_date': start_date,
	'end_date': end_date,
    }

