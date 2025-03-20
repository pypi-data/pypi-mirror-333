from tests import BaseTestClass

from src.structure.body_health import Summary
from tests.factory_json import body_health_summary_json


class TestBodyHealthSummary(BaseTestClass):

    def test_body_health_summary_success(self):
        result = Summary.build_json(body_health_summary_json())
        event_type = result['body_health']['summary']['body_summary']

        self.assertEqual(event_type[0]['metadata']['user_id_string'], self.user_id[:-9])
        self.assertIn('metadata', event_type[0])
        self.assertIn('body_summary', event_type[0])

        body_health_content = [
            'blood_glucose', 'blood_pressure', 'body_metrics', 'heart_rate', 'hydration',
            'menstruation', 'mood', 'nutrition', 'oxygenation', 'temperature'
            ]

        for item in body_health_content:
            self.assertIn(item, event_type[0]['body_summary'])

        self.assertIn('non_structured_data_array', event_type[0])

    def test_body_health_summary_without_params(self):
        expectative = ['', None]

        for expect_item in expectative:
            with self.assertRaises(ValueError):
                Summary.build_json(expect_item)
