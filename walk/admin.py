from django.contrib import admin

# Register your models here.
from walk.models import Algorithm, Comment
admin.site.register(Algorithm)
admin.site.register(Comment)

