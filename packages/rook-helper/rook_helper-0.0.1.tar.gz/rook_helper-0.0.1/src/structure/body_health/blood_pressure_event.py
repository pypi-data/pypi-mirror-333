from src import convert_to_type
from src.structure import StructureBase


class BloodPressureEvent(StructureBase):

    PILLAR = 'body_health'
    DATA_STRUCTURE_TYPE = 'blood_pressure_event'
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
            'blood_pressure': cls.blood_pressure_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def blood_pressure_data(cls, _data: dict) -> dict:

        blood_pressure_day_avg_old = cls._bp_data_systolic_diastolic_bp_number(
            _data, 'blood_pressure_day_avg_systolic_diastolic_bp_number')

        if blood_pressure_day_avg_old:
            blood_pressure_avg_array = [
                {
                    'diastolic_mmHg_int': entry.get('diastolic_bp'),
                    'systolic_mmHg_int': entry.get('systolic_bp')
                    }
                for entry in blood_pressure_day_avg_old
                ]

            blood_pressure_avg_object = {
                k: v for d in blood_pressure_avg_array for k, v in d.items()
                }
        else:
            blood_pressure_avg_object = {
                'systolic_mmHg_int': None,
                'diastolic_mmHg_int': None
                }

        blood_pressure_granular_data_array_old = cls._bp_data_systolic_diastolic_bp_number(
            _data, 'blood_pressure_granular_data_systolic_diastolic_bp_number')

        blood_pressure_granular_data_array = []

        if blood_pressure_granular_data_array_old:
            blood_pressure_granular_data_array = [
                {
                    'diastolic_mmHg_int': entry.get('diastolic_bp'),
                    'systolic_mmHg_int': entry.get('systolic_bp'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in blood_pressure_granular_data_array_old
                ]

        return {
            'blood_pressure_avg_object': blood_pressure_avg_object,
            'blood_pressure_granular_data_array': blood_pressure_granular_data_array,
            }

    @staticmethod
    def _bp_data_systolic_diastolic_bp_number(_data: dict, _variable: str) -> list:

        systolic_diastolic_bp_number = _data.get(_variable, [])

        if not isinstance(systolic_diastolic_bp_number, list):
            return []

        processed_data = []

        for item in systolic_diastolic_bp_number:
            is_dict = isinstance(item, dict)
            missing_keys = 'systolic_bp' not in item and 'diastolic_bp' not in item

            if is_dict and missing_keys:
                continue

            item['systolic_bp'] = convert_to_type(item.get('systolic_bp', None), int)
            item['diastolic_bp'] = convert_to_type(item.get('diastolic_bp', None), int)

            processed_data.append(item)

        return processed_data


build_json = BloodPressureEvent.build_json

__all__ = ['build_json']
