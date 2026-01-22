from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Enrollment, Lesson, Subject

User = get_user_model()


class SubjectConverter:
    regex = r'[^/]+'

    def to_python(self, subject_code: str) -> Subject:
        return get_object_or_404(Subject, code=subject_code)

    def to_url(self, subject: Subject) -> str:
        return str(subject.code)


class LessonConverter:
    regex = r'\d+'

    def to_python(self, lesson_pk: str) -> Lesson:
        return get_object_or_404(Lesson, pk=int(lesson_pk))

    def to_url(self, lesson: Lesson) -> str:
        return str(lesson.pk)


class EnrollmentConverter:
    regex = r'\d+'

    def to_python(self, enrollment_id: str) -> Enrollment:
        return get_object_or_404(Enrollment, pk=int(enrollment_id))

    def to_url(self, enrollment: Enrollment) -> str:
        return str(enrollment.pk)
