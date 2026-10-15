from django.contrib import admin
from app1.models import *
admin.site.register(Genre)
admin.site.register(Director)
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'duration', 'rating', 'genre', 'director')
    