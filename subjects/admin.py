from django.contrib import admin

from .models import Enrollment, Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')
    search_fields = (
        'code',
        'name',
        'teacher__username',
        'teacher__first_name',
        'teacher__last_name',
    )
    list_filter = ('teacher',)
    ordering = ('code',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    search_fields = ('title', 'subject__code', 'subject__name')
    list_filter = ('subject',)
    ordering = ('subject', 'title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrolled_at', 'mark')
    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'subject__code',
        'subject__name',
    )
    list_filter = ('subject', 'enrolled_at', 'mark')
    ordering = ('subject', 'student')
