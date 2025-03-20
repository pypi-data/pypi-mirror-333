
# This is a generated file

"""csp_subcomponent - CSP subcomponents"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    't_step': float,
    'T_amb': Array,
    'mdot_src': Array,
    'mdot_sink': Array,
    'hot_tank_bypassed': Array,
    'T_src_out': Array,
    'T_sink_out': Array,
    'T_tank_hot_ini': float,
    'T_tank_cold_ini': float,
    'P_ref': float,
    'eta_ref': float,
    'solar_mult': float,
    'T_loop_in_des': float,
    'T_loop_out': float,
    'pb_pump_coef': float,
    'tes_type': float,
    'Fluid': float,
    'field_fl_props': Matrix,
    'tshours': float,
    'is_h_tank_fixed': float,
    'h_tank_in': float,
    'd_tank_in': float,
    'u_tank': float,
    'tank_pairs': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'cold_tank_Thtr': float,
    'cold_tank_max_heat': float,
    'h_tank_min': float,
    'init_hot_htf_percent': float,
    'tes_n_tsteps': float,
    'V_tes_des': float,
    'calc_design_pipe_vals': float,
    'tes_pump_coef': float,
    'eta_pump': float,
    'has_hot_tank_bypass': float,
    'T_tank_hot_inlet_min': float,
    'custom_tes_p_loss': float,
    'custom_tes_pipe_sizes': float,
    'k_tes_loss_coeffs': Matrix,
    'tes_diams': Matrix,
    'tes_wallthicks': Matrix,
    'tes_lengths': Matrix,
    'HDR_rough': float,
    'DP_SGS': float,
    'store_fluid': float,
    'store_fl_props': Matrix,
    'dt_hot': float,
    'tanks_in_parallel': float,
    'tes_pb_n_xsteps': float,
    'tes_pb_k_eff': float,
    'tes_pb_void_frac': float,
    'tes_pb_dens_solid': float,
    'tes_pb_cp_solid': float,
    'tes_pb_T_hot_delta': float,
    'tes_pb_T_cold_delta': float,
    'tes_pb_T_charge_min': float,
    'tes_pb_f_oversize': float,
    'tes_pb_T_grad_ini': Array,
    'tes_cyl_tank_thick': float,
    'tes_cyl_tank_cp': float,
    'tes_cyl_tank_dens': float,
    'tes_cyl_piston_loss_poly': Array,
    'tes_cyl_tank_insul_percent': float,
    'T_src_in': Array,
    'T_sink_in': Array,
    'T_tank_cold': Array,
    'T_tank_hot': Array,
    'tes_diameter': float,
    'tes_radius': float,
    'tes_height': float,
    'hot_tank_vol_frac': Array,
    'q_dot_dc_to_htf': Array,
    'q_dot_ch_from_htf': Array,
    'q_dc_to_htf': Array,
    'q_ch_from_htf': Array,
    'tes_error': Array,
    'tes_error_percent': Array,
    'piston_loc': Array,
    'piston_frac': Array,
    'tes_leak_error': Array,
    'tes_E_hot': Array,
    'tes_E_cold': Array,
    'tes_wall_error': Array,
    'tes_error_corrected': Array,
    'tes_exp_wall_mass': Array,
    'tes_exp_length': Array,
    'tes_mass_cold': Array,
    'tes_mass_hot': Array,
    'tes_V_cold': Array,
    'tes_V_hot': Array,
    'hot_tank_mass_perc': Array,
    'T_grad_final': Matrix
}, total=False)

class Data(ssc.DataDict):
    t_step: float = INPUT(label='Timestep duration', units='s', type='NUMBER', group='system', required='*')
    T_amb: Array = INPUT(label='Ambient temperature', units='C', type='ARRAY', group='weather', required='*')
    mdot_src: Array = INPUT(label='Mass flow from heat source', units='kg/s', type='ARRAY', group='TES', required='*')
    mdot_sink: Array = INPUT(label='Mass flow to heat sink or power block', units='kg/s', type='ARRAY', group='TES', required='*')
    hot_tank_bypassed: Array = INPUT(label='Is mass flow from source going straight to cold tank?', units='-', type='ARRAY', group='TES', required='*')
    T_src_out: Array = INPUT(label='Temperature from heat source', units='C', type='ARRAY', group='TES', required='*')
    T_sink_out: Array = INPUT(label='Temperature from heat sink or power block', units='C', type='ARRAY', group='TES', required='*')
    T_tank_hot_ini: float = INPUT(label='Temperature of fluid in hot tank at beginning of step', units='C', type='NUMBER', group='TES')
    T_tank_cold_ini: float = INPUT(label='Temperature of fluid in cold tank at beginning of step', units='C', type='NUMBER', group='TES')
    P_ref: float = INPUT(label='Rated plant capacity', units='MWe', type='NUMBER', group='powerblock', required='*')
    eta_ref: float = INPUT(label='Power cycle efficiency at design', units='none', type='NUMBER', group='powerblock', required='*')
    solar_mult: float = INPUT(label='Actual solar multiple of system', units='-', type='NUMBER', group='system', required='*')
    T_loop_in_des: float = INPUT(label='Design loop inlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    T_loop_out: float = INPUT(label='Target loop outlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='powerblock', required='*')
    tes_type: float = INPUT(label='Standard two tank (1), Packed Bed (2), Piston Cylinder (3)', units='-', type='NUMBER', group='TES', required='?=1')
    Fluid: float = INPUT(label='Field HTF fluid ID number', units='-', type='NUMBER', group='solar_field', required='*')
    field_fl_props: Matrix = INPUT(label='User defined field fluid property data', units='-', type='MATRIX', group='solar_field', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='TES', required='*')
    is_h_tank_fixed: float = INPUT(label='[1] Use fixed height (calculate diameter) [0] Use fixed diameter [2] Use fixed d and h (for packed bed)', units='-', type='NUMBER', group='TES', required='?=1')
    h_tank_in: float = INPUT(label='Total height of tank input (height of HTF when tank is full', units='m', type='NUMBER', group='TES', required='is_h_tank_fixed=1')
    d_tank_in: float = INPUT(label='Tank diameter input', units='m', type='NUMBER', group='TES', required='is_h_tank_fixed=0|is_h_tank_fixed=2')
    u_tank: float = INPUT(label='Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    tank_pairs: float = INPUT(label='Number of equivalent tank pairs', units='-', type='NUMBER', group='TES', required='*', constraints='INTEGER')
    hot_tank_Thtr: float = INPUT(label='Minimum allowable hot tank HTF temp', units='C', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    hot_tank_max_heat: float = INPUT(label='Rated heater capacity for hot tank heating', units='MWe', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    cold_tank_Thtr: float = INPUT(label='Minimum allowable cold tank HTF temp', units='C', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    cold_tank_max_heat: float = INPUT(label='Rated heater capacity for cold tank heating', units='MWe', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    h_tank_min: float = INPUT(label='Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='TES', required='tes_type=1|tes_type=3')
    init_hot_htf_percent: float = INPUT(label='Initial fraction of avail. vol that is hot', units='%', type='NUMBER', group='TES', required='*')
    tes_n_tsteps: float = INPUT(label='Number of subtimesteps (for NT and packed bed)', type='NUMBER', group='TES', required='tes_type>1')
    V_tes_des: float = INPUT(label='Design-point velocity to size the TES pipe diameters', units='m/s', type='NUMBER', group='controller', required='*')
    calc_design_pipe_vals: float = INPUT(label='Calculate temps and pressures at design conditions for runners and headers', units='none', type='NUMBER', group='solar_field', required='*')
    tes_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through tes loop', units='kW/(kg/s)', type='NUMBER', group='controller', required='*')
    eta_pump: float = INPUT(label='HTF pump efficiency', units='none', type='NUMBER', group='solar_field', required='*')
    has_hot_tank_bypass: float = INPUT(label='Bypass valve connects field outlet to cold tank', units='-', type='NUMBER', group='controller', required='*')
    T_tank_hot_inlet_min: float = INPUT(label='Minimum hot tank htf inlet temperature', units='C', type='NUMBER', group='controller', required='*')
    custom_tes_p_loss: float = INPUT(label='TES pipe losses are based on custom lengths and coeffs', units='-', type='NUMBER', group='controller', required='*')
    custom_tes_pipe_sizes: float = INPUT(label='Use custom TES pipe diams, wallthks, and lengths', units='-', type='NUMBER', group='controller', required='*')
    k_tes_loss_coeffs: Matrix = INPUT(label='Minor loss coeffs for the coll, gen, and bypass loops', units='-', type='MATRIX', group='controller', required='*')
    tes_diams: Matrix = INPUT(label='Custom TES diameters', units='m', type='MATRIX', group='controller', required='*')
    tes_wallthicks: Matrix = INPUT(label='Custom TES wall thicknesses', units='m', type='MATRIX', group='controller', required='*')
    tes_lengths: Matrix = INPUT(label='Custom TES lengths', units='m', type='MATRIX', group='controller')
    HDR_rough: float = INPUT(label='Header pipe roughness', units='m', type='NUMBER', group='solar_field', required='*')
    DP_SGS: float = INPUT(label='Pressure drop within the steam generator', units='bar', type='NUMBER', group='controller', required='*')
    store_fluid: float = INPUT(label='Material number for storage fluid', units='-', type='NUMBER', group='TES', required='tes_type=1')
    store_fl_props: Matrix = INPUT(label='User defined storage fluid property data', units='-', type='MATRIX', group='TES', required='tes_type=1')
    dt_hot: float = INPUT(label='Hot side HX approach temp', units='C', type='NUMBER', group='TES', required='tes_type=1')
    tanks_in_parallel: float = INPUT(label='Tanks are in parallel, not in series, with solar field', units='-', type='NUMBER', group='controller', required='tes_type=1')
    tes_pb_n_xsteps: float = INPUT(label='Number of spatial segments', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_k_eff: float = INPUT(label='TES packed bed effective conductivity', units='W/m K', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_void_frac: float = INPUT(label='TES packed bed void fraction', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_dens_solid: float = INPUT(label='TES packed bed media density', units='kg/m3', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_cp_solid: float = INPUT(label='TES particle specific heat', units='kJ/kg K', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_hot_delta: float = INPUT(label='Max allowable decrease in hot discharge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_cold_delta: float = INPUT(label='Max allowable increase in cold discharge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_charge_min: float = INPUT(label='Min charge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_f_oversize: float = INPUT(label='Packed bed oversize factor', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_grad_ini: Array = INPUT(label='TES Temperature gradient at beginning of timestep', units='C', type='ARRAY', group='TES', required='?=[-274]')
    tes_cyl_tank_thick: float = INPUT(label='Tank wall thickness (used for Piston Cylinder)', units='m', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_tank_cp: float = INPUT(label='Tank wall cp (used for Piston Cylinder)', units='kJ/kg-K', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_tank_dens: float = INPUT(label='Tank wall thickness (used for Piston Cylinder)', units='kg/m3', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_piston_loss_poly: Array = INPUT(label='Polynomial coefficients describing piston heat loss function (f(kg/s)=%)', type='ARRAY', group='TES', required='tes_type=3')
    tes_cyl_tank_insul_percent: float = INPUT(label='Percent additional wall mass due to insulation (used for Piston Cylinder)', units='%', type='NUMBER', group='TES', required='?=0')
    T_src_in: Final[Array] = OUTPUT(label='Temperature to heat source', units='C', type='ARRAY', group='TES', required='*')
    T_sink_in: Final[Array] = OUTPUT(label='Temperature to heat sink or power block', units='C', type='ARRAY', group='TES', required='*')
    T_tank_cold: Final[Array] = OUTPUT(label='Temperature of cold tank (end of timestep)', units='C', type='ARRAY', group='TES', required='*')
    T_tank_hot: Final[Array] = OUTPUT(label='Temperature of hot tank (end of timestep)', units='C', type='ARRAY', group='TES', required='*')
    tes_diameter: Final[float] = OUTPUT(label='TES Diameter', units='m', type='NUMBER', group='TES', required='*')
    tes_radius: Final[float] = OUTPUT(label='TES Radius', units='m', type='NUMBER', group='TES', required='*')
    tes_height: Final[float] = OUTPUT(label='TES Height', units='m', type='NUMBER', group='TES', required='*')
    hot_tank_vol_frac: Final[Array] = OUTPUT(label='Hot tank volume fraction of total', type='ARRAY', group='TES', required='*')
    q_dot_dc_to_htf: Final[Array] = OUTPUT(label='Thermal power to HTF from storage', units='MWt', type='ARRAY', group='TES', required='*')
    q_dot_ch_from_htf: Final[Array] = OUTPUT(label='Thermal power from the HTF to storage', units='MWt', type='ARRAY', group='TES', required='*')
    q_dc_to_htf: Final[Array] = OUTPUT(label='Thermal energy to HTF from storage', units='MJt', type='ARRAY', group='TES', required='*')
    q_ch_from_htf: Final[Array] = OUTPUT(label='Thermal energy from the HTF to storage', units='MJt', type='ARRAY', group='TES', required='*')
    tes_error: Final[Array] = OUTPUT(label='TES energy balance error', units='MW', type='ARRAY', group='TES', required='tes_type=3')
    tes_error_percent: Final[Array] = OUTPUT(label='TES energy balance error percent', units='%', type='ARRAY', group='TES', required='tes_type=3')
    piston_loc: Final[Array] = OUTPUT(label='Piston Location (distance from left cold side)', units='m', type='ARRAY', group='TES', required='tes_type=3')
    piston_frac: Final[Array] = OUTPUT(label='Piston Fraction (distance from left cold side)', type='ARRAY', group='TES', required='tes_type=3')
    tes_leak_error: Final[Array] = OUTPUT(label='TES energy balance error due to leakage assumption', units='MWt', type='ARRAY', group='TES', required='tes_type=3')
    tes_E_hot: Final[Array] = OUTPUT(label='TES hot side internal energy', units='MJ', type='ARRAY', group='TES', required='tes_type=3')
    tes_E_cold: Final[Array] = OUTPUT(label='TES cold side internal energy', units='MJ', type='ARRAY', group='TES', required='tes_type=3')
    tes_wall_error: Final[Array] = OUTPUT(label='TES energy balance error due to wall temperature assumption', units='MWt', type='ARRAY', group='TES', required='tes_type=3')
    tes_error_corrected: Final[Array] = OUTPUT(label='TES energy balance error, accounting for wall and temperature assumption error', units='MWt', type='ARRAY', group='TES', required='tes_type=3')
    tes_exp_wall_mass: Final[Array] = OUTPUT(label='TES expansion tank effective wall mass', units='kg', type='ARRAY', group='TES', required='tes_type=3')
    tes_exp_length: Final[Array] = OUTPUT(label='TES expansion tank effective length', units='m', type='ARRAY', group='TES', required='tes_type=3')
    tes_mass_cold: Final[Array] = OUTPUT(label='TES cold fluid mass', units='kg', type='ARRAY', group='TES', required='tes_type=3')
    tes_mass_hot: Final[Array] = OUTPUT(label='TES hot fluid mass', units='kg', type='ARRAY', group='TES', required='tes_type=3')
    tes_V_cold: Final[Array] = OUTPUT(label='TES cold fluid volume', units='kg', type='ARRAY', group='TES', required='tes_type=3')
    tes_V_hot: Final[Array] = OUTPUT(label='TES hot fluid volume', units='kg', type='ARRAY', group='TES', required='tes_type=3')
    hot_tank_mass_perc: Final[Array] = OUTPUT(label='TES hot tank mass percent of total (end)', units='kg', type='ARRAY', group='TES', required='*')
    T_grad_final: Final[Matrix] = OUTPUT(label='TES Temperature gradient at end of timestep', units='C', type='MATRIX', group='TES', required='tes_type=2')

    def __init__(self, *args: Mapping[str, Any],
                 t_step: float = ...,
                 T_amb: Array = ...,
                 mdot_src: Array = ...,
                 mdot_sink: Array = ...,
                 hot_tank_bypassed: Array = ...,
                 T_src_out: Array = ...,
                 T_sink_out: Array = ...,
                 T_tank_hot_ini: float = ...,
                 T_tank_cold_ini: float = ...,
                 P_ref: float = ...,
                 eta_ref: float = ...,
                 solar_mult: float = ...,
                 T_loop_in_des: float = ...,
                 T_loop_out: float = ...,
                 pb_pump_coef: float = ...,
                 tes_type: float = ...,
                 Fluid: float = ...,
                 field_fl_props: Matrix = ...,
                 tshours: float = ...,
                 is_h_tank_fixed: float = ...,
                 h_tank_in: float = ...,
                 d_tank_in: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 cold_tank_Thtr: float = ...,
                 cold_tank_max_heat: float = ...,
                 h_tank_min: float = ...,
                 init_hot_htf_percent: float = ...,
                 tes_n_tsteps: float = ...,
                 V_tes_des: float = ...,
                 calc_design_pipe_vals: float = ...,
                 tes_pump_coef: float = ...,
                 eta_pump: float = ...,
                 has_hot_tank_bypass: float = ...,
                 T_tank_hot_inlet_min: float = ...,
                 custom_tes_p_loss: float = ...,
                 custom_tes_pipe_sizes: float = ...,
                 k_tes_loss_coeffs: Matrix = ...,
                 tes_diams: Matrix = ...,
                 tes_wallthicks: Matrix = ...,
                 tes_lengths: Matrix = ...,
                 HDR_rough: float = ...,
                 DP_SGS: float = ...,
                 store_fluid: float = ...,
                 store_fl_props: Matrix = ...,
                 dt_hot: float = ...,
                 tanks_in_parallel: float = ...,
                 tes_pb_n_xsteps: float = ...,
                 tes_pb_k_eff: float = ...,
                 tes_pb_void_frac: float = ...,
                 tes_pb_dens_solid: float = ...,
                 tes_pb_cp_solid: float = ...,
                 tes_pb_T_hot_delta: float = ...,
                 tes_pb_T_cold_delta: float = ...,
                 tes_pb_T_charge_min: float = ...,
                 tes_pb_f_oversize: float = ...,
                 tes_pb_T_grad_ini: Array = ...,
                 tes_cyl_tank_thick: float = ...,
                 tes_cyl_tank_cp: float = ...,
                 tes_cyl_tank_dens: float = ...,
                 tes_cyl_piston_loss_poly: Array = ...,
                 tes_cyl_tank_insul_percent: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
