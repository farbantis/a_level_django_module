# Generated by Django 4.1.6 on 2023-02-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_merchandise_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchandise',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m'),
        ),
    ]