from django.contrib import admin
from review.models import Border,BorderImage

# Register your models here.
class BorderAdmin(admin.ModelAdmin):
    list_display = ['trip_detail', '작성일']

class BorderImgAdmin(admin.ModelAdmin):
    list_display = ['id','image']

admin.site.register(Border, BorderAdmin)
admin.site.register(BorderImage, BorderImgAdmin)