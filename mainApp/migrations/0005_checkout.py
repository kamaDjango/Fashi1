# Generated by Django 3.2.8 on 2021-12-25 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.TextField()),
                ('total', models.IntegerField()),
                ('shipping', models.IntegerField()),
                ('final', models.IntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.buyer')),
            ],
        ),
    ]