from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class Enrollment(models.Model):
    student = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollments', on_delete=models.CASCADE
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )


class Subject(models.Model):
    code = models.CharField(unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, related_name='teaching', on_delete=models.PROTECT)
    students = models.ManyToManyField(
        User, related_name='enrolled', through='Enrollment', blank=True
    )

    def get_absolute_url(self):
        return reverse('subjects:subject_detail', args=[self.code])


class Lesson(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', related_name='lessons', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500, blank=True)

    def get_absolute_url(self):
        return reverse('lessons:lesson_detail', args=[self.pk])
