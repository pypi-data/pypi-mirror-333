# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Emit a broadcast notification "The database has been initialized."

"""

import datetime
from django.utils import translation
from lino.utils import i2t
from lino.api import dd, rt, _

from django.conf import settings
from django.utils.timezone import make_aware


def objects():
    now = datetime.datetime.combine(dd.today(), i2t(548))
    if settings.USE_TZ:
        now = make_aware(now)
    mt = rt.models.notify.MessageTypes.system

    rt.models.notify.Message.emit_broadcast_notification(
        "The database has been initialized.", message_type=mt, created=now
    )
    # return []
    for u in rt.models.users.User.objects.exclude(first_name="").order_by('username'):
        with translation.override(u.language):
            yield rt.models.notify.Message.create_message(
                u, subject=_("Welcome on board, {}.").format(u.first_name),
                mail_mode=u.mail_mode, created=now, message_type=mt,
                sent=now)
            # print("20240710", u, u.language)
