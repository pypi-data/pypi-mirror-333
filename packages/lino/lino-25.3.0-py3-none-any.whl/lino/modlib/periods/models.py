# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.api import dd
from lino import mixins
from lino.utils import ONE_DAY
from lino.mixins.periods import DateRange
from lino.mixins import Referrable
from lino.modlib.system.choicelists import DurationUnits
from lino.modlib.office.roles import OfficeStaff
from .choicelists import PeriodTypes, PeriodStates

NEXT_YEAR_SEP = "/"
YEAR_PERIOD_SEP = "-"



class StoredYear(DateRange, Referrable):

    class Meta:
        app_label = 'periods'
        verbose_name = dd.plugins.periods.year_name
        verbose_name_plural = dd.plugins.periods.year_name_plural
        ordering = ['ref']

    preferred_foreignkey_width = 10

    state = PeriodStates.field(default='open')

    @classmethod
    def get_simple_parameters(cls):
        yield super().get_simple_parameters()
        yield "state"

    @classmethod
    def get_ref_for_date(cls, date):
        year = date.year
        if date.month < dd.plugins.periods.start_month:
            year -= 1
        if dd.plugins.periods.fix_y2k:
            if year < 2000:
                return str(year)[-2:]
            elif year < 3000:
                return chr(int(str(year)[-3:-1]) + 65) + str(year)[-1]
            else:
                raise Exception("fix_y2k not supported after 2999")
        elif dd.plugins.periods.short_ref:
            if dd.plugins.periods.start_month == 1:
                return str(year)[-2:]
            return str(year)[-2:] + NEXT_YEAR_SEP + str(year+1)[-2:]
        elif dd.plugins.periods.start_month == 1:
            return str(year)
        return str(year) + NEXT_YEAR_SEP + str(year+1)[-2:]

    @classmethod
    def get_range_for_date(cls, date):
        month = date.month
        year = date.year
        month -= dd.plugins.periods.start_month - 1
        if month < 1:
            year -= 1
        sd = datetime.date(year, dd.plugins.periods.start_month, 1)
        ed = sd.replace(year=year+1) - ONE_DAY
        return (sd, ed)

    @classmethod
    def get_or_create_from_date(cls, date, save=True):
        ref = cls.get_ref_for_date(date)
        obj = cls.get_by_ref(ref, None)
        if obj is None:
            sd, ed = cls.get_range_for_date(date)
            obj = cls(ref=ref, start_date=sd, end_date=ed)
            if save:
                obj.full_clean()
                obj.save()
        return obj

    def __str__(self):
        return self.ref


