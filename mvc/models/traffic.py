from dataclasses import dataclass
from shared.rules import base_level, final_level, result

@dataclass
class Road:
    data: dict

    def analyze(self):
        r = self.data
        level = final_level(base_level(r['average_speed'], r['vehicles_per_minute']), r['accident'], r['weather'], r.get('event', False))
        return result(r, level)
