from django.http import HttpResponse

def default_route(request):
    return HttpResponse(status=200)