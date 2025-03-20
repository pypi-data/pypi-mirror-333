from src import convert_to_type
from src.structure import StructureBase


class HeartRatePhysicalEvent(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'heart_rate_event'
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
            'heart_rate': cls.heart_rate_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json['physical_health']['events']['heart_rate_event'] = events

        return data_json

    @classmethod
    def heart_rate_data(cls, _data: dict) -> dict:

        granular_definitions = [
            ('hrv_sdnn_granular_data_number', 'hrv_sdnn', 'hrv_sdnn_float', True),
            ('hrv_rmssd_granular_data_number', 'hrv_rmssd', 'hrv_rmssd_float', True),
            ('hr_granular_data_bpm', 'hr_bpm', 'hr_bpm_int', False)
            ]

        granular_data_arrays = {}

        for data_key, variable_key, target_key, is_float_key in granular_definitions:
            old_data = cls._granular_data(_data, data_key, variable_key, is_float_key)

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(variable_key),
                        'datetime_string': entry.get('datetime'),
                        'interval_duration_seconds_float': entry.get('interval_duration_seconds')
                        }
                    for entry in old_data
                    ]
                if old_data else []
                )

        return {
            'hr_maximum_bpm_int': convert_to_type(_data.get('hr_max_bpm', None), int),
            'hr_minimum_bpm_int': convert_to_type(_data.get('hr_minimum_bpm', None), int),
            'hr_avg_bpm_int': convert_to_type(_data.get('hr_avg_bpm', None), int),
            'hr_resting_bpm_int': convert_to_type(_data.get('hr_resting_bpm', None), int),
            'hrv_avg_rmssd_float': convert_to_type(_data.get('hrv_avg_rmssd_number', None), float),
            'hrv_avg_sdnn_float': convert_to_type(_data.get('hrv_avg_sdnn_number', None), float),
            'hr_granular_data_array': granular_data_arrays.get('hr_bpm'),
            'hrv_sdnn_granular_data_array': granular_data_arrays.get('hrv_sdnn'),
            'hrv_rmssd_granular_data_array': granular_data_arrays.get('hrv_rmssd')
            }

    @staticmethod
    def _granular_data(_data: dict,
                       _granular_data: str,
                       _variable: str,
                       _float_type: bool = True,) -> list:

        granular_data = _data.get(_granular_data, [])

        if not isinstance(granular_data, list):
            return []

        processed_data = []

        for item in granular_data:
            if not isinstance(item, dict) or _variable not in item:
                continue

            item[_variable] = convert_to_type(item[_variable], float if _float_type else int)

            if 'interval_duration_seconds' in item:
                item['interval_duration_seconds'] = convert_to_type(
                    item.get('interval_duration_seconds', None), float)

            processed_data.append(item)

        return processed_data


build_json = HeartRatePhysicalEvent.build_json

__all__ = ['build_json']
