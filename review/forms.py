from django.forms import ModelForm
from review.models import ReviewEntry
from django.utils.html import strip_tags
from django import forms

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewEntry
        fields = ["rating", "deskripsi"]

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)

    def clean_deskripsi(self):
        komentar = self.cleaned_data["deskripsi"]
        return strip_tags(komentar)
