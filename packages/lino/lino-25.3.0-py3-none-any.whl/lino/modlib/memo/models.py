# -*- coding: UTF-8 -*-
# Copyright 2023-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from PIL.Image import open as imgopen
from typing import overload
from django.contrib.contenttypes.models import ContentType
from django.utils.text import format_lazy

# from rstgen.sphinxconf.sigal_image import line2html
from lino.api import dd, rt, _
from lino.core import constants
from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField
from .parser import split_name_rest
# from .mixins import *

# Translators: will also be concatenated with '(type)' and '(object)'
target_label = _("Target")


class Mention(Controllable):
    class Meta(object):
        app_label = "memo"
        abstract = dd.is_abstract_model(__name__, "Mention")
        verbose_name = _("Mention")
        verbose_name_plural = _("Mentions")

    target_type = dd.ForeignKey(
        ContentType,
        editable=True,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_target_set",
        verbose_name=format_lazy("{} {}", target_label, _("(type)")),
    )

    target_id = GenericForeignKeyIdField(
        target_type,
        editable=True,
        blank=True,
        null=True,
        verbose_name=format_lazy("{} {}", target_label, _("(object)")),
    )

    target = GenericForeignKey("target_type", "target_id", verbose_name=target_label)

    # quick_search_fields = "target"
    # django.core.exceptions.FieldError: Field 'target' does not generate an
    # automatic reverse relation and therefore cannot be used for reverse
    # querying. If it is a GenericForeignKey, consider adding a GenericRelation.

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "target_type"
        yield "target_id"

    def as_summary_item(self, ar, text=None, **kwargs):
        # raise Exception("20240613")
        if ar is None:
            obj = super()
        elif ar.is_obvious_field('target'):
            obj = self.owner
        elif ar.is_obvious_field('owner'):
            obj = self.target
        else:
            obj = super()
        return obj.as_summary_item(ar, text, **kwargs)

dd.update_field(Mention, 'owner', verbose_name=_("Referrer"))

class Mentions(dd.Table):
    required_roles = dd.login_required(SiteStaff)
    editable = False
    model = "memo.Mention"
    column_names = "owner target *"
    # detail_layout = """
    # id comment owner created
    # """

# Not used because when you are on the owner, you can see the mentions in the memo text
# class MentionsByOwner(Mentions):
#     label = _("Mentions")
#     master_key = "owner"
#     column_names = "target *"
#     default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

class MentionsByTarget(Mentions):
    label = _("Mentioned by")
    master_key = "target"
    column_names = "owner *"
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
