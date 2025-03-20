
# This is a generated file

"""fresnel_physical - Physical Fresnel applications"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'sim_type': float,
    'file_name': str,
    'solar_mult_in': float,
    'total_Ap_in': float,
    'solar_mult_or_Ap': float,
    'T_loop_in_des': float,
    'T_loop_out': float,
    'I_bn_des': float,
    'P_ref': float,
    'eta_ref': float,
    'tshours': float,
    'gross_net_conversion_factor': float,
    'nMod': float,
    'eta_pump': float,
    'HDR_rough': float,
    'theta_stow': float,
    'theta_dep': float,
    'FieldConfig': float,
    'Fluid': float,
    'T_fp': float,
    'V_hdr_max': float,
    'V_hdr_min': float,
    'Pipe_hl_coef': float,
    'mc_bal_hot': float,
    'mc_bal_cold': float,
    'mc_bal_sca': float,
    'water_per_wash': float,
    'washes_per_year': float,
    'rec_htf_vol': float,
    'T_amb_sf_des': float,
    'V_wind_des': float,
    'field_fl_props': Matrix,
    'SCA_drives_elec': float,
    'land_mult': float,
    'T_startup': float,
    'p_start': float,
    'L_rnr_pb': float,
    'use_abs_or_rel_mdot_limit': float,
    'm_dot_htfmin': float,
    'm_dot_htfmax': float,
    'f_htfmin': float,
    'f_htfmax': float,
    'ColAz': float,
    'opt_model': float,
    'A_aperture': float,
    'reflectivity': float,
    'TrackingError': float,
    'GeomEffects': float,
    'Dirt_mirror': float,
    'Error': float,
    'L_mod': float,
    'IAM_T_coefs': Array,
    'IAM_L_coefs': Array,
    'OpticalTable': Matrix,
    'rec_model': float,
    'HCE_FieldFrac': Array,
    'D_abs_in': Array,
    'D_abs_out': Array,
    'D_glass_in': Array,
    'D_glass_out': Array,
    'D_plug': Array,
    'Flow_type': Array,
    'Rough': Array,
    'alpha_env': Array,
    'epsilon_abs_1': Matrix,
    'epsilon_abs_2': Matrix,
    'epsilon_abs_3': Matrix,
    'epsilon_abs_4': Matrix,
    'alpha_abs': Array,
    'Tau_envelope': Array,
    'epsilon_glass': Array,
    'GlazingIntactIn': Array,
    'P_a': Array,
    'AnnulusGas': Array,
    'AbsorberMaterial': Array,
    'Shadowing': Array,
    'dirt_env': Array,
    'Design_loss': Array,
    'L_mod_spacing': float,
    'L_crossover': float,
    'HL_T_coefs': Array,
    'HL_w_coefs': Array,
    'DP_nominal': float,
    'DP_coefs': Array,
    'nRecVar': float,
    'startup_time': float,
    'startup_frac': float,
    'q_sby_frac': float,
    'pb_pump_coef': float,
    'cycle_max_frac': float,
    'cycle_cutoff_frac': float,
    'pc_config': float,
    'dT_cw_ref': float,
    'T_amb_des': float,
    'CT': float,
    'T_approach': float,
    'T_ITD_des': float,
    'P_cond_ratio': float,
    'pb_bd_frac': float,
    'P_cond_min': float,
    'n_pl_inc': float,
    'F_wc': Array,
    'tech_type': float,
    'DP_SGS': float,
    'ud_f_W_dot_cool_des': float,
    'ud_m_dot_water_cool_des': float,
    'ud_is_sco2_regr': float,
    'ud_ind_od': Matrix,
    'store_fluid': float,
    'store_fl_props': Matrix,
    'h_tank': float,
    'u_tank': float,
    'tank_pairs': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'cold_tank_Thtr': float,
    'cold_tank_max_heat': float,
    'dt_hot': float,
    'h_tank_min': float,
    'dt_cold': float,
    'init_hot_htf_percent': float,
    'tes_pump_coef': float,
    'tanks_in_parallel': float,
    'V_tes_des': float,
    'is_timestep_load_fractions': float,
    'timestep_load_fractions': Array,
    'pb_fixed_par': float,
    'bop_array': Array,
    'aux_array': Array,
    'is_dispatch': float,
    'disp_frequency': float,
    'disp_horizon': float,
    'disp_max_iter': float,
    'disp_timeout': float,
    'disp_mip_gap': float,
    'disp_time_weighting': float,
    'disp_rsu_cost_rel': float,
    'disp_csu_cost_rel': float,
    'disp_pen_ramping': float,
    'can_cycle_use_standby': float,
    'disp_steps_per_hour': float,
    'disp_spec_presolve': float,
    'disp_spec_bb': float,
    'disp_reporting': float,
    'disp_spec_scaling': float,
    'disp_inventory_incentive': float,
    'q_rec_standby': float,
    'q_rec_heattrace': float,
    'rec_su_delay': float,
    'rec_qf_delay': float,
    'csp_financial_model': float,
    'weekday_schedule': Matrix,
    'weekend_schedule': Matrix,
    'is_tod_pc_target_also_pc_max': float,
    'f_turb_tou_periods': Array,
    'en_electricity_rates': float,
    'ppa_multiplier_model': float,
    'dispatch_factors_ts': Array,
    'dispatch_sched_weekday': Matrix,
    'dispatch_sched_weekend': Matrix,
    'dispatch_tod_factors': Array,
    'ppa_soln_mode': float,
    'ppa_price_input': Array,
    'mp_energy_market_revenue': Matrix,
    'site_improvements_spec_cost': float,
    'solar_field_spec_cost': float,
    'htf_system_spec_cost': float,
    'storage_spec_cost': float,
    'fossil_spec_cost': float,
    'power_plant_spec_cost': float,
    'bop_spec_cost': float,
    'contingency_percent': float,
    'epc_cost_per_acre': float,
    'epc_cost_percent_direct': float,
    'epc_cost_per_watt': float,
    'epc_cost_fixed': float,
    'plm_cost_per_acre': float,
    'plm_cost_percent_direct': float,
    'plm_cost_per_watt': float,
    'plm_cost_fixed': float,
    'sales_tax_percent': float,
    'sales_tax_rate': float,
    'const_per_interest_rate1': float,
    'const_per_interest_rate2': float,
    'const_per_interest_rate3': float,
    'const_per_interest_rate4': float,
    'const_per_interest_rate5': float,
    'const_per_months1': float,
    'const_per_months2': float,
    'const_per_months3': float,
    'const_per_months4': float,
    'const_per_months5': float,
    'const_per_percent1': float,
    'const_per_percent2': float,
    'const_per_percent3': float,
    'const_per_percent4': float,
    'const_per_percent5': float,
    'const_per_upfront_rate1': float,
    'const_per_upfront_rate2': float,
    'const_per_upfront_rate3': float,
    'const_per_upfront_rate4': float,
    'const_per_upfront_rate5': float,
    'system_capacity': float,
    'cp_system_nameplate': float,
    'cp_battery_nameplate': float,
    'solar_mult': float,
    'total_Ap': float,
    'nLoops': float,
    'nameplate': float,
    'A_loop': float,
    'loop_opt_eff': float,
    'loop_therm_eff': float,
    'loop_eff': float,
    'sm1_aperture': float,
    'sm1_nLoops': float,
    'total_tracking_power': float,
    'A_field': float,
    'q_field_des_actual': float,
    'q_field_des_ideal': float,
    'm_dot_htfmin_actual': float,
    'm_dot_htfmax_actual': float,
    'f_htfmin_actual': float,
    'f_htfmax_actual': float,
    'field_area': float,
    'total_land_area': float,
    'field_htf_min_temp': float,
    'field_htf_max_temp': float,
    'mdot_field_des': float,
    'dP_field_des_SS': float,
    'Q_field_des_SS': float,
    'T_field_out_des_SS': float,
    'm_dot_des_SS': float,
    'm_dot_loop_des_SS': float,
    'V_hdr_min_des_SS': float,
    'V_hdr_max_des_SS': float,
    'eta_optical_des_SS': float,
    'therm_eff_des_SS': float,
    'eff_des_SS': float,
    'W_dot_pump_des_SS': float,
    'T_loop_out_des_SS': float,
    'Q_loop_des_SS': float,
    'therm_eff_loop_des_SS': float,
    'eff_loop_des_SS': float,
    'Q_loss_receiver_des_SS': float,
    'Q_loss_hdr_rnr_des_SS': float,
    'DP_pressure_loss': float,
    'avg_dt_des': float,
    'hl_des': float,
    'opt_derate': float,
    'opt_normal': float,
    'q_dot_cycle_des': float,
    'mdot_cycle_des': float,
    'vol_tank': float,
    'Q_tes_des': float,
    'd_tank': float,
    'vol_min': float,
    'q_dot_loss_tes_des': float,
    'tes_htf_min_temp': float,
    'tes_htf_max_temp': float,
    'tes_htf_dens': float,
    'tes_htf_cp': float,
    'W_dot_bop_design': float,
    'W_dot_fixed': float,
    'aux_design': float,
    'site_improvements_cost': float,
    'solar_field_cost': float,
    'htf_system_cost': float,
    'ts_cost': float,
    'fossil_backup_cost': float,
    'power_plant_cost': float,
    'bop_cost': float,
    'contingency_cost': float,
    'total_direct_cost': float,
    'epc_total_cost': float,
    'plm_total_cost': float,
    'total_indirect_cost': float,
    'sales_tax_total': float,
    'total_installed_cost': float,
    'installed_per_capacity': float,
    'const_per_principal1': float,
    'const_per_principal2': float,
    'const_per_principal3': float,
    'const_per_principal4': float,
    'const_per_principal5': float,
    'const_per_interest1': float,
    'const_per_interest2': float,
    'const_per_interest3': float,
    'const_per_interest4': float,
    'const_per_interest5': float,
    'const_per_total1': float,
    'const_per_total2': float,
    'const_per_total3': float,
    'const_per_total4': float,
    'const_per_total5': float,
    'const_per_percent_total': float,
    'const_per_principal_total': float,
    'const_per_interest_total': float,
    'construction_financing_cost': float,
    'time_hr': Array,
    'month': Array,
    'hour_day': Array,
    'solazi': Array,
    'solzen': Array,
    'beam': Array,
    'tdry': Array,
    'twet': Array,
    'rh': Array,
    'wspd': Array,
    'pres': Array,
    'defocus': Array,
    'EqOpteff': Array,
    'SCAs_def': Array,
    'q_inc_sf_tot': Array,
    'q_dot_rec_inc': Array,
    'q_dot_rec_thermal_loss': Array,
    'q_dot_rec_abs': Array,
    'rec_thermal_eff': Array,
    'q_dot_piping_loss': Array,
    'e_dot_field_int_energy': Array,
    'q_dot_htf_sf_out': Array,
    'q_dot_freeze_prot': Array,
    'm_dot_loop': Array,
    'm_dot_field_recirc': Array,
    'm_dot_field_delivered': Array,
    'T_field_cold_in': Array,
    'T_rec_cold_in': Array,
    'T_rec_hot_out': Array,
    'T_field_hot_out': Array,
    'deltaP_field': Array,
    'W_dot_sca_track': Array,
    'W_dot_field_pump': Array,
    'eta': Array,
    'q_pb': Array,
    'm_dot_pc': Array,
    'q_dot_pc_startup': Array,
    'P_cycle': Array,
    'T_pc_in': Array,
    'T_pc_out': Array,
    'm_dot_water_pc': Array,
    'q_pc_startup': Array,
    'cycle_htf_pump_power': Array,
    'P_cooling_tower_tot': Array,
    'tank_losses': Array,
    'q_tes_heater': Array,
    'T_tes_hot': Array,
    'T_tes_cold': Array,
    'mass_tes_cold': Array,
    'mass_tes_hot': Array,
    'q_dc_tes': Array,
    'q_ch_tes': Array,
    'e_ch_tes': Array,
    'm_dot_cr_to_tes_hot': Array,
    'm_dot_tes_hot_out': Array,
    'm_dot_pc_to_tes_cold': Array,
    'm_dot_tes_cold_out': Array,
    'm_dot_field_to_cycle': Array,
    'm_dot_cycle_to_field': Array,
    'm_dot_cold_tank_to_hot_tank': Array,
    'tes_htf_pump_power': Array,
    'op_mode_1': Array,
    'op_mode_2': Array,
    'op_mode_3': Array,
    'm_dot_balance': Array,
    'q_balance': Array,
    'monthly_energy': Array,
    'annual_energy': float,
    'annual_thermal_consumption': float,
    'annual_total_water_use': float,
    'annual_field_freeze_protection': float,
    'annual_tes_freeze_protection': float,
    'n_op_modes': Array,
    'tou_value': Array,
    'pricing_mult': Array,
    'q_dot_pc_sb': Array,
    'q_dot_pc_min': Array,
    'q_dot_pc_target': Array,
    'q_dot_pc_max': Array,
    'is_rec_su_allowed': Array,
    'is_pc_su_allowed': Array,
    'is_pc_sb_allowed': Array,
    'q_dot_est_cr_su': Array,
    'q_dot_est_cr_on': Array,
    'q_dot_est_tes_dc': Array,
    'q_dot_est_tes_ch': Array,
    'operating_modes_a': Array,
    'operating_modes_b': Array,
    'operating_modes_c': Array,
    'disp_rel_mip_gap': Array,
    'disp_solve_state': Array,
    'disp_subopt_flag': Array,
    'disp_solve_iter': Array,
    'disp_objective': Array,
    'disp_obj_relax': Array,
    'disp_qsf_expected': Array,
    'disp_qsfprod_expected': Array,
    'disp_qsfsu_expected': Array,
    'disp_tes_expected': Array,
    'disp_pceff_expected': Array,
    'disp_thermeff_expected': Array,
    'disp_qpbsu_expected': Array,
    'disp_wpb_expected': Array,
    'disp_rev_expected': Array,
    'disp_presolve_nconstr': Array,
    'disp_presolve_nvar': Array,
    'disp_solve_time': Array,
    'avg_suboptimal_rel_mip_gap': float,
    'P_fixed': Array,
    'P_plant_balance_tot': Array,
    'P_out_net': Array,
    'gen': Array,
    'annual_W_cycle_gross': float,
    'conversion_factor': float,
    'capacity_factor': float,
    'kwh_per_kw': float,
    'sim_duration': float,
    'recirculating': Array,
    'pipe_tes_diams': Array,
    'pipe_tes_wallthk': Array,
    'pipe_tes_lengths': Array,
    'pipe_tes_mdot_dsn': Array,
    'pipe_tes_vel_dsn': Array,
    'pipe_tes_T_dsn': Array,
    'pipe_tes_P_dsn': Array,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix
}, total=False)

class Data(ssc.DataDict):
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='System Control', required='?=1')
    file_name: str = INPUT(label='Local weather file with path', units='none', type='STRING', group='weather', required='*', constraints='LOCAL_FILE')
    solar_mult_in: float = INPUT(label='Solar multiple Input', type='NUMBER', group='System_Design', required='*')
    total_Ap_in: float = INPUT(label='Field aperture Input', units='m3', type='NUMBER', group='System_Design', required='*')
    solar_mult_or_Ap: float = INPUT(label='Design using specified solar mult or field aperture', units='m3', type='NUMBER', group='System_Design', required='?=0')
    T_loop_in_des: float = INPUT(label='Design loop inlet temperature', units='C', type='NUMBER', group='System_Design', required='*')
    T_loop_out: float = INPUT(label='Target loop outlet temperature', units='C', type='NUMBER', group='System_Design', required='*')
    I_bn_des: float = INPUT(label='Solar irradiation at design', units='W/m2', type='NUMBER', group='System_Design', required='*')
    P_ref: float = INPUT(label='Design Turbine Net Output', units='MWe', type='NUMBER', group='System_Design', required='*')
    eta_ref: float = INPUT(label='Cycle thermal efficiency at design point', units='-', type='NUMBER', group='System_Design', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='System_Design', required='*')
    gross_net_conversion_factor: float = INPUT(label='Estimated gross to net conversion factor', type='NUMBER', group='System_Design', required='*')
    nMod: float = INPUT(label='Number of collector modules in a loop', type='NUMBER', group='Solar_Field', required='*', constraints='INTEGER')
    eta_pump: float = INPUT(label='HTF pump efficiency', type='NUMBER', group='Solar_Field', required='*')
    HDR_rough: float = INPUT(label='Header pipe roughness', units='m', type='NUMBER', group='Solar_Field', required='*')
    theta_stow: float = INPUT(label='stow angle', units='deg', type='NUMBER', group='Solar_Field', required='*')
    theta_dep: float = INPUT(label='deploy angle', units='deg', type='NUMBER', group='Solar_Field', required='*')
    FieldConfig: float = INPUT(label='Number of subfield headers', type='NUMBER', group='Solar_Field', required='*')
    Fluid: float = INPUT(label='Field HTF fluid number', type='NUMBER', group='Solar_Field', required='*', constraints='INTEGER')
    T_fp: float = INPUT(label='Freeze protection temperature (heat trace activation temperature)', units='C', type='NUMBER', group='Solar_Field', required='*')
    V_hdr_max: float = INPUT(label='Maximum HTF velocity in the header at design', units='m/s', type='NUMBER', group='Solar_Field', required='*')
    V_hdr_min: float = INPUT(label='Minimum HTF velocity in the header at design', units='m/s', type='NUMBER', group='Solar_Field', required='*')
    Pipe_hl_coef: float = INPUT(label='Loss coefficient from the header - runner pipe - and non-HCE piping', units='W/m2-K', type='NUMBER', group='Solar_Field', required='*')
    mc_bal_hot: float = INPUT(label='The heat capacity of the balance of plant on the hot side', units='kWht/K-MWt', type='NUMBER', group='Solar_Field', required='*')
    mc_bal_cold: float = INPUT(label='The heat capacity of the balance of plant on the cold side', units='kWht/K-MWt', type='NUMBER', group='Solar_Field', required='*')
    mc_bal_sca: float = INPUT(label='Non-HTF heat capacity associated with each SCA - per meter basis', units='Wht/K-m', type='NUMBER', group='Solar_Field', required='*')
    water_per_wash: float = INPUT(label='Water usage per wash', units='L/m2_aper', type='NUMBER', group='Solar_Field', required='*')
    washes_per_year: float = INPUT(label='Mirror washing frequency', units='none', type='NUMBER', group='Solar_Field', required='*')
    rec_htf_vol: float = INPUT(label='Volume of HTF in a single collector unit per unit aperture area', units='L/m2-ap', type='NUMBER', group='Solar_Field', required='*')
    T_amb_sf_des: float = INPUT(label='Ambient design-point temperature for the solar field', units='C', type='NUMBER', group='Solar_Field', required='*')
    V_wind_des: float = INPUT(label='Design-point wind velocity', units='m/s', type='NUMBER', group='Solar_Field', required='*')
    field_fl_props: Matrix = INPUT(label='Fluid property data', type='MATRIX', group='Solar_Field', required='*')
    SCA_drives_elec: float = INPUT(label='Tracking power in Watts per SCA drive', units='W/module', type='NUMBER', group='Solar_Field', required='*')
    land_mult: float = INPUT(label='Non-solar field land area multiplier', units='-', type='NUMBER', group='Solar_Field', required='*')
    T_startup: float = INPUT(label='Power block startup temperature', units='C', type='NUMBER', group='Solar_Field', required='*')
    p_start: float = INPUT(label='Collector startup energy, per SCA', units='kWhe', type='NUMBER', group='Solar_Field', required='*')
    L_rnr_pb: float = INPUT(label='Length of runner pipe in power block', units='m', type='NUMBER', group='Solar_Field', required='*')
    use_abs_or_rel_mdot_limit: float = INPUT(label='Use mass flow abs (0) or relative (1) limits', type='NUMBER', group='Solar_Field', required='?=0')
    m_dot_htfmin: float = INPUT(label='Minimum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='use_abs_or_rel_mdot_limit=0')
    m_dot_htfmax: float = INPUT(label='Maximum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='use_abs_or_rel_mdot_limit=0')
    f_htfmin: float = INPUT(label='Minimum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='use_abs_or_rel_mdot_limit=1')
    f_htfmax: float = INPUT(label='Maximum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='use_abs_or_rel_mdot_limit=1')
    ColAz: float = INPUT(label='Collector azimuth angle', units='deg', type='NUMBER', group='Col_Rec', required='*')
    opt_model: float = INPUT(label='The optical model', type='NUMBER', group='Col_Rec', required='*', constraints='INTEGER')
    A_aperture: float = INPUT(label='Reflective aperture area of the collector', units='m2', type='NUMBER', group='Col_Rec', required='*')
    reflectivity: float = INPUT(label='Solar-weighted mirror reflectivity value', type='NUMBER', group='Col_Rec', required='*')
    TrackingError: float = INPUT(label='Tracking error derate', type='NUMBER', group='Col_Rec', required='*')
    GeomEffects: float = INPUT(label='Geometry effects derate', type='NUMBER', group='Col_Rec', required='*')
    Dirt_mirror: float = INPUT(label='User-defined dirt on mirror derate', type='NUMBER', group='Col_Rec', required='*')
    Error: float = INPUT(label='User-defined general optical error derate', type='NUMBER', group='Col_Rec', required='*')
    L_mod: float = INPUT(label='The length of the collector module', units='m', type='NUMBER', group='Col_Rec', required='*')
    IAM_T_coefs: Array = INPUT(label='Incidence angle modifier coefficients - transversal plane', type='ARRAY', group='Col_Rec', required='*')
    IAM_L_coefs: Array = INPUT(label='Incidence angle modifier coefficients - longitudinal plane', type='ARRAY', group='Col_Rec', required='*')
    OpticalTable: Matrix = INPUT(label='Values of the optical efficiency table', type='MATRIX', group='Col_Rec', required='*')
    rec_model: float = INPUT(label='Receiver model type (1=Polynomial ; 2=Evac tube)', type='NUMBER', group='Col_Rec', required='*', constraints='INTEGER')
    HCE_FieldFrac: Array = INPUT(label='The fraction of the field occupied by this HCE type', type='ARRAY', group='Col_Rec', required='*')
    D_abs_in: Array = INPUT(label='The inner absorber tube diameter', units='m', type='ARRAY', group='Col_Rec', required='*')
    D_abs_out: Array = INPUT(label='The outer absorber tube diameter', units='m', type='ARRAY', group='Col_Rec', required='*')
    D_glass_in: Array = INPUT(label='The inner glass envelope diameter', units='m', type='ARRAY', group='Col_Rec', required='*')
    D_glass_out: Array = INPUT(label='The outer glass envelope diameter', units='m', type='ARRAY', group='Col_Rec', required='*')
    D_plug: Array = INPUT(label='The diameter of the absorber flow plug (optional)', units='m', type='ARRAY', group='Col_Rec', required='*')
    Flow_type: Array = INPUT(label='The flow type through the absorber', type='ARRAY', group='Col_Rec', required='*')
    Rough: Array = INPUT(label='Roughness of the internal surface', units='m', type='ARRAY', group='Col_Rec', required='*')
    alpha_env: Array = INPUT(label='Envelope absorptance', type='ARRAY', group='Col_Rec', required='*')
    epsilon_abs_1: Matrix = INPUT(label='Absorber emittance - HCE variation 1', type='MATRIX', group='Col_Rec', required='*')
    epsilon_abs_2: Matrix = INPUT(label='Absorber emittance - HCE variation 2', type='MATRIX', group='Col_Rec', required='*')
    epsilon_abs_3: Matrix = INPUT(label='Absorber emittance - HCE variation 3', type='MATRIX', group='Col_Rec', required='*')
    epsilon_abs_4: Matrix = INPUT(label='Absorber emittance - HCE variation 4', type='MATRIX', group='Col_Rec', required='*')
    alpha_abs: Array = INPUT(label='Absorber absorptance', type='ARRAY', group='Col_Rec', required='*')
    Tau_envelope: Array = INPUT(label='Envelope transmittance', type='ARRAY', group='Col_Rec', required='*')
    epsilon_glass: Array = INPUT(label='Glass envelope emissivity', type='ARRAY', group='Col_Rec', required='*')
    GlazingIntactIn: Array = INPUT(label='The glazing intact flag', type='ARRAY', group='Col_Rec', required='*')
    P_a: Array = INPUT(label='Annulus gas pressure', units='torr', type='ARRAY', group='Col_Rec', required='*')
    AnnulusGas: Array = INPUT(label='Annulus gas type (1=air; 26=Ar; 27=H2)', type='ARRAY', group='Col_Rec', required='*')
    AbsorberMaterial: Array = INPUT(label='Absorber material type', type='ARRAY', group='Col_Rec', required='*')
    Shadowing: Array = INPUT(label='Receiver bellows shadowing loss factor', type='ARRAY', group='Col_Rec', required='*')
    dirt_env: Array = INPUT(label='Loss due to dirt on the receiver envelope', type='ARRAY', group='Col_Rec', required='*')
    Design_loss: Array = INPUT(label='Receiver heat loss at design', units='W/m', type='ARRAY', group='Col_Rec', required='*')
    L_mod_spacing: float = INPUT(label='Piping distance between sequential modules in a loop', units='m', type='NUMBER', group='Col_Rec', required='*')
    L_crossover: float = INPUT(label='Length of crossover piping in a loop', units='m', type='NUMBER', group='Col_Rec', required='*')
    HL_T_coefs: Array = INPUT(label='HTF temperature-dependent heat loss coefficients', units='W/m-K', type='ARRAY', group='Col_Rec', required='*')
    HL_w_coefs: Array = INPUT(label='Wind-speed-dependent heat loss coefficients', units='W/m-(m/s)', type='ARRAY', group='Col_Rec', required='*')
    DP_nominal: float = INPUT(label='Pressure drop across a single collector assembly at design', units='bar', type='NUMBER', group='Col_Rec', required='*')
    DP_coefs: Array = INPUT(label='Pressure drop mass flow based part-load curve', type='ARRAY', group='Col_Rec', required='*')
    nRecVar: float = INPUT(label='Number of receiver variations', type='NUMBER', group='Col_Rec', required='?=4', constraints='INTEGER')
    startup_time: float = INPUT(label='Time needed for power block startup', units='hr', type='NUMBER', group='Powerblock', required='*')
    startup_frac: float = INPUT(label='Fraction of design thermal power needed for startup', units='none', type='NUMBER', group='Powerblock', required='*')
    q_sby_frac: float = INPUT(label='Fraction of thermal power required for standby mode', units='none', type='NUMBER', group='Powerblock', required='*')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='Powerblock', required='*')
    cycle_max_frac: float = INPUT(label='Maximum turbine over design operation fraction', type='NUMBER', group='Powerblock', required='*')
    cycle_cutoff_frac: float = INPUT(label='Minimum turbine operation fraction before shutdown', type='NUMBER', group='Powerblock', required='*')
    pc_config: float = INPUT(label='0: Steam Rankine (224), 1: user defined', units='-', type='NUMBER', group='Powerblock', required='?=0', constraints='INTEGER')
    dT_cw_ref: float = INPUT(label='Reference condenser cooling water inlet/outlet T diff', units='C', type='NUMBER', group='Powerblock', required='pc_config=0')
    T_amb_des: float = INPUT(label='Reference ambient temperature at design point', units='C', type='NUMBER', group='Powerblock', required='pc_config=0')
    CT: float = INPUT(label='Flag for using dry cooling or wet cooling system', units='none', type='NUMBER', group='Powerblock', required='pc_config=0')
    T_approach: float = INPUT(label='Cooling tower approach temperature', units='C', type='NUMBER', group='Powerblock', required='pc_config=0')
    T_ITD_des: float = INPUT(label='ITD at design for dry system', units='C', type='NUMBER', group='Powerblock', required='pc_config=0')
    P_cond_ratio: float = INPUT(label='Condenser pressure ratio', units='none', type='NUMBER', group='Powerblock', required='pc_config=0')
    pb_bd_frac: float = INPUT(label='Power block blowdown steam fraction ', units='none', type='NUMBER', group='Powerblock', required='pc_config=0')
    P_cond_min: float = INPUT(label='Minimum condenser pressure', units='inHg', type='NUMBER', group='Powerblock', required='pc_config=0')
    n_pl_inc: float = INPUT(label='Number of part-load increments for the heat rejection system', units='none', type='NUMBER', group='Powerblock', required='pc_config=0')
    F_wc: Array = INPUT(label='Fraction indicating wet cooling use for hybrid system', units='none', type='ARRAY', group='Powerblock', required='pc_config=0', meta='constant=[0,0,0,0,0,0,0,0,0]')
    tech_type: float = INPUT(label='Turbine inlet pressure control flag (sliding=user, fixed=fresnel)', units='1/2/3', type='NUMBER', group='Powerblock', required='pc_config=0', meta='tower/trough/user')
    DP_SGS: float = INPUT(label='Pressure drop within the steam generator', units='bar', type='NUMBER', group='Powerblock', required='*')
    ud_f_W_dot_cool_des: float = INPUT(label='Percent of user-defined power cycle design gross output consumed by cooling', units='%', type='NUMBER', group='user_defined_PC', required='pc_config=1')
    ud_m_dot_water_cool_des: float = INPUT(label='Mass flow rate of water required at user-defined power cycle design point', units='kg/s', type='NUMBER', group='user_defined_PC', required='pc_config=1')
    ud_is_sco2_regr: float = INPUT(label='0: (default) simple max htf mass flow correction; 1: sco2 heuristic regression; 2: no correction', type='NUMBER', group='user_defined_PC', required='?=0')
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='user_defined_PC', required='pc_config=1')
    store_fluid: float = INPUT(label='Storage HTF ID', type='NUMBER', group='Storage', required='*')
    store_fl_props: Matrix = INPUT(label='Storage user-defined HTF Properties', type='MATRIX', group='Storage', required='*')
    h_tank: float = INPUT(label='Height of HTF when tank is full', type='NUMBER', group='Storage', required='*')
    u_tank: float = INPUT(label='Loss coefficient from tank', type='NUMBER', group='Storage', required='*')
    tank_pairs: float = INPUT(label='Number of equivalent tank pairs', type='NUMBER', group='Storage', required='*', constraints='INTEGER')
    hot_tank_Thtr: float = INPUT(label='Hot tank heater set point', type='NUMBER', group='Storage', required='*')
    hot_tank_max_heat: float = INPUT(label='Rated heater capacity for hot tank heating', units='MWe', type='NUMBER', group='Storage', required='*')
    cold_tank_Thtr: float = INPUT(label='Cold tank heater set point', type='NUMBER', group='Storage', required='*')
    cold_tank_max_heat: float = INPUT(label='Rated heater capacity for cold tank heating', units='MWe', type='NUMBER', group='Storage', required='*')
    dt_hot: float = INPUT(label='Hot side HX approach temp', type='NUMBER', group='Storage', required='*')
    h_tank_min: float = INPUT(label='Minimum tank fluid height', type='NUMBER', group='Storage', required='*')
    dt_cold: float = INPUT(label='Cold side HX approach temp', type='NUMBER', group='Storage', required='*')
    init_hot_htf_percent: float = INPUT(label='Initial fraction of avail. vol that is hot', units='%', type='NUMBER', group='Storage', required='*')
    tes_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through tes loop', units='kW/(kg/s)', type='NUMBER', group='Storage', required='*')
    tanks_in_parallel: float = INPUT(label='Tanks are in parallel, not in series, with solar field', units='-', type='NUMBER', group='Storage', required='*')
    V_tes_des: float = INPUT(label='Design-point velocity to size the TES pipe diameters', units='m/s', type='NUMBER', group='Storage', required='?=1.85')
    is_timestep_load_fractions: float = INPUT(label='Use turbine load fraction for each timestep instead of block dispatch?', type='NUMBER', group='tou', required='?=0')
    timestep_load_fractions: Array = INPUT(label='Turbine load fraction for each timestep, alternative to block dispatch', type='ARRAY', group='tou', required='?')
    pb_fixed_par: float = INPUT(label='Fixed parasitic load - runs at all times', type='NUMBER', group='Sys_Control', required='*')
    bop_array: Array = INPUT(label='Balance of plant parasitic power fraction', type='ARRAY', group='Sys_Control', required='*')
    aux_array: Array = INPUT(label='Aux heater, boiler parasitic', type='ARRAY', group='Sys_Control', required='*')
    is_dispatch: float = INPUT(label='Allow dispatch optimization?', units='-', type='NUMBER', group='Sys_Control', required='?=0')
    disp_frequency: float = INPUT(label='Frequency for dispatch optimization calculations', units='hour', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_horizon: float = INPUT(label='Time horizon for dispatch optimization', units='hour', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_max_iter: float = INPUT(label='Max. no. dispatch optimization iterations', units='-', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_timeout: float = INPUT(label='Max. dispatch optimization solve duration', units='s', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_mip_gap: float = INPUT(label='Dispatch optimization solution tolerance', units='-', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_time_weighting: float = INPUT(label='Dispatch optimization future time discounting factor', units='-', type='NUMBER', group='Sys_Control', required='?=0.99')
    disp_rsu_cost_rel: float = INPUT(label='Receiver startup cost', units='$/MWt/start', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_csu_cost_rel: float = INPUT(label='Cycle startup cost', units='$/MWe-cycle/start', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_pen_ramping: float = INPUT(label='Dispatch cycle production change penalty', units='$/MWe-change', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    can_cycle_use_standby: float = INPUT(label='Can the cycle use standby operation?', type='NUMBER', group='tou', required='?=0')
    disp_steps_per_hour: float = INPUT(label='Time steps per hour for dispatch optimization calculations', units='-', type='NUMBER', group='tou', required='?=1')
    disp_spec_presolve: float = INPUT(label='Dispatch optimization presolve heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_bb: float = INPUT(label='Dispatch optimization B&B heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_reporting: float = INPUT(label='Dispatch optimization reporting level', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_scaling: float = INPUT(label='Dispatch optimization scaling heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_inventory_incentive: float = INPUT(label='Dispatch storage terminal inventory incentive multiplier', type='NUMBER', group='System Control', required='?=0.0')
    q_rec_standby: float = INPUT(label='Receiver standby energy consumption', units='kWt', type='NUMBER', group='tou', required='?=9e99')
    q_rec_heattrace: float = INPUT(label='Receiver heat trace energy consumption during startup', units='kWhe', type='NUMBER', group='tou', required='?=0.0')
    rec_su_delay: float = INPUT(label='Fixed startup delay time for the receiver', units='hr', type='NUMBER', group='Sys_Control', required='*')
    rec_qf_delay: float = INPUT(label='Energy-based receiver startup delay (fraction of rated thermal power)', units='-', type='NUMBER', group='Sys_Control', required='*')
    csp_financial_model: float = INPUT(units='1-8', type='NUMBER', group='Financial Model', required='?=1', constraints='INTEGER,MIN=0')
    weekday_schedule: Matrix = INPUT(label='12x24 Time of Use Values for week days', type='MATRIX', group='Sys_Control', required='*')
    weekend_schedule: Matrix = INPUT(label='12x24 Time of Use Values for week end days', type='MATRIX', group='Sys_Control', required='*')
    is_tod_pc_target_also_pc_max: float = INPUT(label='Is the TOD target cycle heat input also the max cycle heat input?', type='NUMBER', group='tou', required='?=0')
    f_turb_tou_periods: Array = INPUT(label='Dispatch logic for turbine load fraction', units='-', type='ARRAY', group='tou', required='*')
    en_electricity_rates: float = INPUT(label='Enable electricity rates for grid purchase', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model 0: dispatch factors dispatch_factorX, 1: hourly multipliers dispatch_factors_ts', units='0/1', type='NUMBER', group='tou', required='?=0', constraints='INTEGER,MIN=0')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor array', type='ARRAY', group='tou', required='ppa_multiplier_model=1&csp_financial_model<5&is_dispatch=1')
    dispatch_sched_weekday: Matrix = INPUT(label='PPA pricing weekday schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekend: Matrix = INPUT(label='PPA pricing weekend schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_tod_factors: Array = INPUT(label='TOD factors for periods 1 through 9', type='ARRAY', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1', meta='We added this array input after SAM 2022.12.21 to replace the functionality of former single value inputs dispatch_factor1 through dispatch_factor9')
    ppa_soln_mode: float = INPUT(label='PPA solution mode (0=Specify IRR target, 1=Specify PPA price)', type='NUMBER', group='Financial Solution Mode', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    ppa_price_input: Array = INPUT(label='PPA solution mode (0=Specify IRR target, 1=Specify PPA price)', type='ARRAY', group='Financial Solution Mode', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    mp_energy_market_revenue: Matrix = INPUT(label='Energy market revenue input', type='MATRIX', group='Revenue', required='csp_financial_model=6&is_dispatch=1&sim_type=1', meta='Lifetime x 2[Cleared Capacity(MW),Price($ / MWh)]')
    site_improvements_spec_cost: float = INPUT(label='Site Improvement Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    solar_field_spec_cost: float = INPUT(label='Solar Field Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    htf_system_spec_cost: float = INPUT(label='HTF System Cost Per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    storage_spec_cost: float = INPUT(label='Storage cost per kWht', units='$/kWht', type='NUMBER', group='Capital_Costs', required='?=0')
    fossil_spec_cost: float = INPUT(label='Fossil Backup Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    power_plant_spec_cost: float = INPUT(label='Power Plant Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    bop_spec_cost: float = INPUT(label='Balance of Plant Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    contingency_percent: float = INPUT(label='Contingency Percent', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    epc_cost_per_acre: float = INPUT(label='EPC Costs per acre', units='$/acre', type='NUMBER', group='Capital_Costs', required='?=0')
    epc_cost_percent_direct: float = INPUT(label='EPC Costs % direct', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    epc_cost_per_watt: float = INPUT(label='EPC Cost Wac', units='$/Wac', type='NUMBER', group='Capital_Costs', required='?=0')
    epc_cost_fixed: float = INPUT(label='Fixed EPC Cost', units='$', type='NUMBER', group='Capital_Costs', required='?=0')
    plm_cost_per_acre: float = INPUT(label='Land Cost per acre', units='$/acre', type='NUMBER', group='Capital_Costs', required='?=0')
    plm_cost_percent_direct: float = INPUT(label='Land Cost % direct', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    plm_cost_per_watt: float = INPUT(label='Land Cost Wac', units='$/Wac', type='NUMBER', group='Capital_Costs', required='?=0')
    plm_cost_fixed: float = INPUT(label='Fixed Land Cost', units='$', type='NUMBER', group='Capital_Costs', required='?=0')
    sales_tax_percent: float = INPUT(label='Sales Tax Percentage of Direct Cost', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    sales_tax_rate: float = INPUT(label='Sales Tax Rate', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    const_per_interest_rate1: float = INPUT(label='Interest rate, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest_rate2: float = INPUT(label='Interest rate, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest_rate3: float = INPUT(label='Interest rate, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest_rate4: float = INPUT(label='Interest rate, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest_rate5: float = INPUT(label='Interest rate, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_months1: float = INPUT(label='Months prior to operation, loan 1', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_months2: float = INPUT(label='Months prior to operation, loan 2', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_months3: float = INPUT(label='Months prior to operation, loan 3', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_months4: float = INPUT(label='Months prior to operation, loan 4', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_months5: float = INPUT(label='Months prior to operation, loan 5', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent1: float = INPUT(label='Percent of total installed cost, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent2: float = INPUT(label='Percent of total installed cost, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent3: float = INPUT(label='Percent of total installed cost, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent4: float = INPUT(label='Percent of total installed cost, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent5: float = INPUT(label='Percent of total installed cost, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_upfront_rate1: float = INPUT(label='Upfront fee on principal, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_upfront_rate2: float = INPUT(label='Upfront fee on principal, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_upfront_rate3: float = INPUT(label='Upfront fee on principal, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_upfront_rate4: float = INPUT(label='Upfront fee on principal, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_upfront_rate5: float = INPUT(label='Upfront fee on principal, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    system_capacity: Final[float] = OUTPUT(label='System capacity', units='kWe', type='NUMBER', group='System Design', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWe', type='NUMBER', group='System Design', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWe', type='NUMBER', group='System Design', required='*')
    solar_mult: Final[float] = OUTPUT(label='Actual solar multiple', type='NUMBER', group='System Design Calc', required='*')
    total_Ap: Final[float] = OUTPUT(label='Actual field aperture', units='m2', type='NUMBER', group='System Design Calc', required='*')
    nLoops: Final[float] = OUTPUT(label='Number of loops in the field', type='NUMBER', group='controller', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    A_loop: Final[float] = OUTPUT(label='Aperture of a single loop', units='m2', type='NUMBER', group='Receiver', required='*')
    loop_opt_eff: Final[float] = OUTPUT(label='Loop optical efficiency at design', type='NUMBER', group='Receiver', required='*')
    loop_therm_eff: Final[float] = OUTPUT(label='Loop thermal efficiency at design', type='NUMBER', group='Receiver', required='*')
    loop_eff: Final[float] = OUTPUT(label='Total loop conversion efficiency at design', type='NUMBER', group='Receiver', required='*')
    sm1_aperture: Final[float] = OUTPUT(label='Total required aperture, SM=1', units='m2', type='NUMBER', group='Receiver', required='*')
    sm1_nLoops: Final[float] = OUTPUT(label='Required number of loops, SM=1', type='NUMBER', group='Receiver', required='*')
    total_tracking_power: Final[float] = OUTPUT(label='Design tracking power', units='MW', type='NUMBER', group='Receiver', required='*')
    A_field: Final[float] = OUTPUT(label='Total field aperture', units='m2', type='NUMBER', group='Receiver', required='*')
    q_field_des_actual: Final[float] = OUTPUT(label='Design-point thermal power from the solar field limited by mass flow', units='MW', type='NUMBER', group='Receiver', required='*')
    q_field_des_ideal: Final[float] = OUTPUT(label='Design-point thermal power from the solar field with no limit', units='MW', type='NUMBER', group='Receiver', required='*')
    m_dot_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='*')
    m_dot_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='*')
    f_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='*')
    f_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='*')
    field_area: Final[float] = OUTPUT(label='Solar field area', units='acres', type='NUMBER', group='Receiver', required='*')
    total_land_area: Final[float] = OUTPUT(label='Total land area', units='acres', type='NUMBER', group='Receiver', required='*')
    field_htf_min_temp: Final[float] = OUTPUT(label='Minimum field htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    field_htf_max_temp: Final[float] = OUTPUT(label='Maximum field htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    mdot_field_des: Final[float] = OUTPUT(label='Field design HTF mass flow rate', units='kg/s', type='NUMBER', group='Receiver', required='*')
    dP_field_des_SS: Final[float] = OUTPUT(label='Steady State Field design total pressure drop', units='bar', type='NUMBER', group='Receiver', required='*')
    Q_field_des_SS: Final[float] = OUTPUT(label='Steady State Field design thermal power', units='MWt', type='NUMBER', group='Receiver', required='*')
    T_field_out_des_SS: Final[float] = OUTPUT(label='Steady State Field design outlet temperature', units='C', type='NUMBER', group='Receiver', required='*')
    m_dot_des_SS: Final[float] = OUTPUT(label='Steady State Field mass flow rate', units='kg/s', type='NUMBER', group='Receiver', required='*')
    m_dot_loop_des_SS: Final[float] = OUTPUT(label='Steady State Loop mass flow rate', units='kg/s', type='NUMBER', group='Receiver', required='*')
    V_hdr_min_des_SS: Final[float] = OUTPUT(label='Steady State min header velocity', units='m/s', type='NUMBER', group='Receiver', required='*')
    V_hdr_max_des_SS: Final[float] = OUTPUT(label='Steady State max header velocity', units='m/s', type='NUMBER', group='Receiver', required='*')
    eta_optical_des_SS: Final[float] = OUTPUT(label='Steady State optical efficiency', type='NUMBER', group='Receiver', required='*')
    therm_eff_des_SS: Final[float] = OUTPUT(label='Steady State field optical efficiency', type='NUMBER', group='Receiver', required='*')
    eff_des_SS: Final[float] = OUTPUT(label='Steady State field total efficiency', type='NUMBER', group='Receiver', required='*')
    W_dot_pump_des_SS: Final[float] = OUTPUT(label='Steady State field pumping power', units='MWe', type='NUMBER', group='Receiver', required='*')
    T_loop_out_des_SS: Final[float] = OUTPUT(label='Steady State loop design outlet temperature', units='C', type='NUMBER', group='Receiver', required='*')
    Q_loop_des_SS: Final[float] = OUTPUT(label='Steady State loop design thermal power', units='MWt', type='NUMBER', group='Receiver', required='*')
    therm_eff_loop_des_SS: Final[float] = OUTPUT(label='Steady State loop optical efficiency', type='NUMBER', group='Receiver', required='*')
    eff_loop_des_SS: Final[float] = OUTPUT(label='Steady State loop total efficiency', type='NUMBER', group='Receiver', required='*')
    Q_loss_receiver_des_SS: Final[float] = OUTPUT(label='Steady State field heat loss from receiver', units='MWt', type='NUMBER', group='Receiver', required='*')
    Q_loss_hdr_rnr_des_SS: Final[float] = OUTPUT(label='Steady State field heat loss from headers and runners', units='MWt', type='NUMBER', group='Receiver', required='*')
    DP_pressure_loss: Final[float] = OUTPUT(label='Total loop pressure loss at design', units='bar', type='NUMBER', group='Receiver', required='*')
    avg_dt_des: Final[float] = OUTPUT(label='Average field temp difference at design', units='C', type='NUMBER', group='Receiver', required='*')
    hl_des: Final[float] = OUTPUT(label='Heat loss at design', units='W/m', type='NUMBER', group='Receiver', required='*')
    opt_derate: Final[float] = OUTPUT(label='Receiver optical derate', type='NUMBER', group='Receiver', required='*')
    opt_normal: Final[float] = OUTPUT(label='Collector optical loss at normal incidence', type='NUMBER', group='Receiver', required='*')
    q_dot_cycle_des: Final[float] = OUTPUT(label='PC thermal input at design', units='MWt', type='NUMBER', group='Power Cycle', required='*')
    mdot_cycle_des: Final[float] = OUTPUT(label='PC mass flow rate at design', units='kg/s', type='NUMBER', group='Power Cycle', required='*')
    vol_tank: Final[float] = OUTPUT(label='Total tank volume', units='m3', type='NUMBER', group='Power Cycle', required='*')
    Q_tes_des: Final[float] = OUTPUT(label='TES design capacity', units='MWt-hr', type='NUMBER', group='Power Cycle', required='*')
    d_tank: Final[float] = OUTPUT(label='Tank diameter', units='m', type='NUMBER', group='Power Cycle', required='*')
    vol_min: Final[float] = OUTPUT(label='Minimum Fluid Volume', units='m3', type='NUMBER', group='Power Cycle', required='*')
    q_dot_loss_tes_des: Final[float] = OUTPUT(label='Estimated TES Heat Loss', units='MW', type='NUMBER', group='Power Cycle', required='*')
    tes_htf_min_temp: Final[float] = OUTPUT(label='Minimum storage htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    tes_htf_max_temp: Final[float] = OUTPUT(label='Maximum storage htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    tes_htf_dens: Final[float] = OUTPUT(label='Storage htf density', units='kg/m3', type='NUMBER', group='Power Cycle', required='*')
    tes_htf_cp: Final[float] = OUTPUT(label='Storage htf specific heat', units='kJ/kg-K', type='NUMBER', group='Power Cycle', required='*')
    W_dot_bop_design: Final[float] = OUTPUT(label='BOP parasitics at design', units='MWe', type='NUMBER', group='Power Cycle', required='*')
    W_dot_fixed: Final[float] = OUTPUT(label='Fixed parasitic at design', units='MWe', type='NUMBER', group='Power Cycle', required='*')
    aux_design: Final[float] = OUTPUT(label='Aux parasitics at design', units='MWe', type='NUMBER', group='System Control', required='*')
    site_improvements_cost: Final[float] = OUTPUT(label='Site improvements cost', units='$', type='NUMBER', group='Capital Costs')
    solar_field_cost: Final[float] = OUTPUT(label='Solar field cost', units='$', type='NUMBER', group='Capital Costs')
    htf_system_cost: Final[float] = OUTPUT(label='HTF system cost', units='$', type='NUMBER', group='Capital Costs')
    ts_cost: Final[float] = OUTPUT(label='Thermal storage cost', units='$', type='NUMBER', group='Capital Costs')
    fossil_backup_cost: Final[float] = OUTPUT(label='Fossil backup cost', units='$', type='NUMBER', group='Capital Costs')
    power_plant_cost: Final[float] = OUTPUT(label='Power plant cost', units='$', type='NUMBER', group='Capital Costs')
    bop_cost: Final[float] = OUTPUT(label='Balance of plant cost', units='$', type='NUMBER', group='Capital Costs')
    contingency_cost: Final[float] = OUTPUT(label='Contingency cost', units='$', type='NUMBER', group='Capital Costs')
    total_direct_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    epc_total_cost: Final[float] = OUTPUT(label='EPC total cost', units='$', type='NUMBER', group='Capital Costs')
    plm_total_cost: Final[float] = OUTPUT(label='Total land cost', units='$', type='NUMBER', group='Capital Costs')
    total_indirect_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    sales_tax_total: Final[float] = OUTPUT(label='Sales tax total', units='$', type='NUMBER', group='Capital Costs')
    total_installed_cost: Final[float] = OUTPUT(label='Total installed cost', units='$', type='NUMBER', group='Capital Costs')
    installed_per_capacity: Final[float] = OUTPUT(label='Estimated total installed cost per net capacity ($/kW)', units='$/kW', type='NUMBER', group='Capital Costs')
    const_per_principal1: Final[float] = OUTPUT(label='Principal, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_principal2: Final[float] = OUTPUT(label='Principal, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_principal3: Final[float] = OUTPUT(label='Principal, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_principal4: Final[float] = OUTPUT(label='Principal, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_principal5: Final[float] = OUTPUT(label='Principal, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest1: Final[float] = OUTPUT(label='Interest cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest2: Final[float] = OUTPUT(label='Interest cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest3: Final[float] = OUTPUT(label='Interest cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest4: Final[float] = OUTPUT(label='Interest cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest5: Final[float] = OUTPUT(label='Interest cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_total1: Final[float] = OUTPUT(label='Total financing cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_total2: Final[float] = OUTPUT(label='Total financing cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_total3: Final[float] = OUTPUT(label='Total financing cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_total4: Final[float] = OUTPUT(label='Total financing cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_total5: Final[float] = OUTPUT(label='Total financing cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_percent_total: Final[float] = OUTPUT(label='Total percent of installed costs, all loans', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_principal_total: Final[float] = OUTPUT(label='Total principal, all loans', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    const_per_interest_total: Final[float] = OUTPUT(label='Total interest costs, all loans', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    construction_financing_cost: Final[float] = OUTPUT(label='Total construction financing cost', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model<5|csp_financial_model=6')
    time_hr: Final[Array] = OUTPUT(label='Time at end of timestep', units='hr', type='ARRAY', group='solver', required='sim_type=1')
    month: Final[Array] = OUTPUT(label='Resource Month', type='ARRAY', group='weather', required='sim_type=1')
    hour_day: Final[Array] = OUTPUT(label='Resource Hour of Day', type='ARRAY', group='weather', required='sim_type=1')
    solazi: Final[Array] = OUTPUT(label='Resource Solar Azimuth', units='deg', type='ARRAY', group='weather', required='sim_type=1')
    solzen: Final[Array] = OUTPUT(label='Resource Solar Zenith', units='deg', type='ARRAY', group='weather', required='sim_type=1')
    beam: Final[Array] = OUTPUT(label='Resource Beam normal irradiance', units='W/m2', type='ARRAY', group='weather', required='sim_type=1')
    tdry: Final[Array] = OUTPUT(label='Resource Dry bulb temperature', units='C', type='ARRAY', group='weather', required='sim_type=1')
    twet: Final[Array] = OUTPUT(label='Resource Wet bulb temperature', units='C', type='ARRAY', group='weather', required='sim_type=1')
    rh: Final[Array] = OUTPUT(label='Resource Relative Humidity', units='%', type='ARRAY', group='weather', required='sim_type=1')
    wspd: Final[Array] = OUTPUT(label='Resource Wind Speed', units='m/s', type='ARRAY', group='weather', required='sim_type=1')
    pres: Final[Array] = OUTPUT(label='Resource Pressure', units='mbar', type='ARRAY', group='weather', required='sim_type=1')
    defocus: Final[Array] = OUTPUT(label='Field optical focus fraction', type='ARRAY', group='weather', required='sim_type=1')
    EqOpteff: Final[Array] = OUTPUT(label='Field optical efficiency before defocus', type='ARRAY', group='Solar_Field', required='sim_type=1')
    SCAs_def: Final[Array] = OUTPUT(label='Field fraction of focused SCAs', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_inc_sf_tot: Final[Array] = OUTPUT(label='Field thermal power incident', units='MWt', type='ARRAY', group='Solar_Field', required='*')
    q_dot_rec_inc: Final[Array] = OUTPUT(label='Receiver thermal power incident', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_rec_thermal_loss: Final[Array] = OUTPUT(label='Receiver thermal losses', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_rec_abs: Final[Array] = OUTPUT(label='Receiver thermal power absorbed', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    rec_thermal_eff: Final[Array] = OUTPUT(label='Receiver thermal efficiency', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_piping_loss: Final[Array] = OUTPUT(label='Field piping thermal losses', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    e_dot_field_int_energy: Final[Array] = OUTPUT(label='Field change in material/htf internal energy', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_htf_sf_out: Final[Array] = OUTPUT(label='Field thermal power leaving in HTF', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_freeze_prot: Final[Array] = OUTPUT(label='Field freeze protection required', units='MWt', type='ARRAY', group='Solar_Field', required='sim_type=1')
    m_dot_loop: Final[Array] = OUTPUT(label='Receiver mass flow rate', units='kg/s', type='ARRAY', group='Solar_Field', required='sim_type=1')
    m_dot_field_recirc: Final[Array] = OUTPUT(label='Field total mass flow recirculated', units='kg/s', type='ARRAY', group='Solar_Field', required='sim_type=1')
    m_dot_field_delivered: Final[Array] = OUTPUT(label='Field total mass flow delivered', units='kg/s', type='ARRAY', group='Solar_Field', required='sim_type=1')
    T_field_cold_in: Final[Array] = OUTPUT(label='Field timestep-averaged inlet temperature', units='C', type='ARRAY', group='Solar_Field', required='sim_type=1')
    T_rec_cold_in: Final[Array] = OUTPUT(label='Loop timestep-averaged inlet temperature', units='C', type='ARRAY', group='Solar_Field', required='sim_type=1')
    T_rec_hot_out: Final[Array] = OUTPUT(label='Loop timestep-averaged outlet temperature', units='C', type='ARRAY', group='Solar_Field', required='sim_type=1')
    T_field_hot_out: Final[Array] = OUTPUT(label='Field timestep-averaged outlet temperature', units='C', type='ARRAY', group='Solar_Field', required='sim_type=1')
    deltaP_field: Final[Array] = OUTPUT(label='Field pressure drop', units='bar', type='ARRAY', group='Solar_Field', required='sim_type=1')
    W_dot_sca_track: Final[Array] = OUTPUT(label='Field collector tracking power', units='MWe', type='ARRAY', group='Solar_Field', required='sim_type=1')
    W_dot_field_pump: Final[Array] = OUTPUT(label='Field htf pumping power', units='MWe', type='ARRAY', group='Solar_Field', required='sim_type=1')
    eta: Final[Array] = OUTPUT(label='PC efficiency: gross', type='ARRAY', group='powerblock', required='sim_type=1')
    q_pb: Final[Array] = OUTPUT(label='PC input energy', units='MWt', type='ARRAY', group='powerblock', required='sim_type=1')
    m_dot_pc: Final[Array] = OUTPUT(label='PC HTF mass flow rate', units='kg/s', type='ARRAY', group='powerblock', required='sim_type=1')
    q_dot_pc_startup: Final[Array] = OUTPUT(label='PC startup thermal power', units='MWt', type='ARRAY', group='powerblock', required='sim_type=1')
    P_cycle: Final[Array] = OUTPUT(label='PC electrical power output: gross', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    T_pc_in: Final[Array] = OUTPUT(label='PC HTF inlet temperature', units='C', type='ARRAY', group='powerblock', required='sim_type=1')
    T_pc_out: Final[Array] = OUTPUT(label='PC HTF outlet temperature', units='C', type='ARRAY', group='powerblock', required='sim_type=1')
    m_dot_water_pc: Final[Array] = OUTPUT(label='PC water consumption: makeup + cooling', units='kg/s', type='ARRAY', group='powerblock', required='sim_type=1')
    q_pc_startup: Final[Array] = OUTPUT(label='PC startup thermal energy', units='MWht', type='ARRAY', group='powerblock', required='sim_type=1')
    cycle_htf_pump_power: Final[Array] = OUTPUT(label='PC HTF pump power', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    P_cooling_tower_tot: Final[Array] = OUTPUT(label='Parasitic power condenser operation', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    tank_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', group='TES', required='sim_type=1')
    q_tes_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWe', type='ARRAY', group='TES', required='sim_type=1')
    T_tes_hot: Final[Array] = OUTPUT(label='TES hot temperature', units='C', type='ARRAY', group='TES', required='sim_type=1')
    T_tes_cold: Final[Array] = OUTPUT(label='TES cold temperature', units='C', type='ARRAY', group='TES', required='sim_type=1')
    mass_tes_cold: Final[Array] = OUTPUT(label='TES cold tank mass (end)', units='kg', type='ARRAY', group='TES', required='sim_type=1')
    mass_tes_hot: Final[Array] = OUTPUT(label='TES hot tank mass (end)', units='kg', type='ARRAY', group='TES', required='sim_type=1')
    q_dc_tes: Final[Array] = OUTPUT(label='TES discharge thermal power', units='MWt', type='ARRAY', group='TES', required='sim_type=1')
    q_ch_tes: Final[Array] = OUTPUT(label='TES charge thermal power', units='MWt', type='ARRAY', group='TES', required='sim_type=1')
    e_ch_tes: Final[Array] = OUTPUT(label='TES charge state', units='MWht', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_cr_to_tes_hot: Final[Array] = OUTPUT(label='Mass flow: field to hot TES', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_tes_hot_out: Final[Array] = OUTPUT(label='Mass flow: TES hot out', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_pc_to_tes_cold: Final[Array] = OUTPUT(label='Mass flow: cycle to cold TES', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_tes_cold_out: Final[Array] = OUTPUT(label='Mass flow: TES cold out', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_field_to_cycle: Final[Array] = OUTPUT(label='Mass flow: field to cycle', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_cycle_to_field: Final[Array] = OUTPUT(label='Mass flow: cycle to field', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    m_dot_cold_tank_to_hot_tank: Final[Array] = OUTPUT(label='Mass flow: cold tank to hot tank', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    tes_htf_pump_power: Final[Array] = OUTPUT(label='TES HTF pump power', units='MWe', type='ARRAY', group='TES', required='sim_type=1')
    op_mode_1: Final[Array] = OUTPUT(label='1st operating mode', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_2: Final[Array] = OUTPUT(label='2nd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_3: Final[Array] = OUTPUT(label='3rd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    m_dot_balance: Final[Array] = OUTPUT(label='Relative mass flow balance error', type='ARRAY', group='solver', required='sim_type=1')
    q_balance: Final[Array] = OUTPUT(label='Relative energy balance error', type='ARRAY', group='solver', required='sim_type=1')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly AC energy in Year 1', units='kWh', type='ARRAY', group='Post-process', required='sim_type=1', constraints='LENGTH=12')
    annual_energy: Final[float] = OUTPUT(label='Annual net electrical energy w/ avail. derate', units='kWhe', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_thermal_consumption: Final[float] = OUTPUT(label='Annual thermal freeze protection required', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_total_water_use: Final[float] = OUTPUT(label='Total annual water usage', units='m^3', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_field_freeze_protection: Final[float] = OUTPUT(label='Annual thermal power for field freeze protection', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_tes_freeze_protection: Final[float] = OUTPUT(label='Annual thermal power for TES freeze protection', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    n_op_modes: Final[Array] = OUTPUT(label='Operating modes in reporting timestep', type='ARRAY', group='solver', required='sim_type=1')
    tou_value: Final[Array] = OUTPUT(label='CSP operating Time-of-use value', type='ARRAY', group='solver', required='sim_type=1')
    pricing_mult: Final[Array] = OUTPUT(label='PPA price multiplier', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_sb: Final[Array] = OUTPUT(label='Thermal power for PC standby', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_min: Final[Array] = OUTPUT(label='Thermal power for PC min operation', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_target: Final[Array] = OUTPUT(label='Target thermal power to PC', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_max: Final[Array] = OUTPUT(label='Max thermal power to PC', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    is_rec_su_allowed: Final[Array] = OUTPUT(label='is receiver startup allowed', type='ARRAY', group='solver', required='sim_type=1')
    is_pc_su_allowed: Final[Array] = OUTPUT(label='is power cycle startup allowed', type='ARRAY', group='solver', required='sim_type=1')
    is_pc_sb_allowed: Final[Array] = OUTPUT(label='is power cycle standby allowed', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_est_cr_su: Final[Array] = OUTPUT(label='Estimate rec. startup thermal power', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_est_cr_on: Final[Array] = OUTPUT(label='Estimate rec. thermal power TO HTF', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_est_tes_dc: Final[Array] = OUTPUT(label='Estimate max TES discharge thermal power', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_est_tes_ch: Final[Array] = OUTPUT(label='Estimate max TES charge thermal power', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    operating_modes_a: Final[Array] = OUTPUT(label='First 3 operating modes tried', type='ARRAY', group='solver', required='sim_type=1')
    operating_modes_b: Final[Array] = OUTPUT(label='Next 3 operating modes tried', type='ARRAY', group='solver', required='sim_type=1')
    operating_modes_c: Final[Array] = OUTPUT(label='Final 3 operating modes tried', type='ARRAY', group='solver', required='sim_type=1')
    disp_rel_mip_gap: Final[Array] = OUTPUT(label='Dispatch relative MIP gap', type='ARRAY', group='tou', required='sim_type=1')
    disp_solve_state: Final[Array] = OUTPUT(label='Dispatch solver state', type='ARRAY', group='tou', required='sim_type=1')
    disp_subopt_flag: Final[Array] = OUTPUT(label='Dispatch suboptimal solution flag', type='ARRAY', group='tou', required='sim_type=1')
    disp_solve_iter: Final[Array] = OUTPUT(label='Dispatch iterations count', type='ARRAY', group='tou', required='sim_type=1')
    disp_objective: Final[Array] = OUTPUT(label='Dispatch objective function value', type='ARRAY', group='tou', required='sim_type=1')
    disp_obj_relax: Final[Array] = OUTPUT(label='Dispatch objective function - relaxed max', type='ARRAY', group='tou', required='sim_type=1')
    disp_qsf_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field available energy', units='MWt', type='ARRAY', group='tou', required='sim_type=1')
    disp_qsfprod_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field generation', units='MWt', type='ARRAY', group='tou', required='sim_type=1')
    disp_qsfsu_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field startup enegy', units='MWt', type='ARRAY', group='tou', required='sim_type=1')
    disp_tes_expected: Final[Array] = OUTPUT(label='Dispatch expected TES charge level', units='MWht', type='ARRAY', group='tou', required='sim_type=1')
    disp_pceff_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle efficiency adj.', type='ARRAY', group='tou', required='sim_type=1')
    disp_thermeff_expected: Final[Array] = OUTPUT(label='Dispatch expected SF thermal efficiency adj.', type='ARRAY', group='tou', required='sim_type=1')
    disp_qpbsu_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle startup energy', units='MWht', type='ARRAY', group='tou', required='sim_type=1')
    disp_wpb_expected: Final[Array] = OUTPUT(label='Dispatch expected power generation', units='MWe', type='ARRAY', group='tou', required='sim_type=1')
    disp_rev_expected: Final[Array] = OUTPUT(label='Dispatch expected revenue factor', type='ARRAY', group='tou', required='sim_type=1')
    disp_presolve_nconstr: Final[Array] = OUTPUT(label='Dispatch number of constraints in problem', type='ARRAY', group='tou', required='sim_type=1')
    disp_presolve_nvar: Final[Array] = OUTPUT(label='Dispatch number of variables in problem', type='ARRAY', group='tou', required='sim_type=1')
    disp_solve_time: Final[Array] = OUTPUT(label='Dispatch solver time', units='sec', type='ARRAY', group='tou', required='sim_type=1')
    avg_suboptimal_rel_mip_gap: Final[float] = OUTPUT(label='Average suboptimal relative MIP gap', units='%', type='NUMBER', group='tou', required='sim_type=1')
    P_fixed: Final[Array] = OUTPUT(label='Parasitic power fixed load', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    P_plant_balance_tot: Final[Array] = OUTPUT(label='Parasitic power generation-dependent load', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    P_out_net: Final[Array] = OUTPUT(label='System net electrical power', units='MWe', type='ARRAY', group='system', required='*')
    gen: Final[Array] = OUTPUT(label='System net electrical power w/ avail. derate', units='kWe', type='ARRAY', group='system', required='sim_type=1')
    annual_W_cycle_gross: Final[float] = OUTPUT(label='Electrical source - Power cycle gross output', units='kWhe', type='NUMBER', group='system', required='sim_type=1')
    conversion_factor: Final[float] = OUTPUT(label='Gross to Net Conversion Factor', units='%', type='NUMBER', group='system', required='sim_type=1')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='system', required='sim_type=1')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', group='system', required='sim_type=1')
    sim_duration: Final[float] = OUTPUT(label='Computational time of timeseries simulation', units='s', type='NUMBER', group='system', required='sim_type=1')
    recirculating: Final[Array] = OUTPUT(label='Field recirculating (bypass valve open)', units='-', type='ARRAY', group='Solar_Field', required='sim_type=1')
    pipe_tes_diams: Final[Array] = OUTPUT(label='Pipe diameters in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_wallthk: Final[Array] = OUTPUT(label='Pipe wall thickness in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_lengths: Final[Array] = OUTPUT(label='Pipe lengths in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_mdot_dsn: Final[Array] = OUTPUT(label='Mass flow TES pipes at design conditions', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_vel_dsn: Final[Array] = OUTPUT(label='Velocity in TES pipes at design conditions', units='m/s', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_T_dsn: Final[Array] = OUTPUT(label='Temperature in TES pipes at design conditions', units='C', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_P_dsn: Final[Array] = OUTPUT(label='Pressure in TES pipes at design conditions', units='bar', type='ARRAY', group='TES', required='sim_type=1')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")

    def __init__(self, *args: Mapping[str, Any],
                 sim_type: float = ...,
                 file_name: str = ...,
                 solar_mult_in: float = ...,
                 total_Ap_in: float = ...,
                 solar_mult_or_Ap: float = ...,
                 T_loop_in_des: float = ...,
                 T_loop_out: float = ...,
                 I_bn_des: float = ...,
                 P_ref: float = ...,
                 eta_ref: float = ...,
                 tshours: float = ...,
                 gross_net_conversion_factor: float = ...,
                 nMod: float = ...,
                 eta_pump: float = ...,
                 HDR_rough: float = ...,
                 theta_stow: float = ...,
                 theta_dep: float = ...,
                 FieldConfig: float = ...,
                 Fluid: float = ...,
                 T_fp: float = ...,
                 V_hdr_max: float = ...,
                 V_hdr_min: float = ...,
                 Pipe_hl_coef: float = ...,
                 mc_bal_hot: float = ...,
                 mc_bal_cold: float = ...,
                 mc_bal_sca: float = ...,
                 water_per_wash: float = ...,
                 washes_per_year: float = ...,
                 rec_htf_vol: float = ...,
                 T_amb_sf_des: float = ...,
                 V_wind_des: float = ...,
                 field_fl_props: Matrix = ...,
                 SCA_drives_elec: float = ...,
                 land_mult: float = ...,
                 T_startup: float = ...,
                 p_start: float = ...,
                 L_rnr_pb: float = ...,
                 use_abs_or_rel_mdot_limit: float = ...,
                 m_dot_htfmin: float = ...,
                 m_dot_htfmax: float = ...,
                 f_htfmin: float = ...,
                 f_htfmax: float = ...,
                 ColAz: float = ...,
                 opt_model: float = ...,
                 A_aperture: float = ...,
                 reflectivity: float = ...,
                 TrackingError: float = ...,
                 GeomEffects: float = ...,
                 Dirt_mirror: float = ...,
                 Error: float = ...,
                 L_mod: float = ...,
                 IAM_T_coefs: Array = ...,
                 IAM_L_coefs: Array = ...,
                 OpticalTable: Matrix = ...,
                 rec_model: float = ...,
                 HCE_FieldFrac: Array = ...,
                 D_abs_in: Array = ...,
                 D_abs_out: Array = ...,
                 D_glass_in: Array = ...,
                 D_glass_out: Array = ...,
                 D_plug: Array = ...,
                 Flow_type: Array = ...,
                 Rough: Array = ...,
                 alpha_env: Array = ...,
                 epsilon_abs_1: Matrix = ...,
                 epsilon_abs_2: Matrix = ...,
                 epsilon_abs_3: Matrix = ...,
                 epsilon_abs_4: Matrix = ...,
                 alpha_abs: Array = ...,
                 Tau_envelope: Array = ...,
                 epsilon_glass: Array = ...,
                 GlazingIntactIn: Array = ...,
                 P_a: Array = ...,
                 AnnulusGas: Array = ...,
                 AbsorberMaterial: Array = ...,
                 Shadowing: Array = ...,
                 dirt_env: Array = ...,
                 Design_loss: Array = ...,
                 L_mod_spacing: float = ...,
                 L_crossover: float = ...,
                 HL_T_coefs: Array = ...,
                 HL_w_coefs: Array = ...,
                 DP_nominal: float = ...,
                 DP_coefs: Array = ...,
                 nRecVar: float = ...,
                 startup_time: float = ...,
                 startup_frac: float = ...,
                 q_sby_frac: float = ...,
                 pb_pump_coef: float = ...,
                 cycle_max_frac: float = ...,
                 cycle_cutoff_frac: float = ...,
                 pc_config: float = ...,
                 dT_cw_ref: float = ...,
                 T_amb_des: float = ...,
                 CT: float = ...,
                 T_approach: float = ...,
                 T_ITD_des: float = ...,
                 P_cond_ratio: float = ...,
                 pb_bd_frac: float = ...,
                 P_cond_min: float = ...,
                 n_pl_inc: float = ...,
                 F_wc: Array = ...,
                 tech_type: float = ...,
                 DP_SGS: float = ...,
                 ud_f_W_dot_cool_des: float = ...,
                 ud_m_dot_water_cool_des: float = ...,
                 ud_is_sco2_regr: float = ...,
                 ud_ind_od: Matrix = ...,
                 store_fluid: float = ...,
                 store_fl_props: Matrix = ...,
                 h_tank: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 cold_tank_Thtr: float = ...,
                 cold_tank_max_heat: float = ...,
                 dt_hot: float = ...,
                 h_tank_min: float = ...,
                 dt_cold: float = ...,
                 init_hot_htf_percent: float = ...,
                 tes_pump_coef: float = ...,
                 tanks_in_parallel: float = ...,
                 V_tes_des: float = ...,
                 is_timestep_load_fractions: float = ...,
                 timestep_load_fractions: Array = ...,
                 pb_fixed_par: float = ...,
                 bop_array: Array = ...,
                 aux_array: Array = ...,
                 is_dispatch: float = ...,
                 disp_frequency: float = ...,
                 disp_horizon: float = ...,
                 disp_max_iter: float = ...,
                 disp_timeout: float = ...,
                 disp_mip_gap: float = ...,
                 disp_time_weighting: float = ...,
                 disp_rsu_cost_rel: float = ...,
                 disp_csu_cost_rel: float = ...,
                 disp_pen_ramping: float = ...,
                 can_cycle_use_standby: float = ...,
                 disp_steps_per_hour: float = ...,
                 disp_spec_presolve: float = ...,
                 disp_spec_bb: float = ...,
                 disp_reporting: float = ...,
                 disp_spec_scaling: float = ...,
                 disp_inventory_incentive: float = ...,
                 q_rec_standby: float = ...,
                 q_rec_heattrace: float = ...,
                 rec_su_delay: float = ...,
                 rec_qf_delay: float = ...,
                 csp_financial_model: float = ...,
                 weekday_schedule: Matrix = ...,
                 weekend_schedule: Matrix = ...,
                 is_tod_pc_target_also_pc_max: float = ...,
                 f_turb_tou_periods: Array = ...,
                 en_electricity_rates: float = ...,
                 ppa_multiplier_model: float = ...,
                 dispatch_factors_ts: Array = ...,
                 dispatch_sched_weekday: Matrix = ...,
                 dispatch_sched_weekend: Matrix = ...,
                 dispatch_tod_factors: Array = ...,
                 ppa_soln_mode: float = ...,
                 ppa_price_input: Array = ...,
                 mp_energy_market_revenue: Matrix = ...,
                 site_improvements_spec_cost: float = ...,
                 solar_field_spec_cost: float = ...,
                 htf_system_spec_cost: float = ...,
                 storage_spec_cost: float = ...,
                 fossil_spec_cost: float = ...,
                 power_plant_spec_cost: float = ...,
                 bop_spec_cost: float = ...,
                 contingency_percent: float = ...,
                 epc_cost_per_acre: float = ...,
                 epc_cost_percent_direct: float = ...,
                 epc_cost_per_watt: float = ...,
                 epc_cost_fixed: float = ...,
                 plm_cost_per_acre: float = ...,
                 plm_cost_percent_direct: float = ...,
                 plm_cost_per_watt: float = ...,
                 plm_cost_fixed: float = ...,
                 sales_tax_percent: float = ...,
                 sales_tax_rate: float = ...,
                 const_per_interest_rate1: float = ...,
                 const_per_interest_rate2: float = ...,
                 const_per_interest_rate3: float = ...,
                 const_per_interest_rate4: float = ...,
                 const_per_interest_rate5: float = ...,
                 const_per_months1: float = ...,
                 const_per_months2: float = ...,
                 const_per_months3: float = ...,
                 const_per_months4: float = ...,
                 const_per_months5: float = ...,
                 const_per_percent1: float = ...,
                 const_per_percent2: float = ...,
                 const_per_percent3: float = ...,
                 const_per_percent4: float = ...,
                 const_per_percent5: float = ...,
                 const_per_upfront_rate1: float = ...,
                 const_per_upfront_rate2: float = ...,
                 const_per_upfront_rate3: float = ...,
                 const_per_upfront_rate4: float = ...,
                 const_per_upfront_rate5: float = ...,
                 adjust_constant: float = ...,
                 adjust_en_timeindex: float = ...,
                 adjust_en_periods: float = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
