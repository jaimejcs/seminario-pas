"""API sem dependências externas. Execute: python3 server.py"""
import argparse
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from time import perf_counter
from blackboard.engine import analyze as blackboard
from mvc.controllers.traffic_controller import analyze as mvc
from multitiers.backend.services.traffic_service import TrafficService
from multitiers.backend.repositories.road_repository import RoadRepository

ROOT = Path(__file__).resolve().parent
SAMPLE = json.loads((ROOT / 'shared/sample-data.json').read_text())

def validate(roads):
    if not isinstance(roads, list) or len(roads) != 4:
        raise ValueError('Informe as quatro vias.')
    for road, original in zip(roads, SAMPLE):
        if road.get('id') != original['id'] or road.get('road') != original['road']:
            raise ValueError('Identificação de via inválida.')
        for key, maximum in [('average_speed', 120), ('vehicles_per_minute', 200), ('traffic_light_green_time', 120)]:
            value = road.get(key)
            if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= maximum:
                raise ValueError(f'Valor inválido: {key}.')
        if type(road.get('accident')) is not bool or type(road.get('event', False)) is not bool:
            raise ValueError('Incidente e evento devem ser booleanos.')
        if road.get('weather') not in ('clear', 'light_rain', 'heavy_rain'):
            raise ValueError('Clima inválido.')
    return roads

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/roads':
            return self.send_json(200, {'roads': SAMPLE})
        self.send_json(404, {'error': 'Rota não encontrada.'})

    def do_POST(self):
        if self.path != '/api/analyze':
            return self.send_json(404, {'error': 'Rota não encontrada.'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            if not 0 < length <= 32000:
                raise ValueError('Tamanho de requisição inválido.')
            payload = json.loads(self.rfile.read(length))
            architecture = payload.get('architecture')
            engines = {'blackboard': blackboard, 'mvc': mvc, 'multitiers': self.server.service.analyze}
            if architecture not in engines:
                raise ValueError('Arquitetura inválida.')
            roads = validate(payload.get('roads'))
            start = perf_counter()
            output = engines[architecture](roads)
            self.send_json(200, {**output, 'architecture': architecture, 'duration_ms': round((perf_counter() - start) * 1000, 3)})
        except (ValueError, TypeError, AttributeError, KeyError) as error:
            self.send_json(400, {'error': str(error)})
        except Exception:
            self.send_json(500, {'error': 'Falha interna ao analisar as vias.'})
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--db', default=str(ROOT / 'multitiers/database/traffic.db'))
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    server.service = TrafficService(RoadRepository(args.db))
    print(f'API: http://localhost:{args.port}', flush=True)
    server.serve_forever()
