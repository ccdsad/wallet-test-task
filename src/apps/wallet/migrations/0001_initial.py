# Generated by Django 5.0.7 on 2024-07-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='WalletModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=256)),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
