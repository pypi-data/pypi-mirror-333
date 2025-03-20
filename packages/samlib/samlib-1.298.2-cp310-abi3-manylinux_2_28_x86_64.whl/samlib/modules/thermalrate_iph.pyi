
# This is a generated file

"""thermalrate_iph - Thermal flat rate structure net revenue calculator"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'en_thermal_rates': float,
    'analysis_period': float,
    'system_use_lifetime_output': float,
    'gen_heat': Array,
    'thermal_load_heat_btu': Array,
    'inflation_rate': float,
    'thermal_degradation': Array,
    'thermal_load_escalation': Array,
    'thermal_rate_escalation': Array,
    'thermal_conversion_efficiency': float,
    'thermal_buy_rate_option': float,
    'thermal_buy_rate_flat_heat_btu': float,
    'thermal_timestep_buy_rate_heat_btu': Array,
    'thermal_monthly_buy_rate_heat_btu': Array,
    'thermal_sell_rate_option': float,
    'thermal_sell_rate_flat_heat_btu': float,
    'thermal_timestep_sell_rate_heat_btu': Array,
    'thermal_monthly_sell_rate_heat_btu': Array,
    'annual_thermal_value': Array,
    'thermal_revenue_with_system': Array,
    'thermal_revenue_without_system': Array,
    'thermal_cost_with_system': Array,
    'thermal_cost_without_system': Array,
    'thermal_load_year1': float,
    'thermal_savings_year1': float,
    'thermal_cost_with_system_year1': float,
    'thermal_cost_without_system_year1': float,
    'year1_monthly_load_heat': Array
}, total=False)

class Data(ssc.DataDict):
    en_thermal_rates: float = INPUT(label='Optionally enable/disable thermal_rate', units='years', type='NUMBER', group='Thermal Rate', constraints='INTEGER,MIN=0,MAX=1')
    analysis_period: float = INPUT(label='Number of years in analysis', units='years', type='NUMBER', group='Lifetime', required='*', constraints='INTEGER,POSITIVE')
    system_use_lifetime_output: float = INPUT(label='Lifetime hourly system outputs', units='0/1', type='NUMBER', group='Lifetime', required='*', constraints='INTEGER,MIN=0,MAX=1', meta='0=hourly first year,1=hourly lifetime')
    gen_heat: Array = INPUT(label='Thermal power generated', units='kWt', type='ARRAY', group='Thermal Rate', required='*')
    thermal_load_heat_btu: Array = INOUT(label='Thermal load (year 1)', units='MMBtu/hr', type='ARRAY', group='Thermal Rate')
    inflation_rate: float = INPUT(label='Inflation rate', units='%', type='NUMBER', group='Lifetime', required='*', constraints='MIN=-99')
    thermal_degradation: Array = INPUT(label='Annual energy degradation', units='%', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_load_escalation: Array = INPUT(label='Annual load escalation', units='%/year', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_rate_escalation: Array = INPUT(label='Annual thermal rate escalation', units='%/year', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_conversion_efficiency: float = INPUT(label='Heat conversion efficiency (buy)', units='%', type='NUMBER', group='Thermal Rate', required='?=100')
    thermal_buy_rate_option: float = INPUT(label='Thermal buy rate option', units='0-2', type='NUMBER', group='Thermal Rate', required='?=0', constraints='INTEGER,MIN=0,MAX=2', meta='0=flat,1=timestep,2=monthly')
    thermal_buy_rate_flat_heat_btu: float = INPUT(label='Thermal buy rate flat', units='$/MMBtu', type='NUMBER', group='Thermal Rate', required='?=0')
    thermal_timestep_buy_rate_heat_btu: Array = INPUT(label='Thermal buy rate', units='$/MMBtu', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_monthly_buy_rate_heat_btu: Array = INPUT(label='Monthly thermal buy rate', units='$/MMBtu', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_sell_rate_option: float = INPUT(label='Thermal sell rate option', units='0-2', type='NUMBER', group='Thermal Rate', required='?=0', constraints='INTEGER,MIN=0,MAX=2', meta='0=flat,1=timestep,2=monthly')
    thermal_sell_rate_flat_heat_btu: float = INPUT(label='Thermal sell rate flat', units='$/MMBtu', type='NUMBER', group='Thermal Rate', required='?=0')
    thermal_timestep_sell_rate_heat_btu: Array = INPUT(label='Thermal sell rate timestep', units='$/MMBtu', type='ARRAY', group='Thermal Rate', required='?=0')
    thermal_monthly_sell_rate_heat_btu: Array = INPUT(label='Thermal sell rate monthly', units='$/MMBtu', type='ARRAY', group='Thermal Rate', required='?=0')
    annual_thermal_value: Final[Array] = OUTPUT(label='Thermal value', units='$', type='ARRAY', group='Annual', required='*')
    thermal_revenue_with_system: Final[Array] = OUTPUT(label='Thermal revenue with system', units='$', type='ARRAY', group='Time Series', required='*')
    thermal_revenue_without_system: Final[Array] = OUTPUT(label='Thermal revenue without system', units='$', type='ARRAY', group='Time Series', required='*')
    thermal_cost_with_system: Final[Array] = OUTPUT(label='Thermal cost with system', units='$', type='ARRAY', group='Time Series', required='*')
    thermal_cost_without_system: Final[Array] = OUTPUT(label='Thermal cost without system', units='$', type='ARRAY', group='Time Series', required='*')
    thermal_load_year1: Final[float] = OUTPUT(label='Thermal load total', units='MMBtu/hr', type='NUMBER', required='*')
    thermal_savings_year1: Final[float] = OUTPUT(label='Thermal savings (year 1)', units='$', type='NUMBER', required='*')
    thermal_cost_with_system_year1: Final[float] = OUTPUT(label='Thermal cost with sytem (year 1)', units='$', type='NUMBER', required='*')
    thermal_cost_without_system_year1: Final[float] = OUTPUT(label='Thermal cost without system (year 1)', units='$', type='NUMBER', required='*')
    year1_monthly_load_heat: Final[Array] = OUTPUT(label='Thermal load', units='kWht/mo', type='ARRAY', group='Monthly', required='*', constraints='LENGTH=12')

    def __init__(self, *args: Mapping[str, Any],
                 en_thermal_rates: float = ...,
                 analysis_period: float = ...,
                 system_use_lifetime_output: float = ...,
                 gen_heat: Array = ...,
                 thermal_load_heat_btu: Array = ...,
                 inflation_rate: float = ...,
                 thermal_degradation: Array = ...,
                 thermal_load_escalation: Array = ...,
                 thermal_rate_escalation: Array = ...,
                 thermal_conversion_efficiency: float = ...,
                 thermal_buy_rate_option: float = ...,
                 thermal_buy_rate_flat_heat_btu: float = ...,
                 thermal_timestep_buy_rate_heat_btu: Array = ...,
                 thermal_monthly_buy_rate_heat_btu: Array = ...,
                 thermal_sell_rate_option: float = ...,
                 thermal_sell_rate_flat_heat_btu: float = ...,
                 thermal_timestep_sell_rate_heat_btu: Array = ...,
                 thermal_monthly_sell_rate_heat_btu: Array = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
