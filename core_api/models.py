from django.db import models

# Create your models here.
class PdfFile(models.Model):
    name = models.CharField(max_length=2000)
    file = models.FileField(upload_to='static')

    def __str__(self):
        return self.name

class PdfFilepath(models.Model):
    name = models.CharField(max_length=2000)
    file = models.ForeignKey(PdfFile, on_delete=models.CASCADE)
    path = models.FilePathField(path='static/')

class ReceiptRequest(models.Model):
    receipt_name = models.CharField(max_length=2000)
    user_no = models.CharField(max_length=50, null=True)
    timeanddate = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.receipt_name + ' by ' + self.user_no

class Business(models.Model):
    SIMPLE = 'Poor'
    CORPORATE = 'Meh'
    COOL = 'Mid'
    CASUAL = 'Decent'
    RAD = 'Rad'
    TEMP_CHOICE = [
       (SIMPLE, ('Poor')),
       (CORPORATE, ('Meh')),
       (COOL, ('Mid')),
       (CASUAL, ('Decent')),
       (RAD, ('Rad')),
    ]
    name = models.CharField(max_length=2000)
    website = models.CharField(max_length=2000)
    biz_code = models.CharField(max_length=2000, unique=True)
    text = models.CharField(max_length=500, null=True)
    template = models.CharField(max_length=10, choices=TEMP_CHOICE, null=True)
    user_no = models.IntegerField(null=True)

    def __str__(self):
        return self.name
