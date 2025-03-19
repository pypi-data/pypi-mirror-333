from django.db import models
from django.db.models import PositiveSmallIntegerField as PSInt
from djinntoux.abstract.ab_mod import UUIDpk7

'''
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

https://en.wikipedia.org/wiki/Central_European_Time
'''

class TZAbbreviation(UUIDpk7):

    abbr = models.CharField(max_length=4, unique=True, help_text='CEST')

    identifier = models.CharField(max_length=30, unique=True,
        help_text='Central European Summer Time')

    offset = models.CharField(max_length=6, help_text='+02:00')

    class Meta:
        ordering = ['offset']

    def __str__(self):
        return self.abbr


class TimeZone(UUIDpk7):

    identifier = models.CharField(max_length=20, unique=True,
        help_text='America/New_York')

    # weight = PSInt(default=9999)

    class TZType(models.IntegerChoices):
        CAN = 1, 'canonical'
        LNK = 2, 'link (alias)'
        LKP = 3, 'link, previously canonical'

    tz_type = PSInt(choices=TZType.choices, default=TZType.CAN)

    class SrcFile(models.IntegerChoices):
        FAC = 1, 'factory'
        ETC = 2, 'etcetera'
        BAC = 3, 'backward'
        EUR = 4, 'europe'
        ASI = 5, 'asia'
        AUS = 6, 'australasia'
        NAM = 7, 'northamerica'
        SAM = 8, 'southamerica'
        AFR = 9, 'africa'
        ANT = 10, 'antarctica'

    src_file = PSInt(choices=SrcFile.choices, default=SrcFile.NAM)

    aliases = models.CharField(max_length=30, unique=True,
        help_text='US/Eastern, EST5EDT', null=True, blank=True)

    std = models.ForeignKey('TZAbbreviation', on_delete=models.PROTECT,
        related_name='rn_tz_abbr_std')

    dst = models.ForeignKey('TZAbbreviation', on_delete=models.PROTECT,
        related_name='rn_tz_abbr_dst', null=True, blank=True)

    class Meta:
        ordering = ['identifier']

    def __str__(self):
        return self.identifier
