# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-11 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_dashboard', '0008_auto_20180904_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='hezuodanwei',
            field=models.CharField(blank=True, help_text='\u9879\u76ee\u5408\u4f5c\u5355\u4f4d', max_length=256, null=True, verbose_name='\u9879\u76ee\u5408\u4f5c\u5355\u4f4d'),
        ),
    ]
