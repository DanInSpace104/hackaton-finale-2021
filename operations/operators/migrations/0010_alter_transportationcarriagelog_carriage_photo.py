# Generated by Django 3.2.9 on 2021-12-03 12:08

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0009_auto_20211203_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationcarriagelog',
            name='carriage_photo',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to='carriage'),
        ),
    ]