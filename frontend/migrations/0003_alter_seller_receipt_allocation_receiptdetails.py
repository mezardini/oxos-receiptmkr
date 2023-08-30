# Generated by Django 4.1.5 on 2023-08-23 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_paymentlogs_pay_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='receipt_allocation',
            field=models.IntegerField(default=50),
        ),
        migrations.CreateModel(
            name='ReceiptDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('items', models.TextField()),
                ('receipt_code', models.CharField(max_length=20)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.seller')),
            ],
        ),
    ]
