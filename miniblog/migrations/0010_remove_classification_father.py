# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0009_classification_father'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classification',
            name='father',
        ),
    ]
