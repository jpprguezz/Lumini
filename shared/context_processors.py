from subjects.models import Subject


def user_subjects(request):
    subjects = Subject.objects.none()

    if not request.user.is_authenticated:
        return {'subjects': subjects}

    user = request.user

    profile = getattr(user, 'profile', None)

    if not profile:
        return {'subjects': subjects}

    role = getattr(profile, 'role', 'S')

    if role == 'T':
        subjects = Subject.objects.filter(teacher=user)
    elif role == 'S':
        subjects = Subject.objects.filter(students=user)

    return {'subjects': subjects}
