# -*- coding: UTF-8 -*-
# Copyright 2020-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
import json
from django.conf import settings
from django.utils.timezone import now
from lino.api import rt, dd
from lino.modlib.linod.utils import CHANNEL_NAME, BROADCAST_CHANNEL, get_channel_name

NOTIFICATION = "NOTIFICATION"
CHAT = "CHAT"
LIVE_PANEL_UPDATE = "PANEL_UPDATE"

NOTIFICATION_TYPES = [NOTIFICATION, CHAT, LIVE_PANEL_UPDATE]


# def send_panel_update(actorIDs: list[str], pk: int):
def send_panel_update(data):
    """
    API function to send live panel update to react UI

    :param list[str] actorIDs: actor id(s) for the panels that should be updated
    :param typing.Union[int, None] pk: id of the database row that has been modified
    """
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()

    data.update(type=LIVE_PANEL_UPDATE)

    try:
        async_to_sync(channel_layer.send)(
            CHANNEL_NAME, {"type": "send.panel.update", "text": json.dumps(data)}
        )
    except Exception as e:
        logger.exception(e)


def send_notification(
    user=None,
    primary_key=None,
    subject=None,
    body=None,
    created=None,
    action_url=None,
    action_title="OK",
):
    """

    `action_url` : the URL to show when user clicks on the
    OK button of their desktop notification.

    """
    if user is None:
        return

    created = created.strftime("%a %d %b %Y %H:%M")

    if dd.get_plugin_setting("linod", "use_channels"):
        # importing channels at module level would cause certain things to fail
        # when channels isn't installed, e.g. `manage.py prep` in `lino_book.projects.workflows`.
        from channels.layers import get_channel_layer
        from channels.exceptions import ChannelFull
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()

        msg = dict(
            type=NOTIFICATION,
            subject=subject,
            id=primary_key,
            body=body,
            created=created,
            action_url=action_url,
        )

        try:
            async_to_sync(channel_layer.group_send)(
                get_channel_name(user.id),
                {
                    "type": "send.notification",  # method name in consumer
                    "text": json.dumps(msg),
                },
            )  # data
        except Exception as e:
            logger.exception(e)

        if dd.plugins.notify.use_push_api:
            data = dict(
                action_url=action_url,
                subject=subject,
                body=body,
                action_title=action_title,
            )
            try:
                async_to_sync(channel_layer.send)(
                    CHANNEL_NAME,
                    {
                        "type": "send.push",
                        "data": data,
                        "user_id": user.id if user is not None else None,
                    },
                )
            except (
                ChannelFull
            ) as e:  # happens on older Pythons and can cause many tracebacks
                # logger.exception(e)
                # logger.warning(str(e))
                pass
