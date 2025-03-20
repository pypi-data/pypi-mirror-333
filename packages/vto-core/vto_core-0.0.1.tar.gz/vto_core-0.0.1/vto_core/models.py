'''
REFERENCES:

https://github.com/django/django/blob/5a1cae3a5675c5733daf5949759476d65aa0e636/django/contrib/auth/models.py#L471C1-L475C6
'''

# import zoneinfo
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import PositiveSmallIntegerField as PSInt
from djinntoux.abstract.ab_mod import UUIDpk7
# from timezone_field import TimeZoneField

'''
    more info:
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
'''


class TZAbbreviation(UUIDpk7):

    identifier = models.CharField(max_length=30, unique=True,
        help_text='Central European Summer Time')

    offset = models.CharField(max_length=6, help_text='+02:00')

    abbr = models.CharField(max_length=4, unique=True, help_text='CEST')

    class Meta:
        ordering = ['offset']
        verbose_name = 'Time zone abbreviation'
        verbose_name_plural = 'Tme zone abbreviations'

    def __str__(self):
        return self.abbr


class TimeZone(UUIDpk7):

    identifier = models.CharField(max_length=20, unique=True,
        help_text='America/New_York')

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

    # nullable, as some zones may not observe DST
    dst = models.ForeignKey('TZAbbreviation', on_delete=models.PROTECT,
        related_name='rn_tz_abbr_dst', null=True, blank=True)

    class Meta:
        ordering = ['identifier']
        verbose_name = 'IANA time zone'
        verbose_name_plural = 'IANA time zones'

    def __str__(self):
        return self.identifier


class User(UUIDpk7, AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    surname = models.CharField(blank=True, max_length=150)
    given_names = models.CharField(blank=True, max_length=150)
    surname_first = models.BooleanField(default=False)

    # timezone = TimeZoneField(default='America/New_York')
    # timezone = models.CharField(max_length=40, default='America/New_York')
    timezone = models.ForeignKey('TimeZone', on_delete=models.PROTECT,
        null=True, blank=True)

    # override verbose name in admin change list
    # do I need to make a new migration?
    is_staff = models.BooleanField(verbose_name='Staff', default=False,
        help_text='Designates whether the user can log into this admin site.')

    # override verbose name in admin change list
    # do I need to make a new migration?
    is_superuser = models.BooleanField(verbose_name='Super', default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.')

    class Meta:
        ordering = ['-is_superuser', 'username']  # added

    def get_short_name(self):
        """Return the short name for the user."""
        return self.given_names

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.surname_first:
            full_name = "%s %s" % (self.surname, self.given_names)
        else:
            full_name = "%s %s" % (self.given_names, self.surname)
        return full_name.strip()