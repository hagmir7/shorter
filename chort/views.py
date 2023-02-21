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
from django.db.models import Count

from django.utils import timezone
from datetime import timedelta







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
            user = url.user,
            os=agent.os[0],
            browser=agent.browser[0],
            country=getLocaction(ip).get('country_name'),
            country_flag=getLocaction(ip).get("country_flag"),
            country_code=getLocaction(ip).get("country_code3"),
            city=getLocaction(ip).get("city"),
        )
    else:
        location = Location.objects.get(ip=ip)

    url.views.add(location)
    url.save()
    if ("http" in url.original):
        return redirect(url.original)
    else:
        return redirect(f"https://{url.original}")




def countryChart(request):

    locations = Location.objects.values('country_code', 'country') \
    .annotate(count=Count('country_code')) \
    .filter(user=request.user).order_by('-count')[0:10]


    data = []
    for item in locations:
        data.append({
            "country_code": item.get('country_code'),
            "count":  item.get('count'),
            "country": item.get('country'),
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




def recent_views(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_views = Location.objects.filter(date=seven_days_ago)

    # Create a dictionary to store the post counts by day
    location_counts_by_day = {}
    for post in recent_views:
        created_at_day = post.date.strftime('%Y-%m-%d')
        location_counts_by_day[created_at_day] = location_counts_by_day.get(created_at_day, 0) + 1

    # Create a list of tuples that contains the date and the post count for each day
    post_counts = []
    for i in range(7):
        date = (timezone.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        post_count = location_counts_by_day.get(date, 0)
        post_counts.append((date, post_count))

    context = {
        'post_counts': post_counts,
    }
    return render(request, 'recent_views.html', context)
    
    

