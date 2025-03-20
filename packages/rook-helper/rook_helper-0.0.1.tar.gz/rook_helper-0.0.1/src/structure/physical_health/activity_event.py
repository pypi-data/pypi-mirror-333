from src import convert_to_type
from src.structure import StructureBase
from src.structure.physical_health import (HeartRatePhysicalEvent,
                                           OxygenationPhysicalEvent, StressEvent)


class ActivityEvents(StructureBase):

    PILLAR = 'physical_health'
    DATA_STRUCTURE_TYPE = 'activity_events'
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
            'activity':  cls.activity_data(_data),
            'calories': cls.calories_data(_data),
            'distance': cls.distance_data(_data),
            'heart_rate': HeartRatePhysicalEvent.heart_rate_data(_data),
            'movement': cls.movement_data(_data),
            'power': cls.power_data(_data),
            'position': cls.position_data(_data),
            'oxygenation': OxygenationPhysicalEvent.oxygenation_data(_data),
            'stress': StressEvent.stress_data(_data),
            'non_structured_data_array': _data.get('non_structured_data', None)
            })

        data_json['physical_health']['events']['activity_event'] = events

        return data_json

    @classmethod
    def activity_data(cls, _data: dict) -> dict:

        activity_level_granular_data_old = _data.get('activity_level_granular_data_number', [])
        activity_level_granular_data_array = []

        if activity_level_granular_data_old:
            activity_level_granular_data_array = [
                {
                    'activity_level_float': entry.get('activity_level'),
                    'activity_level_label_string': entry.get('activity_level_label_string'),
                    'datetime_string': entry.get('datetime'),
                    'interval_duration_seconds_float': entry.get('interval_duration_seconds')
                    }
                for entry in activity_level_granular_data_old
                ]

        return {
            'activity_start_datetime_string': convert_to_type(
                _data.get('activity_start_time_date_time', None), str),
            'activity_end_datetime_string': convert_to_type(
                _data.get('activity_end_time_date_time', None), str),
            'activity_duration_seconds_int': convert_to_type(
                _data.get('activity_duration_seconds', None), int),
            'activity_type_name_string': convert_to_type(
                _data.get('activity_type_name', None), str),
            'active_seconds_int': convert_to_type(_data.get('active_seconds', None), int),
            'rest_seconds_int': convert_to_type(_data.get('rest_seconds', None), str),
            'low_intensity_seconds_int': convert_to_type(
                _data.get('low_intensity_seconds', None), int),
            'moderate_intensity_seconds_int': convert_to_type(
                _data.get('moderate_intensity_seconds', None), int),
            'vigorous_intensity_seconds_int': convert_to_type(
                _data.get('vigorous_intensity_seconds', None), int),
            'inactivity_seconds_int': convert_to_type(
                _data.get('inactivity_seconds', None), int),
            'continuous_inactive_periods_int': convert_to_type(
                _data.get('continuous_inactive_periods_number', None), int),
            'activity_strain_level_float': convert_to_type(
                _data.get('activity_strain_level_number', None), float),
            'activity_work_kilojoules_float': convert_to_type(
                _data.get('activity_work_kilojoules', None), float),
            'activity_energy_kilojoules_float': convert_to_type(
                _data.get('activity_energy_kilojoules', None), float),
            'activity_energy_planned_kilojoules_float': convert_to_type(
                _data.get('activity_energy_planned_kilojoules', None), float),
            'activity_level_granular_data_array': activity_level_granular_data_array
            }

    @classmethod
    def calories_data(cls, _data: dict) -> dict:

        return {
            'calories_net_intake_kcal_float': convert_to_type(
                _data.get('calories_net_intake_kilocalories', None), float),
            'calories_expenditure_kcal_float': convert_to_type(
                _data.get('calories_expenditure_kilocalories', None), float),
            'calories_net_active_kcal_float': convert_to_type(
                _data.get('calories_net_active_kilocalories', None), float),
            'calories_basal_metabolic_rate_kcal_float': convert_to_type(
                _data.get('calories_basal_metabolic_rate_kilocalories', None), float),
            'fat_percentage_of_calories_int': convert_to_type(
                _data.get('fat_percentage_of_calories_percentage', None), int),
            'carbohydrate_percentage_of_calories_int': convert_to_type(
                _data.get('carbohydrate_percentage_of_calories_percentage', None), int),
            'protein_percentage_of_calories_int': convert_to_type(
                _data.get('protein_percentage_of_calories_percentage', None), int)
            }

    @classmethod
    def distance_data(cls, _data: dict) -> dict:

        array_definitions = [
            ('steps_granular_data_steps_per_min', 'steps_granular',
             {'steps_int': 'steps', 'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('traveled_distance_granular_data_meters', 'distance_granular',
             {'traveled_distance_meters_float': 'traveled_distance_meters',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('floors_climbed_granular_data_floors_number', 'climbed_granular',
             {'floors_climbed_float': 'floors_climbed',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('elevation_granular_data_meters', 'elevation_granular',
             {'elevation_change_meters_float': 'elevation_change',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('swimming_distance_granular_data_meters', 'swimming_granular',
             {'swimming_distance_meters_float': 'swimming_distance_meters',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'})
            ]

        granular_data_arrays = {}

        for data_key, variable_key, mapping in array_definitions:
            old_data = _data.get(data_key, [])

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(source_key, None)
                        for target_key, source_key in mapping.items()
                        }
                    for entry in old_data
                    ]
                if old_data else []
                )

        return {
            'steps_int': convert_to_type(_data.get('steps_number', None), int),
            'walked_distance_meters_float': convert_to_type(
                _data.get('walked_distance_meters', None), float),
            'traveled_distance_meters_float': convert_to_type(
                _data.get('traveled_distance_meters', None), float),
            'floors_climbed_float': convert_to_type(
                _data.get('floors_climbed_number', None), float),
            'elevation_avg_altitude_meters_float': convert_to_type(
                _data.get('elevation_avg_altitude_meters', None), float),
            'elevation_minimum_altitude_meters_float': convert_to_type(
                _data.get('elevation_minimum_altitude_meters', None), float),
            'elevation_maximum_altitude_meters_float': convert_to_type(
                _data.get('elevation_max_altitude_meters', None), float),
            'elevation_loss_actual_altitude_meters_float': convert_to_type(
                _data.get('elevation_loss_actual_altitude_meters', None), float),
            'elevation_gain_actual_altitude_meters_float': convert_to_type(
                _data.get('elevation_gain_actual_altitude_meters', None), float),
            'elevation_planned_gain_meters_float': convert_to_type(
                _data.get('elevation_planned_gain_meters', None), float),
            'swimming_num_strokes_float': convert_to_type(
                _data.get('swimming_num_strokes_number', None), float),
            'swimming_num_laps_int': convert_to_type(
                _data.get('swimming_num_laps_number', None), int),
            'swimming_pool_length_meters_float': convert_to_type(
                _data.get('swimming_pool_length_meters', None), float),
            'swimming_total_distance_meters_float': convert_to_type(
                _data.get('swimming_total_distance_meters', None), float),
            'elevation_granular_data_array': granular_data_arrays['elevation_granular'],
            'floors_climbed_granular_data_array': granular_data_arrays['climbed_granular'],
            'traveled_distance_granular_data_array': granular_data_arrays['distance_granular'],
            'steps_granular_data_array': granular_data_arrays['steps_granular'],
            'swimming_distance_granular_data_array': granular_data_arrays['swimming_granular']
            }

    @classmethod
    def movement_data(cls, _data: dict) -> dict:

        obj_definitions = [
            ('velocity_vector_avg_speed_and_direction', 'velocity_avg_object'),
            ('velocity_vector_max_speed_and_direction', 'velocity_max_object')
            ]

        position_objects = {}

        for data_key, obj_name in obj_definitions:
            position_obj = _data.get(data_key, {})

            position_objects[obj_name] = (
                [
                    {
                        'speed_meters_per_second_float': entry.get('speed_meters_per_second'),
                        'direction_string': entry.get('direction')
                        }
                    for entry in position_obj
                    ]
                if isinstance(position_obj, list) and position_obj
                else {
                    'speed_meters_per_second_float': None,
                    'direction_string': None
                    }
                )

        array_definitions = [
            ('speed_granular_data_meters_per_second', 'speed_granular',
             {'speed_meters_per_second_float': 'speed_meters_per_second',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('cadence_granular_data_rpm', 'cadence_granular',
             {'cadence_rpm_float': 'cadence_rpm',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('torque_granular_data_newton_meters', 'torque_granular',
             {'torque_newton_meters_float': 'torque_newton_meters',
              'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'}),
            ('lap_granular_data_laps_number', 'lap_granular',
             {'laps_int': 'laps', 'interval_duration_seconds_float': 'interval_duration_seconds',
              'datetime_string': 'datetime'})
            ]

        granular_data_arrays = {}

        for data_key, variable_key, mapping in array_definitions:
            old_data = _data.get(data_key, [])

            granular_data_arrays[variable_key] = (
                [
                    {
                        target_key: entry.get(source_key, None)
                        for target_key, source_key in mapping.items()
                        }
                    for entry in old_data
                    ]
                if old_data else []
                )

        return {
            'speed_normalized_meters_per_second_float': convert_to_type(
                _data.get('speed_normalized_meters_per_second', None), float),
            'speed_avg_meters_per_second_float': convert_to_type(
                _data.get('speed_avg_meters_per_second', None), float),
            'speed_maximum_meters_per_second_float': convert_to_type(
                _data.get('speed_max_meters_per_second', None), float),
            'pace_avg_min_per_km_float': convert_to_type(
                _data.get('pace_avg_minutes_per_kilometer', None), float),
            'pace_maximum_min_per_km_float': convert_to_type(
                _data.get('pace_max_minutes_per_kilometer', None), float),
            'cadence_avg_rpm_float': convert_to_type(_data.get('cadence_avg_rpm', None), float),
            'cadence_maximum_rpm_float': convert_to_type(
                _data.get('cadence_max_rpm', None), float),
            'torque_avg_newton_meters_float': convert_to_type(
                _data.get('torque_avg_newton_meters', None), float),
            'torque_maximum_newton_meters_float': convert_to_type(
                _data.get('torque_max_newton_meters', None), float),
            'velocity_avg_object': position_objects['velocity_avg_object'],
            'velocity_maximum_object': position_objects['velocity_max_object'],
            'cadence_granular_data_array': granular_data_arrays['cadence_granular'],
            'lap_granular_data_array': granular_data_arrays['lap_granular'],
            'speed_granular_data_array': granular_data_arrays['speed_granular'],
            'torque_granular_data_array': granular_data_arrays['torque_granular']
            }

    @classmethod
    def power_data(cls, _data: dict) -> dict:

        power_granular_data_array_old = _data.get('power_granular_data_watts_number', [])
        power_granular_data_array = []

        if power_granular_data_array_old:
            power_granular_data_array = [
                {
                    'power_watts_float': entry.get('power_watts'),
                    'interval_duration_seconds_float': entry.get('interval_duration_seconds'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in power_granular_data_array_old
                ]

        return {
            'power_avg_watts_float': convert_to_type(
                _data.get('power_avg_watts_number', None), float),
            'power_maximum_watts_float': convert_to_type(
                _data.get('power_max_watts_number', None), float),
            'power_granular_data_array': power_granular_data_array
            }

    @classmethod
    def position_data(cls, _data: dict) -> dict:

        position_definitions = [
            ('position_start_lat_lng_deg', 'position_start_object'),
            ('position_centroid_lat_lng_deg', 'position_centroid_object'),
            ('position_end_lat_lng_deg', 'position_end_object')
            ]

        position_objects = {}

        for data_key, obj_name in position_definitions:
            position_data = _data.get(data_key, {})

            position_objects[obj_name] = (
                [
                    {
                        'lat_deg_float': entry.get('lat', None),
                        'lng_deg_float': entry.get('lng', None)
                        }
                    for entry in position_data
                    ]
                if isinstance(position_data, list) and position_data
                else {
                    'lat_deg_float': None,
                    'lng_deg_float': None
                    }
                )

        position_granular_data_array_old = _data.get('position_granular_data_lat_lng_deg', [])
        position_granular_data_array = []

        if position_granular_data_array_old:
            position_granular_data_array = [
                {
                    'lat_deg_float': entry.get('lat'),
                    'lng_deg_float': entry.get('lng'),
                    'interval_duration_seconds_float': entry.get('interval_duration_seconds'),
                    'datetime_string': entry.get('datetime')
                    }
                for entry in position_granular_data_array_old
                ]

        return {
            'position_start_object': position_objects['position_start_object'],
            'position_centroid_object': position_objects['position_centroid_object'],
            'position_end_object': position_objects['position_end_object'],
            'position_granular_data_array': position_granular_data_array,
            'position_polyline_map_data_summary_string': convert_to_type(
                _data.get('position_polyline_map_data_summary_string', None), str)
            }


build_json = ActivityEvents.build_json

__all__ = ['build_json']
