import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class CollabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", "default_room")
        self.room_group_name = f"collab_{self.room_name}"

        # Reject anonymous users
        if user.is_anonymous:
            await self.close()
            logger.warning("Anonymous user tried to connect to WebSocket")
            return

        # Add this channel to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"{user.email} connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        # Remove channel from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        user = self.scope.get("user")
        logger.info(f"{user.email} disconnected from {self.room_group_name}")

    async def receive(self, text_data):
        """
        Receive JSON message from WebSocket client and broadcast to group
        """
        user = self.scope.get("user")

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            logger.error(f"{user.email} sent invalid JSON: {text_data}")
            return

        # Optionally validate data keys
        message = data.get("message")
        if not message:
            await self.send(text_data=json.dumps({"error": "Missing 'message' field"}))
            return

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "collab_message",
                "user": user.full_name,
                "message": message,
            }
        )

    async def collab_message(self, event):
        """
        Handler for messages sent to the group
        """
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "message": event["message"],
        }))
