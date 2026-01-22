from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('<str:subject_code>/', login_required(views.subject_detail), name='subject_detail'),
    path('<str:subject_code>/lessons/add/', login_required(views.add_lesson), name='add_lesson'),
    path(
        '<str:subject_code>/lessons/<int:lesson_pk>/',
        login_required(views.lesson_detail),
        name='lesson_detail',
    ),
    path(
        '<str:subject_code>/lessons/<int:lesson_pk>/edit/',
        login_required(views.edit_lesson),
        name='edit_lesson',
    ),
    path(
        '<str:subject_code>/lessons/<int:lesson_pk>/delete/',
        login_required(views.delete_lesson),
        name='delete_lesson',
    ),
    path('<str:subject_code>/marks/', login_required(views.mark_list), name='mark_list'),
    path('<str:subject_code>/marks/edit/', login_required(views.edit_marks), name='edit_marks'),
    path('enroll/', login_required(views.enroll_subjects), name='enroll_subjects'),
    path('unenroll/', login_required(views.unenroll_subjects), name='unenroll_subjects'),
    path('certificate/', login_required(views.request_certificate), name='request_certificate'),
]
