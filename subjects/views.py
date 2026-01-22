from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Enrollment, Lesson, Subject


def _is_teacher(user):
    role = getattr(getattr(user, 'profile', None), 'role', None)
    if role:
        return role == 'T'
    return user.groups.filter(name='T').exists()


def _is_student(user):
    role = getattr(getattr(user, 'profile', None), 'role', None)
    if role:
        return role == 'S'
    return user.groups.filter(name__in=['S', 'Student']).exists()


@login_required
def subject_list(request):
    if _is_teacher(request.user):
        subjects = Subject.objects.filter(teacher=request.user)
        can_request_certificate = False
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        subjects = [e.subject for e in enrollments]
        can_request_certificate = enrollments.exists() and all(
            e.mark is not None for e in enrollments
        )

    return render(
        request,
        'subjects/subject_list.html',
        {'subjects': subjects, 'can_request_certificate': can_request_certificate},
    )


@login_required
def subject_detail(request, subject_code):
    subject = get_object_or_404(Subject, code=subject_code)
    user = request.user

    if _is_teacher(user):
        if subject.teacher != user:
            return HttpResponseForbidden()
    else:
        if not Enrollment.objects.filter(student=user, subject=subject).exists():
            return HttpResponseForbidden()

    lessons = subject.lessons.all()

    enrollment = None
    if not _is_teacher(user):
        enrollment = Enrollment.objects.filter(student=user, subject=subject).first()

    return render(
        request,
        'subjects/subject_detail.html',
        {'subject': subject, 'lessons': lessons, 'enrollment': enrollment},
    )


@login_required
def add_lesson(request, subject_code):
    subject = get_object_or_404(Subject, code=subject_code)
    user = request.user

    if not _is_teacher(user) or subject.teacher != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Lesson.objects.create(subject=subject, title=title, content=content)
            messages.success(request, 'Lesson was successfully added.')
            return redirect(f'/subjects/{subject_code}/')

    return render(request, 'subjects/add_lesson.html', {'subject': subject})


@login_required
def lesson_detail(request, subject_code, lesson_pk):
    subject = get_object_or_404(Subject, code=subject_code)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, subject=subject)
    user = request.user

    if _is_teacher(user):
        if subject.teacher != user:
            return HttpResponseForbidden()
    else:
        if not Enrollment.objects.filter(student=user, subject=subject).exists():
            return HttpResponseForbidden()

    return render(request, 'subjects/lesson_detail.html', {'lesson': lesson, 'subject': subject})


@login_required
def edit_lesson(request, subject_code, lesson_pk):
    subject = get_object_or_404(Subject, code=subject_code)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, subject=subject)
    user = request.user

    if not _is_teacher(user) or subject.teacher != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        lesson.title = request.POST.get('title')
        lesson.content = request.POST.get('content')
        lesson.save()

        messages.success(request, 'Changes were successfully saved.')
        return redirect(f'/subjects/{subject_code}/lessons/{lesson_pk}/')

    return render(request, 'subjects/edit_lesson.html', {'lesson': lesson, 'subject': subject})


@login_required
def delete_lesson(request, subject_code, lesson_pk):
    subject = get_object_or_404(Subject, code=subject_code)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, subject=subject)
    user = request.user

    if not _is_teacher(user) or subject.teacher != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson was successfully deleted.')
        return redirect(f'/subjects/{subject_code}/')

    return render(request, 'subjects/delete_lesson.html', {'lesson': lesson, 'subject': subject})


@login_required
def mark_list(request, subject_code):
    subject = get_object_or_404(Subject, code=subject_code)
    user = request.user

    if not _is_teacher(user) or subject.teacher != user:
        return HttpResponseForbidden()

    enrollments = subject.enrollments.all()

    return render(
        request, 'subjects/mark_list.html', {'subject': subject, 'enrollments': enrollments}
    )


@login_required
def edit_marks(request, subject_code):
    subject = get_object_or_404(Subject, code=subject_code)
    user = request.user

    if not _is_teacher(user) or subject.teacher != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        enrollments = subject.enrollments.all()

        for enrollment in enrollments:
            field_name = f'mark_{enrollment.student.id}'
            new_mark = request.POST.get(field_name)

            if new_mark:
                try:
                    enrollment.mark = int(new_mark)
                    enrollment.save()
                except:
                    pass

        messages.success(request, 'Marks were successfully saved.')
        return redirect(f'/subjects/{subject_code}/marks/edit/')

    enrollments = subject.enrollments.all()
    return render(
        request, 'subjects/edit_marks.html', {'subject': subject, 'enrollments': enrollments}
    )


@login_required
def enroll_subjects(request):
    user = request.user

    if not _is_student(user):
        raise Http404()

    enrolled_subject_ids = Enrollment.objects.filter(student=user).values_list(
        'subject_id', flat=True
    )
    my_subjects = Subject.objects.filter(id__in=enrolled_subject_ids)
    available = Subject.objects.exclude(id__in=enrolled_subject_ids)

    if request.method == 'POST':
        selected = request.POST.getlist('subjects') + request.POST.getlist('subject_codes')

        for val in selected:
            subject = None
            if str(val).isdigit():
                subject = Subject.objects.filter(id=int(val)).first()
            else:
                subject = Subject.objects.filter(code=val).first()

            if subject:
                Enrollment.objects.get_or_create(
                    student=user, subject=subject, defaults={'enrolled_at': timezone.now().date()}
                )

        messages.success(request, 'Successfully enrolled in the chosen subjects.')
        return redirect('/subjects/')

    return render(
        request, 'subjects/enroll.html', {'subjects': available, 'my_subjects': my_subjects}
    )


@login_required
def unenroll_subjects(request):
    user = request.user

    if not _is_student(user):
        raise Http404()

    enrolled_subject_ids = Enrollment.objects.filter(student=user).values_list(
        'subject_id', flat=True
    )
    my_subjects = Subject.objects.filter(id__in=enrolled_subject_ids)

    if request.method == 'POST':
        selected = request.POST.getlist('subjects') + request.POST.getlist('subject_codes')

        for val in selected:
            subject = None
            if str(val).isdigit():
                subject = Subject.objects.filter(id=int(val)).first()
            else:
                subject = Subject.objects.filter(code=val).first()

            if subject:
                Enrollment.objects.filter(student=user, subject=subject).delete()

        messages.success(request, 'Successfully unenrolled from the chosen subjects.')
        return redirect('/subjects/')

    return render(request, 'subjects/unenroll.html', {'my_subjects': my_subjects})


@login_required
def request_certificate(request):
    user = request.user

    if not _is_student(user):
        raise Http404()

    enrollments = user.enrollments.all()
    if not enrollments.exists() or any(e.mark is None for e in enrollments):
        return HttpResponseForbidden()

    if request.method == 'POST':
        email = request.POST.get('email', user.email)
        messages.success(request, f'You will get the grade certificate quite soon at {email}')
        return redirect('/subjects/')

    return render(request, 'subjects/certificate.html')
