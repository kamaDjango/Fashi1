# Generated by Django 3.2.4 on 2022-01-09 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_auto_20220102_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order_id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'SUCCESS'), (2, 'PENDING')], default=2),
        ),
        migrations.AddField(
            model_name='checkout',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.IntegerField(choices=[(1, 'Not Packed'), (2, 'Ready For Shipment'), (3, 'Shipped'), (4, 'Delivered')], default=1),
        ),
    ]
