from django.contrib import admin
from review.models import Border

# Register your models here.
class BorderAdmin(admin.ModelAdmin):
    list_display = ['trip_detail', '제목', '작성일']


admin.site.register(Border, BorderAdmin)