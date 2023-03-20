from django.core.management import BaseCommand

from api.models import Post


class Command(BaseCommand):
    help = 'Create post'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int)

    def handle(self, *args, **options):
        n = options.get('number')
        try:
            for _ in range(n):
                Post.objects.create(
                    title='d',
                    content='d'
                )
            self.stdout.write(self.style.SUCCESS(f"{n} SUCCESS"))
        except Exception as e:
            self.stdout.write(e)



