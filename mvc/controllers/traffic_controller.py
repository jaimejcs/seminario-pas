from mvc.models.traffic import Road
from mvc.views.dashboard import present

def analyze(roads):
    outputs, traces = [], {}
    for road in roads:
        model = Road(road)
        output = model.analyze()
        outputs.append(output)
        traces[str(road['id'])] = [
            {'component': 'View', 'message': 'Interface envia os dados dos sensores.'},
            {'component': 'TrafficController', 'message': 'Recebe evento e instancia o Road Model.'},
            {'component': 'Road Model', 'message': 'Atualiza atributos da via.'},
            {'component': 'TrafficAnalysis', 'message': f"Regra do Model executada: {output['congestion']}."},
            {'component': 'TrafficController', 'message': 'Entrega resultado à View.'},
            {'component': 'View', 'message': 'Serializa os dados para atualização do painel.'}]
    return present(outputs, traces)
