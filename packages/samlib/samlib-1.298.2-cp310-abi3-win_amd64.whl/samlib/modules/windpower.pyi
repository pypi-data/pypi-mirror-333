
# This is a generated file

"""windpower - Utility scale wind farm model (adapted from TRNSYS code by P.Quinlan and openWind software by AWS Truepower)"""

# VERSION: 2

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'wind_resource_model_choice': float,
    'wind_resource_filename': str,
    'wind_resource_data': Table,
    'wind_resource_distribution': Matrix,
    'weibull_reference_height': float,
    'weibull_k_factor': float,
    'weibull_wind_speed': float,
    'wind_resource_shear': float,
    'wind_turbine_rotor_diameter': float,
    'wind_turbine_powercurve_windspeeds': Array,
    'wind_turbine_powercurve_powerout': Array,
    'wind_turbine_hub_ht': float,
    'wind_turbine_max_cp': float,
    'wind_farm_wake_model': float,
    'park_wake_decay_constant': float,
    'wind_resource_turbulence_coeff': float,
    'system_capacity': float,
    'wind_farm_xCoordinates': Array,
    'wind_farm_yCoordinates': Array,
    'max_turbine_override': float,
    'en_low_temp_cutoff': float,
    'low_temp_cutoff': float,
    'en_icing_cutoff': float,
    'icing_cutoff_temp': float,
    'icing_cutoff_rh': float,
    'icing_persistence_timesteps': float,
    'wake_loss_multiplier': float,
    'wind_turbine_ct_curve': Array,
    'wake_int_loss': float,
    'wake_ext_loss': float,
    'wake_future_loss': float,
    'avail_bop_loss': float,
    'avail_grid_loss': float,
    'avail_turb_loss': float,
    'elec_eff_loss': float,
    'elec_parasitic_loss': float,
    'env_degrad_loss': float,
    'env_exposure_loss': float,
    'env_env_loss': float,
    'env_icing_loss': float,
    'ops_env_loss': float,
    'ops_grid_loss': float,
    'ops_load_loss': float,
    'ops_strategies_loss': float,
    'turb_generic_loss': float,
    'turb_hysteresis_loss': float,
    'turb_perf_loss': float,
    'turb_specific_loss': float,
    'turbine_output_by_windspeed_bin': Array,
    'wind_direction': Array,
    'wind_speed': Array,
    'temp': Array,
    'pressure': Array,
    'lat': float,
    'lon': float,
    'elev': float,
    'year': float,
    'wake_loss_internal_kW': Array,
    'wake_loss_internal_percent': Array,
    'monthly_energy': Array,
    'annual_energy': float,
    'annual_gross_energy': float,
    'capacity_factor': float,
    'kwh_per_kw': float,
    'wind_speed_average': float,
    'avail_losses': float,
    'elec_losses': float,
    'env_losses': float,
    'ops_losses': float,
    'turb_losses': float,
    'annual_wake_loss_internal_percent': float,
    'annual_wake_loss_internal_kWh': float,
    'annual_wake_loss_total_percent': float,
    'cutoff_losses': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix,
    'gen': Array,
    'annual_energy_distribution_time': Matrix,
    'total_uncert': float,
    'annual_energy_p75': float,
    'annual_energy_p90': float,
    'annual_energy_p95': float,
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
    wind_resource_model_choice: float = INPUT(label='Hourly, Weibull or Distribution model', units='0/1/2', type='NUMBER', group='Resource', required='*', constraints='INTEGER')
    wind_resource_filename: str = INPUT(label='Local wind data file path', type='STRING', group='Resource', required='?', constraints='LOCAL_FILE')
    wind_resource_data: Table = INPUT(label='Wind resouce data in memory', type='TABLE', group='Resource', required='?')
    wind_resource_distribution: Matrix = INPUT(label='Wind Speed x Dir Distribution as 2-D PDF', units='m/s,deg', type='MATRIX', group='Resource', required='wind_resource_model_choice=2')
    weibull_reference_height: float = INPUT(label='Reference height for Weibull wind speed', units='m', type='NUMBER', group='Resource', required='?=50', constraints='MIN=0')
    weibull_k_factor: float = INPUT(label='Weibull K factor for wind resource', type='NUMBER', group='Resource', required='wind_resource_model_choice=1')
    weibull_wind_speed: float = INPUT(label='Average wind speed for Weibull model', type='NUMBER', group='Resource', required='wind_resource_model_choice=1', constraints='MIN=0')
    wind_resource_shear: float = INPUT(label='Shear exponent', type='NUMBER', group='Turbine', required='*', constraints='MIN=0')
    wind_turbine_rotor_diameter: float = INPUT(label='Rotor diameter', units='m', type='NUMBER', group='Turbine', required='*', constraints='POSITIVE')
    wind_turbine_powercurve_windspeeds: Array = INOUT(label='Power curve wind speed array', units='m/s', type='ARRAY', group='Turbine', required='*')
    wind_turbine_powercurve_powerout: Array = INOUT(label='Power curve turbine output array', units='kW', type='ARRAY', group='Turbine', required='*', constraints='LENGTH_EQUAL=wind_turbine_powercurve_windspeeds')
    wind_turbine_hub_ht: float = INPUT(label='Hub height', units='m', type='NUMBER', group='Turbine', required='*', constraints='POSITIVE')
    wind_turbine_max_cp: float = INPUT(label='Max Coefficient of Power', type='NUMBER', group='Turbine', required='wind_resource_model_choice=1', constraints='MIN=0')
    wind_farm_wake_model: float = INPUT(label='Wake Model [Simple, Park, EV, Constant]', units='0/1/2/3', type='NUMBER', group='Farm', required='*', constraints='INTEGER')
    park_wake_decay_constant: float = INPUT(label='Wake decay constant for Park model', units='0..1', type='NUMBER', group='Farm')
    wind_resource_turbulence_coeff: float = INPUT(label='Turbulence coefficient', units='%', type='NUMBER', group='Farm', required='*', constraints='MIN=0')
    system_capacity: float = INPUT(label='Nameplate capacity', units='kW', type='NUMBER', group='Farm', required='*', constraints='MIN=0')
    wind_farm_xCoordinates: Array = INPUT(label='Turbine X coordinates', units='m', type='ARRAY', group='Farm', required='*')
    wind_farm_yCoordinates: Array = INPUT(label='Turbine Y coordinates', units='m', type='ARRAY', group='Farm', required='*', constraints='LENGTH_EQUAL=wind_farm_xCoordinates')
    max_turbine_override: float = INPUT(label='Override the max number of turbines for wake modeling', units='numTurbines', type='NUMBER', group='Farm', meta='set new max num turbines')
    en_low_temp_cutoff: float = INPUT(label='Enable Low Temperature Cutoff', units='0/1', type='NUMBER', group='Losses', required='?=0', constraints='INTEGER')
    low_temp_cutoff: float = INPUT(label='Low Temperature Cutoff', units='C', type='NUMBER', group='Losses', required='en_low_temp_cutoff=1')
    en_icing_cutoff: float = INPUT(label='Enable Icing Cutoff', units='0/1', type='NUMBER', group='Losses', required='?=0', constraints='INTEGER')
    icing_cutoff_temp: float = INPUT(label='Icing Cutoff Temperature', units='C', type='NUMBER', group='Losses', required='en_icing_cutoff=1')
    icing_cutoff_rh: float = INPUT(label='Icing Cutoff Relative Humidity', units='%', type='NUMBER', group='Losses', required='en_icing_cutoff=1', constraints='MIN=0', meta="'rh' required in wind_resource_data")
    icing_persistence_timesteps: float = INPUT(label='Num timesteps icing lasts if conditions are met', type='NUMBER', group='Losses', required='?=1', constraints='MIN=1,INTEGER', meta='includes initial timestep')
    wake_loss_multiplier: float = INPUT(label='Multiplier for the calculated wake loss', type='NUMBER', group='Farm', constraints='MIN=0', meta='>1 increases loss, <1 decreases loss')
    wind_turbine_ct_curve: Array = INOUT(label='User-defined Ct curve vs WS for wake models', type='ARRAY', group='Turbine', constraints='LENGTH_EQUAL=wind_turbine_powercurve_windspeeds', meta='uses same wind speeds as power curve')
    wake_int_loss: float = INPUT(label='Constant Wake Model, internal wake loss', units='%', type='NUMBER', group='Losses', required='wind_farm_wake_model=3', constraints='MIN=0,MAX=100')
    wake_ext_loss: float = INPUT(label='External Wake loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    wake_future_loss: float = INPUT(label='Future Wake loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    avail_bop_loss: float = INPUT(label='Balance-of-plant availability loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    avail_grid_loss: float = INPUT(label='Grid availability loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    avail_turb_loss: float = INPUT(label='Turbine availabaility loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    elec_eff_loss: float = INPUT(label='Electrical efficiency loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    elec_parasitic_loss: float = INPUT(label='Electrical parasitic consumption loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    env_degrad_loss: float = INPUT(label='Environmental Degradation loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    env_exposure_loss: float = INPUT(label='Environmental Exposure loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    env_env_loss: float = INPUT(label='Environmental External Conditions loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    env_icing_loss: float = INPUT(label='Environmental Icing loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    ops_env_loss: float = INPUT(label='Environmental/Permit Curtailment loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    ops_grid_loss: float = INPUT(label='Grid curtailment loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    ops_load_loss: float = INPUT(label='Load curtailment loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    ops_strategies_loss: float = INPUT(label='Operational strategies loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    turb_generic_loss: float = INPUT(label='Turbine Generic Powercurve loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    turb_hysteresis_loss: float = INPUT(label='Turbine High Wind Hysteresis loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    turb_perf_loss: float = INPUT(label='Turbine Sub-optimal performance loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    turb_specific_loss: float = INPUT(label='Turbine Site-specific Powercurve loss', units='%', type='NUMBER', group='Losses', required='?=0', constraints='MIN=0,MAX=100')
    turbine_output_by_windspeed_bin: Final[Array] = OUTPUT(label='Turbine output by wind speed bin', units='kW', type='ARRAY', group='Power Curve', constraints='LENGTH_EQUAL=wind_turbine_powercurve_windspeeds')
    wind_direction: Final[Array] = OUTPUT(label='Wind direction', units='degrees', type='ARRAY', group='Time Series', required='wind_resource_model_choice=0')
    wind_speed: Final[Array] = OUTPUT(label='Wind speed', units='m/s', type='ARRAY', group='Time Series', required='wind_resource_model_choice=0')
    temp: Final[Array] = OUTPUT(label='Air temperature', units="'C", type='ARRAY', group='Time Series', required='wind_resource_model_choice=0')
    pressure: Final[Array] = OUTPUT(label='Pressure', units='atm', type='ARRAY', group='Time Series', required='wind_resource_model_choice=0')
    lat: Final[float] = OUTPUT(label='Latitude', units='degrees', type='NUMBER', group='Location', required='wind_resource_model_choice=0')
    lon: Final[float] = OUTPUT(label='Longitude', units='degrees', type='NUMBER', group='Location', required='wind_resource_model_choice=0')
    elev: Final[float] = OUTPUT(label='Site elevation', units='m', type='NUMBER', group='Location', required='wind_resource_model_choice=0')
    year: Final[float] = OUTPUT(label='Year', type='NUMBER', group='Location', required='wind_resource_model_choice=0')
    wake_loss_internal_kW: Final[Array] = OUTPUT(label='Internal wake loss in kW', units='kW', type='ARRAY', group='Time Series')
    wake_loss_internal_percent: Final[Array] = OUTPUT(label='Internal wake loss percent', units='%', type='ARRAY', group='Time Series')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly AC energy in Year 1', units='kWh', type='ARRAY', group='Monthly', required='*', constraints='LENGTH=12')
    annual_energy: Final[float] = OUTPUT(label='Annual AC energy in Year 1', units='kWh', type='NUMBER', group='Annual', required='*')
    annual_gross_energy: Final[float] = OUTPUT(label='Annual gross AC energy in Year 1', units='kWh', type='NUMBER', group='Annual', required='*')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='Annual', required='*')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', group='Annual', required='*')
    wind_speed_average: Final[float] = OUTPUT(label='Average Wind speed', units='m/s', type='NUMBER', group='Annual')
    avail_losses: Final[float] = OUTPUT(label='Availability losses', units='%', type='NUMBER', group='Annual')
    elec_losses: Final[float] = OUTPUT(label='Electrical losses', units='%', type='NUMBER', group='Annual')
    env_losses: Final[float] = OUTPUT(label='Environmental losses', units='%', type='NUMBER', group='Annual')
    ops_losses: Final[float] = OUTPUT(label='Operational losses', units='%', type='NUMBER', group='Annual')
    turb_losses: Final[float] = OUTPUT(label='Turbine losses', units='%', type='NUMBER', group='Annual')
    annual_wake_loss_internal_percent: Final[float] = OUTPUT(label='Annual internal wake loss percentage', units='%', type='NUMBER', group='Annual')
    annual_wake_loss_internal_kWh: Final[float] = OUTPUT(label='Annual internal wake loss', units='kWh', type='NUMBER', group='Annual')
    annual_wake_loss_total_percent: Final[float] = OUTPUT(label='Annual total wake loss percentage', units='%', type='NUMBER', group='Annual')
    cutoff_losses: Final[float] = OUTPUT(label='Low temp and Icing Cutoff losses', units='%', type='NUMBER', group='Annual')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='Time Series', required='*')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')
    total_uncert: float = INPUT(label='Total uncertainty in energy production as percent of annual energy', units='%', type='NUMBER', group='Uncertainty', constraints='MIN=0,MAX=100')
    annual_energy_p75: Final[float] = OUTPUT(label='Annual energy with 75% probability of exceedance', units='kWh', type='NUMBER', group='Uncertainty')
    annual_energy_p90: Final[float] = OUTPUT(label='Annual energy with 90% probability of exceedance', units='kWh', type='NUMBER', group='Uncertainty')
    annual_energy_p95: Final[float] = OUTPUT(label='Annual energy with 95% probability of exceedance', units='kWh', type='NUMBER', group='Uncertainty')
    cf_om_production: Final[Array] = OUTPUT(label='production O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_capacity: Final[Array] = OUTPUT(label='capacity O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fixed: Final[Array] = OUTPUT(label='fixed O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_land_lease: Final[Array] = OUTPUT(label='land lease O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fuel_cost: Final[Array] = OUTPUT(label='fossil fuel O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_battery_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_fuelcell_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_energy_net: Final[Array] = OUTPUT(label='annual energy', units='kWh', type='ARRAY', group='HybridCosts')

    def __init__(self, *args: Mapping[str, Any],
                 wind_resource_model_choice: float = ...,
                 wind_resource_filename: str = ...,
                 wind_resource_data: Table = ...,
                 wind_resource_distribution: Matrix = ...,
                 weibull_reference_height: float = ...,
                 weibull_k_factor: float = ...,
                 weibull_wind_speed: float = ...,
                 wind_resource_shear: float = ...,
                 wind_turbine_rotor_diameter: float = ...,
                 wind_turbine_powercurve_windspeeds: Array = ...,
                 wind_turbine_powercurve_powerout: Array = ...,
                 wind_turbine_hub_ht: float = ...,
                 wind_turbine_max_cp: float = ...,
                 wind_farm_wake_model: float = ...,
                 park_wake_decay_constant: float = ...,
                 wind_resource_turbulence_coeff: float = ...,
                 system_capacity: float = ...,
                 wind_farm_xCoordinates: Array = ...,
                 wind_farm_yCoordinates: Array = ...,
                 max_turbine_override: float = ...,
                 en_low_temp_cutoff: float = ...,
                 low_temp_cutoff: float = ...,
                 en_icing_cutoff: float = ...,
                 icing_cutoff_temp: float = ...,
                 icing_cutoff_rh: float = ...,
                 icing_persistence_timesteps: float = ...,
                 wake_loss_multiplier: float = ...,
                 wind_turbine_ct_curve: Array = ...,
                 wake_int_loss: float = ...,
                 wake_ext_loss: float = ...,
                 wake_future_loss: float = ...,
                 avail_bop_loss: float = ...,
                 avail_grid_loss: float = ...,
                 avail_turb_loss: float = ...,
                 elec_eff_loss: float = ...,
                 elec_parasitic_loss: float = ...,
                 env_degrad_loss: float = ...,
                 env_exposure_loss: float = ...,
                 env_env_loss: float = ...,
                 env_icing_loss: float = ...,
                 ops_env_loss: float = ...,
                 ops_grid_loss: float = ...,
                 ops_load_loss: float = ...,
                 ops_strategies_loss: float = ...,
                 turb_generic_loss: float = ...,
                 turb_hysteresis_loss: float = ...,
                 turb_perf_loss: float = ...,
                 turb_specific_loss: float = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...,
                 total_uncert: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
