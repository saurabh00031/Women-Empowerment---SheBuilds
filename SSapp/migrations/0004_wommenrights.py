# Generated by Django 4.1.1 on 2023-01-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SSapp', '0003_alter_schollershiplist_body_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WommenRights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(max_length=1500)),
            ],
        ),
    ]