# Generated by Django 3.2.8 on 2021-12-11 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_auto_20211205_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wid', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.product')),
            ],
        ),
    ]
