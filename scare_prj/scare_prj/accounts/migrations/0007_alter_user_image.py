# Generated by Django 5.0.7 on 2024-07-20 13:25

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='media/default_mypage_image.jpg', upload_to=accounts.models.upload_filepath),
        ),
    ]
