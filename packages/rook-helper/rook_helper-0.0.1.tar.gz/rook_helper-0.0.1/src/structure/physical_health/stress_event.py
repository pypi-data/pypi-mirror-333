from src import convert_to_type
from src.structure import StructureBase


class StressEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'stress_event'
    DATA_TYPE = 'events'

    @classmethod
    def build_json(cls, _data: dict) -> dict:

        if not _data:
            raise ValueError('The data is empty')

        _data.update({
            'pillar': cls.PILLAR,
            'data_structure_type': cls.DATA_STRUCTURE_TYPE,
            'data_type': cls.DATA_TYPE
            })

        data_json = cls.build_data_structure(**_data)

        events = []

        events.append({
            'metadata': cls.build_metadata(**_data),
            'stress': cls.stress_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json['physical_health']['events']['stress_event'] = events

        return data_json

    @classmethod
    def stress_data(cls, _data: dict) -> dict:

        tss_granular_data_array_old = cls._granular_data(
            _data, 'tss_granular_data_1_500_score_number')

        tss_granular_data_array = []

        if tss_granular_data_array_old:
            tss_granular_data_array = [
                {
                    'tss_score_int': entry.get('tss_1_500_score'),
                    'datetime_string': entry.get('datetime'),
                    'interval_duration_seconds_float': entry.get('interval_duration_seconds')
                    }
                for entry in tss_granular_data_array_old
                ]

        return {
            'stress_at_rest_duration_seconds_int': convert_to_type(
                _data.get('stress_at_rest_duration_seconds', None), int),
            'stress_duration_seconds_int': convert_to_type(
                _data.get('stress_duration_seconds', None), int),
            'low_stress_duration_seconds_int': convert_to_type(
                _data.get('low_stress_duration_seconds', None), int),
            'medium_stress_duration_seconds_int': convert_to_type(
                _data.get('medium_stress_duration_seconds', None), int),
            'high_stress_duration_seconds_int': convert_to_type(
                _data.get('high_stress_duration_seconds', None), int),
            'stress_avg_level_int': convert_to_type(
                _data.get('stress_avg_level_number', None), int),
            'stress_maximum_level_int': convert_to_type(
                _data.get('stress_max_level_number', None), int),
            'tss_granular_data_array': tss_granular_data_array
            }

    @staticmethod
    def _granular_data(_data: dict, _granular_data: str) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            is_dict = isinstance(item, dict)
            missing_key = 'interval_duration_seconds' not in item and 'tss_1_500_score' not in item

            if is_dict and missing_key:
                continue

            item['interval_duration_seconds'] = convert_to_type(
                item.get('interval_duration_seconds', None), float)

            item['tss_1_500_score'] = convert_to_type(item.get('tss_1_500_score', None), int)

            processed_data.append(item)

        return processed_data


build_json = StressEvent.build_json

__all__ = ['build_json']
