from django.core.management.base import BaseCommand
from appNotification.models import Category

class Command(BaseCommand):
    help = 'Load initial categories into the database'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Tanks', 'value': 'tanks', 'description': 'Tank classes and roles'},
            {'name': 'Heals', 'value': 'heals', 'description': 'Healer classes and roles'},
            {'name': 'DD', 'value': 'dd', 'description': 'Damage dealer classes and roles'},
            {'name': 'Traders', 'value': 'traders', 'description': 'Trading and economy'},
            {'name': 'Guildmasters', 'value': 'guildmasters', 'description': 'Guild leadership and management'},
            {'name': 'Questgivers', 'value': 'questgivers', 'description': 'Quest related discussions'},
            {'name': 'Blacksmiths', 'value': 'blacksmiths', 'description': 'Blacksmithing and crafting'},
            {'name': 'Tanners', 'value': 'tanners', 'description': 'Leatherworking and skinning'},
            {'name': 'Potionmakers', 'value': 'potionmakers', 'description': 'Alchemy and potion making'},
            {'name': 'Spellmasters', 'value': 'spellmasters', 'description': 'Spell casting and magic'},
        ]

        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                value=cat_data['value'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} categories')
        )
