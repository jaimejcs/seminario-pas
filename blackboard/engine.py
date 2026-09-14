"""Especialistas só recebem o quadro: não referenciam outros especialistas."""
from shared.rules import base_level, final_level, result

class Blackboard:
    def __init__(self, road):
        self.sensor_data = road
        self.facts = {}
        self.observations = []
        self.output = None

    def publish(self, expert, key, value, message):
        self.facts[key] = value
        self.observations.append({'component': expert, 'message': message})

class SpeedExpert:
    def run(self, board):
        value = board.sensor_data['average_speed']
        board.publish(type(self).__name__, 'speed', value, f'Velocidade observada: {value} km/h.')

class VolumeExpert:
    def run(self, board):
        value = board.sensor_data['vehicles_per_minute']
        board.publish(type(self).__name__, 'volume', value, f'Volume observado: {value} veículos/min.')

class AccidentExpert:
    def run(self, board):
        value = board.sensor_data['accident']
        board.publish(type(self).__name__, 'accident', value, 'Incidente: +1 nível.' if value else 'Nenhum incidente detectado.')

class WeatherExpert:
    def run(self, board):
        value = board.sensor_data['weather']
        board.publish(type(self).__name__, 'weather', value, 'Chuva forte: +1 nível.' if value == 'heavy_rain' else 'Clima sem agravamento.')

class EventExpert:
    def run(self, board):
        value = board.sensor_data.get('event', False)
        board.publish(type(self).__name__, 'event', value, 'Evento esportivo: +1 nível.' if value else 'Sem evento esportivo.')

class TrafficDecisionExpert:
    def run(self, board):
        f = board.facts
        level = final_level(base_level(f['speed'], f['volume']), f['accident'], f['weather'], f.get('event', False))
        board.publish(type(self).__name__, 'level', level, f'Decisão consolidada: nível {level} (0–3).')

class RecommendationExpert:
    def run(self, board):
        board.output = result(board.sensor_data, board.facts['level'])
        board.publish(type(self).__name__, 'recommendation', board.output['recommendation'], board.output['recommendation'])

def analyze(roads):
    outputs, traces, boards = [], {}, {}
    for road in roads:
        board = Blackboard(road)
        experts = [SpeedExpert(), VolumeExpert(), AccidentExpert(), WeatherExpert()]
        if road.get('event'):
            experts.append(EventExpert())
        for expert in [*experts, TrafficDecisionExpert(), RecommendationExpert()]:
            expert.run(board)
        outputs.append(board.output)
        traces[str(road['id'])] = [{'component': 'BlackboardController', 'message': 'Sensores publicados no quadro compartilhado.'}, *board.observations]
        boards[str(road['id'])] = {'sensor_data': road, 'observations': board.observations, 'facts': board.facts}
    return {'roads': outputs, 'traces': traces, 'boards': boards}
