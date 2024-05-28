from django.db import models

# Create your models here.

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES)
    date = models.DateField()
    trip_id = models.CharField(max_length=50)  # Assuming trip_id is a string identifier for the trip

    def __str__(self):
        return f"{self.입력} - {self.총금액} - {self.카테고리} - {self.일정날짜}"