from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from django.core import serializers






def home(request):
    return render(request, 'index.html')



def get_QRCode(data):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # convert to PIL.Image object
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue())
    return image_file



@csrf_exempt
def link(request):
    if request.method == "POST":
        data = json.loads(request.body)

        original = Link.objects.create(original=data.get('url'))
        if request.user.is_authenticated:
            original.user = request.user
            original.qr_code.save(f'{original.slug}.png', get_QRCode(data.get('url')))
        if original:
            return JsonResponse({'message': original.hash, 'id': original.id})
        else:
            return JsonResponse({'message': "Fiel to shorten link"})
    else:
        return JsonResponse({'message': "Please POST request."})



def getLocaction(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2df9c865ff864fb4bcbf81ebbe0386eb&ip={ip}"
    response = requests.get(url)
    return response.json()


def find(request, slug):
    url = get_object_or_404(Link, slug=slug)
    agent = get_user_agent(request)

    # user_ip = request.META.get('REMOTE_ADDR')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if not Location.objects.filter(ip=ip).exists():
        location = Location.objects.create(
            ip=ip,
            os=agent.os[0],
            browser=agent.browser[0],
            country=getLocaction(ip).get('country_name'),
            country_flag=getLocaction(ip).get("country_flag"),
            country_code=getLocaction(ip).get("country_code3"),
            city=getLocaction(ip).get("city"),
        )
        View.objects.create(url=url, location=location,user=url.user)


    if ("http" in url.original):
        return redirect(url.original)
    else:
        return redirect(f"https://{url.original}")


def countryChart(request):
    query = 'SELECT *, count(*) as number FROM chort_location GROUP BY country ORDER BY number'
    locations = Location.objects.raw(query)[0: 1]
    data = []
    for item in locations:
        data.append({
            "country": item.country,
            "number":  item.number,
        })

    return JsonResponse({'data': data})


def dashboard(request):
    context = {}
    return render(request, 'dashboard/index.html', context)



def links(request):
    return render(request, 'dashboard/links.html')


def QRcodes(request):
    return render(request, 'dashboard/qr-codes.html')


def customLinks(request):
    return render(request, 'dashboard/custom-links.html')


def settings(request):
    return render(request, 'dashboard/settings.html')


def contact(request):
    return render(request, 'dashboard/contact.html')
    
    

