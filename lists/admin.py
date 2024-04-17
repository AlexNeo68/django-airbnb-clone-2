from django.contrib import admin
from .models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = 'name', 'count_rooms'
    filter_horizontal = 'rooms',

    def count_rooms(self, obj):
        return obj.rooms.count()
