
# This is a generated file

"""mhk_tidal - MHK Tidal power calculation model using power distribution."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'tidal_resource': Matrix,
    'tidal_power_curve': Matrix,
    'number_devices': float,
    'fixed_charge_rate': float,
    'device_costs_total': float,
    'balance_of_system_cost_total': float,
    'financial_cost_total': float,
    'total_operating_cost': float,
    'system_capacity': float,
    'tidal_resource_model_choice': float,
    'tidal_velocity': Array,
    'loss_array_spacing': float,
    'loss_resource_overprediction': float,
    'loss_transmission': float,
    'loss_downtime': float,
    'loss_additional': float,
    'device_rated_capacity': float,
    'device_average_power': float,
    'annual_energy': float,
    'gen': Array,
    'capacity_factor': float,
    'annual_energy_distribution': Array,
    'annual_cumulative_energy_distribution': Array,
    'tidal_resource_start_velocity': float,
    'tidal_resource_end_velocity': float,
    'tidal_power_start_velocity': float,
    'tidal_power_end_velocity': float,
    'total_capital_cost_kwh': float,
    'total_device_cost_kwh': float,
    'total_bos_cost_kwh': float,
    'total_financial_cost_kwh': float,
    'total_om_cost_kwh': float,
    'total_capital_cost_lcoe': float,
    'total_device_cost_lcoe': float,
    'total_bos_cost_lcoe': float,
    'total_financial_cost_lcoe': float,
    'total_om_cost_lcoe': float,
    'total_capital_cost_per_kw': float,
    'total_device_cost_per_kw': float,
    'total_bos_cost_per_kw': float,
    'total_financial_cost_per_kw': float,
    'total_operations_cost_per_kw': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix
}, total=False)

class Data(ssc.DataDict):
    tidal_resource: Matrix = INPUT(label='Frequency distribution of resource as a function of stream speeds', type='MATRIX', group='MHKTidal', required='*')
    tidal_power_curve: Matrix = INPUT(label='Power curve of tidal energy device as function of stream speeds', units='kW', type='MATRIX', group='MHKTidal', required='*')
    number_devices: float = INPUT(label='Number of tidal devices in the system', type='NUMBER', group='MHKTidal', required='?=1', constraints='INTEGER')
    fixed_charge_rate: float = INPUT(label='FCR from LCOE Cost page', type='NUMBER', group='MHKTidal', required='?=1')
    device_costs_total: float = INPUT(label='Device costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    balance_of_system_cost_total: float = INPUT(label='BOS costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    financial_cost_total: float = INPUT(label='Financial costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    total_operating_cost: float = INPUT(label='O&M costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    system_capacity: float = INPUT(label='System Nameplate Capacity', units='kW', type='NUMBER', group='MHKTidal', required='?=0')
    tidal_resource_model_choice: float = INPUT(label='Resource distribution or time series tidal resource data', units='0/1', type='NUMBER', group='MHKTidal', required='?=0', constraints='INTEGER')
    tidal_velocity: Array = INPUT(label='Tidal velocity', units='m/s', type='ARRAY', group='MHKTidal', required='?')
    loss_array_spacing: float = INPUT(label='Array spacing loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_resource_overprediction: float = INPUT(label='Resource overprediction loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_transmission: float = INPUT(label='Transmission losses', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_downtime: float = INPUT(label='Array/WEC downtime loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_additional: float = INPUT(label='Additional losses', units='%', type='NUMBER', group='MHKTidal', required='*')
    device_rated_capacity: Final[float] = OUTPUT(label='Rated capacity of device', units='kW', type='NUMBER', group='MHKTidal')
    device_average_power: Final[float] = OUTPUT(label='Average power production of a single device', units='kW', type='NUMBER', group='MHKTidal', required='*')
    annual_energy: Final[float] = OUTPUT(label='Annual AC energy in Year 1', units='kWh', type='NUMBER', group='MHKTidal', required='*')
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='MHKTidal')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='MHKTidal', required='*')
    annual_energy_distribution: Final[Array] = OUTPUT(label='Annual energy production of array as function of speed', units='kWh', type='ARRAY', group='MHKTidal')
    annual_cumulative_energy_distribution: Final[Array] = OUTPUT(label='Cumulative annual energy production of array as function of speed', units='kWh', type='ARRAY', group='MHKTidal')
    tidal_resource_start_velocity: Final[float] = OUTPUT(label='First tidal velocity where probability distribution is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_resource_end_velocity: Final[float] = OUTPUT(label='Last tidal velocity where probability distribution is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_power_start_velocity: Final[float] = OUTPUT(label='First tidal velocity where power curve is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_power_end_velocity: Final[float] = OUTPUT(label='Last tidal velocity where power curve is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_kwh: Final[float] = OUTPUT(label='Capital costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_device_cost_kwh: Final[float] = OUTPUT(label='Device costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_bos_cost_kwh: Final[float] = OUTPUT(label='Balance of system costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_financial_cost_kwh: Final[float] = OUTPUT(label='Financial costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_om_cost_kwh: Final[float] = OUTPUT(label='O&M costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_lcoe: Final[float] = OUTPUT(label='Capital cost as percentage of overall LCOE', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_device_cost_lcoe: Final[float] = OUTPUT(label='Device cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_bos_cost_lcoe: Final[float] = OUTPUT(label='BOS cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_financial_cost_lcoe: Final[float] = OUTPUT(label='Financial cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_om_cost_lcoe: Final[float] = OUTPUT(label='O&M cost (annual)', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_per_kw: Final[float] = OUTPUT(label='Capital cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_device_cost_per_kw: Final[float] = OUTPUT(label='Device cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_bos_cost_per_kw: Final[float] = OUTPUT(label='Balance of Systems cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_financial_cost_per_kw: Final[float] = OUTPUT(label='Financial cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_operations_cost_per_kw: Final[float] = OUTPUT(label='O&M cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")

    def __init__(self, *args: Mapping[str, Any],
                 tidal_resource: Matrix = ...,
                 tidal_power_curve: Matrix = ...,
                 number_devices: float = ...,
                 fixed_charge_rate: float = ...,
                 device_costs_total: float = ...,
                 balance_of_system_cost_total: float = ...,
                 financial_cost_total: float = ...,
                 total_operating_cost: float = ...,
                 system_capacity: float = ...,
                 tidal_resource_model_choice: float = ...,
                 tidal_velocity: Array = ...,
                 loss_array_spacing: float = ...,
                 loss_resource_overprediction: float = ...,
                 loss_transmission: float = ...,
                 loss_downtime: float = ...,
                 loss_additional: float = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
