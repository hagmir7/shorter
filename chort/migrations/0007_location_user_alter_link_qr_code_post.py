# Generated by Django 4.1.7 on 2023-02-21 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chort', '0006_alter_link_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='link',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='QRCode'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, default='d_post.webp', null=True, upload_to='Post')),
                ('body', models.TextField()),
                ('tags', models.CharField(blank=True, max_length=150, null=True)),
                ('is_page', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
