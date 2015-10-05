# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0011_classification_father'),
    ]

    operations = [
        migrations.CreateModel(
            name='RootClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='classification',
            name='father',
            field=models.ForeignKey(to='miniblog.RootClassification'),
            preserve_default=True,
        ),
    ]
