from django import forms
from django_countries.fields import CountryField

from .models import Amenity, Facility, RoomType


class SearchForm(forms.Form):
    city = forms.CharField(max_length=140, required=False)
    country = CountryField(default="RU").formfield()
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(queryset=Facility.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), required=False)
    instant_book = forms.BooleanField(required=False)
