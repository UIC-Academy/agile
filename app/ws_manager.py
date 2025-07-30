import asyncio

from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self._connections = dict[int, WebSocket]
        self.lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()

        async with self.lock():
            self._connections[user_id] = websocket

    async def disconnect(self, user_id):
        async with self.lock():
            self._connections.pop(user_id)

    async def send_to_user(self, user_id: int, message: dict):
        websocket = self._connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception:
                await self.disconnect(user_id)

    async def broadcast_to_users(self, user_ids: list[int], message: dict):
        for uid in user_ids:
            await self.send_to_user(uid, message)

    async def broadcast_to_all(self, message: dict):
        for uid in self._connections:
            await self.send_to_user(uid, message)
