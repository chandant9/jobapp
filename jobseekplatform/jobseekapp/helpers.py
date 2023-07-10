from datetime import datetime, timedelta
from django.utils.timesince import timesince
from django.conf import settings
import jwt
from rest_framework_simplejwt.tokens import AccessToken


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


def generate_access_token(user):
    # Define the token payload with user information
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time (e.g., 1 day)
    }

    # Generate the access token using the secret key
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # Return the access token as a string
    return access_token
