# Generated by Django 2.2 on 2019-04-14 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='email',
            field=models.CharField(default='abc@gmail.com', max_length=50),
        ),
    ]
