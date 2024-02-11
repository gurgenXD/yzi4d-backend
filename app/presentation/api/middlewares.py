import asyncio
import random
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class DelayMiddleware:
    """Задержки перед запросами для тестирования."""

    def __init__(self, app: "ASGIApp", delay: float) -> None:
        self._app = app
        self._delay = delay

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        """Добавить задержки перед запросами для тестирования."""
        await asyncio.sleep(random.uniform(0.0, self._delay))
        await self._app(scope, receive, send)
