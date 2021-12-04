import asyncio  # pragma: no cover

from .event_listener import listen  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    asyncio.get_event_loop().run_until_complete(listen())
