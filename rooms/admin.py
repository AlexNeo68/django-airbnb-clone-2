from django.contrib import admin
from .models import Amenity, Facility, HouseRule, Photo, Room, RoomType

@admin.register(RoomType, Facility, Amenity, HouseRule)
class RoomTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