class StoredPeriod(DateRange, Referrable):

    class Meta:
        ordering = ['ref']
        app_label = 'periods'
        verbose_name = dd.plugins.periods.period_name
        verbose_name_plural = dd.plugins.periods.period_name_plural

    preferred_foreignkey_width = 10

    state = PeriodStates.field(default='open')
    year = dd.ForeignKey('periods.StoredYear', blank=True, null=True, related_name="periods")
    remark = models.CharField(_("Remark"), max_length=250, blank=True)

    @classmethod
    def get_simple_parameters(cls):
        yield super().get_simple_parameters()
        yield "state"
        yield "year"

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super().get_request_queryset(ar)
        if (pv := ar.param_values) is None: return qs

        # if pv.start_date is None or pv.end_date is None:
        #     period = None
        # else:
        #     period = (pv.start_date, pv.end_date)
        # if period is not None:
        #     qs = qs.filter(dd.inrange_filter('start_date', period))
        if pv.start_date or pv.end_date:
            qs = qs.filter(dd.overlap_range_filter(
                pv.start_date, pv.end_date, "start_date", "end_date"))
        # if pv.start_date:
        #     qs = qs.filter(dd.range_filter(pv.start_date, 'start_date', 'end_date'))
        #     # qs = qs.filter(start_date__gte=pv.start_date)
        # if pv.end_date:
        #     qs = qs.filter(dd.range_filter(pv.end_date, 'start_date', 'end_date'))
            # qs = qs.filter(end_date__lte=pv.end_date)
        return qs

    @classmethod
    def get_available_periods(cls, today):
        """Return a queryset of periods available for booking."""
        if today is None:  # added 20160531
            today = dd.today()
        fkw = dict(start_date__lte=today, end_date__gte=today)
        return cls.objects.filter(**fkw)

    @classmethod
    def get_periods_in_range(cls, p1, p2):
        return cls.objects.filter(ref__gte=p1.ref, ref__lte=p2.ref)

    @classmethod
    def get_period_filter(cls, fieldname, p1, p2, **kwargs):
        if p1 is None:
            return kwargs

        # ignore preliminary movements if a start_period is given:
        # kwargs[voucher_prefix + "journal__preliminary"] = False

        # accounting_period = voucher_prefix + "accounting_period"

        if p2 is None:
            kwargs[fieldname] = p1
        else:
            periods = cls.get_periods_in_range(p1, p2)
            kwargs[fieldname + '__in'] = periods
        return kwargs

    @classmethod
    def get_ref_for_date(cls, date):
        pt = dd.plugins.periods.period_type
        month = date.month
        month_offset = month - dd.plugins.periods.start_month
        if month_offset < 0:
            month_offset += 12
        period = int(month_offset / pt.duration) + 1
        # periods_per_year = int(12 / p.duration)
        # period = (month_offset % (periods_per_year-1)) + 1
        return pt.ref_template.format(**locals())

    @classmethod
    def get_range_for_date(cls, date):
        """
        Return the default start and end date of the period to create for the given
        date.
        """
        pt = dd.plugins.periods.period_type
        month = date.month
        year = date.year
        month -= dd.plugins.periods.start_month
        if month < 1:
            month += 12
            year -= 1
        period = int(month / pt.duration)
        month = dd.plugins.periods.start_month + period * pt.duration
        if month > 12:
            month -= 12
            year += 1
        sd = datetime.date(year, month, 1)
        # ed = sd.replace(month=sd.month + pt.duration + 1, 1) - ONE_DAY
        ed = DurationUnits.months.add_duration(sd, pt.duration) - ONE_DAY
        return (sd, ed)

    @classmethod
    def get_or_create_from_date(cls, date):  # get_default_for_date until 20241020
        ref = date2ref(date)
        obj = cls.get_by_ref(ref, None)
        if obj is None:
            sd, ed = cls.get_range_for_date(date)
            obj = cls(ref=ref, start_date=sd, end_date=ed)
            obj.full_clean()
            obj.save()
        return obj

    def full_clean(self, *args, **kwargs):
        if self.start_date is None:
            self.start_date = dd.today().replace(day=1)
        if not self.year_id:
            self.year = StoredYear.get_or_create_from_date(self.start_date)
        super().full_clean(*args, **kwargs)

    def __str__(self):
        if not self.ref:
            return dd.obj2str(self)
            # "{0} {1} (#{0})".format(self.pk, self.year)
        return self.ref

    # def get_str_words(self, ar):
    #     # if ar.is_obvious_field("year"):
    #     if self.year.covers_date(dd.today()):
    #         # yield self.nickname
    #         yield f"{dd.plugins.periods.period_name} {self.nickname}"
    #     else:
    #         yield str(self)

    @property
    def nickname(self):
        if self.year.covers_date(dd.today()):
            if self.ref and len(parts := self.ref.split(YEAR_PERIOD_SEP)) == 2:
                # return "{} {}".format(dd.plugins.periods.period_name, parts[1])
                return parts[1]
        return self.ref

StoredPeriod.set_widget_options('ref', width=6)

def date2ref(d):
    return StoredYear.get_ref_for_date(d) + YEAR_PERIOD_SEP + StoredPeriod.get_ref_for_date(d)

class StoredYears(dd.Table):
    model = 'periods.StoredYear'
    required_roles = dd.login_required(OfficeStaff)
    column_names = "ref start_date end_date state *"
    # detail_layout = """
    # ref id
    # start_date end_date
    # """

class StoredPeriods(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = 'periods.StoredPeriod'
    order_by = ["ref", "start_date", "year"]
    column_names = "ref start_date end_date year state remark *"
