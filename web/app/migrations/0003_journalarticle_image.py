# Generated by Django 3.2.4 on 2021-06-24 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_journalarticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalarticle',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
