# Generated by Django 2.2.1 on 2019-05-16 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='songs',
            name='album',
            field=models.CharField(default='New Album', max_length=255),
        ),
    ]
