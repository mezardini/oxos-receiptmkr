# Generated by Django 4.1.5 on 2023-04-30 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0007_alter_receiptrequest_user_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptrequest',
            name='user_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]