from src import format_datetime, convert_to_type
from src.structure import StructureBase


class Summary(StructureBase):

    PILLAR = 'sleep_health'
    DATA_STRUCTURE_TYPE = 'sleep_summary'
    DATA_TYPE = 'summary'

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
            'sleep_summary': cls.summary_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json[cls.PILLAR][cls.DATA_TYPE][cls.DATA_STRUCTURE_TYPE] = events

        return data_json

    @classmethod
    def summary_data(cls, _data: dict) -> dict:

        return {
            'breathing': cls._breathing_data(_data),
            'duration': cls._duration_data(_data),
            'heart_rate': cls._heart_rate_data(_data),
            'scores': cls._scores_rate_data(_data),
            'temperature': cls._temperature_rate_data(_data)
            }

    @staticmethod
    def _breathing_data(_data: dict) -> dict:

        granular_definitions = [
            ('breathing_granular_data_breaths_per_min',
             {'breaths_per_min_int': 'breaths_per_min', 'datetime_string': 'datetime'}),

            ('snoring_granular_data_snores',
             {'interval_duration_seconds_float': 'interval_duration_seconds',
              'snoring_events_count_int': 'snoring_events_count_number',
              'datetime_string': 'datetime'}),

            ('saturation_granular_data_percentage',
             {'interval_duration_seconds_float_number': 'interval_duration_seconds',
              'saturation_percentage_int': 'saturation_percentage', 'datetime_string': 'datetime'})
            ]

        granular_data_arrays = {
            data_key: [
                {
                    target_key: entry.get(source_key, None)
                    for target_key, source_key in target_object.items()
                    }
                for entry in _data.get(data_key, [])
                ]
            for data_key, target_object in granular_definitions
            }

        return {
            'breaths_minimum_per_min_int': convert_to_type(
                _data.get('breaths_minimum_per_min', None), int),
            'breaths_avg_per_min_int': convert_to_type(
                _data.get('breaths_avg_per_min', None), int),
            'breaths_maximum_per_min_int': convert_to_type(
                _data.get('breaths_max_per_min', None), int),
            'snoring_events_count_int': convert_to_type(
                _data.get('snoring_events_count_number', None), int),
            'snoring_duration_total_seconds_int': convert_to_type(
                _data.get('snoring_duration_total_seconds', None), int),
            'saturation_avg_percentage_int': convert_to_type(
                _data.get('saturation_avg_percentage', None), int),
            'saturation_minimum_percentage_int': convert_to_type(
                _data.get('saturation_min_percentage', None), int),
            'saturation_maximum_percentage_int': convert_to_type(
                _data.get('saturation_max_percentage', None), int),
            'breathing_granular_data_array': granular_data_arrays.get(
                'breathing_granular_data_breaths_per_min'),
            'snoring_granular_data_array': granular_data_arrays.get(
                'snoring_granular_data_snores'),
            'saturation_granular_data_array': granular_data_arrays.get(
                'saturation_granular_data_percentage'),
            }

    @staticmethod
    def _duration_data(_data: dict) -> dict:

        return {
            'sleep_start_datetime_string': format_datetime(
                _data.get('sleep_start_datetime', None)),
            'sleep_end_datetime_string': format_datetime(_data.get('sleep_end_datetime', None)),
            'sleep_date_string': format_datetime(_data.get('sleep_date', None)),
            'sleep_duration_seconds_int': convert_to_type(
                _data.get('sleep_duration_seconds', None), int),
            'time_in_bed_seconds_int': convert_to_type(
                _data.get('time_in_bed_seconds', None), int),
            'light_sleep_duration_seconds_int': convert_to_type(
                _data.get('light_sleep_duration_seconds', None), int),
            'rem_sleep_duration_seconds_int': convert_to_type(
                _data.get('rem_sleep_duration_seconds', None), int),
            'deep_sleep_duration_seconds_int': convert_to_type(
                _data.get('deep_sleep_duration_seconds', None), int),
            'time_to_fall_asleep_seconds_int': convert_to_type(
                _data.get('time_to_fall_asleep_seconds', None), int),
            'time_awake_during_sleep_seconds_int': convert_to_type(
                _data.get('time_awake_during_sleep_seconds', None), int)
            }

    @staticmethod
    def _heart_rate_data(_data: dict) -> dict:

        granular_definitions = [
            ('hrv_sdnn_granular_data', 'hrv_sdnn', 'hrv_sdnn_float'),
            ('hrv_rmssd_granular_data', 'hrv_rmssd', 'hrv_rmssd_float'),
            ('hr_granular_data_bpm', 'hr_bpm', 'hr_bpm_int')
            ]

        granular_data_arrays = {}

        for data_key, variable_key, target_key in granular_definitions:
            old_data = _data.get(data_key, [])

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(variable_key),
                        'datetime_string': entry.get('datetime')
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
            'hr_basal_bpm_int': convert_to_type(_data.get('hr_basal_bpm', None), int),
            'hrv_avg_rmssd_float': convert_to_type(_data.get('hrv_avg_rmssd_number', None), float),
            'hrv_avg_sdnn_float': convert_to_type(_data.get('hrv_avg_sdnn_number', None), float),
            'hr_granular_data_array': granular_data_arrays.get('hr_bpm'),
            'hrv_sdnn_granular_data_array': granular_data_arrays.get('hrv_sdnn'),
            'hrv_rmssd_granular_data_array': granular_data_arrays.get('hrv_rmssd')
            }

    @staticmethod
    def _scores_rate_data(_data: dict) -> dict:

        return {
            'sleep_quality_rating_1_5_score_int': convert_to_type(
                _data.get('sleep_quality_rating_1_5_score', None), int),
            'sleep_efficiency_1_100_score_int': convert_to_type(
                _data.get('sleep_efficiency_1_100_score', None), int),
            'sleep_goal_seconds_int': convert_to_type(_data.get('sleep_goal_seconds', None), int),
            'sleep_continuity_1_5_score_int': convert_to_type(
                _data.get('sleep_continuity_1_5_score', None), int),
            'sleep_continuity_1_5_rating_int': convert_to_type(
                _data.get('sleep_continuity_1_5_rating', None), int)
            }

    @staticmethod
    def _temperature_rate_data(_data: dict) -> dict:

        minimum = _data.get('temperature_minimum_celsius', None)

        if minimum:
            minimum_var = minimum[0].get('temperature_celsius', None)
        else:
            minimum_var = None

        avg = _data.get('temperature_avg_celsius', [])

        if avg:
            avg_var = avg[0].get('temperature_celsius', None)
        else:
            avg_var = None

        max = _data.get('temperature_max_celsius', [])

        if max:
            max_var = max[0].get('temperature_celsius', None)
        else:
            max_var = None

        delta = _data.get('temperature_delta_celsius', None)

        if delta:
            delta_var = delta[0].get('temperature_celsius', None)
        else:
            delta_var = None

        temperature_granular_data_array_old = _data.get('temperature_granular_data_celsius', [])
        temperature_granular_data_array = []

        if temperature_granular_data_array_old:
            temperature_granular_data_array = [
                {
                    'temperature_celsius_float': entry.get('temperature_celsius'),
                    'measurement_type_string': entry.get('measurement_type'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in temperature_granular_data_array_old
                ]

        return {
            'temperature_minimum_celsius_float': convert_to_type(minimum_var, float),
            'temperature_avg_celsius_float': convert_to_type(avg_var, float),
            'temperature_maximum_celsius_float': convert_to_type(max_var, float),
            'temperature_delta_celsius_float': convert_to_type(delta_var, float),
            'temperature_granular_data_array': temperature_granular_data_array
            }


build_json = Summary.build_json

__all__ = ['build_json']
