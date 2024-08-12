# Generated by Django 5.0.7 on 2024-08-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximaapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('pdetails', models.CharField(max_length=100)),
                ('cat', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='msg',
        ),
    ]
