
# This is a generated file

"""geothermal_costs - Geothermal monthly and hourly models using general power block code from TRNSYS Type 224 code by M.Wagner, and some GETEM model code."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'conversion_type': float,
    'ppi_base_year': float,
    'gross_output': float,
    'gross_cost_output': float,
    'design_temp': float,
    'dt_prod_well': float,
    'eff_secondlaw': float,
    'qRejectTotal': float,
    'qCondenser': float,
    'v_stage_1': float,
    'v_stage_2': float,
    'v_stage_3': float,
    'GF_flowrate': float,
    'qRejectByStage_1': float,
    'qRejectByStage_2': float,
    'qRejectByStage_3': float,
    'ncg_condensate_pump': float,
    'cw_pump_work': float,
    'pressure_ratio_1': float,
    'pressure_ratio_2': float,
    'pressure_ratio_3': float,
    'condensate_pump_power': float,
    'cwflow': float,
    'cw_pump_head': float,
    'spec_vol': float,
    'spec_vol_lp': float,
    'x_hp': float,
    'x_lp': float,
    'hp_flash_pressure': float,
    'lp_flash_pressure': float,
    'flash_count': float,
    'calc_drill_costs': float,
    'geotherm.cost.inj_cost_curve_welltype': float,
    'geotherm.cost.prod_cost_curve_welltype': float,
    'geotherm.cost.inj_cost_curve_welldiam': float,
    'geotherm.cost.prod_cost_curve_welldiam': float,
    'geotherm.cost.inj_cost_curve': float,
    'geotherm.cost.prod_cost_curve': float,
    'resource_depth': float,
    'geotherm.cost.prod_wells_drilled': float,
    'geotherm.cost.inj_wells_drilled': float,
    'baseline_cost': float,
    'inj_total_cost': float,
    'prod_total_cost': float
}, total=False)

class Data(ssc.DataDict):
    conversion_type: float = INPUT(label='Conversion Type', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    ppi_base_year: float = INPUT(label='PPI Base Year', type='NUMBER', group='GeoHourly', required='?=19')
    gross_output: float = INPUT(label='Gross output from GETEM', units='kW', type='NUMBER', group='GeoHourly', required='*')
    gross_cost_output: float = INPUT(label='Gross output from GETEM for cost calculations', units='MW', type='NUMBER', group='GeoHourly', required='*')
    design_temp: float = INPUT(label='Power block design temperature', units='C', type='NUMBER', group='GeoHourly', required='*')
    dt_prod_well: float = INPUT(label='Temperature loss in production well', units='C', type='NUMBER', group='GeoHourly', required='*')
    eff_secondlaw: float = INPUT(label='Second Law Efficiency', units='%', type='NUMBER', group='GeoHourly', required='*')
    qRejectTotal: float = INPUT(label='Total Rejected Heat', units='btu/h', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    qCondenser: float = INPUT(label='Condenser Heat Rejected', units='btu/h', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    v_stage_1: float = INPUT(label='Vacumm Pump Stage 1', units='kW', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    v_stage_2: float = INPUT(label='Vacumm Pump Stage 2', units='kW', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    v_stage_3: float = INPUT(label='Vacumm Pump Stage 3', units='kW', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    GF_flowrate: float = INPUT(label='GF Flow Rate', units='lb/h', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    qRejectByStage_1: float = INPUT(label='Heat Rejected by NCG Condenser Stage 1', units='BTU/hr', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    qRejectByStage_2: float = INPUT(label='Heat Rejected by NCG Condenser Stage 2', units='BTU/hr', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    qRejectByStage_3: float = INPUT(label='Heat Rejected by NCG Condenser Stage 3', units='BTU/hr', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    ncg_condensate_pump: float = INPUT(label='Condensate Pump Work', units='kW', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    cw_pump_work: float = INPUT(label='CW Pump Work', units='kW', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    pressure_ratio_1: float = INPUT(label='Suction Steam Ratio 1', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    pressure_ratio_2: float = INPUT(label='Suction Steam Ratio 2', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    pressure_ratio_3: float = INPUT(label='Suction Steam Ratio 3', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    condensate_pump_power: float = INPUT(label='hp', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    cwflow: float = INPUT(label='Cooling Water Flow', units='lb/h', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    cw_pump_head: float = INPUT(label='Cooling Water Pump Head', units='lb/h', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    spec_vol: float = INPUT(label='Specific Volume', units='cft/lb', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    spec_vol_lp: float = INPUT(label='LP Specific Volume', units='cft/lb', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    x_hp: float = INPUT(label='HP Mass Fraction', units='%', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    x_lp: float = INPUT(label='LP Mass Fraction', units='%', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    hp_flash_pressure: float = INPUT(label='HP Flash Pressure', units='psia', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    lp_flash_pressure: float = INPUT(label='LP Flash Pressure', units='psia', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    flash_count: float = INPUT(label='Flash Count', units='(1 -2)', type='NUMBER', group='GeoHourly', required='conversion_type=1')
    calc_drill_costs: float = INPUT(label='Calculate drill costs', units='0/1', type='NUMBER', group='GeoHourly', required='?=0', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_inj_cost_curve_welltype: float = INPUT(name='geotherm.cost.inj_cost_curve_welltype', label='Injection well type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1')
    geotherm_cost_prod_cost_curve_welltype: float = INPUT(name='geotherm.cost.prod_cost_curve_welltype', label='Production well type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1')
    geotherm_cost_inj_cost_curve_welldiam: float = INPUT(name='geotherm.cost.inj_cost_curve_welldiam', label='Injection well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_prod_cost_curve_welldiam: float = INPUT(name='geotherm.cost.prod_cost_curve_welldiam', label='Production well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_inj_cost_curve: float = INPUT(name='geotherm.cost.inj_cost_curve', label='Injection well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_prod_cost_curve: float = INPUT(name='geotherm.cost.prod_cost_curve', label='Production well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    resource_depth: float = INPUT(label='Resource Depth', units='m', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1')
    geotherm_cost_prod_wells_drilled: float = INPUT(name='geotherm.cost.prod_wells_drilled', label='Number of drilled production wells', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_inj_wells_drilled: float = INPUT(name='geotherm.cost.inj_wells_drilled', label='Number of drilled injection wells', units='0/1', type='NUMBER', group='GeoHourly', required='calc_drill_costs=1', meta='0=LargerDiameter,1=SmallerDiameter')
    baseline_cost: Final[float] = OUTPUT(label='Baseline Cost', units='$/kW', type='NUMBER', group='GeoHourly', required='?')
    inj_total_cost: Final[float] = OUTPUT(label='Total Injection well cost', units='$/kW', type='NUMBER', group='GeoHourly', required='?')
    prod_total_cost: Final[float] = OUTPUT(label='Total Production well cost', units='$/kW', type='NUMBER', group='GeoHourly', required='?')

    def __init__(self, *args: Mapping[str, Any],
                 conversion_type: float = ...,
                 ppi_base_year: float = ...,
                 gross_output: float = ...,
                 gross_cost_output: float = ...,
                 design_temp: float = ...,
                 dt_prod_well: float = ...,
                 eff_secondlaw: float = ...,
                 qRejectTotal: float = ...,
                 qCondenser: float = ...,
                 v_stage_1: float = ...,
                 v_stage_2: float = ...,
                 v_stage_3: float = ...,
                 GF_flowrate: float = ...,
                 qRejectByStage_1: float = ...,
                 qRejectByStage_2: float = ...,
                 qRejectByStage_3: float = ...,
                 ncg_condensate_pump: float = ...,
                 cw_pump_work: float = ...,
                 pressure_ratio_1: float = ...,
                 pressure_ratio_2: float = ...,
                 pressure_ratio_3: float = ...,
                 condensate_pump_power: float = ...,
                 cwflow: float = ...,
                 cw_pump_head: float = ...,
                 spec_vol: float = ...,
                 spec_vol_lp: float = ...,
                 x_hp: float = ...,
                 x_lp: float = ...,
                 hp_flash_pressure: float = ...,
                 lp_flash_pressure: float = ...,
                 flash_count: float = ...,
                 calc_drill_costs: float = ...,
                 geotherm_cost_inj_cost_curve_welltype: float = ...,
                 geotherm_cost_prod_cost_curve_welltype: float = ...,
                 geotherm_cost_inj_cost_curve_welldiam: float = ...,
                 geotherm_cost_prod_cost_curve_welldiam: float = ...,
                 geotherm_cost_inj_cost_curve: float = ...,
                 geotherm_cost_prod_cost_curve: float = ...,
                 resource_depth: float = ...,
                 geotherm_cost_prod_wells_drilled: float = ...,
                 geotherm_cost_inj_wells_drilled: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
