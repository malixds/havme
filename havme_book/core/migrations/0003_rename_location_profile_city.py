# Generated by Django 4.2 on 2023-04-14 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_post_profile_age_profile_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location',
            new_name='city',
        ),
    ]
