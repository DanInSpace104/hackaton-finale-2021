# Generated by Django 3.2.9 on 2021-12-05 04:39

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0013_rename_name_transportationlog_name_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarriagePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriage_photo', stdimage.models.StdImageField(blank=True, null=True, upload_to='carriage')),
                ('carriage_quality_photo', stdimage.models.StdImageField(blank=True, null=True, upload_to='carriage_quality')),
                ('carriage', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carriage', to='operators.transportationcarriagelog')),
            ],
        ),
    ]
