from django.http import HttpResponse

from app.models import Image


def simple_view(request):
    image = Image.objects.first()
    html = f'<html><body><img src="{image.upload.url}"></body></html>'
    return HttpResponse(html)
