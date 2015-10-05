# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('tag_line', models.CharField(max_length=100)),
                ('entries_per_page', models.IntegerField(default=10)),
                ('recents', models.IntegerField(default=5)),
                ('recent_comments', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('text', markupfield.fields.MarkupField(rendered_field=True)),
                ('text_markup_type', models.CharField(max_length=30, default='plain', choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain')])),
                ('summary', models.TextField()),
                ('_text_rendered', models.TextField(editable=False)),
                ('created_on', models.DateTimeField(editable=False, default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999))),
                ('is_page', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('publish_date', models.DateTimeField(null=True)),
                ('comments_allowed', models.BooleanField(default=True)),
                ('is_rte', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Blog entries',
            },
        ),
    ]
