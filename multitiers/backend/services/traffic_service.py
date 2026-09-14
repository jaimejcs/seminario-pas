from shared.rules import base_level, final_level, result

class TrafficAnalyzer:
    def analyze(self, road):
        return final_level(base_level(road['average_speed'], road['vehicles_per_minute']), road['accident'], road['weather'], road.get('event', False))

class RecommendationService:
    def build(self, road, level):
        return result(road, level)

class TrafficService:
    def __init__(self, repository):
        self.repository = repository

    def analyze(self, roads):
        stored = self.repository.save_and_load(roads)
        outputs = [RecommendationService().build(r, TrafficAnalyzer().analyze(r)) for r in stored]
        traces = {str(r['id']): [
            {'component': 'Presentation Tier', 'message': 'POST /api/analyze → HTTP/JSON.'},
            {'component': 'Traffic API', 'message': 'Valida requisição e chama o serviço.'},
            {'component': 'RoadRepository', 'message': 'Persiste leitura e consulta SQLite em transação.'},
            {'component': 'TrafficAnalyzer', 'message': f"Business Tier calcula: {r['congestion']}."},
            {'component': 'RecommendationService', 'message': r['recommendation']},
            {'component': 'Presentation Tier', 'message': 'Recebe resposta JSON e apresenta os resultados.'}
        ] for r in outputs}
        return {'roads': outputs, 'traces': traces}
