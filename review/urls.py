from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.index),
    path('detail/<int:userId>/', views.detail),
    path('tripDetail/<int:tripId>/', views.tripDetail),
    path('upload/', views.upload_file, name='upload_file'),
    path('add/<int:tripdetailId>/', views.add),
    path('delete/<int:borderId>/<path:image_url>/', views.delete_image),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
