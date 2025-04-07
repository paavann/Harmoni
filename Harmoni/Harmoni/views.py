from django.http import HttpResponse


def homepage(request):
    return HttpResponse("hello world! this is homepage")