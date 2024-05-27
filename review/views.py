from django.shortcuts import render
from review.models import Review

# Create your views here.

def index(request):
    review=Review.objects.all()
    content={
        'review':review,
    }
    return render(request,'review/index.html',content);
