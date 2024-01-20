import asyncio


def sync_to_async(func):
	async def wraper(*args, **kwargs):
		return await asyncio.to_thread(func, *args, **kwargs)
	return wraper
