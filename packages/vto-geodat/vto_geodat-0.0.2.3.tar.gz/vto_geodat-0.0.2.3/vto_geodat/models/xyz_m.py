from django.db import models
from django.db.models import PositiveSmallIntegerField as PSInt
from djinntoux.abstract.ab_mod import UUIDpk7


# class FirstLevelAdminDivision(UUIDpk7):

class MacroZone(UUIDpk7):

    identifier = models.CharField(max_length=30, unique=True,
        help_text='North America, Caribbean, Eurasia')

    class Meta:
        ordering = ['identifier']

    def __str__(self):
        return self.identifier


class Term(UUIDpk7):

    identifier = models.CharField(max_length=30, unique=True,
        help_text='autonomous community (Spain)')

    '''class AdminDivLevel(models.IntegerChoices):
        FST = 1, 'first'
        SND = 2, 'second'
        TRD = 3, 'third'
        FOR = 4, 'fourth'
        FIF = 5, 'fifth'

    administrative_division_level = PSInt(AdmDivLvl=AdminDivLevel.choices,
        default=AdminDivLevel.FST, verbose_name='AdDvLv')'''

    class Meta:
        ordering = ['identifier']

    def __str__(self):
        return self.identifier


class QuasiNation(UUIDpk7):

    # continent = PSInt(Continent=Radius.choices, default=Continent.NAM)

    identifier = models.CharField(max_length=20, unique=True)

    code = models.CharField(max_length=2, unique=True, help_text='FR')

    abbr = models.CharField(max_length=8, unique=True, help_text='FR (eur)')

    class Meta:
        ordering = ['identifier']

    def __str__(self):
        return self.identifier

    def save(self, *args, **kwargs):
        if not self.abbr:
            self.abbr = self.code
        super(QuasiNation, self).save(*args, **kwargs)


class Settlement(UUIDpk7):

    identifier = models.CharField(max_length=20, unique=True)

    tz = models.ForeignKey('vda_tz.TimeZone', on_delete=models.PROTECT)

    class Meta:
        ordering = ['identifier']

    def __str__(self):
        return self.identifier
