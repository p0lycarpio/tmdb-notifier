import logging

from aiohttp_retry import RetryClient, JitterRetry

class HTTPSession(RetryClient):
    def __init__(self) -> None:
        logger = logging.getLogger('aiohttp')
        logger.setLevel(logging.INFO)

        retry_options = JitterRetry(
            attempts=5,
            start_timeout=1.2,
            statuses=set([429]),
        )
        super().__init__(
            raise_for_status=True,
            retry_options=retry_options,
            logger=logger,
        )
        

    async def close(self):
        await self._client.close()
