# Generated by Django 5.1.6 on 2025-03-30 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
    ]
