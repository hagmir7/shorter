from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Do something with the data
        return JsonResponse({'success': True})




def home(request):
    return render(request, 'index.html')





@csrf_exempt
def link(request):
    if request.method == "POST":
        data = json.loads(request.body)
        original = Link.objects.create(original=data.get('url'))
        if original:
            return JsonResponse({'message': original.hash, 'id': original.id})
        else:
            return JsonResponse({'message': "Fiel to shorten link"})
    else:
        return JsonResponse({'message': "Please POST request."})



def find(request, slug):
    url = get_object_or_404(Link, slug=slug)
    # url = Link.objects.get(hash=hash)
    return redirect(url.original)
    

