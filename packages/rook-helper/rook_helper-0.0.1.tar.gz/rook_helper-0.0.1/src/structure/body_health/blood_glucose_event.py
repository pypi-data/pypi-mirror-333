from src import convert_to_type
from src.structure import StructureBase


class BloodGlucoseEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'blood_glucose_event'
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
            'blood_glucose': cls.blood_glucose_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def blood_glucose_data(cls, _data: dict) -> dict:

        granular_data_array_old = cls._granular_data_mg_per_dL_number(_data)
        granular_data_array = []

        if granular_data_array_old:
            granular_data_array = [
                {
                    'blood_glucose_mg_per_dL_int': entry.get('blood_glucose_mg_per_dL'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in granular_data_array_old
                ]

        return {
            'blood_glucose_avg_mg_per_dL_int': convert_to_type(
                _data.get('blood_glucose_day_avg_mg_per_dL_number', None), int),
            'blood_glucose_granular_data_array': granular_data_array
            }

    @staticmethod
    def _granular_data_mg_per_dL_number(_data: dict) -> list:

        glucose_data = _data.get('blood_glucose_granular_data_mg_per_dL_number', [])

        if not isinstance(glucose_data, list):
            return []

        processed_data = []

        for item in glucose_data:
            if not isinstance(item, dict) or 'blood_glucose_mg_per_dL' not in item:
                continue

            item['blood_glucose_mg_per_dL'] = convert_to_type(
                item.get('blood_glucose_mg_per_dL', None), int)
            processed_data.append(item)

        return processed_data


build_json = BloodGlucoseEvent.build_json

__all__ = ['build_json']
