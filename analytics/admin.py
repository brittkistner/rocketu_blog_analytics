from django.contrib import admin
from analytics.models import Page, Location, View


admin.site.register(View)
admin.site.register(Location)
admin.site.register(Page)