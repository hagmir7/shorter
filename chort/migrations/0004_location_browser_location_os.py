# Generated by Django 4.1.7 on 2023-02-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chort', '0003_location_view_delete_ipaddress_link_user_view_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='browser',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='os',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]