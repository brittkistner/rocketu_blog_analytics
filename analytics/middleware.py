from django.conf import settings
from ipware.ip import get_real_ip
import requests
from analytics.models import Page, Location, View


class LocationMiddleware(object):
    def process_request(self,request):
        #Get the IP Address of this request
        ip = get_real_ip(request)

        # If we didn't get an IP Address and we're developing locally,
        # make an API call to get our IP Address.
        if ip is None and settings.DEBUG:
            ip = requests.get('http://icanhazip.com/').text

        if ip is not None:
            response = requests.get('http://ipinfo.io/{}/json'.format(ip))
            if response.status_code == 200:
                request.location = response.json()  #now this is a python dictionary, we have this wherever we are
                # Split out the lat and long from the location
                request.location['latitude'], request.location['longitude'] = request.location['loc'].split(',')

        request.ip = ip

class PageViewMiddleware(object):
    def process_request(self, request):
        #everytime a page is viewed:
        # 1. Page instance will either be retrieved or created.
        # 2. Location instance will either be retrieved or created.
        # 3. View will be created

        page, created = Page.objects.get_or_create(url=request.META['PATH_INFO'])
        #get_or_create, creates a tuple
        #page, created, created will either be true or false based on whether or not it was created
        #stores web analytics (request.META)

        location, created = Location.objects.get_or_create(city=request.location['city'],
                                                  country=request.location['country'],
                                                  region=request.location['region'])


        View.objects.create(longitude=request.location['longitude'],
                                          latitude=request.location['latitude'],
                                          location=location,
                                          page=page,
                                          ip_address=request.ip)