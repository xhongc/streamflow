# Generated by Django 2.2.6 on 2022-09-22 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_auto_20220921_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='fail_count',
            field=models.IntegerField(default=0, verbose_name='失败执行次数'),
        ),
        migrations.AddField(
            model_name='task',
            name='success_count',
            field=models.IntegerField(default=0, verbose_name='成功执行次数'),
        ),
    ]
