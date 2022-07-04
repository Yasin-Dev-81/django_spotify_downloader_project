from django.shortcuts import render


def home_view(request):
    project_apps = [
        {'name': 'track',},
        {'name': 'artist'},
        {'name': 'album'},
        {'name': 'playlist'},
    ]
    return render(request, 'home/home.html', context={'project_apps': project_apps})
