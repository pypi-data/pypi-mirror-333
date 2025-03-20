from src import convert_to_type
from src.structure import StructureBase


class HydrationEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'hydration_event'
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
            'hydration': cls.hydration_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def hydration_data(cls, _data: dict) -> dict:

        granular_definitions = [
            ('hydration_amount_granular_data_ml_number', 'hydration_amount_ml',
             'hydration_amount_mL_int'),
            ('hydration_level_granular_data_percentage_number', 'hydration_level_percentage',
             'hydration_level_percentage_int')
            ]

        granular_data_arrays = {}

        for data_key, variable_key, target_key in granular_definitions:
            old_data = cls._hydration_granular_data(_data, data_key, variable_key)

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(variable_key),
                        'datetime_string': entry.get('datetime'),
                        'interval_duration_seconds_float': entry.get('interval_duration_seconds'),
                        }
                    for entry in old_data
                    ]
                if old_data else []
                )

        return {
            'water_total_consumption_mL_int': convert_to_type(
                _data.get('water_total_consumption_ml_number', None), int),
            'hydration_amount_granular_data_array': granular_data_arrays.get('hydration_amount_ml'),
            'hydration_level_granular_data_array': granular_data_arrays.get(
                'hydration_level_percentage')
            }

    @staticmethod
    def _hydration_granular_data(_data: dict, _granular_data: str, _variable: str) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or _variable not in item:
                continue

            item['interval_duration_seconds'] = convert_to_type(
                item.get('interval_duration_seconds', None), float)

            item[_variable] = convert_to_type(item[_variable], int)

            processed_data.append(item)

        return processed_data


build_json = HydrationEvent.build_json

__all__ = ['build_json']
