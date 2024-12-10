# Generated by Django 4.2.16 on 2024-12-10 12:39

from django.db import migrations

def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('user_profile', 'Profile')
    for user in User.objects.all():
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, name=user.username)

class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_profile_contact_phone_alter_profile_name_and_more'),
    ]

    operations = [
        migrations.RunPython(create_profiles),
    ]
