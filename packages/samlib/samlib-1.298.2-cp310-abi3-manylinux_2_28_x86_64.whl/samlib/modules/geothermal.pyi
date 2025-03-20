
# This is a generated file

"""geothermal - Geothermal monthly and hourly models using general power block code from TRNSYS Type 224 code by M.Wagner, and some GETEM model code."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'ui_calculations_only': float,
    'system_use_lifetime_output': float,
    'geotherm.cost.inj_prod_well_ratio': float,
    'drilling_success_rate': float,
    'stim_success_rate': float,
    'failed_prod_flow_ratio': float,
    'file_name': str,
    'resource_potential': float,
    'resource_type': float,
    'resource_temp': float,
    'resource_depth': float,
    'geothermal_analysis_period': float,
    'model_choice': float,
    'reservoir_model_inputs': Matrix,
    'specified_pump_work_amount': float,
    'nameplate': float,
    'analysis_type': float,
    'num_wells': float,
    'num_wells_getem': float,
    'conversion_type': float,
    'plant_efficiency_input': float,
    'conversion_subtype': float,
    'decline_type': float,
    'temp_decline_rate': float,
    'temp_decline_max': float,
    'dt_prod_well': float,
    'prod_well_choice': float,
    'wet_bulb_temp': float,
    'use_weather_file_conditions': float,
    'ambient_pressure': float,
    'well_flow_rate': float,
    'pump_efficiency': float,
    'delta_pressure_equip': float,
    'excess_pressure_pump': float,
    'geotherm.cost.inj_cost_curve_welltype': float,
    'geotherm.cost.prod_cost_curve_welltype': float,
    'geotherm.cost.inj_cost_curve_welldiam': float,
    'geotherm.cost.prod_cost_curve_welldiam': float,
    'design_temp': float,
    'specify_pump_work': float,
    'rock_thermal_conductivity': float,
    'rock_specific_heat': float,
    'rock_density': float,
    'reservoir_pressure_change_type': float,
    'reservoir_pressure_change': float,
    'injectivity_index': float,
    'exploration_wells_production': float,
    'reservoir_width': float,
    'reservoir_height': float,
    'reservoir_permeability': float,
    'inj_prod_well_distance': float,
    'subsurface_water_loss': float,
    'fracture_aperature': float,
    'fracture_length': float,
    'fracture_spacing': float,
    'fracture_width': float,
    'num_fractures': float,
    'fracture_angle': float,
    'T_htf_cold_ref': float,
    'T_htf_hot_ref': float,
    'HTF': float,
    'P_boil': float,
    'eta_ref': float,
    'q_sby_frac': float,
    'startup_frac': float,
    'startup_time': float,
    'pb_bd_frac': float,
    'T_amb_des': float,
    'CT': float,
    'dT_cw_ref': float,
    'T_approach': float,
    'T_ITD_des': float,
    'P_cond_ratio': float,
    'P_cond_min': float,
    'hr_pl_nlev': float,
    'hc_ctl1': float,
    'hc_ctl2': float,
    'hc_ctl3': float,
    'hc_ctl4': float,
    'hc_ctl5': float,
    'hc_ctl6': float,
    'hc_ctl7': float,
    'hc_ctl8': float,
    'hc_ctl9': float,
    'hybrid_dispatch_schedule': str,
    'allow_reservoir_replacements': float,
    'num_wells_getem_output': float,
    'num_wells_getem_inj': float,
    'plant_brine_eff': float,
    'pump_watthr_per_lb': float,
    'pumpwork_prod': float,
    'pumpwork_inj': float,
    'inj_pump_hp': float,
    'gross_output': float,
    'gross_cost_output': float,
    'pump_depth_ft': float,
    'pump_hp': float,
    'reservoir_pressure': float,
    'reservoir_avg_temp': float,
    'bottom_hole_pressure': float,
    'pump_work': float,
    'gen': Array,
    'annual_energy_distribution_time': Matrix,
    'system_lifetime_recapitalize': Array,
    'monthly_resource_temperature': Array,
    'monthly_power': Array,
    'monthly_energy': Array,
    'monthly_energy_lifetime': Array,
    'timestep_resource_temperature': Array,
    'timestep_test_values': Array,
    'timestep_pressure': Array,
    'timestep_dry_bulb': Array,
    'timestep_wet_bulb': Array,
    'lifetime_output': float,
    'first_year_output': float,
    'annual_energy': float,
    'capacity_factor': float,
    'kwh_per_kw': float,
    'eff_secondlaw': float,
    'qRejectTotal': float,
    'qCondenser': float,
    'hp_flash_pressure': float,
    'lp_flash_pressure': float,
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
    'flash_count': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix
}, total=False)

class Data(ssc.DataDict):
    ui_calculations_only: float = INPUT(label='If = 1, only run UI calculations', type='NUMBER', group='GeoHourly', required='*')
    system_use_lifetime_output: float = INPUT(label='Geothermal lifetime simulation', units='0/1', type='NUMBER', group='GeoHourly', required='?=0', constraints='BOOLEAN', meta='0=SingleYearRepeated,1=RunEveryYear')
    geotherm_cost_inj_prod_well_ratio: float = INPUT(name='geotherm.cost.inj_prod_well_ratio', label='Ratio of injection wells to production wells', type='NUMBER', group='GeoHourly')
    drilling_success_rate: float = INPUT(label='Drilling success rate', units='%', type='NUMBER', group='GeoHourly')
    stim_success_rate: float = INPUT(label='Stimulation success rate', units='%', type='NUMBER', group='GeoHourly')
    failed_prod_flow_ratio: float = INPUT(label='Failed production well flow ratio', type='NUMBER', group='GeoHourly')
    file_name: str = INPUT(label='local weather file path', type='STRING', group='GeoHourly', required='ui_calculations_only=0', constraints='LOCAL_FILE')
    resource_potential: float = INPUT(label='Resource Potential', units='MW', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    resource_type: float = INPUT(label='Type of Resource', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    resource_temp: float = INPUT(label='Resource Temperature', units='C', type='NUMBER', group='GeoHourly', required='*', constraints='MAX=373')
    resource_depth: float = INPUT(label='Resource Depth', units='m', type='NUMBER', group='GeoHourly', required='*')
    geothermal_analysis_period: float = INPUT(label='Analysis Lifetime', units='years', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    model_choice: float = INPUT(label='Which model to run (0,1,2)', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    reservoir_model_inputs: Matrix = INPUT(label='Reservoir temperatures over time', type='MATRIX', group='GeoHourly', required='reservoir_pressure_change_type=3')
    specified_pump_work_amount: float = INPUT(label='Pump work specified by user', units='MW', type='NUMBER', group='GeoHourly', required='*')
    nameplate: float = INPUT(label='Desired plant output', units='kW', type='NUMBER', group='GeoHourly', required='*')
    analysis_type: float = INPUT(label='Analysis Type', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    num_wells: float = INPUT(label='Number of Wells', type='NUMBER', group='GeoHourly', required='*')
    num_wells_getem: float = INPUT(label="Number of Wells GETEM calc'd", type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    conversion_type: float = INPUT(label='Conversion Type', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    plant_efficiency_input: float = INPUT(label='Plant efficiency', type='NUMBER', group='GeoHourly', required='*')
    conversion_subtype: float = INPUT(label='Conversion Subtype', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    decline_type: float = INPUT(label='Temp decline Type', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    temp_decline_rate: float = INPUT(label='Temperature decline rate', units='%/yr', type='NUMBER', group='GeoHourly', required='*')
    temp_decline_max: float = INPUT(label='Maximum temperature decline', units='C', type='NUMBER', group='GeoHourly', required='*')
    dt_prod_well: float = INPUT(label='Temperature loss in production well', units='C', type='NUMBER', group='GeoHourly', required='*')
    prod_well_choice: float = INPUT(label='Temperature loss in production well choice', units='0/1', type='NUMBER', group='GeoHourly', required='*')
    wet_bulb_temp: float = INPUT(label='Wet Bulb Temperature', units='C', type='NUMBER', group='GeoHourly', required='*')
    use_weather_file_conditions: float = INPUT(label='Use weather file ambient temperature', units='0/1', type='NUMBER', group='GeoHourly', required='?=0')
    ambient_pressure: float = INPUT(label='Ambient pressure', units='psi', type='NUMBER', group='GeoHourly', required='*')
    well_flow_rate: float = INPUT(label='Production flow rate per well', units='kg/s', type='NUMBER', group='GeoHourly', required='*')
    pump_efficiency: float = INPUT(label='Pump efficiency', units='%', type='NUMBER', group='GeoHourly', required='*')
    delta_pressure_equip: float = INPUT(label='Delta pressure across surface equipment', units='psi', type='NUMBER', group='GeoHourly', required='*')
    excess_pressure_pump: float = INPUT(label='Excess pressure @ pump suction', units='psi', type='NUMBER', group='GeoHourly', required='*')
    geotherm_cost_inj_cost_curve_welltype: float = INPUT(name='geotherm.cost.inj_cost_curve_welltype', label='Injection well type', units='0/1', type='NUMBER', group='GeoHourly', required='*')
    geotherm_cost_prod_cost_curve_welltype: float = INPUT(name='geotherm.cost.prod_cost_curve_welltype', label='Production well type', units='0/1', type='NUMBER', group='GeoHourly', required='*')
    geotherm_cost_inj_cost_curve_welldiam: float = INPUT(name='geotherm.cost.inj_cost_curve_welldiam', label='Injection well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='*', meta='0=LargerDiameter,1=SmallerDiameter')
    geotherm_cost_prod_cost_curve_welldiam: float = INPUT(name='geotherm.cost.prod_cost_curve_welldiam', label='Production well diameter type', units='0/1', type='NUMBER', group='GeoHourly', required='*', meta='0=LargerDiameter,1=SmallerDiameter')
    design_temp: float = INPUT(label='Power block design temperature', units='C', type='NUMBER', group='GeoHourly', required='*')
    specify_pump_work: float = INPUT(label='Did user specify pump work?', units='0 or 1', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    rock_thermal_conductivity: float = INPUT(label='Rock thermal conductivity', units='J/m-day-C', type='NUMBER', group='GeoHourly', required='*')
    rock_specific_heat: float = INPUT(label='Rock specific heat', units='J/kg-C', type='NUMBER', group='GeoHourly', required='*')
    rock_density: float = INPUT(label='Rock density', units='kg/m^3', type='NUMBER', group='GeoHourly', required='*')
    reservoir_pressure_change_type: float = INPUT(label='Reservoir pressure change type', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    reservoir_pressure_change: float = INPUT(label='Pressure change', units='psi-h/1000lb', type='NUMBER', group='GeoHourly', required='*')
    injectivity_index: float = INPUT(label='Injectivity index', units='lb/hr-psi', type='NUMBER', group='GeoHourly', required='*')
    exploration_wells_production: float = INPUT(label='Exploration wells used for production', type='NUMBER', group='GeoHourly', required='*')
    reservoir_width: float = INPUT(label='Reservoir width', units='m', type='NUMBER', group='GeoHourly', required='*')
    reservoir_height: float = INPUT(label='Reservoir height', units='m', type='NUMBER', group='GeoHourly', required='*')
    reservoir_permeability: float = INPUT(label='Reservoir Permeability', units='darcys', type='NUMBER', group='GeoHourly', required='*')
    inj_prod_well_distance: float = INPUT(label='Distance from injection to production wells', units='m', type='NUMBER', group='GeoHourly', required='*')
    subsurface_water_loss: float = INPUT(label='Subsurface water loss', units='%', type='NUMBER', group='GeoHourly', required='*')
    fracture_aperature: float = INPUT(label='Fracture aperature', units='m', type='NUMBER', group='GeoHourly', required='*')
    fracture_length: float = INPUT(label='Fracture length', units='m', type='NUMBER', group='GeoHourly', required='*')
    fracture_spacing: float = INPUT(label='Fracture spacing', units='m', type='NUMBER', group='GeoHourly', required='*')
    fracture_width: float = INPUT(label='Fracture width', units='m', type='NUMBER', group='GeoHourly', required='*')
    num_fractures: float = INPUT(label='Number of fractures', type='NUMBER', group='GeoHourly', required='*', constraints='INTEGER')
    fracture_angle: float = INPUT(label='Fracture angle', units='deg', type='NUMBER', group='GeoHourly', required='*')
    T_htf_cold_ref: float = INPUT(label='Outlet design temp', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    T_htf_hot_ref: float = INPUT(label='Inlet design temp', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    HTF: float = INPUT(label='Heat trans fluid type ID', units='(1-27)', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0', constraints='INTEGER')
    P_boil: float = INPUT(label='Design Boiler Pressure', units='bar', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    eta_ref: float = INPUT(label='Desgin conversion efficiency', units='%', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    q_sby_frac: float = INPUT(label='% thermal power for standby mode', units='%', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    startup_frac: float = INPUT(label='% thermal power for startup', units='%', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    startup_time: float = INPUT(label='Hours to start power block', units='hours', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    pb_bd_frac: float = INPUT(label='Blowdown steam fraction', units='%', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    T_amb_des: float = INPUT(label='Design ambient temperature', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    CT: float = INPUT(label='Condenser type (Wet, Dry,Hybrid)', units='(1-3)', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0', constraints='INTEGER')
    dT_cw_ref: float = INPUT(label='Design condenser cooling water inlet/outlet T diff', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    T_approach: float = INPUT(label='Approach Temperature', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    T_ITD_des: float = INPUT(label='Design ITD for dry system', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    P_cond_ratio: float = INPUT(label='Condenser pressure ratio', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    P_cond_min: float = INPUT(label='Minimum condenser pressure', units='in Hg', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hr_pl_nlev: float = INPUT(label='# part-load increments', units='(0-9)', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0', constraints='INTEGER')
    hc_ctl1: float = INPUT(label='HC Control 1', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl2: float = INPUT(label='HC Control 2', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl3: float = INPUT(label='HC Control 3', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl4: float = INPUT(label='HC Control 4', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl5: float = INPUT(label='HC Control 5', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl6: float = INPUT(label='HC Control 6', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl7: float = INPUT(label='HC Control 7', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl8: float = INPUT(label='HC Control 8', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hc_ctl9: float = INPUT(label='HC Control 9', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    hybrid_dispatch_schedule: str = INPUT(label='Daily dispatch schedule', type='STRING', group='GeoHourly', required='ui_calculations_only=0', constraints='TOUSCHED')
    allow_reservoir_replacements: float = INPUT(label='Allow reservoir replacements', type='NUMBER', group='GeoHourly', required='?=0')
    num_wells_getem_output: Final[float] = OUTPUT(label='Number of wells calculated by GETEM', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    num_wells_getem_inj: Final[float] = OUTPUT(label='Number of wells calculated by GETEM', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    plant_brine_eff: Final[float] = OUTPUT(label='Plant Brine Efficiency', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    pump_watthr_per_lb: Final[float] = OUTPUT(label='Pump work Efficiency', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    pumpwork_prod: Final[float] = OUTPUT(label='Production Pump work Efficiency', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    pumpwork_inj: Final[float] = OUTPUT(label='Injection Pump work Efficiency', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    inj_pump_hp: Final[float] = OUTPUT(label='Injection Pump horsepower', units='hp', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    gross_output: Final[float] = OUTPUT(label='Gross output from GETEM', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    gross_cost_output: Final[float] = OUTPUT(label='Gross output from GETEM for cost', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    pump_depth_ft: Final[float] = OUTPUT(label='Pump depth calculated by GETEM', units='ft', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    pump_hp: Final[float] = OUTPUT(label='Pump hp calculated by GETEM', units='hp', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    reservoir_pressure: Final[float] = OUTPUT(label='Reservoir pres calculated by GETEM', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    reservoir_avg_temp: Final[float] = OUTPUT(label='Avg reservoir temp calculated by GETEM', units='C', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    bottom_hole_pressure: Final[float] = OUTPUT(label='Bottom hole pres calculated by GETEM', type='NUMBER', group='GeoHourly', required='ui_calculations_only=1')
    pump_work: Final[float] = OUTPUT(label='Pump work calculated by GETEM', units='MW', type='NUMBER', group='GeoHourly', required='*')
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', meta='GeoHourly')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of Time', type='MATRIX', group='Heatmaps')
    system_lifetime_recapitalize: Final[Array] = OUTPUT(label='Resource replacement? (1=yes)', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    monthly_resource_temperature: Final[Array] = OUTPUT(label='Monthly avg resource temperature', units='C', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    monthly_power: Final[Array] = OUTPUT(label='Monthly power', units='kW', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly AC energy in Year 1', units='kWh/mo', type='ARRAY', group='GeoHourly', constraints='LENGTH=12')
    monthly_energy_lifetime: Final[Array] = OUTPUT(label='Monthly energy before performance adjustments', units='kWh', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    timestep_resource_temperature: Final[Array] = OUTPUT(label='Resource temperature', units='C', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    timestep_test_values: Final[Array] = OUTPUT(label='Test output values in each time step', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    timestep_pressure: Final[Array] = OUTPUT(label='Atmospheric pressure', units='atm', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    timestep_dry_bulb: Final[Array] = OUTPUT(label='Dry bulb temperature', units='C', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    timestep_wet_bulb: Final[Array] = OUTPUT(label='Wet bulb temperature', units='C', type='ARRAY', group='GeoHourly', required='ui_calculations_only=0')
    lifetime_output: Final[float] = OUTPUT(label='Lifetime output', units='kWh', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    first_year_output: Final[float] = OUTPUT(label='First year output', units='kWh', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    annual_energy: Final[float] = OUTPUT(label='Annual AC energy in Year 1', units='kWh', type='NUMBER', group='GeoHourly', required='ui_calculations_only=0')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', type='NUMBER', required='*')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', type='NUMBER', required='*')
    eff_secondlaw: Final[float] = OUTPUT(label='Second Law Efficiency', units='C', type='NUMBER', group='GeoHourly')
    qRejectTotal: Final[float] = OUTPUT(label='Total Heat Rejection', units='btu/h', type='NUMBER', group='GeoHourly')
    qCondenser: Final[float] = OUTPUT(label='Condenser Heat Rejected', units='btu/h', type='NUMBER', group='GeoHourly')
    hp_flash_pressure: Final[float] = OUTPUT(label='HP Flash Pressure', units='psia', type='NUMBER', group='GeoHourly')
    lp_flash_pressure: Final[float] = OUTPUT(label='LP Flash Pressure', units='psia', type='NUMBER', group='GeoHourly')
    v_stage_1: Final[float] = OUTPUT(label='Vacumm Pump Stage 1', units='kW', type='NUMBER', group='GeoHourly')
    v_stage_2: Final[float] = OUTPUT(label='Vacumm Pump Stage 2', units='kW', type='NUMBER', group='GeoHourly')
    v_stage_3: Final[float] = OUTPUT(label='Vacumm Pump Stage 3', units='kW', type='NUMBER', group='GeoHourly')
    GF_flowrate: Final[float] = OUTPUT(label='GF Flow Rate', units='lb/h', type='NUMBER', group='GeoHourly')
    qRejectByStage_1: Final[float] = OUTPUT(label='Heat Rejected by NCG Condenser Stage 1', units='BTU/h', type='NUMBER', group='GeoHourly')
    qRejectByStage_2: Final[float] = OUTPUT(label='Heat Rejected by NCG Condenser Stage 2', units='BTU/h', type='NUMBER', group='GeoHourly')
    qRejectByStage_3: Final[float] = OUTPUT(label='Heat Rejected by NCG Condenser Stage 3', units='BTU/h', type='NUMBER', group='GeoHourly')
    ncg_condensate_pump: Final[float] = OUTPUT(label='Condensate Pump Work', units='kW', type='NUMBER', group='GeoHourly')
    cw_pump_work: Final[float] = OUTPUT(label='CW Pump Work', units='kW', type='NUMBER', group='GeoHourly')
    pressure_ratio_1: Final[float] = OUTPUT(label='Suction Steam Ratio 1', type='NUMBER', group='GeoHourly')
    pressure_ratio_2: Final[float] = OUTPUT(label='Suction Steam Ratio 2', type='NUMBER', group='GeoHourly')
    pressure_ratio_3: Final[float] = OUTPUT(label='Suction Steam Ratio 3', type='NUMBER', group='GeoHourly')
    condensate_pump_power: Final[float] = OUTPUT(label='hp', type='NUMBER', group='GeoHourly')
    cwflow: Final[float] = OUTPUT(label='Cooling Water Flow', units='lb/h', type='NUMBER', group='GeoHourly')
    cw_pump_head: Final[float] = OUTPUT(label='Cooling Water Pump Head', units='lb/h', type='NUMBER', group='GeoHourly')
    spec_vol: Final[float] = OUTPUT(label='HP Specific Volume', units='cft/lb', type='NUMBER', group='GeoHourly')
    spec_vol_lp: Final[float] = OUTPUT(label='LP Specific Volume', units='cft/lb', type='NUMBER', group='GeoHourly')
    x_hp: Final[float] = OUTPUT(label='HP Mass Fraction', units='%', type='NUMBER', group='GeoHourly')
    x_lp: Final[float] = OUTPUT(label='LP Mass Fraction', units='%', type='NUMBER', group='GeoHourly')
    flash_count: Final[float] = OUTPUT(label='Flash Count', units='(1 -2)', type='NUMBER', group='GeoHourly')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")

    def __init__(self, *args: Mapping[str, Any],
                 ui_calculations_only: float = ...,
                 system_use_lifetime_output: float = ...,
                 geotherm_cost_inj_prod_well_ratio: float = ...,
                 drilling_success_rate: float = ...,
                 stim_success_rate: float = ...,
                 failed_prod_flow_ratio: float = ...,
                 file_name: str = ...,
                 resource_potential: float = ...,
                 resource_type: float = ...,
                 resource_temp: float = ...,
                 resource_depth: float = ...,
                 geothermal_analysis_period: float = ...,
                 model_choice: float = ...,
                 reservoir_model_inputs: Matrix = ...,
                 specified_pump_work_amount: float = ...,
                 nameplate: float = ...,
                 analysis_type: float = ...,
                 num_wells: float = ...,
                 num_wells_getem: float = ...,
                 conversion_type: float = ...,
                 plant_efficiency_input: float = ...,
                 conversion_subtype: float = ...,
                 decline_type: float = ...,
                 temp_decline_rate: float = ...,
                 temp_decline_max: float = ...,
                 dt_prod_well: float = ...,
                 prod_well_choice: float = ...,
                 wet_bulb_temp: float = ...,
                 use_weather_file_conditions: float = ...,
                 ambient_pressure: float = ...,
                 well_flow_rate: float = ...,
                 pump_efficiency: float = ...,
                 delta_pressure_equip: float = ...,
                 excess_pressure_pump: float = ...,
                 geotherm_cost_inj_cost_curve_welltype: float = ...,
                 geotherm_cost_prod_cost_curve_welltype: float = ...,
                 geotherm_cost_inj_cost_curve_welldiam: float = ...,
                 geotherm_cost_prod_cost_curve_welldiam: float = ...,
                 design_temp: float = ...,
                 specify_pump_work: float = ...,
                 rock_thermal_conductivity: float = ...,
                 rock_specific_heat: float = ...,
                 rock_density: float = ...,
                 reservoir_pressure_change_type: float = ...,
                 reservoir_pressure_change: float = ...,
                 injectivity_index: float = ...,
                 exploration_wells_production: float = ...,
                 reservoir_width: float = ...,
                 reservoir_height: float = ...,
                 reservoir_permeability: float = ...,
                 inj_prod_well_distance: float = ...,
                 subsurface_water_loss: float = ...,
                 fracture_aperature: float = ...,
                 fracture_length: float = ...,
                 fracture_spacing: float = ...,
                 fracture_width: float = ...,
                 num_fractures: float = ...,
                 fracture_angle: float = ...,
                 T_htf_cold_ref: float = ...,
                 T_htf_hot_ref: float = ...,
                 HTF: float = ...,
                 P_boil: float = ...,
                 eta_ref: float = ...,
                 q_sby_frac: float = ...,
                 startup_frac: float = ...,
                 startup_time: float = ...,
                 pb_bd_frac: float = ...,
                 T_amb_des: float = ...,
                 CT: float = ...,
                 dT_cw_ref: float = ...,
                 T_approach: float = ...,
                 T_ITD_des: float = ...,
                 P_cond_ratio: float = ...,
                 P_cond_min: float = ...,
                 hr_pl_nlev: float = ...,
                 hc_ctl1: float = ...,
                 hc_ctl2: float = ...,
                 hc_ctl3: float = ...,
                 hc_ctl4: float = ...,
                 hc_ctl5: float = ...,
                 hc_ctl6: float = ...,
                 hc_ctl7: float = ...,
                 hc_ctl8: float = ...,
                 hc_ctl9: float = ...,
                 hybrid_dispatch_schedule: str = ...,
                 allow_reservoir_replacements: float = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
