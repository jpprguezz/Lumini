from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('subjects:list')
    return render(request, 'shared/index.html')
