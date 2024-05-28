from django.shortcuts import render,get_object_or_404
from review.models import Review, Border
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    userId=request.user.id
    query=request.GET.get('topic','')
    if query:
        border=Border.objects.filter(내용__icontains=f'#{query}')
    else:
        border=Border.objects.all()

    content={
        'border':border,
        'userId':userId,
        'topic':query,
    }
    return render(request,'review/index.html',content);

@login_required
def detail(request,userId,borderId):
    border=get_object_or_404(Border,id=userId)
    content={
        'border':border,
    }
    return render(request,'review/detail.html',content);