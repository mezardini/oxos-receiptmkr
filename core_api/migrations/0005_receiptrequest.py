# Generated by Django 4.1.5 on 2023-04-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0004_business_user_no_alter_business_biz_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('user_no', models.IntegerField(null=True)),
            ],
        ),
    ]
