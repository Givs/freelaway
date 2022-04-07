from django.http import HttpResponse
from django.shortcuts import render


def encontrar_jobs(request):
    if request.method == 'GET':
        jobs = Jobs.objects.filter(reservado=False)
        return render(request, 'encontrar_jobs.html', {'jobs': jobs})