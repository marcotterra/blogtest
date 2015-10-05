# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogentry',
            name='_text_rendered',
        ),
        migrations.RemoveField(
            model_name='blogentry',
            name='text_markup_type',
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='text',
            field=models.TextField(),
        ),
    ]
