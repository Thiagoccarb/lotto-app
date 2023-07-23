from typing import Any
import asyncio
import json

from utils.http_client import HttpClient

class Lotofacil:
    def __init__(self) -> None:
        self._http_client = HttpClient()
        self.url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/{}'
        
    async def get_results_by_number(self, number: int) -> Any:
        result = await self._http_client.get(self.url.format(str(number)))
        response_string = result.decode("utf-8")
        response_json = json.loads(response_string)
        return response_json    

    async def get_last_result(self) -> Any:
        result = await self._http_client.get(self.url.format(''))
        response_string = result.decode("utf-8")
        response_json = json.loads(response_string)
        return response_json    
 
    def create_report(self, data: dict) -> dict:
        report = {}
        for _ in data.items():
            report['accumulated'] = data.get('acumulado') 
            report['date'] = data.get('dataApuracao')
            report['numbers'] = data.get('listaDezenas')
            prizes_data = [
                {
                    'points': int(item.get('descricaoFaixa').split(' ')[0]), 
                    'count':  item.get('numeroDeGanhadores', 0)
                } for item in data.get("listaRateioPremio", {})
            ]
            report['prizes_data'] = prizes_data
            report['accumulated'] = data.get('acumulado') 
            report['accumulated'] = data.get('acumulado') 
            report['accumulated'] = data.get('acumulado') 
            report['id'] = data['numero']
            report['last_draw'] = data['ultimoConcurso']
        return report
    
async def main():
    lotofacil = Lotofacil() 
    tasks = [lotofacil.get_results_by_number(n) for n in range(1, 2)]
    results, = await asyncio.gather(*tasks)
    print(results)
    print(lotofacil.create_report(results))

if __name__ == "__main__":
    asyncio.run(main())