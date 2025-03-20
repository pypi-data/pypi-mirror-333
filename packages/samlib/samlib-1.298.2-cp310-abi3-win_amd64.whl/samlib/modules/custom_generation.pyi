
# This is a generated file

"""custom_generation - Custom Generation Profile (formerly Generic System)"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'spec_mode': float,
    'derate': float,
    'system_capacity': float,
    'user_capacity_factor': float,
    'heat_rate': float,
    'conv_eff': float,
    'energy_output_array': Array,
    'system_use_lifetime_output': float,
    'analysis_period': float,
    'generic_degradation': Array,
    'monthly_energy': Array,
    'annual_energy': float,
    'annual_fuel_usage': float,
    'water_usage': float,
    'system_heat_rate': float,
    'capacity_factor': float,
    'kwh_per_kw': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix,
    'gen': Array,
    'annual_energy_distribution_time': Matrix,
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
    spec_mode: float = INPUT(label='Spec mode: 0=constant CF,1=profile', type='NUMBER', group='Plant', required='*')
    derate: float = INPUT(label='Derate', units='%', type='NUMBER', group='Plant', required='*')
    system_capacity: float = INOUT(label='Nameplace Capcity', units='kW', type='NUMBER', group='Plant', required='*')
    user_capacity_factor: float = INPUT(label='Capacity Factor', units='%', type='NUMBER', group='Plant', required='*')
    heat_rate: float = INPUT(label='Heat Rate', units='MMBTUs/MWhe', type='NUMBER', group='Plant', required='*')
    conv_eff: float = INPUT(label='Conversion Efficiency', units='%', type='NUMBER', group='Plant', required='*')
    energy_output_array: Array = INPUT(label='Array of Energy Output Profile', units='kW', type='ARRAY', group='Plant', required='spec_mode=1')
    system_use_lifetime_output: float = INPUT(label='Custom generation profile lifetime simulation', units='0/1', type='NUMBER', group='Lifetime', required='?=0', constraints='INTEGER,MIN=0,MAX=1')
    analysis_period: float = INPUT(label='Lifetime analysis period', units='years', type='NUMBER', group='Lifetime', required='system_use_lifetime_output=1')
    generic_degradation: Array = INPUT(label='Annual AC degradation', units='%/year', type='ARRAY', group='Lifetime', required='system_use_lifetime_output=1')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly Energy Gross', units='kWh', type='ARRAY', group='Monthly', required='*', constraints='LENGTH=12')
    annual_energy: Final[float] = OUTPUT(label='Annual Energy', units='kWh', type='NUMBER', group='Annual', required='*')
    annual_fuel_usage: Final[float] = OUTPUT(label='Annual Fuel Usage', units='kWht', type='NUMBER', group='Annual', required='*')
    water_usage: Final[float] = OUTPUT(label='Annual Water Usage', type='NUMBER', group='Annual', required='*')
    system_heat_rate: Final[float] = OUTPUT(label='Heat Rate Conversion Factor', units='MMBTUs/MWhe', type='NUMBER', group='Annual', required='*')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='Annual', required='*')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', group='Annual', required='*')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='Time Series', required='*')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')
    cf_om_production: Final[Array] = OUTPUT(label='production O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_capacity: Final[Array] = OUTPUT(label='capacity O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fixed: Final[Array] = OUTPUT(label='fixed O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_land_lease: Final[Array] = OUTPUT(label='land lease O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_om_fuel_cost: Final[Array] = OUTPUT(label='fossil fuel O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_battery_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_fuelcell_replacement_cost_schedule: Final[Array] = OUTPUT(label='replacement O&M costs', units='$', type='ARRAY', group='HybridCosts')
    cf_energy_net: Final[Array] = OUTPUT(label='annual energy', units='kWh', type='ARRAY', group='HybridCosts')

    def __init__(self, *args: Mapping[str, Any],
                 spec_mode: float = ...,
                 derate: float = ...,
                 system_capacity: float = ...,
                 user_capacity_factor: float = ...,
                 heat_rate: float = ...,
                 conv_eff: float = ...,
                 energy_output_array: Array = ...,
                 system_use_lifetime_output: float = ...,
                 analysis_period: float = ...,
                 generic_degradation: Array = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
