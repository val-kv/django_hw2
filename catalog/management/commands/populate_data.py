# populate_data.py

from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Очистка базы данных от старых данных
        Category.objects.all().delete()

        # Создание новых данных
        Category.objects.create(name='Одежда')
        Category.objects.create(name='Автозапчасти')
        Category.objects.create(name='Продукты')

        self.stdout.write(self.style.SUCCESS('Data populated successfully'))
