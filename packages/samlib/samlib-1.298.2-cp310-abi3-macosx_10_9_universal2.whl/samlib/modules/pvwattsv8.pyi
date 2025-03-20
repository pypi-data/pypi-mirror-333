
# This is a generated file

"""pvwattsv8 - PVWatts V8 - integrated hourly weather reader and PV system simulator."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'gen': Array,
    'annual_energy_distribution_time': Matrix,
    'solar_resource_file': str,
    'solar_resource_data': Table,
    'albedo': Array,
    'albedo_default': float,
    'albedo_default_snow': float,
    'use_wf_albedo': float,
    'system_use_lifetime_output': float,
    'analysis_period': float,
    'dc_degradation': Array,
    'system_capacity': float,
    'module_type': float,
    'dc_ac_ratio': float,
    'bifaciality': float,
    'array_type': float,
    'tilt': float,
    'azimuth': float,
    'gcr': float,
    'rotlim': float,
    'soiling': Array,
    'losses': float,
    'enable_wind_stow': float,
    'stow_wspd': float,
    'gust_factor': float,
    'wind_stow_angle': float,
    'en_snowloss': float,
    'inv_eff': float,
    'xfmr_nll': float,
    'xfmr_ll': float,
    'shading_en_string_option': float,
    'shading_string_option': float,
    'shading_en_timestep': float,
    'shading_timestep': Matrix,
    'shading_en_mxh': float,
    'shading_mxh': Matrix,
    'shading_en_azal': float,
    'shading_azal': Matrix,
    'shading_en_diff': float,
    'shading_diff': float,
    'batt_simple_enable': float,
    'gh': Array,
    'dn': Array,
    'df': Array,
    'tamb': Array,
    'wspd': Array,
    'snow': Array,
    'alb': Array,
    'soiling_f': Array,
    'sunup': Array,
    'shad_beam_factor': Array,
    'ss_beam_factor': Array,
    'ss_sky_diffuse_factor': Array,
    'ss_gnd_diffuse_factor': Array,
    'aoi': Array,
    'poa': Array,
    'tpoa': Array,
    'tcell': Array,
    'dcsnowderate': Array,
    'snow_cover': Array,
    'dc': Array,
    'ac': Array,
    'ac_pre_adjust': Array,
    'inv_eff_output': Array,
    'poa_monthly': Array,
    'solrad_monthly': Array,
    'dc_monthly': Array,
    'ac_monthly': Array,
    'monthly_energy': Array,
    'solrad_annual': float,
    'ac_annual': float,
    'ac_annual_pre_adjust': float,
    'annual_energy': float,
    'capacity_factor': float,
    'capacity_factor_ac': float,
    'kwh_per_kw': float,
    'location': str,
    'city': str,
    'state': str,
    'lat': float,
    'lon': float,
    'tz': float,
    'elev': float,
    'inverter_efficiency': float,
    'ts_shift_hours': float,
    'percent_complete': float,
    'system_capacity_ac': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix,
    'cf_om_production': Array,
    'cf_om_capacity': Array,
    'cf_om_fixed': Array,
    'cf_om_land_lease': Array,
    'cf_om_fuel_cost': Array,
    'cf_battery_replacement_cost_schedule': Array,
    'cf_fuelcell_replacement_cost_schedule': Array,
    'cf_energy_net': Array
}, total=False)

class Data(ssc.DataDict):
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='Time Series', required='*')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')
    solar_resource_file: str = INPUT(label='Weather file path', type='STRING', group='Solar Resource')
    solar_resource_data: Table = INPUT(label='Weather data', type='TABLE', group='Solar Resource', meta='dn,df,tdry,wspd,lat,lon,tz,elev')
    albedo: Array = INPUT(label='Albedo', units='0..1', type='ARRAY', group='Solar Resource', meta='albedo input array of 1 constant value or 12 monthly values')
    albedo_default: float = INPUT(label='Albedo default', units='0..1', type='NUMBER', group='Solar Resource', required='?=0.2', meta='default when albedo invalid')
    albedo_default_snow: float = INPUT(label='Albedo default for snow', units='0..1', type='NUMBER', group='Solar Resource', required='?=0.6', meta='default when albedo invalid and snow model enabled')
    use_wf_albedo: float = INPUT(label='Use albedo from weather file', units='0/1', type='NUMBER', group='Solar Resource', required='?=1', constraints='BOOLEAN', meta='0=albedo input, 1=albedo from weather file (use albedo default if invalid)')
    system_use_lifetime_output: float = INOUT(label='Run lifetime simulation', units='0/1', type='NUMBER', group='Lifetime', required='?=0')
    analysis_period: float = INPUT(label='Analysis period', units='years', type='NUMBER', group='Lifetime', required='system_use_lifetime_output=1')
    dc_degradation: Array = INPUT(label='Annual DC degradation for lifetime simulations', units='%/year', type='ARRAY', group='Lifetime', required='system_use_lifetime_output=1')
    system_capacity: float = INPUT(label='System size (DC nameplate)', units='kW', type='NUMBER', group='System Design', required='*')
    module_type: float = INPUT(label='Module type', units='0/1/2', type='NUMBER', group='System Design', required='?=0', constraints='MIN=0,MAX=2,INTEGER', meta='standard,premium,thin film')
    dc_ac_ratio: float = INPUT(label='DC to AC ratio', units='ratio', type='NUMBER', group='System Design', required='?=1.1', constraints='POSITIVE')
    bifaciality: float = INPUT(label='Module bifaciality factor', units='0 or ~0.65', type='NUMBER', group='System Design', required='?=0')
    array_type: float = INPUT(label='Array type', units='0/1/2/3/4', type='NUMBER', group='System Design', required='*', constraints='MIN=0,MAX=4,INTEGER', meta='fixed open rack,fixed roof mount,1-axis tracking,1-axis backtracking,2-axis tracking')
    tilt: float = INPUT(label='Tilt angle', units='degrees', type='NUMBER', group='System Design', required='array_type<4', constraints='MIN=0,MAX=90', meta='H=0,V=90')
    azimuth: float = INPUT(label='Azimuth angle', units='degrees', type='NUMBER', group='System Design', required='array_type<4', constraints='MIN=0,MAX=360', meta='E=90,S=180,W=270')
    gcr: float = INPUT(label='Ground coverage ratio', units='0..1', type='NUMBER', group='System Design', required='?=0.3', constraints='MIN=0.01,MAX=0.99')
    rotlim: float = INPUT(label='Tracker rotation angle limit', units='degrees', type='NUMBER', group='System Design', required='?=45.0')
    soiling: Array = INPUT(label='Soiling loss', units='%', type='ARRAY', group='System Design', required='?')
    losses: float = INPUT(label='DC system losses', units='%', type='NUMBER', group='System Design', required='*', constraints='MIN=-5,MAX=99', meta='total system losses')
    enable_wind_stow: float = INPUT(label='Enable tracker stow at high wind speeds', units='0/1', type='NUMBER', group='System Design', required='?=0', constraints='BOOLEAN')
    stow_wspd: float = INPUT(label='Tracker stow wind speed threshold', units='m/s', type='NUMBER', group='System Design', required='?=10')
    gust_factor: float = INPUT(label='Wind gust estimation factor', type='NUMBER', group='System Design', required='?')
    wind_stow_angle: float = INPUT(label='Tracker angle for wind stow', units='degrees', type='NUMBER', group='System Design', required='?=30.0')
    en_snowloss: float = INPUT(label='Enable snow loss model', units='0/1', type='NUMBER', group='System Design', required='?=0', constraints='BOOLEAN')
    inv_eff: float = INPUT(label='Inverter efficiency at rated power', units='%', type='NUMBER', group='System Design', required='?=96', constraints='MIN=90,MAX=99.5')
    xfmr_nll: float = INPUT(label='GSU transformer no load loss (iron core)', units='%(ac)', type='NUMBER', group='System Design', required='?=0.0')
    xfmr_ll: float = INPUT(label='GSU transformer load loss (resistive)', units='%(ac)', type='NUMBER', group='System Design', required='?=0.0')
    shading_en_string_option: float = INPUT(label='Enable shading string option', units='0/1', type='NUMBER', group='Shading', required='?=0', constraints='BOOLEAN', meta='0=false,1=true')
    shading_string_option: float = INPUT(label='Shading string option', type='NUMBER', group='Shading', required='?=-1', constraints='INTEGER,MIN=-1,MAX=4', meta='0=shadingdb,1=average,2=maximum,3=minimum')
    shading_en_timestep: float = INPUT(label='Enable timestep beam shading losses', units='0/1', type='NUMBER', group='Shading', required='?=0', constraints='BOOLEAN', meta='0=false,1=true')
    shading_timestep: Matrix = INPUT(label='Timestep beam shading losses', units='%', type='MATRIX', group='Shading', required='?')
    shading_en_mxh: float = INPUT(label='Enable month x Hour beam shading losses', units='0/1', type='NUMBER', group='Shading', required='?=0', constraints='BOOLEAN', meta='0=false,1=true')
    shading_mxh: Matrix = INPUT(label='Month x Hour beam shading losses', units='%', type='MATRIX', group='Shading', required='?')
    shading_en_azal: float = INPUT(label='Enable azimuth x altitude beam shading losses', units='0/1', type='NUMBER', group='Shading', required='?=0', constraints='BOOLEAN', meta='0=false,1=true')
    shading_azal: Matrix = INPUT(label='Azimuth x altitude beam shading losses', units='%', type='MATRIX', group='Shading', required='?')
    shading_en_diff: float = INPUT(label='Enable diffuse shading loss', units='0/1', type='NUMBER', group='Shading', required='?=0', constraints='BOOLEAN', meta='0=false,1=true')
    shading_diff: float = INPUT(label='Diffuse shading loss', units='%', type='NUMBER', group='Shading', required='?')
    batt_simple_enable: float = INPUT(label='Enable Battery', units='0/1', type='NUMBER', group='System Design', required='?=0', constraints='BOOLEAN')
    gh: Final[Array] = OUTPUT(label='Weather file global horizontal irradiance', units='W/m2', type='ARRAY', group='Time Series', required='*')
    dn: Final[Array] = OUTPUT(label='Weather file beam irradiance', units='W/m2', type='ARRAY', group='Time Series', required='*')
    df: Final[Array] = OUTPUT(label='Weather file diffuse irradiance', units='W/m2', type='ARRAY', group='Time Series', required='*')
    tamb: Final[Array] = OUTPUT(label='Weather file ambient temperature', units='C', type='ARRAY', group='Time Series', required='*')
    wspd: Final[Array] = OUTPUT(label='Weather file wind speed', units='m/s', type='ARRAY', group='Time Series', required='*')
    snow: Final[Array] = OUTPUT(label='Weather file snow depth', units='cm', type='ARRAY', group='Time Series')
    alb: Final[Array] = OUTPUT(label='Albedo', type='ARRAY', group='Time Series')
    soiling_f: Final[Array] = OUTPUT(label='Soiling factor', type='ARRAY', group='Time Series')
    sunup: Final[Array] = OUTPUT(label='Sun up over horizon', units='0/1', type='ARRAY', group='Time Series', required='*')
    shad_beam_factor: Final[Array] = OUTPUT(label='External shading factor for beam radiation', type='ARRAY', group='Time Series', required='*')
    ss_beam_factor: Final[Array] = OUTPUT(label='Calculated self-shading factor for beam radiation', type='ARRAY', group='Time Series', required='*', meta='1=no shading')
    ss_sky_diffuse_factor: Final[Array] = OUTPUT(label='Calculated self-shading factor for sky diffuse radiation', type='ARRAY', group='Time Series', required='*', meta='1=no shading')
    ss_gnd_diffuse_factor: Final[Array] = OUTPUT(label='Calculated self-shading factor for ground-reflected diffuse radiation', type='ARRAY', group='Time Series', required='*', meta='1=no shading')
    aoi: Final[Array] = OUTPUT(label='Angle of incidence', units='degrees', type='ARRAY', group='Time Series', required='*')
    poa: Final[Array] = OUTPUT(label='Plane of array irradiance', units='W/m2', type='ARRAY', group='Time Series', required='*')
    tpoa: Final[Array] = OUTPUT(label='Transmitted plane of array irradiance', units='W/m2', type='ARRAY', group='Time Series', required='*')
    tcell: Final[Array] = OUTPUT(label='Module temperature', units='C', type='ARRAY', group='Time Series', required='*')
    dcsnowderate: Final[Array] = OUTPUT(label='DC power loss due to snow', units='%', type='ARRAY', group='Time Series', required='*')
    snow_cover: Final[Array] = OUTPUT(label='Fraction of row covered by snow', units='0..1', type='ARRAY', group='Time Series', required='*')
    dc: Final[Array] = OUTPUT(label='DC inverter input power', units='W', type='ARRAY', group='Time Series', required='*')
    ac: Final[Array] = OUTPUT(label='AC inverter output power', units='W', type='ARRAY', group='Time Series', required='*')
    ac_pre_adjust: Final[Array] = OUTPUT(label='AC inverter output power before system availability', units='W', type='ARRAY', group='Time Series', required='*')
    inv_eff_output: Final[Array] = OUTPUT(label='Inverter efficiency', units='%', type='ARRAY', group='Time Series', required='*')
    poa_monthly: Final[Array] = OUTPUT(label='Plane of array irradiance', units='kWh/m2', type='ARRAY', group='Monthly', constraints='LENGTH=12')
    solrad_monthly: Final[Array] = OUTPUT(label='Daily average solar irradiance', units='kWh/m2/day', type='ARRAY', group='Monthly', constraints='LENGTH=12')
    dc_monthly: Final[Array] = OUTPUT(label='Monthly DC energy', units='kWh', type='ARRAY', group='Monthly', constraints='LENGTH=12')
    ac_monthly: Final[Array] = OUTPUT(label='Monthly AC energy', units='kWh', type='ARRAY', group='Monthly', constraints='LENGTH=12')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly AC energy in Year 1', units='kWh', type='ARRAY', group='Monthly', constraints='LENGTH=12')
    solrad_annual: Final[float] = OUTPUT(label='Daily average solar irradiance', units='kWh/m2/day', type='NUMBER', group='Annual')
    ac_annual: Final[float] = OUTPUT(label='Annual AC output', units='kWh', type='NUMBER', group='Annual')
    ac_annual_pre_adjust: Final[float] = OUTPUT(label='Annual AC output before system availability', units='kWh', type='NUMBER', group='Annual')
    annual_energy: Final[float] = OUTPUT(label='Annual AC energy in Year 1', units='kWh', type='NUMBER', group='Annual')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor based on nameplate DC capacity', units='%', type='NUMBER', group='Annual')
    capacity_factor_ac: Final[float] = OUTPUT(label='Capacity factor based on total AC capacity', units='%', type='NUMBER', group='Annual')
    kwh_per_kw: Final[float] = OUTPUT(label='Energy yield', units='kWh/kW', type='NUMBER', group='Annual')
    location: Final[str] = OUTPUT(label='Location ID', type='STRING', group='Location', required='*')
    city: Final[str] = OUTPUT(label='City', type='STRING', group='Location', required='*')
    state: Final[str] = OUTPUT(label='State', type='STRING', group='Location', required='*')
    lat: Final[float] = OUTPUT(label='Latitude', units='degrees', type='NUMBER', group='Location', required='*')
    lon: Final[float] = OUTPUT(label='Longitude', units='degrees', type='NUMBER', group='Location', required='*')
    tz: Final[float] = OUTPUT(label='Time zone', units='UTC offset', type='NUMBER', group='Location', required='*')
    elev: Final[float] = OUTPUT(label='Site elevation', units='m', type='NUMBER', group='Location', required='*')
    inverter_efficiency: Final[float] = OUTPUT(label='Inverter efficiency at rated power', units='%', type='NUMBER', group='PVWatts')
    ts_shift_hours: Final[float] = OUTPUT(label='Time offset for interpreting time series outputs', units='hours', type='NUMBER', group='Miscellaneous', required='*')
    percent_complete: Final[float] = OUTPUT(label='Estimated percent of total completed simulation', units='%', type='NUMBER', group='Miscellaneous')
    system_capacity_ac: Final[float] = OUTPUT(label='System nameplate AC rating', units='kWac', type='NUMBER', group='Miscellaneous')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")
    cf_om_production: Final[Array] = OUTPUT(label='production O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_capacity: Final[Array] = OUTPUT(label='capacity O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fixed: Final[Array] = OUTPUT(label='fixed O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_land_lease: Final[Array] = OUTPUT(label='land lease O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fuel_cost: Final[Array] = OUTPUT(label='fossil fuel O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_battery_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_fuelcell_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_energy_net: Final[Array] = OUTPUT(label='annual energy', units='kWh', type='ARRAY', group='HybridCosts')

    def __init__(self, *args: Mapping[str, Any],
                 solar_resource_file: str = ...,
                 solar_resource_data: Table = ...,
                 albedo: Array = ...,
                 albedo_default: float = ...,
                 albedo_default_snow: float = ...,
                 use_wf_albedo: float = ...,
                 system_use_lifetime_output: float = ...,
                 analysis_period: float = ...,
                 dc_degradation: Array = ...,
                 system_capacity: float = ...,
                 module_type: float = ...,
                 dc_ac_ratio: float = ...,
                 bifaciality: float = ...,
                 array_type: float = ...,
                 tilt: float = ...,
                 azimuth: float = ...,
                 gcr: float = ...,
                 rotlim: float = ...,
                 soiling: Array = ...,
                 losses: float = ...,
                 enable_wind_stow: float = ...,
                 stow_wspd: float = ...,
                 gust_factor: float = ...,
                 wind_stow_angle: float = ...,
                 en_snowloss: float = ...,
                 inv_eff: float = ...,
                 xfmr_nll: float = ...,
                 xfmr_ll: float = ...,
                 shading_en_string_option: float = ...,
                 shading_string_option: float = ...,
                 shading_en_timestep: float = ...,
                 shading_timestep: Matrix = ...,
                 shading_en_mxh: float = ...,
                 shading_mxh: Matrix = ...,
                 shading_en_azal: float = ...,
                 shading_azal: Matrix = ...,
                 shading_en_diff: float = ...,
                 shading_diff: float = ...,
                 batt_simple_enable: float = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
