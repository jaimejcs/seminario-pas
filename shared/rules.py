"""Contrato determinístico compartilhado pelas três implementações."""
LEVELS = ['NORMAL', 'MODERADO', 'ALTO', 'CRÍTICO']

def base_level(speed, volume):
    if speed < 20 and volume > 80:
        return 3
    if speed < 30 and volume > 60:
        return 2
    return 1 if speed < 40 else 0

def final_level(base, accident, weather, event=False):
    return min(3, base + int(accident) + int(weather == 'heavy_rain') + int(event))

def recommendation(level, accident):
    if accident:
        return 'Priorizar atendimento do incidente e recomendar desvio de tráfego.'
    return ['Nenhuma intervenção necessária.', 'Monitorar via.',
            'Aumentar tempo verde em 10 segundos.',
            'Aumentar tempo verde em 15 segundos e emitir alerta ao operador.'][level]

def result(road, level):
    return {**road, 'level': level, 'congestion': LEVELS[level],
            'recommendation': recommendation(level, road['accident']),
            'suggested_green_time': road['traffic_light_green_time'] + (0 if road['accident'] else [0, 0, 10, 15][level])}
