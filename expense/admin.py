from django.contrib import admin
from .models import ExpenseDetail

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['memo','receipt']

admin.site.register(ExpenseDetail, ExpenseAdmin)