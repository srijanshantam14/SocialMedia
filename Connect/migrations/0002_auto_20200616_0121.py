# Generated by Django 3.0.7 on 2020-06-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatabase',
            name='Degree',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='company',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='experience',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='location',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='website',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
    ]
