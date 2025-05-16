from django.core.management.base import BaseCommand, CommandError
from expenses.models import ExpenseCategory
from expenses.constants import EXPENSE_CATEGORIES

class Command(BaseCommand):
    help = 'Initializes hardcoded expense categories in the database.'

    def handle(self, *args, **options):
        try:
            created_count = 0
            for code, label in EXPENSE_CATEGORIES:
                obj, created = ExpenseCategory.objects.get_or_create(
                    code=code,
                    defaults={'label': label}
                )
                if created:
                    created_count += 1
                elif obj.label != label:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Category '{code}' exists but label differs. DB: '{obj.label}', expected: '{label}'"
                        )
                    )
            self.stdout.write(self.style.SUCCESS(f'{created_count} categories created.'))
        except Exception as e:
            raise CommandError(f'Failed to initialize categories: {e}')
