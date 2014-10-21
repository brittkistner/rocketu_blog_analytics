from django.http import HttpResponse
from django.shortcuts import render
from analytics.models import Page


def portal(request):
    # Create a main page, which lists all of our Pages and how many times they've been viewed.
    return render(request, 'page_view.html', {'pages': Page.objects.all})


# page.views.count
def detail_view(request, page_id):
    page = Page.objects.get(pk=page_id)
    views = page.views.all()
    view_and_count = {}

    for view in views:
        view_and_count[view] = page.views.filter(latitude=view.latitude, longitude=view.longitude).count()

    data = {
        'view_and_count': view_and_count,
    }
    return render(request, 'detail_view.html', data)







