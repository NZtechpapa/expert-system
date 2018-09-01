# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-20 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_dashboard', '0003_auto_20180820_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertdomain',
            name='domainname',
            field=models.CharField(blank=True, choices=[('\u56fd\u5bb6\u79d1\u6280\u90e8\u9886\u57df', [['\u6570\u5b66', '\u6570\u5b66'], ['A001 \u6570\u5b66\u4e00\u7ea7', 'A001 \u6570\u5b66\u4e00\u7ea7'], ['A0001 \u6570\u5b66\u4e8c\u7ea7', 'A0001 \u6570\u5b66\u4e8c\u7ea7'], ['A0002 \u6570\u5b66\u4e8c\u7ea7', 'A0002 \u6570\u5b66\u4e8c\u7ea7'], ['A002 \u6570\u5b66\u4e00\u7ea7', 'A002 \u6570\u5b66\u4e00\u7ea7'], ['A0001 \u6570\u5b66\u4e8c\u7ea7', 'A0001 \u6570\u5b66\u4e8c\u7ea7'], ['\u4fe1\u606f\u79d1\u5b66\u4e0e\u7cfb\u7edf\u79d1\u5b66', '\u4fe1\u606f\u79d1\u5b66\u4e0e\u7cfb\u7edf\u79d1\u5b66'], ['\u7269\u7406\u5b66', '\u7269\u7406\u5b66'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11', '11'], ['12', '12'], ['13', '13'], ['14', '14'], ['15', '15'], ['16', '16'], ['17', '17'], ['18', '18'], ['19', '19']]), ('\u56fd\u5bb6\u57fa\u91d1\u59d4\u9886\u57df', [['\u6570\u7406\u79d1\u5b66', '\u6570\u7406\u79d1\u5b66'], ['\u5316\u5b66\u79d1\u5b66', '\u5316\u5b66\u79d1\u5b66'], ['\u751f\u547d\u79d1\u5b66', '\u751f\u547d\u79d1\u5b66']])], help_text='\u5728\u8be5\u7814\u7a76\u9886\u57df\u7814\u7a76\u7684\u5b66\u79d1\u540d\u79f0', max_length=32, verbose_name='*\u5b66\u79d1\u540d\u79f0'),
        ),
    ]