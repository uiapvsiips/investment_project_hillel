# Generated by Django 4.2 on 2023-04-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_money', models.IntegerField()),
                ('max_money', models.IntegerField()),
                ('percent_for_day', models.FloatField()),
                ('term', models.IntegerField()),
            ],
        ),
    ]
