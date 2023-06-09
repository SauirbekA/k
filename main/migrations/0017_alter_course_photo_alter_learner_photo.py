# Generated by Django 4.0 on 2023-01-27 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_learner_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='photo',
            field=models.ImageField(blank=True, default='default/anonymous-user.png', upload_to='photos/courses'),
        ),
        migrations.AlterField(
            model_name='learner',
            name='photo',
            field=models.FileField(blank=True, default='default/anonymous-user.png', null=True, upload_to='photos/users/'),
        ),
    ]
