from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import Loan


class Command(BaseCommand):
    help = 'Проверяет и обновляет статусы просроченных выдач'

    def handle(self, *args, **options):
        overdue_loans = Loan.objects.filter(
            status='active',
            expiry_date__lt=timezone.now()
        )

        count = overdue_loans.count()
        for loan in overdue_loans:
            loan.status = 'expired'
            loan.save()

        self.stdout.write(
            self.style.SUCCESS(f'Обновлено {count} просроченных выдач')
        )