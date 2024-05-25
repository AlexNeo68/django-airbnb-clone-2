from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    cleanliness = forms.IntegerField(min_value=1, max_value=5)
    accuracy = forms.IntegerField(min_value=1, max_value=5)
    check_in = forms.IntegerField(min_value=1, max_value=5)
    communication = forms.IntegerField(min_value=1, max_value=5)
    location = forms.IntegerField(min_value=1, max_value=5)
    value = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = (
            'review',
            'cleanliness',
            'accuracy',
            'check_in',
            'communication',
            'location',
            'value',
        )

    def save(self, commit=True):
        review = super(ReviewForm, self).save(commit=False)
        return review
