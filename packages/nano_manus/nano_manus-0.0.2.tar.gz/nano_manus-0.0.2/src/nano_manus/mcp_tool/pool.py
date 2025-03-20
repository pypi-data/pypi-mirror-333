from .type import BaseMCP
from typing import Dict, List
from contextlib import AsyncExitStack


class MCPPool:
    def __init__(self):
        self.mcp_clients: Dict[str, BaseMCP] = {}
        self.exit_stack = AsyncExitStack()

    def add_mcp_client(self, name: str, mcp_client: BaseMCP):
        self.mcp_clients[name] = mcp_client

    def get_mcp_client(self, name: str) -> BaseMCP:
        return self.mcp_clients[name]

    def get_all_mcp_clients(self) -> List[BaseMCP]:
        return list(self.mcp_clients.values())

    async def start(self, names: List[str] = None):
        if names:
            for name in names:
                await self.mcp_clients[name].connect(self.exit_stack)
            return
        for mcp_client in self.mcp_clients.values():
            await mcp_client.connect(self.exit_stack)

    async def stop(self):
        await self.exit_stack.aclose()
