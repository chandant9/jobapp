from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobseekplatform.jobseekapp.models import RecruiterGroup


class Command(BaseCommand):
    help = 'Move existing recruiters to the RecruiterGroup'

    def handle(self, *args, **options):
        recruiters = User.objects.filter(email__endswith='xyz.com')
        recruiter_group = RecruiterGroup.objects.first()

        if recruiter_group:
            recruiter_group.group.user_set.set(recruiters)
            self.stdout.write(self.style.SUCCESS('Recruiters moved successfully.'))
        else:
            self.stdout.write(self.style.ERROR('RecruiterGroup does not exist. Please create the group before running this command.'))
