# Generated by Django 2.0.7 on 2020-01-20 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_message_sign_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('user', 'user_key')},
        ),
    ]