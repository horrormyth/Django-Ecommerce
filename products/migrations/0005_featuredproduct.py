# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20180106_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=products.models.image_upload_to_featured)),
                ('title', models.CharField(max_length=120, null=True, blank=True)),
                ('text', models.CharField(max_length=220, null=True, blank=True)),
                ('text_right', models.BooleanField(default=False)),
                ('show_price', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
    ]
