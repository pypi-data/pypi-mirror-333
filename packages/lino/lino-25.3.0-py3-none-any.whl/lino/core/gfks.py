# Copyright 2010-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Helper methods for GenericForeignKey

"""

from django.conf import settings
from django.db.models import Model, ForeignKey
# from lino.utils import MissingRow

if settings.SITE.is_installed("contenttypes"):
    from lino.modlib.gfks.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.contenttypes.fields import (
        GenericForeignKey as DjangoGenericForeignKey,
    )

    from django.contrib.contenttypes.fields import GenericRelation, GenericRel

    def is_foreignkey(fld):
        return isinstance(fld, (ForeignKey, DjangoGenericForeignKey))
else:
    from lino.core.utils import UnresolvedField, UnresolvedModel

    GenericForeignKey = UnresolvedField
    ContentType = UnresolvedModel
    GenericRelation = UnresolvedField
    GenericRel = UnresolvedField

    def is_foreignkey(fld):
        return isinstance(fld, ForeignKey)


def gfk2lookup(gfk, obj, **kw):
    """
    Return a `dict` with the lookup keywords for the given
    GenericForeignKey field `gfk` on the given database object `obj`.

    If `obj` has a non-integer primary key, only the `ct_field` is
    set.

    See also :ref:`book.specs.gfks`.
    """
    if isinstance(obj, Model):
        assert not obj._meta.abstract
        ct = ContentType.objects.get_for_model(obj.__class__)
        kw[gfk.ct_field] = ct
        if not isinstance(obj.pk, int):
            # IntegerField gives `long` when using MySQL
            return kw
        kw[gfk.fk_field] = obj.pk
    else:
        # 20120222 : here was only `pass`, and the two other lines
        # were uncommented. don't remember why I commented them out.
        # But it caused all tasks to appear in UploadsByController of
        # an insert window for uploads.
        kw[gfk.ct_field] = None
        kw[gfk.fk_field] = None
    return kw
