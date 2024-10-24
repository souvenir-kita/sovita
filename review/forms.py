from django.forms import ModelForm
from review.models import ReviewEntry
from django.utils.html import strip_tags

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewEntry
        fields = ["rating", "description"]

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
