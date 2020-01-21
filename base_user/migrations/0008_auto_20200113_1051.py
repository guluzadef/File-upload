# Generated by Django 3.0.2 on 2020-01-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0007_auto_20191005_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='user_type',
        ),
        migrations.AddField(
            model_name='myuser',
            name='facebook',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='instagram',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='twitter',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
