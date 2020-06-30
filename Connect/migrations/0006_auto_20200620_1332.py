# Generated by Django 3.0.7 on 2020-06-20 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Connect', '0005_auto_20200616_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connections',
            name='status',
            field=models.CharField(blank=True, default='sent', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userdatabase',
            name='name',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.CreateModel(
            name='Company_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('number', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]