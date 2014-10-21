from django.contrib import admin
from blog.models import Post, Author, Tag, AdImage


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(AdImage)