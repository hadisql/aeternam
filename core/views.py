from django.shortcuts import render, redirect


def index(request):

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('albums:albums_view') #forces to redirect to main page when user is authenticated

    return render(request, "core/index.html")
