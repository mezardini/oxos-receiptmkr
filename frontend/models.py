from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    biz_code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    date = models.DateTimeField(auto_now_add=True)
    receipt_allocation = models.IntegerField(default=50)

    def __str__(self):
        return self.biz_code
    
class ReceiptDetails(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    items = models.TextField()
    receipt_code = models.CharField(max_length=20)

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
    status = models.CharField(max_length=20)
    pay_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.payer.username} - {self.amount}"