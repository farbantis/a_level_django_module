# Generated by Django 4.1.6 on 2023-02-06 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_merchandise_return_order_to_return_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='order_to_return',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
    ]