from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates the mocspa user with specific password'

    def handle(self, *args, **options):
        username = 'mocspa'
        password = '25leloi'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email='admin@mocspa.vn')
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User "{username}" already exists. Password updated.'))
