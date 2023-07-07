from datetime import datetime
from django.utils.timesince import timesince


def get_posted_ago(posted_date):
    now = datetime.now().replace(tzinfo=None)
    posted_date = posted_date.replace(tzinfo=None)

    difference = now - posted_date

    if difference.days < 1:
        if difference.seconds < 3600:  # Less than 1 hour
            minutes = difference.seconds // 60
            return f'{minutes} minutes ago'
        else:
            hours = difference.seconds // 3600
            return f'{hours} hours ago'
    elif difference.days == 1:
        return 'Yesterday'
    elif difference.days < 7:
        return f'{difference.days} days ago'
    elif 7 <= difference.days < 8:
        return '1 week ago'
    elif 8 <= difference.days < 14:
        return f'{difference.days} days ago'
    elif 14 <= difference.days < 15:
        return '2 weeks ago'
    elif 15 <= difference.days < 21:
        return f'{difference.days} days ago'
    elif 21 <= difference.days < 22:
        return '3 weeks ago'
    elif 22 <= difference.days < 28:
        return f'{difference.days} days ago'
    else:
        return timesince(posted_date).split(",")[0] + 'days ago'
