from django.http import HttpResponse


def simple_view(request):
    html = "<html><body>HELLO</body></html>"
    return HttpResponse(html)