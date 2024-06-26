from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, View, UpdateView, CreateView, DeleteView

from rooms.forms import SearchForm
from rooms.models import Room, Photo
from users.mixins import LoginRequiredMixin


def room_details(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', context={'room': room})


class RoomDetailView(DetailView):
    model = Room


class CreateRoomView(LoginRequiredMixin, CreateView):
    model = Room
    template_name = 'rooms/room_create.html'
    fields = [
        'name',
        'description',
        'country',
        'city',
        'price',
        'address',
        'guests',
        'amenities',
        'facilities',
        'house_rules',
        'beds',
        'bedrooms',
        'baths',
        'check_in',
        'check_out',
        'instant_book',
        'room_type',
    ]

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def form_valid(self, form):
        room = form.save(commit=False)
        room.host = self.request.user
        room.save()
        form.save_m2m()
        return super().form_valid(form)


class UpdateRoomView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'rooms/room_edit.html'
    fields = [
        'name',
        'description',
        'country',
        'city',
        'price',
        'address',
        'guests',
        'amenities',
        'facilities',
        'house_rules',
        'beds',
        'bedrooms',
        'baths',
        'check_in',
        'check_out',
        'instant_book',
        'room_type',
    ]
    context_object_name = 'room'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


class RoomPhotosView(LoginRequiredMixin, RoomDetailView):
    template_name = 'rooms/room_photos.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


class SearchView(View):

    def get(self, request):
        filters = {}

        country = request.GET.get('country')
        if country:
            form = SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data['city']
                country = form.cleaned_data['country']
                price = form.cleaned_data['price']
                guests = form.cleaned_data['guests']
                beds = form.cleaned_data['beds']
                bedrooms = form.cleaned_data['bedrooms']
                baths = form.cleaned_data['baths']
                amenities = form.cleaned_data['amenities']
                facilities = form.cleaned_data['facilities']
                room_type = form.cleaned_data['room_type']
                instant_book = form.cleaned_data['instant_book']

                if city:
                    filters['city__startswith'] = city

                if country:
                    filters['country'] = country

                if room_type:
                    filters['room_type'] = room_type

                if price:
                    filters['price__lte'] = price

                if guests:
                    filters['guests__gte'] = guests

                if beds:
                    filters['beds__gte'] = beds

                if bedrooms:
                    filters['bedrooms__gte'] = bedrooms

                if baths:
                    filters['baths__gte'] = baths

                if len(amenities) > 0:
                    for amenity in amenities:
                        filters['amenities'] = amenity

                if len(facilities) > 0:
                    for facility in facilities:
                        filters['facilities'] = facility

                if instant_book:
                    filters['instant_book'] = True

                qs = Room.objects.filter(**filters).order_by('-created')

                paginator = Paginator(qs, 5, orphans=5)

                page = request.GET.get('page', 1)

                print(page)

                rooms = paginator.get_page(page)

                context = {"search_form": form, 'rooms': rooms}

                return render(request, 'rooms/search.html', context)

        else:
            form = SearchForm()
            context = {"search_form": form}
            return render(request, 'rooms/search.html', context)


def search(request):
    filters = {}

    country = request.GET.get('country')
    if country:
        form = SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            price = form.cleaned_data['price']
            guests = form.cleaned_data['guests']
            beds = form.cleaned_data['beds']
            bedrooms = form.cleaned_data['bedrooms']
            baths = form.cleaned_data['baths']
            amenities = form.cleaned_data['amenities']
            facilities = form.cleaned_data['facilities']
            room_type = form.cleaned_data['room_type']
            instant_book = form.cleaned_data['instant_book']

            if city:
                filters['city__startswith'] = city

            if country:
                filters['country'] = country

            if room_type:
                filters['room_type'] = room_type

            if price:
                filters['price__lte'] = price

            if guests:
                filters['guests__gte'] = guests

            if beds:
                filters['beds__gte'] = beds

            if bedrooms:
                filters['bedrooms__gte'] = bedrooms

            if baths:
                filters['baths__gte'] = baths

            if len(amenities) > 0:
                for amenity in amenities:
                    filters['amenities'] = amenity

            if len(facilities) > 0:
                for facility in facilities:
                    filters['facilities'] = facility

            if instant_book:
                filters['instant_book'] = True

    else:
        form = SearchForm()

    print(filters)

    rooms = Room.objects.filter(**filters)

    context = {"search_form": form, 'rooms': rooms}

    return render(request, 'rooms/search.html', context)


@login_required
def photo_delete(request, room_pk, photo_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        if room.host.pk != request.user.pk:
            messages.error(request, 'You do not have permission to delete this photo.')
            return redirect(reverse('rooms:room_detail', kwargs={'pk': room_pk}))
        else:
            Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, 'Photo successfully deleted.')
        return redirect(reverse('rooms:photos', kwargs={'pk': room_pk}))
    except Room.DoesNotExist:
        raise Http404


class DeleteRoomPhotoView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Photo
    template_name = 'rooms/room_photo_confirm_delete.html'
    success_message = 'Photo successfully deleted.'
    pk_url_kwarg = 'photo_pk'
    context_object_name = 'photo'

    def get_success_url(self):
        return reverse('rooms:photos', kwargs={'pk': self.kwargs['room_pk']})


class UpdateRoomPhotoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = 'rooms/room_photo_edit.html'
    success_message = 'Photo successfully updated.'
    pk_url_kwarg = 'photo_pk'
    fields = [
        'caption'
    ]

    def get_success_url(self):
        return reverse_lazy('rooms:photos', kwargs={'pk': self.kwargs['room_pk']})

    def get_object(self, queryset=None):
        room = Room.objects.get(pk=self.kwargs['room_pk'])
        photo = Photo.objects.get(pk=self.kwargs['photo_pk'])
        if room.host.pk != self.request.user.pk:
            raise Http404
        return photo


class CreateRoomPhotoView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Photo
    template_name = 'rooms/room_photo_create.html'
    success_message = 'Photo successfully upload'
    fields = [
        'caption',
        'file',
        # 'room'
    ]

    def get_success_url(self):
        return reverse_lazy('rooms:photos', kwargs={'pk': self.kwargs['room_pk']})

    def render_to_response(self, context, **response_kwargs):
        context['room_pk'] = self.kwargs['room_pk']
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    # def save(self, *args, **kwargs):
    #     room = Room.objects.get(pk=self.kwargs['room_pk'])

    def form_valid(self, form):
        photo = form.save(commit=False)
        room = Room.objects.get(pk=self.kwargs['room_pk'])
        photo.room = room
        photo.save()
        return super().form_valid(form)
