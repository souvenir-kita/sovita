from django.forms import ModelForm
from review.models import ReviewEntry

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewEntry
        fields = ["rating", "description"]
