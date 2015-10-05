# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0006_remove_classification_father'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='father',
            field=models.ForeignKey(default=None, to='miniblog.Classification'),
            preserve_default=False,
        ),
    ]
