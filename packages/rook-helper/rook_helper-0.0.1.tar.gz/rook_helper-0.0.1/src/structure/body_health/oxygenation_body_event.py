from src import convert_to_type
from src.structure import StructureBase


class OxygenationBodyEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'oxygenation_event'
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
            'oxygenation': cls.oxygenation_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def oxygenation_data(cls, _data: dict) -> dict:

        granular_definitions = [
            ('saturation_granular_data_percentage', 'saturation_percentage',
             'saturation_percentage_int'),
            ('vo2_granular_data_ml_per_min', 'vo2_ml_per_min', 'vo2_mL_per_min_per_kg_int')
            ]

        granular_data_arrays = {}

        for data_key, variable_key, target_key in granular_definitions:
            old_data = cls._granular_data(_data, data_key, variable_key)

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(variable_key),
                        'datetime_string': entry.get('datetime'),
                        'interval_duration_seconds_float': entry.get(
                            'interval_duration_seconds_float')
                        }
                    for entry in old_data
                    ]
                if old_data else []
                )

        return {
            'saturation_avg_percentage_int': convert_to_type(
                _data.get('saturation_avg_percentage', None), int),
            'vo2max_mL_per_min_per_kg_int': convert_to_type(
                _data.get('vo2max_ml_per_min_per_kg', None), int),
            'saturation_granular_data_array': granular_data_arrays.get('saturation_percentage'),
            'vo2_granular_data_array': granular_data_arrays.get('vo2_ml_per_min')
            }

    @staticmethod
    def _granular_data(_data: dict, _granular_data: str, _variable: str) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or _variable not in item:
                continue

            item[_variable] = convert_to_type(item[_variable], int)

            if 'interval_duration_seconds' in item:
                item['interval_duration_seconds'] = convert_to_type(
                    item.get('interval_duration_seconds', None), float)

            processed_data.append(item)

        return processed_data


build_json = OxygenationBodyEvent.build_json

__all__ = ['build_json']
