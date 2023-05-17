from __future__ import absolute_import, unicode_literals
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geef.settings')
import django
django.setup()

from contracts.models import *

if __name__ == '__main__':
    if len(Contracts.objects.all())==0:
        Contracts.objects.create(name='Contract1', en_name='Contract1', min_money=100, max_money=1000,
                                 percent_for_day=0.3, term=365, show_to_all=True)
        Contracts.objects.create(name='Contract2', en_name='Contract2', min_money=1001, max_money=2000,
                                             percent_for_day=0.5, term=365, show_to_all=True)
        Contracts.objects.create(name='Contract3', en_name='Contract3', min_money=2001, max_money=5000,
                                 percent_for_day=0.7, term=365, show_to_all=True)
