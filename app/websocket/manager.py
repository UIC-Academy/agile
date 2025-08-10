import asyncio
from collections import defaultdict

from fastapi import WebSocket


class WSManager:
    def __init__(self):
        """
        - Local connections = {user_id: websocket}
        - Project Members = {project_id: {user_id: role}}
        - Lock
        """
        self.local_connections: dict[int, WebSocket] = {}
        self.project_members: dict[int, dict[int, str]] = defaultdict(dict)
        self.lock = asyncio.Lock()

    async def connect(
        self, user_id: int, role: str, projects: list[int], websocket: WebSocket
    ):
        await websocket.accept()

        async with self.lock:
            self.local_connections[user_id] = websocket
            for project_id in projects:
                self.project_members[project_id][user_id] = role

    async def disconnect(self, user_id):
        async with self.lock:
            self.local_connections.pop(user_id)
            for project in self.project_members.values():
                project.pop(user_id, None)

    async def send_to_roles(
        self, project_id: int, message: dict, allowed_roles: set[str]
    ):
        members = self.project_members.get(project_id, {})
        for user_id, role in members.items():
            if role in allowed_roles and user_id in self.local_connections:
                await self.local_connections[user_id].send_json(message)

    async def send_to_all_project_members(self, project_id: int, message: dict):
        members = self.project_members.get(project_id, {})
        for user_id in members.keys():
            for user_id in self.local_connections.keys():
                await self.local_connections[user_id].send_json(message)
