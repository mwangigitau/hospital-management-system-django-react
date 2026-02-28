"""
Central HMS WebSocket consumer.

A single endpoint (ws/hms/) serves all real-time needs:
  • Every authenticated client joins:
      - `broadcast`        – hospital-wide events visible to all staff
      - `user_<id>`        – personal notifications for that user
  • Clients can subscribe to per-app groups by sending
      {"type": "subscribe", "app": "<app_name>"}
    This lets the frontend only process the events it cares about,
    though broadcast group events are always forwarded.

Message shapes from server → client
────────────────────────────────────
data.update  (data changed in a model)
{
  "type": "data.update",
  "app": "patients",
  "model": "Patient",
  "action": "created" | "updated" | "deleted",
  "object_id": "<uuid>",
  "summary": {<lightweight key fields>},
  "notification": {"title": "...", "message": "...", "level": "success|info|warning|error"},
  "timestamp": "<ISO-8601>"
}

notification  (personal or broadcast alert)
{
  "type": "notification",
  "title": "...",
  "message": "...",
  "level": "info",
  "timestamp": "<ISO-8601>"
}
"""
import json

from channels.generic.websocket import AsyncWebsocketConsumer

# Apps that can be subscribed to individually
VALID_APPS = frozenset({
    'patients', 'adt', 'appointments', 'clinical',
    'nursing', 'pharmacy', 'inventory', 'laboratory', 'billing',
})


class HMSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.user = user
        self.user_group = f'user_{user.id}'
        self.subscribed_groups: set[str] = set()

        # Always join the personal group and the hospital-wide broadcast group
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.channel_layer.group_add('broadcast', self.channel_name)

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connected',
            'user_id': str(user.id),
            'username': user.username,
        }))

    async def disconnect(self, close_code):
        if not hasattr(self, 'user_group'):
            return
        await self.channel_layer.group_discard(self.user_group, self.channel_name)
        await self.channel_layer.group_discard('broadcast', self.channel_name)
        for group in self.subscribed_groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        msg_type = data.get('type')

        if msg_type == 'subscribe':
            app = data.get('app', '').strip()
            if app in VALID_APPS:
                group = f'app_{app}'
                if group not in self.subscribed_groups:
                    await self.channel_layer.group_add(group, self.channel_name)
                    self.subscribed_groups.add(group)
                await self.send(text_data=json.dumps({'type': 'subscribed', 'app': app}))

        elif msg_type == 'unsubscribe':
            app = data.get('app', '').strip()
            group = f'app_{app}'
            if group in self.subscribed_groups:
                await self.channel_layer.group_discard(group, self.channel_name)
                self.subscribed_groups.discard(group)

        elif msg_type == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))

    # ── Handlers called by channel layer group_send ──────────────────────────

    async def data_update(self, event):
        """Forward a data-change event to the connected client."""
        await self.send(text_data=json.dumps(event['payload']))

    async def send_notification(self, event):
        """Forward a personal notification to the connected client."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            **event['notification'],
        }))
