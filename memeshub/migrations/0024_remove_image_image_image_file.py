# Generated by Django 4.2 on 2024-06-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memeshub', '0023_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]