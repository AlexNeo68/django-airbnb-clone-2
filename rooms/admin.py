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
    list_display = (
        'name',
        'country',
        'city',
        'address',
        'guests',
        'beds',
        'bathrooms',
        'price',
        'check_in',
        'check_out',
        'instant_book',
        'room_type',
    )

    list_filter = ('city', 'instant_book', 'country')

    search_fields = ('^city', '^host__username')

    filter_horizontal = (
        'amenities',
        'facilities',
        'house_rules',
    )

    fieldsets = [
        ('Basic information', {
            'fields': [
                'name',
                'description',
                'country',
                'city',
            ],
        }),
        ('Times', {
            'fields': [
                'check_in',
                'check_out',
                'instant_book',
            ]
        })
    ]
