# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_useraddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address_type',
            field=models.CharField(max_length=120, choices=[(b'billing', b'Billing'), (b'shipping', b'Shipping')]),
        ),
    ]
