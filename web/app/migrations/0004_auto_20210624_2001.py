# Generated by Django 3.2.4 on 2021-06-24 20:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_journalarticle_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalarticle',
            name='text',
        ),
        migrations.AddField(
            model_name='journalarticle',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
