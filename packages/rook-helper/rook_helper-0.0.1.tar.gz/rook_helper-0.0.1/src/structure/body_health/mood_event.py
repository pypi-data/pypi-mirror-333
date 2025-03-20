from src import convert_to_type
from src.structure import StructureBase


class MoodEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'mood_event'
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
            'mood': cls.mood_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def mood_data(cls, _data: dict) -> dict:

        mood_granular_data_array_old = cls._mood_granular_data(_data)

        mood_granular_data_array = []

        if mood_granular_data_array_old:
            mood_granular_data_array = [
                {
                    'interval_duration_seconds_float': entry.get('interval_duration_seconds'),
                    'mood_scale_int': entry.get('mood_scale'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in mood_granular_data_array_old
                ]

        return {
            'mood_minimum_scale_int': convert_to_type(_data.get('mood_minimum_scale', None), int),
            'mood_avg_scale_int': convert_to_type(_data.get('mood_avg_scale', None), int),
            'mood_maximum_scale_int': convert_to_type(_data.get('mood_max_scale', None), int),
            'mood_delta_scale_int': convert_to_type(_data.get('mood_delta_scale', None), int),
            'mood_granular_data_array': mood_granular_data_array
            }

    @staticmethod
    def _mood_granular_data(_data: dict) -> list:

        mood_granular_data = _data.get('mood_granular_data_scale', [])

        if not isinstance(mood_granular_data, list):
            return []

        processed_data = []

        for item in mood_granular_data:
            is_dict = isinstance(item, dict)
            missing_keys = 'interval_duration_seconds' not in item and 'mood_scale' not in item

            if is_dict and missing_keys:
                continue

            item['interval_duration_seconds'] = convert_to_type(
                item.get('interval_duration_seconds', None), float)

            item['mood_scale'] = convert_to_type(item['mood_scale'], int)

            processed_data.append(item)

        return processed_data


build_json = MoodEvent.build_json

__all__ = ['build_json']
