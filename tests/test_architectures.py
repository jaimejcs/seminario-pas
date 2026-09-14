from contextlib import closing
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from blackboard.engine import analyze as blackboard
from mvc.controllers.traffic_controller import analyze as mvc
from multitiers.backend.repositories.road_repository import RoadRepository
from multitiers.backend.services.traffic_service import TrafficService
from server import validate

DATA = json.loads((Path(__file__).resolve().parents[1] / 'shared/sample-data.json').read_text())

class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.service = TrafficService(RoadRepository(Path(self.directory.name) / 'test.db'))

    def test_initial_scenarios_and_recommendations(self):
        for engine in (blackboard, mvc, self.service.analyze):
            results = engine(DATA)['roads']
            self.assertEqual([r['level'] for r in results], [3, 0, 3, 0])
            self.assertEqual(results[0]['suggested_green_time'], 45)
            self.assertIn('15 segundos', results[0]['recommendation'])
            self.assertIn('desvio', results[2]['recommendation'])
            self.assertEqual(results[2]['suggested_green_time'], 25)

    def test_boundary_equivalence(self):
        for speed, volume, accident, weather, event in itertools.product([19,20,29,30,39,40], [60,61,80,81], [False,True], ['clear','light_rain','heavy_rain'], [False,True]):
            road = {**DATA[0], 'average_speed':speed, 'vehicles_per_minute':volume, 'accident':accident, 'weather':weather, 'event':event}
            expected = mvc([road])['roads']
            self.assertEqual(blackboard([road])['roads'], expected)
            self.assertEqual(self.service.analyze([road])['roads'], expected)

    def test_threshold_contract(self):
        for speed,volume,expected in [(19,81,3),(20,81,2),(29,61,2),(30,81,1),(39,60,1),(40,60,0),(19,60,1)]:
            road={**DATA[1],'average_speed':speed,'vehicles_per_minute':volume}
            self.assertEqual(mvc([road])['roads'][0]['level'],expected)

    def test_event_extension_and_authorship(self):
        output=blackboard([{**DATA[1],'event':True}])
        self.assertEqual(output['roads'][0]['level'],1)
        self.assertIn('EventExpert',[x['component'] for x in output['traces']['2']])

    def test_repository_persists(self):
        self.service.analyze(DATA)
        import sqlite3
        with closing(sqlite3.connect(Path(self.directory.name) / 'test.db')) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM readings').fetchone()[0],4)

    def test_validation_rejects_invalid_readings(self):
        for change in [{'average_speed':-1},{'average_speed':float('nan')},{'weather':'snow'},{'accident':'false'},{'event':1},{'road':'Outra via'}]:
            with self.assertRaises(ValueError):
                validate([{**DATA[0],**change},*DATA[1:]])

if __name__ == '__main__':
    unittest.main()
