import aiohttp
import inspect
from typing import Any, Dict, Optional, Callable


class AsyncRestClient:
    """Универсальный клиент для работы с REST API и WebSocket."""

    def __init__(self, address: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.address = address.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    async def request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.address}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(method, url, timeout=self.timeout, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

    async def __call__(self, method: str, endpoint: str, **kwargs) -> Any:
        return await self.request(method, endpoint, **kwargs)

    async def websocket(self, endpoint: str, params: Optional[Dict[str, Any]] = None, callback: Callable[[Dict], None] = None) -> None:
        """
        Подключение к WebSocket серверу.
        :param endpoint: URL эндпоинта WebSocket.
        :param params: Параметры для отправки при подключении.
        :param callback: Функция для обработки сообщений.
        """
        url = f"{self.address}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.ws_connect(url, timeout=self.timeout) as ws:
                # Отправка начальных параметров, если они указаны
                if params:
                    await ws.send_json(params)

                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = msg.json()
                        if callback:
                            # Проверяем, является ли callback асинхронной функцией
                            if inspect.iscoroutinefunction(callback):
                                await callback(data)
                            else:
                                callback(data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        raise Exception(f"WebSocket error: {msg.data}")
