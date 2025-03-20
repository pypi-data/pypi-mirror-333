
# This is a generated file

"""tidal_file_reader - SAM Tidal Resource File Reader"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'tidal_resource_model_choice': float,
    'tidal_resource_filename': str,
    'name': str,
    'city': str,
    'state': str,
    'country': str,
    'lat': float,
    'lon': float,
    'nearby_buoy_number': str,
    'average_power_flux': float,
    'bathymetry': str,
    'sea_bed': str,
    'tz': float,
    'data_source': str,
    'notes': str,
    'location_id': str,
    'location': str,
    'distance_to_shore_file': float,
    'water_depth_file': float,
    'year': Array,
    'month': Array,
    'day': Array,
    'hour': Array,
    'minute': Array,
    'tidal_velocity': Array,
    'significant_wave_height': Array,
    'number_records': float,
    'number_hours': float
}, total=False)

class Data(ssc.DataDict):
    tidal_resource_model_choice: float = INPUT(label='Resource distribution or time series tidal resource data', units='0/1', type='NUMBER', group='Weather Reader', required='?=1', constraints='INTEGER')
    tidal_resource_filename: str = INPUT(label='File path with tidal resource data', type='STRING', group='Weather Reader', required='tidal_resource_model_choice=0', constraints='LOCAL_FILE')
    name: Final[str] = OUTPUT(label='Name', type='STRING', group='Weather Reader')
    city: Final[str] = OUTPUT(label='City', type='STRING', group='Weather Reader')
    state: Final[str] = OUTPUT(label='State', type='STRING', group='Weather Reader')
    country: Final[str] = OUTPUT(label='Country', type='STRING', group='Weather Reader')
    lat: Final[float] = OUTPUT(label='Latitude', units='deg', type='NUMBER', group='Weather Reader')
    lon: Final[float] = OUTPUT(label='Longitude', units='deg', type='NUMBER', group='Weather Reader')
    nearby_buoy_number: Final[str] = OUTPUT(label='Nearby buoy number', type='STRING', group='Weather Reader')
    average_power_flux: Final[float] = OUTPUT(label='Average power flux', units='kW/m', type='NUMBER', group='Weather Reader')
    bathymetry: Final[str] = OUTPUT(label='Bathymetry', type='STRING', group='Weather Reader')
    sea_bed: Final[str] = OUTPUT(label='Sea bed', type='STRING', group='Weather Reader')
    tz: Final[float] = OUTPUT(label='Time zone', type='NUMBER', group='Weather Reader')
    data_source: Final[str] = OUTPUT(label='Data source', type='STRING', group='Weather Reader')
    notes: Final[str] = OUTPUT(label='Notes', type='STRING', group='Weather Reader')
    location_id: Final[str] = OUTPUT(label='Location ID', type='STRING', group='Weather Reader', required='tidal_resource_model_choice=1')
    location: Final[str] = OUTPUT(label='Location', type='STRING', group='Weather Reader', required='tidal_resource_model_choice=1')
    distance_to_shore_file: Final[float] = OUTPUT(label='Distance to shore', units='m', type='NUMBER', group='Weather Reader', required='?')
    water_depth_file: Final[float] = OUTPUT(label='Water depth', units='m', type='NUMBER', group='Weather Reader', required='?')
    year: Final[Array] = OUTPUT(label='Year', units='yr', type='ARRAY', group='Weather Reader', required='tidal_resource_model_choice=1')
    month: Final[Array] = OUTPUT(label='Month', units='mn', type='ARRAY', group='Weather Reader', required='tidal_resource_model_choice=1', meta='1-12')
    day: Final[Array] = OUTPUT(label='Day', units='dy', type='ARRAY', group='Weather Reader', required='tidal_resource_model_choice=1', meta='1-365')
    hour: Final[Array] = OUTPUT(label='Hour', units='hr', type='ARRAY', group='Weather Reader', required='tidal_resource_model_choice=1', meta='0-23')
    minute: Final[Array] = OUTPUT(label='Minute', units='min', type='ARRAY', group='Weather Reader', required='tidal_resource_model_choice=1', meta='0-59')
    tidal_velocity: Final[Array] = OUTPUT(label='Tidal velocity', units='m/s', type='ARRAY', group='Weather Reader', required='?')
    significant_wave_height: Final[Array] = OUTPUT(label='Wave height time series data', units='m', type='ARRAY', group='Weather Reader', required='?')
    number_records: Final[float] = OUTPUT(label='Number of records in wave time series', type='NUMBER', group='Weather Reader', required='?')
    number_hours: Final[float] = OUTPUT(label='Number of hours in wave time series', type='NUMBER', group='Weather Reader', required='?')

    def __init__(self, *args: Mapping[str, Any],
                 tidal_resource_model_choice: float = ...,
                 tidal_resource_filename: str = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
