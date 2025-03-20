
# This is a generated file

"""lcoefcr_design - Calculate levelized cost of energy using fixed charge rate method."""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'sim_type': float,
    'ui_fcr_input_option': float,
    'ui_fixed_charge_rate': float,
    'c_inflation': float,
    'c_equity_return': float,
    'c_debt_percent': float,
    'c_nominal_interest_rate': float,
    'c_tax_rate': float,
    'c_lifetime': float,
    'c_depreciation_schedule': Array,
    'c_construction_interest': float,
    'c_construction_cost': Array,
    'total_installed_cost': float,
    'annual_electricity_consumption': float,
    'electricity_rate': float,
    'fixed_operating_cost': float,
    'variable_operating_cost': float,
    'annual_energy': float,
    'crf': float,
    'pfin': float,
    'cfin': float,
    'wacc': float,
    'fixed_charge_rate_calc': float,
    'lcoe_fcr': float
}, total=False)

class Data(ssc.DataDict):
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='System Control', required='?=1')
    ui_fcr_input_option: float = INPUT(label='0: fixed charge rate; 1: calculate', type='NUMBER', group='Simple LCOE', required='*')
    ui_fixed_charge_rate: float = INPUT(label='Input fixed charge rate', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=0')
    c_inflation: float = INPUT(label='Input fixed charge rate', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_equity_return: float = INPUT(label='IRR (nominal)', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_debt_percent: float = INPUT(label='Project term debt (% of capital)', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_nominal_interest_rate: float = INPUT(label='Nominal debt interest rate', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_tax_rate: float = INPUT(label='Effective tax rate', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_lifetime: float = INPUT(label='Analysis period', units='years', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_depreciation_schedule: Array = INPUT(label='Depreciation schedule', units='%', type='ARRAY', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_construction_interest: float = INPUT(label='Nominal construction interest rate', units='%', type='NUMBER', group='Simple LCOE', required='ui_fcr_input_option=1')
    c_construction_cost: Array = INPUT(label='Construction cost schedule', units='%', type='ARRAY', group='Simple LCOE', required='ui_fcr_input_option=1')
    total_installed_cost: float = INPUT(label='Total installed cost', units='$', type='NUMBER', group='System Costs', required='sim_type=1')
    annual_electricity_consumption: float = INPUT(label='Annual electricity consumption with avail derate', units='kWe-hr', type='NUMBER', group='IPH LCOH', required='sim_type=1')
    electricity_rate: float = INPUT(label='Cost of electricity used to operate pumps and trackers', units='$/kWe-hr', type='NUMBER', group='IPH LCOH', required='sim_type=1')
    fixed_operating_cost: float = INPUT(label='Annual fixed operating cost', units='$', type='NUMBER', group='Simple LCOE', required='sim_type=1')
    variable_operating_cost: float = INPUT(label='Annual variable operating cost', units='$/kWh', type='NUMBER', group='Simple LCOE', required='sim_type=1')
    annual_energy: float = INPUT(label='Annual energy production', units='kWh', type='NUMBER', group='Simple LCOE', required='sim_type=1')
    crf: Final[float] = OUTPUT(label='Capital recovery factor', type='NUMBER', group='Simple LCOE', required='*')
    pfin: Final[float] = OUTPUT(label='Project financing factor', type='NUMBER', group='Simple LCOE', required='*')
    cfin: Final[float] = OUTPUT(label='Construction financing factor', type='NUMBER', group='Simple LCOE', required='*')
    wacc: Final[float] = OUTPUT(label='WACC', type='NUMBER', group='Simple LCOE', required='*')
    fixed_charge_rate_calc: Final[float] = OUTPUT(label='Calculated fixed charge rate', type='NUMBER', group='Simple LCOE', required='*')
    lcoe_fcr: Final[float] = OUTPUT(label='LCOE Levelized cost of energy', units='$/kWh', type='NUMBER', group='Simple LCOE', required='sim_type=1')

    def __init__(self, *args: Mapping[str, Any],
                 sim_type: float = ...,
                 ui_fcr_input_option: float = ...,
                 ui_fixed_charge_rate: float = ...,
                 c_inflation: float = ...,
                 c_equity_return: float = ...,
                 c_debt_percent: float = ...,
                 c_nominal_interest_rate: float = ...,
                 c_tax_rate: float = ...,
                 c_lifetime: float = ...,
                 c_depreciation_schedule: Array = ...,
                 c_construction_interest: float = ...,
                 c_construction_cost: Array = ...,
                 total_installed_cost: float = ...,
                 annual_electricity_consumption: float = ...,
                 electricity_rate: float = ...,
                 fixed_operating_cost: float = ...,
                 variable_operating_cost: float = ...,
                 annual_energy: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
