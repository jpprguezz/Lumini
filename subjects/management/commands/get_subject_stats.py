from django.core.management.base import BaseCommand
from django.db.models import Avg
from subjects.models import Subject


class Command(BaseCommand):
    help = 'Show average marks for all subjects'

    def handle(self, *args, **options):
        subjects = Subject.objects.all()

        for subject in subjects:
            enrollments_with_marks = subject.enrollments.filter(mark__isnull=False)

            if enrollments_with_marks.exists():
                result = enrollments_with_marks.aggregate(avg_mark=Avg('mark'))
                average = result['avg_mark'] or 0.00
            else:
                average = 0.00
            self.stdout.write(f'{subject.code}: {average:.2f}')
