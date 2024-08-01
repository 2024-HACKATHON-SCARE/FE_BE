# Generated by Django 5.0.7 on 2024-07-20 13:16

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='default_mypage_image.jpg', upload_to=accounts.models.upload_filepath),
        ),
    ]
