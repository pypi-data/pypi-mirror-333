from tests import BaseTestClass

from src.structure.sleep_health import Summary
from tests.factory_json import sleep_summary_json


class TestSleepHealthSummary(BaseTestClass):

    def test_sleep_health_summary_success(self):
        result = Summary.build_json(sleep_summary_json())
        event_type = result['sleep_health']['summary']['sleep_summary']

        print(event_type[0])

        sleep_health_content = [
            'duration', 'scores', 'heart_rate', 'temperature', 'breathing'
            ]

        for item in sleep_health_content:
            self.assertIn(item, event_type[0]['sleep_summary'])

        self.assertTrue(True)

    def test_sleep_health_summary_without_params(self):
        expectative = ['', None]

        for expect_item in expectative:
            with self.assertRaises(ValueError):
                Summary.build_json(expect_item)
