# Generated by Django 4.0 on 2023-01-21 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_course_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='idUser',
            field=models.IntegerField(null=True),
        ),
    ]
