# Generated by Django 4.0.6 on 2023-03-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='first_assign_user',
            field=models.TextField(default='0', null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='second_assign_user',
            field=models.TextField(default='0', null=True),
        ),
    ]
