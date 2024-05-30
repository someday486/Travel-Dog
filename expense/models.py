from django.db import models
from trips.models import TripDetail
  
class ExpenseDetail(models.Model):
    trip_detail = models.ForeignKey(TripDetail, on_delete=models.CASCADE)
    memo = models.CharField(max_length=100)
    receipt = models.FileField()

    def __str__(self):
        return f"{self.trip_detail}, {self.memo}, {self.receipt}"