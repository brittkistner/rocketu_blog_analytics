from django.db import models

class Page(models.Model):
    #get or create
    url = models.URLField(unique=True)

    def __unicode__(self):
        return u"{}".format(self.url)

class Location(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}, {}, {}".format(self.city, self.region, self.country)

    class Meta:
        unique_together = (('city', 'country', 'region'),)

class View(models.Model):
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    location = models.ForeignKey(Location, related_name='views')
    page = models.ForeignKey(Page, related_name='views')
    # ip_address = models.IPAddressField(blank=True, null=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True)
    time_visited = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u"{} by {} @ {}".format(self.ip_address, self.location, self.time_visited)


    def count_view(self):
        page.views.filter(latitude=self.latitude, longitude=self.longitude).count()