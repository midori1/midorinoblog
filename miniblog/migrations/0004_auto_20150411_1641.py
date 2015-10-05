# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0003_auto_20150411_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(blank=True, to='miniblog.Classification', null=True),
            preserve_default=True,
        ),
    ]
