from django.contrib import admin
from .models import Amenity, Facility, HouseRule, Photo, Room, RoomType


@admin.register(RoomType, Facility, Amenity, HouseRule)
class RoomTypeAdmin(admin.ModelAdmin):
    def used_by(self, obj):
        return obj.rooms.count()

    list_display = ('name', 'used_by')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    def total_rating(self, obj):
        reviews = obj.reviews.all()
        all_ratings = 0
        for review in reviews:
            all_ratings += review.avg_rating()
        return round(all_ratings/len(reviews), 2)

    list_display = (
        'name',
        'total_rating',
        'country',
        'city',
        'address',
        'guests',
        'beds',
        'bedrooms',
        'baths',
        'price',
        'check_in',
        'check_out',
        'instant_book',
        'room_type',
        'count_amenities',
        'count_photos',
    )

    count_amenities.short_description = 'Count of Amenities'

    list_filter = ('city', 'instant_book', 'country')

    search_fields = ('^city', '^host__username')

    filter_horizontal = (
        'amenities',
        'facilities',
        'house_rules',
    )

    ordering = 'name', 'country', 'city', 'beds'

    fieldsets = [
        ('Basic information', {
            'fields': [
                'name',
                'description',
                'country',
                'city',
                'address',
                'price',
                'room_type'
            ],
        }),
        ('Times', {
            'fields': [
                'check_in',
                'check_out',
                'instant_book',
            ]
        }),
        ('Spaces', {
            'fields': [
                'guests',
                'beds',
                'bedrooms',
                'baths',

            ]
        }),
        ('More about the Space', {
            'fields': [
                'amenities',
                'facilities',
                'house_rules',
            ]
        }),
        (
            'Last Details', {
                'fields': [
                    'host'
                ]
            }
        )
    ]
