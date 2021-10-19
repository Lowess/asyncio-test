import json
import asyncio
from aiohttp import ClientSession
import logging

FORMAT = (
    "%(asctime)s,%(msecs)03d %(levelname)8s %(name)s "
    "%(filename)s:%(lineno)d - %(message)s"
)
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)


class Async:
    async def _fetch(self, url, session):
        return await session.request(
            method="GET",
            url=url,
            headers={},
        )

    async def call(self, url, session):

        response = await self._fetch(url, session)

        # Retrieve JSON content from the response
        json_response = {}
        
        async with response:
            content_type = response.headers
            logger.info(content_type)

            if "application/json" in content_type.get("content-type"):
                json_response = await response.json()
            else:
                txt_response = await response.text()
                json_response = json.loads(txt_response)

        return json_response

    async def main(self, urls):
        async with ClientSession(raise_for_status=True) as session:
            tasks = []
            for url in urls:
                tasks.append(cli.call(url, session))
            res = await asyncio.gather(*tasks)
            print(res)


if __name__ == "__main__":
    cli = Async()
    urls = ["https://flair.verity.gumgum.com/api/iab/v2/index.json"]

    asyncio.run(cli.main(urls))
