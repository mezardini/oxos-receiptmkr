from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    biz_code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    date = models.DateTimeField(auto_now_add=True)
    receipt_allocation = models.IntegerField(default=20)

    def __str__(self):
        return self.biz_code
    
class PaymentLogs(models.Model):
    SUCCESS = 'Success'
    FAILED = 'Failed'
    Transaction_status = [
      (SUCCESS, ('Success')),
      (FAILED   , ('Failed')),
   ]
    
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_user')
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Transaction_status)
    expiration_date = models.DateField(default='2023-12-18')

    def __str__(self):
        return f"{self.payer.username} - {self.amount}"