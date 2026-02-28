"""
Lightweight broadcast helpers used by app signals.

These helpers are intentionally synchronous so they can be called from
Django signal handlers (which run in the ORM's synchronous context).
If the channel layer is unavailable (Redis down) the call is silently
swallowed so that a Redis outage never breaks a database write.
"""
from datetime import datetime, timezone

from asgiref.sync import async_to_sync


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def broadcast_event(
    *,
    app: str,
    model: str,
    action: str,
    object_id: str,
    summary: dict,
    notification: dict | None = None,
) -> None:
    """
    Broadcast a model-change event to:
      - the global `broadcast` group (all connected users)
      - the per-app `app_<app>` group (users subscribed to that app)

    Parameters
    ----------
    app:          app label, e.g. "patients"
    model:        model class name, e.g. "Patient"
    action:       "created", "updated", or "deleted"
    object_id:    string UUID of the changed instance
    summary:      small dict with human-readable key fields (no FK objects)
    notification: optional dict with keys title, message, level
    """
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        'type': 'data.update',
        'app': app,
        'model': model,
        'action': action,
        'object_id': object_id,
        'summary': summary,
        'notification': notification,
        'timestamp': _now_iso(),
    }

    # channels layer `type` key must use underscores (maps to consumer method)
    message = {'type': 'data_update', 'payload': payload}

    try:
        send = async_to_sync(channel_layer.group_send)
        send('broadcast', message)
        send(f'app_{app}', message)
    except Exception:
        # Never let a Redis / channel-layer failure propagate into a DB save
        pass


def broadcast_notification(
    *,
    user_id: str,
    title: str,
    message: str,
    level: str = 'info',
    extra: dict | None = None,
) -> None:
    """Send a personal notification directly to one user's WebSocket."""
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    msg = {
        'type': 'send_notification',
        'notification': {
            'title': title,
            'message': message,
            'level': level,
            'extra': extra or {},
            'timestamp': _now_iso(),
        },
    }
    try:
        async_to_sync(channel_layer.group_send)(f'user_{user_id}', msg)
    except Exception:
        pass
