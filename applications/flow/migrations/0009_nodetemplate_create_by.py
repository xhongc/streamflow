# Generated by Django 2.2.6 on 2022-10-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0008_nodetemplate_coding'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodetemplate',
            name='create_by',
            field=models.CharField(default='', max_length=255, verbose_name='创建人'),
        ),
    ]
