from src import convert_to_type
from src.structure import StructureBase


class TemperatureEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'temperature_event'
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
            'temperature': cls.temperature_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def temperature_data(cls, _data: dict) -> dict:

        temperature_avg_celsius_old = cls._temperature_granular_data(
            _data, 'temperature_avg_celsius')

        if temperature_avg_celsius_old:
            temperature_avg_celsius = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type')
                    }
                for entry in temperature_avg_celsius_old
                ]

            temperature_avg_celsius_object = {
                k: v for d in temperature_avg_celsius for k, v in d.items()
                }
        else:
            temperature_avg_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_max_celsius_old = cls._temperature_granular_data(
            _data, 'temperature_max_celsius')

        if temperature_max_celsius_old:
            temperature_max_celsius = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type')
                    }
                for entry in temperature_max_celsius_old
                ]

            temperature_max_object = {
                k: v for d in temperature_max_celsius for k, v in d.items()
                }
        else:
            temperature_max_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_min_celsius_old = cls._temperature_granular_data(
            _data, 'temperature_minimum_celsius')

        if temperature_min_celsius_old:
            temperature_min_celsius = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type')
                    }
                for entry in temperature_min_celsius_old
                ]

            temperature_min_celsius_object = {
                k: v for d in temperature_min_celsius for k, v in d.items()
                }
        else:
            temperature_min_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_delta_celsius_old = cls._temperature_granular_data(
            _data, 'temperature_delta_celsius')

        if temperature_delta_celsius_old:
            temperature_delta_celsius = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type')
                    }
                for entry in temperature_delta_celsius_old
                ]

            temperature_delta_celsius_object = {
                k: v for d in temperature_delta_celsius for k, v in d.items()
                }
        else:
            temperature_delta_celsius_object = {
                'temperature_celsius_float': None,
                'measurement_type_string': None
                }

        temperature_granular_data_old = cls._temperature_granular_data(
            _data, 'temperature_granular_data_celsius')

        temperature_granular_data = []

        if temperature_granular_data_old:
            temperature_granular_data = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in temperature_granular_data_old
                ]

        return {
            'temperature_avg_object': temperature_avg_celsius_object,
            'temperature_maximum_object': temperature_max_object,
            'temperature_minimum_object': temperature_min_celsius_object,
            'temperature_delta_object': temperature_delta_celsius_object,
            'temperature_granular_data_array': temperature_granular_data,

            }

    @staticmethod
    def _temperature_granular_data(_data: dict, _variable: str) -> list:

        granular_data = _data.get(_variable, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or 'temperature_celsius' not in item:
                continue

            item['temperature_celsius'] = convert_to_type(
                item.get('temperature_celsius', None), float)

            processed_data.append(item)

        return processed_data


build_json = TemperatureEvent.build_json

__all__ = ['build_json']
