# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase

# Create your tests here.
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ihome.settings.dev")

django.setup()

if __name__ == '__main__':

    day01 = datetime.datetime.strptime('2019-01-01','%Y-%m-%d')
    day02 = datetime.datetime.strptime('2019-02-03','%Y-%m-%d')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%I:%S'))
    print((day02-day01).days)