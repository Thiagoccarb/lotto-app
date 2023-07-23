import asyncio
from typing import Any
import aiohttp
import json

from utils.logger import Logger


class HttpClient(Logger):
    def __init__(self):
        super().__init__()
        self.http_client = aiohttp

    async def get(self, url) -> Any:
        async with self.http_client.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.get(url) as response:
                    data = await response.read()  # Read the raw HTML content
                    return data
            except aiohttp.ClientError as e:
                self.error(f'Error fetching data from {url}: {e}')
            except Exception as e:
                self.error(f'An unexpected error occurred: {e}')


async def main():
    http_client = HttpClient()
    page = await http_client.get('https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/2820')
    response_string = page.decode("utf-8")

# Convert the string into JSON
    response_json = json.loads(response_string)
    print(response_json)

if __name__ == "__main__":
    asyncio.run(main())