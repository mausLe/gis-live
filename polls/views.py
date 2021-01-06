from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the toughest time in the history")