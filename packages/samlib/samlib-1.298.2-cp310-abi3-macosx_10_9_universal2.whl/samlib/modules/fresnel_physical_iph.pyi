
# This is a generated file

"""fresnel_physical_iph - Physical Fresnel IPH applications"""

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
    'tshours': float,
    'q_pb_design': float,
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
    'rec_su_delay': float,
    'rec_qf_delay': float,
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
    'pb_pump_coef': float,
    'hs_type': float,
    'hs_phys_N_sub': float,
    'hs_phys_tol': float,
    'hs_phys_f_mdot_steam_min': float,
    'hs_phys_f_mdot_steam_max': float,
    'hs_phys_T_steam_cold_des': float,
    'hs_phys_P_steam_hot_des': float,
    'hs_phys_Q_steam_hot_des': float,
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
    'weekday_schedule': Matrix,
    'weekend_schedule': Matrix,
    'f_turb_tou_periods': Array,
    'timestep_load_abs': Array,
    'timestep_load_abs_factor': float,
    'is_tod_pc_target_also_pc_max': float,
    'pb_fixed_par': float,
    'bop_array': Array,
    'aux_array': Array,
    'is_dispatch': float,
    'disp_rsu_cost_rel': float,
    'disp_horizon': float,
    'disp_frequency': float,
    'disp_max_iter': float,
    'disp_timeout': float,
    'disp_mip_gap': float,
    'disp_time_weighting': float,
    'disp_steps_per_hour': float,
    'disp_spec_presolve': float,
    'disp_spec_bb': float,
    'disp_reporting': float,
    'disp_spec_scaling': float,
    'disp_inventory_incentive': float,
    'q_rec_heattrace': float,
    'q_rec_standby': float,
    'csp_financial_model': float,
    'ppa_multiplier_model': float,
    'ppa_soln_mode': float,
    'dispatch_factors_ts': Array,
    'dispatch_sched_weekday': Matrix,
    'dispatch_sched_weekend': Matrix,
    'dispatch_tod_factors': Array,
    'ppa_price_input_heat_btu': Array,
    'site_improvements_spec_cost': float,
    'solar_field_spec_cost': float,
    'htf_system_spec_cost': float,
    'storage_spec_cost': float,
    'heat_sink_spec_cost': float,
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
    'nameplate': float,
    'cp_system_nameplate': float,
    'cp_battery_nameplate': float,
    'solar_mult': float,
    'total_Ap': float,
    'nLoops': float,
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
    'm_dot_htfmin_actual': float,
    'm_dot_htfmax_actual': float,
    'f_htfmin_actual': float,
    'f_htfmax_actual': float,
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
    'timestep_load_fractions_calc': Array,
    'timestep_load_abs_calc': Array,
    'thermal_load_heat_btu': Array,
    'site_improvements_cost': float,
    'solar_field_cost': float,
    'htf_system_cost': float,
    'ts_cost': float,
    'heat_sink_cost': float,
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
    'ppa_price_input': Array,
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
    'recirculating': Array,
    'q_dot_to_heat_sink': Array,
    'W_dot_pc_pump': Array,
    'm_dot_htf_heat_sink': Array,
    'T_heat_sink_in': Array,
    'T_heat_sink_out': Array,
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
    'pipe_tes_diams': Array,
    'pipe_tes_wallthk': Array,
    'pipe_tes_lengths': Array,
    'pipe_tes_mdot_dsn': Array,
    'pipe_tes_vel_dsn': Array,
    'pipe_tes_T_dsn': Array,
    'pipe_tes_P_dsn': Array,
    'P_fixed': Array,
    'P_plant_balance_tot': Array,
    'W_dot_parasitic_tot': Array,
    'tou_value': Array,
    'pricing_mult': Array,
    'n_op_modes': Array,
    'op_mode_1': Array,
    'op_mode_2': Array,
    'op_mode_3': Array,
    'm_dot_balance': Array,
    'q_balance': Array,
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
    'q_dot_pc_sb': Array,
    'q_dot_pc_min': Array,
    'q_dot_pc_max': Array,
    'q_dot_pc_target': Array,
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
    'gen_heat': Array,
    'gen': Array,
    'gen_heat_btu': Array,
    'monthly_energy': Array,
    'monthly_energy_heat_btu': Array,
    'annual_energy': float,
    'annual_energy_heat_btu': float,
    'annual_thermal_consumption': float,
    'annual_electricity_consumption': float,
    'annual_total_water_use': float,
    'annual_field_freeze_protection': float,
    'annual_tes_freeze_protection': float,
    'capacity_factor': float,
    'kwh_per_kw': float,
    'sim_duration': float,
    'W_dot_par_tot_haf': float,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix,
    'annual_energy_distribution_time': Matrix,
    'en_electricity_rates': float,
    'inflation_rate': float,
    'rate_escalation': Array,
    'ur_metering_option': float,
    'ur_nm_yearend_sell_rate': float,
    'ur_nm_credit_month': float,
    'ur_nm_credit_rollover': float,
    'ur_monthly_fixed_charge': float,
    'ur_nb_credit_expire': float,
    'ur_nb_apply_credit_current_month': float,
    'ur_sell_eq_buy': float,
    'ur_monthly_min_charge': float,
    'ur_annual_min_charge': float,
    'ur_en_ts_sell_rate': float,
    'ur_ts_sell_rate': Array,
    'ur_en_ts_buy_rate': float,
    'ur_ts_buy_rate': Array,
    'ur_ec_sched_weekday': Matrix,
    'ur_ec_sched_weekend': Matrix,
    'ur_ec_tou_mat': Matrix,
    'ur_dc_enable': float,
    'ur_dc_sched_weekday': Matrix,
    'ur_dc_sched_weekend': Matrix,
    'ur_dc_tou_mat': Matrix,
    'ur_dc_flat_mat': Matrix,
    'ur_enable_billing_demand': float,
    'ur_billing_demand_minimum': float,
    'ur_billing_demand_lookback_period': float,
    'ur_billing_demand_lookback_percentages': Matrix,
    'ur_dc_billing_demand_periods': Matrix,
    'ur_yearzero_usage_peaks': Array
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
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='System_Design', required='*')
    q_pb_design: float = INPUT(label='Design heat input to power block', units='MWt', type='NUMBER', group='System_Design', required='*')
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
    rec_su_delay: float = INPUT(label='Fixed startup delay time for the receiver', units='hr', type='NUMBER', group='Solar_Field', required='*')
    rec_qf_delay: float = INPUT(label='Energy-based receiver startup delay (fraction of rated thermal power)', units='-', type='NUMBER', group='Solar_Field', required='*')
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
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='Heat Sink', required='*')
    hs_type: float = INPUT(label='0: ideal model, 1: physical steam model', type='NUMBER', group='Heat Sink', required='?=0')
    hs_phys_N_sub: float = INPUT(label='Number physical heat sink HX nodes', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_tol: float = INPUT(label='Physical heat sink solve tolerance', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_f_mdot_steam_min: float = INPUT(label='Min steam mdot fraction for physical heat sink', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_f_mdot_steam_max: float = INPUT(label='Max steam mdot fraction for physical heat sink', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_T_steam_cold_des: float = INPUT(label='Steam inlet temperature for physical heat sink', units='C', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_P_steam_hot_des: float = INPUT(label='Steam outlet (and inlet) pressure for physical heat sink', units='bar', type='NUMBER', group='Heat Sink', required='hs_type=1')
    hs_phys_Q_steam_hot_des: float = INPUT(label='Steam outlet quality for physical heat sink', type='NUMBER', group='Heat Sink', required='hs_type=1')
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
    is_timestep_load_fractions: float = INPUT(label='0: block dispatch, 1: hourly load fraction, 2: absolute load', type='NUMBER', group='tou', required='?=0')
    timestep_load_fractions: Array = INPUT(label='Turbine load fraction for each timestep, alternative to block dispatch', type='ARRAY', group='tou', required='is_timestep_load_fractions=1')
    weekday_schedule: Matrix = INPUT(label='12x24 Time of Use Values for week days', type='MATRIX', group='tou', required='is_timestep_load_fractions=0')
    weekend_schedule: Matrix = INPUT(label='12x24 Time of Use Values for week end days', type='MATRIX', group='tou', required='is_timestep_load_fractions=0')
    f_turb_tou_periods: Array = INPUT(label='Dispatch logic for turbine load fraction', units='-', type='ARRAY', group='tou', required='is_timestep_load_fractions=0')
    timestep_load_abs: Array = INPUT(label='Heat sink hourly load (not normalized)', units='kWt', type='ARRAY', group='tou', required='is_timestep_load_fractions=2')
    timestep_load_abs_factor: float = INPUT(label='Heat sink hourly load scale factor', type='NUMBER', group='tou', required='?=1')
    is_tod_pc_target_also_pc_max: float = INPUT(label='Is the TOD target cycle heat input also the max cycle heat input?', type='NUMBER', group='tou', required='?=0')
    pb_fixed_par: float = INPUT(label='Fixed parasitic load - runs at all times', type='NUMBER', group='Sys_Control', required='*')
    bop_array: Array = INPUT(label='Balance of plant parasitic power fraction', type='ARRAY', group='Sys_Control', required='*')
    aux_array: Array = INPUT(label='Aux heater, boiler parasitic', type='ARRAY', group='Sys_Control', required='*')
    is_dispatch: float = INPUT(label='Allow dispatch optimization?', units='-', type='NUMBER', group='Sys_Control', required='?=0')
    disp_rsu_cost_rel: float = INPUT(label='Receiver startup cost', units='$/MWt/start', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_horizon: float = INPUT(label='Time horizon for dispatch optimization', units='hour', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_frequency: float = INPUT(label='Frequency for dispatch optimization calculations', units='hour', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_max_iter: float = INPUT(label='Max. no. dispatch optimization iterations', units='-', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_timeout: float = INPUT(label='Max. dispatch optimization solve duration', units='s', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_mip_gap: float = INPUT(label='Dispatch optimization solution tolerance', units='-', type='NUMBER', group='Sys_Control', required='is_dispatch=1')
    disp_time_weighting: float = INPUT(label='Dispatch optimization future time discounting factor', units='-', type='NUMBER', group='Sys_Control', required='?=0.99')
    disp_steps_per_hour: float = INPUT(label='Time steps per hour for dispatch optimization calculations', units='-', type='NUMBER', group='tou', required='?=1')
    disp_spec_presolve: float = INPUT(label='Dispatch optimization presolve heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_bb: float = INPUT(label='Dispatch optimization B&B heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_reporting: float = INPUT(label='Dispatch optimization reporting level', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_scaling: float = INPUT(label='Dispatch optimization scaling heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_inventory_incentive: float = INPUT(label='Dispatch storage terminal inventory incentive multiplier', type='NUMBER', group='System Control', required='?=0.0')
    q_rec_heattrace: float = INPUT(label='Receiver heat trace energy consumption during startup', units='kWhe', type='NUMBER', group='tou', required='?=0.0')
    q_rec_standby: float = INPUT(label='Receiver standby energy consumption', units='kWt', type='NUMBER', group='tou', required='?=9e99')
    csp_financial_model: float = INPUT(units='1-8', type='NUMBER', group='Financial Model', required='*', constraints='INTEGER,MIN=0')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model 0: dispatch factors dispatch_factorX, 1: hourly multipliers dispatch_factors_ts', units='0/1', type='NUMBER', group='tou', required='?=0', constraints='INTEGER,MIN=0')
    ppa_soln_mode: float = INPUT(label='PPA solution mode (0=Specify IRR target, 1=Specify PPA price)', type='NUMBER', group='Financial Solution Mode', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor array', type='ARRAY', group='tou', required='ppa_multiplier_model=1&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekday: Matrix = INPUT(label='PPA pricing weekday schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekend: Matrix = INPUT(label='PPA pricing weekend schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_tod_factors: Array = INPUT(label='TOD factors for periods 1 through 9', type='ARRAY', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    ppa_price_input_heat_btu: Array = INPUT(label='PPA prices - yearly', units='$/MMBtu', type='ARRAY', group='Revenue', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
    site_improvements_spec_cost: float = INPUT(label='Site Improvement Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    solar_field_spec_cost: float = INPUT(label='Solar Field Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    htf_system_spec_cost: float = INPUT(label='HTF System Cost Per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    storage_spec_cost: float = INPUT(label='Storage cost per kWht', units='$/kWht', type='NUMBER', group='Capital_Costs', required='?=0')
    heat_sink_spec_cost: float = INPUT(label='Heat Sink Cost per kWt', units='$/kWt', type='NUMBER', group='Capital_Costs', required='?=0')
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
    const_per_interest_rate1: float = INPUT(label='Interest rate, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest_rate2: float = INPUT(label='Interest rate, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest_rate3: float = INPUT(label='Interest rate, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest_rate4: float = INPUT(label='Interest rate, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest_rate5: float = INPUT(label='Interest rate, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_months1: float = INPUT(label='Months prior to operation, loan 1', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_months2: float = INPUT(label='Months prior to operation, loan 2', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_months3: float = INPUT(label='Months prior to operation, loan 3', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_months4: float = INPUT(label='Months prior to operation, loan 4', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_months5: float = INPUT(label='Months prior to operation, loan 5', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent1: float = INPUT(label='Percent of total installed cost, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent2: float = INPUT(label='Percent of total installed cost, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent3: float = INPUT(label='Percent of total installed cost, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent4: float = INPUT(label='Percent of total installed cost, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent5: float = INPUT(label='Percent of total installed cost, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_upfront_rate1: float = INPUT(label='Upfront fee on principal, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_upfront_rate2: float = INPUT(label='Upfront fee on principal, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_upfront_rate3: float = INPUT(label='Upfront fee on principal, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_upfront_rate4: float = INPUT(label='Upfront fee on principal, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_upfront_rate5: float = INPUT(label='Upfront fee on principal, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    system_capacity: Final[float] = OUTPUT(label='System capacity', units='kWt', type='NUMBER', group='System Design', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity', units='MWt', type='NUMBER', group='System Design Calc', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWt', type='NUMBER', group='System Design', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWt', type='NUMBER', group='System Design', required='*')
    solar_mult: Final[float] = OUTPUT(label='Actual solar multiple', type='NUMBER', group='System Design Calc', required='*')
    total_Ap: Final[float] = OUTPUT(label='Actual field aperture', units='m2', type='NUMBER', group='System Design Calc', required='*')
    nLoops: Final[float] = OUTPUT(label='Number of loops in the field', type='NUMBER', group='controller', required='*')
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
    m_dot_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='*')
    m_dot_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop HTF flow rate', units='kg/s', type='NUMBER', group='Solar_Field', required='*')
    f_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='*')
    f_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop mass flow rate fraction of design', type='NUMBER', group='Solar_Field', required='*')
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
    vol_tank: Final[float] = OUTPUT(label='Total tank volume', units='m3', type='NUMBER', group='Power Cycle', required='*')
    Q_tes_des: Final[float] = OUTPUT(label='TES design capacity', units='MWht', type='NUMBER', group='Power Cycle', required='*')
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
    timestep_load_fractions_calc: Final[Array] = OUTPUT(label='Calculated timestep load fractions', type='ARRAY', group='System Control', required='*')
    timestep_load_abs_calc: Final[Array] = OUTPUT(label='Calculated timestep load data', units='kWt', type='ARRAY', group='System Control', required='*')
    thermal_load_heat_btu: Final[Array] = OUTPUT(label='Thermal load (year 1)', units='MMBtu/hr', type='ARRAY', group='Thermal Rate', required='csp_financial_model=5')
    site_improvements_cost: Final[float] = OUTPUT(label='Site improvements cost', units='$', type='NUMBER', group='Capital Costs')
    solar_field_cost: Final[float] = OUTPUT(label='Solar field cost', units='$', type='NUMBER', group='Capital Costs')
    htf_system_cost: Final[float] = OUTPUT(label='HTF system cost', units='$', type='NUMBER', group='Capital Costs')
    ts_cost: Final[float] = OUTPUT(label='Thermal storage cost', units='$', type='NUMBER', group='Capital Costs')
    heat_sink_cost: Final[float] = OUTPUT(label='Heat sink cost', units='$', type='NUMBER', group='Capital Costs')
    bop_cost: Final[float] = OUTPUT(label='Balance of plant cost', units='$', type='NUMBER', group='Capital Costs')
    contingency_cost: Final[float] = OUTPUT(label='Contingency cost', units='$', type='NUMBER', group='Capital Costs')
    total_direct_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    epc_total_cost: Final[float] = OUTPUT(label='EPC total cost', units='$', type='NUMBER', group='Capital Costs')
    plm_total_cost: Final[float] = OUTPUT(label='Total land cost', units='$', type='NUMBER', group='Capital Costs')
    total_indirect_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    sales_tax_total: Final[float] = OUTPUT(label='Sales tax total', units='$', type='NUMBER', group='Capital Costs')
    total_installed_cost: Final[float] = OUTPUT(label='Total installed cost', units='$', type='NUMBER', group='Capital Costs')
    installed_per_capacity: Final[float] = OUTPUT(label='Estimated total installed cost per net capacity ($/kW)', units='$/kW', type='NUMBER', group='Capital Costs')
    const_per_principal1: Final[float] = OUTPUT(label='Principal, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_principal2: Final[float] = OUTPUT(label='Principal, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_principal3: Final[float] = OUTPUT(label='Principal, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_principal4: Final[float] = OUTPUT(label='Principal, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_principal5: Final[float] = OUTPUT(label='Principal, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest1: Final[float] = OUTPUT(label='Interest cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest2: Final[float] = OUTPUT(label='Interest cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest3: Final[float] = OUTPUT(label='Interest cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest4: Final[float] = OUTPUT(label='Interest cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest5: Final[float] = OUTPUT(label='Interest cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_total1: Final[float] = OUTPUT(label='Total financing cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_total2: Final[float] = OUTPUT(label='Total financing cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_total3: Final[float] = OUTPUT(label='Total financing cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_total4: Final[float] = OUTPUT(label='Total financing cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_total5: Final[float] = OUTPUT(label='Total financing cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_percent_total: Final[float] = OUTPUT(label='Total percent of installed costs, all loans', units='%', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_principal_total: Final[float] = OUTPUT(label='Total principal, all loans', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    const_per_interest_total: Final[float] = OUTPUT(label='Total interest costs, all loans', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    construction_financing_cost: Final[float] = OUTPUT(label='Total construction financing cost', units='$', type='NUMBER', group='Financial Parameters', required='csp_financial_model=1')
    ppa_price_input: Final[Array] = OUTPUT(label='PPA prices - yearly', units='$/kWh', type='ARRAY', group='Revenue', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
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
    recirculating: Final[Array] = OUTPUT(label='Field recirculating (bypass valve open)', units='-', type='ARRAY', group='Solar_Field', required='sim_type=1')
    q_dot_to_heat_sink: Final[Array] = OUTPUT(label='Heat sink thermal power', units='MWt', type='ARRAY', group='Heat_Sink', required='sim_type=1')
    W_dot_pc_pump: Final[Array] = OUTPUT(label='Heat sink pumping power', units='MWe', type='ARRAY', group='Heat_Sink', required='sim_type=1')
    m_dot_htf_heat_sink: Final[Array] = OUTPUT(label='Heat sink HTF mass flow', units='kg/s', type='ARRAY', group='Heat_Sink', required='sim_type=1')
    T_heat_sink_in: Final[Array] = OUTPUT(label='Heat sink HTF inlet temp', units='C', type='ARRAY', group='Heat_Sink', required='sim_type=1')
    T_heat_sink_out: Final[Array] = OUTPUT(label='Heat sink HTF outlet temp', units='C', type='ARRAY', group='Heat_Sink', required='sim_type=1')
    tank_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', group='TES', required='sim_type=1')
    q_tes_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWt', type='ARRAY', group='TES', required='sim_type=1')
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
    pipe_tes_diams: Final[Array] = OUTPUT(label='Pipe diameters in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_wallthk: Final[Array] = OUTPUT(label='Pipe wall thickness in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_lengths: Final[Array] = OUTPUT(label='Pipe lengths in TES', units='m', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_mdot_dsn: Final[Array] = OUTPUT(label='Mass flow TES pipes at design conditions', units='kg/s', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_vel_dsn: Final[Array] = OUTPUT(label='Velocity in TES pipes at design conditions', units='m/s', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_T_dsn: Final[Array] = OUTPUT(label='Temperature in TES pipes at design conditions', units='C', type='ARRAY', group='TES', required='sim_type=1')
    pipe_tes_P_dsn: Final[Array] = OUTPUT(label='Pressure in TES pipes at design conditions', units='bar', type='ARRAY', group='TES', required='sim_type=1')
    P_fixed: Final[Array] = OUTPUT(label='Parasitic power fixed load', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    P_plant_balance_tot: Final[Array] = OUTPUT(label='Parasitic power generation-dependent load', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    W_dot_parasitic_tot: Final[Array] = OUTPUT(label='System total electrical parasitic', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    tou_value: Final[Array] = OUTPUT(label='CSP operating Time-of-use value', type='ARRAY', group='solver', required='sim_type=1')
    pricing_mult: Final[Array] = OUTPUT(label='PPA price multiplier', type='ARRAY', group='solver', required='sim_type=1')
    n_op_modes: Final[Array] = OUTPUT(label='Operating modes in reporting timestep', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_1: Final[Array] = OUTPUT(label='1st operating mode', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_2: Final[Array] = OUTPUT(label='2nd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_3: Final[Array] = OUTPUT(label='3rd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    m_dot_balance: Final[Array] = OUTPUT(label='Relative mass flow balance error', type='ARRAY', group='solver', required='sim_type=1')
    q_balance: Final[Array] = OUTPUT(label='Relative energy balance error', type='ARRAY', group='solver', required='sim_type=1')
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
    q_dot_pc_sb: Final[Array] = OUTPUT(label='Thermal power for PC standby', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_min: Final[Array] = OUTPUT(label='Thermal power for PC min operation', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_max: Final[Array] = OUTPUT(label='Max thermal power to PC', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
    q_dot_pc_target: Final[Array] = OUTPUT(label='Target thermal power to PC', units='MWt', type='ARRAY', group='solver', required='sim_type=1')
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
    gen_heat: Final[Array] = OUTPUT(label='System net thermal power w/ avail. derate', units='kWt', type='ARRAY', group='system', required='sim_type=1')
    gen: Final[Array] = OUTPUT(label='System net electrical power w/ avail. derate', units='kWe', type='ARRAY', group='system', required='sim_type=1')
    gen_heat_btu: Final[Array] = OUTPUT(label='System net thermal power w/ avail. derate', units='MMBtu/hr', type='ARRAY', group='system', required='sim_type=1')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly Energy', units='kWh', type='ARRAY', group='Post-process', required='sim_type=1', constraints='LENGTH=12')
    monthly_energy_heat_btu: Final[Array] = OUTPUT(label='Monthly Energy in MMBtu', units='MMBtu', type='ARRAY', group='Post-process', required='sim_type=1', constraints='LENGTH=12')
    annual_energy: Final[float] = OUTPUT(label='Annual net thermal energy w/ avail. derate', units='kWhe', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_energy_heat_btu: Final[float] = OUTPUT(label='Annual net thermal energy w/ avail. derate', units='MMBtu', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_thermal_consumption: Final[float] = OUTPUT(label='Annual thermal freeze protection required', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_electricity_consumption: Final[float] = OUTPUT(label='Annual electricity consumption w/ avail derate', units='kWhe', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_total_water_use: Final[float] = OUTPUT(label='Total Annual Water Usage', units='m^3', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_field_freeze_protection: Final[float] = OUTPUT(label='Annual thermal power for field freeze protection', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_tes_freeze_protection: Final[float] = OUTPUT(label='Annual thermal power for TES freeze protection', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='system', required='sim_type=1')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', group='system', required='sim_type=1')
    sim_duration: Final[float] = OUTPUT(label='Computational time of timeseries simulation', units='s', type='NUMBER', group='system', required='sim_type=1')
    W_dot_par_tot_haf: Final[float] = OUTPUT(label='Adjusted parasitic power', units='kWe', type='NUMBER', group='system')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')
    en_electricity_rates: float = INPUT(label='Optionally enable/disable electricity_rate', units='years', type='NUMBER', group='Electricity Rates', constraints='INTEGER,MIN=0,MAX=1')
    inflation_rate: float = INPUT(label='Inflation rate', units='%', type='NUMBER', group='Lifetime', constraints='MIN=-99')
    rate_escalation: Array = INPUT(label='Annual electricity rate escalation', units='%/year', type='ARRAY', group='Electricity Rates', required='?=0')
    ur_metering_option: float = INPUT(label='Metering options', units='0=net energy metering,1=net energy metering with $ credits,2=net billing,3=net billing with carryover to next month,4=buy all - sell all', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=4', meta='Net metering monthly excess')
    ur_nm_yearend_sell_rate: float = INPUT(label='Net metering true-up credit sell rate', units='$/kWh', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_nm_credit_month: float = INPUT(label='Month of year end payout (true-up)', units='mn', type='NUMBER', group='Electricity Rates', required='?=11', constraints='INTEGER,MIN=0,MAX=11')
    ur_nm_credit_rollover: float = INPUT(label='Apply net metering true-up credits to future bills', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_monthly_fixed_charge: float = INPUT(label='Monthly fixed charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_nb_credit_expire: float = INPUT(label='Credit is lost upon end of year        ', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_nb_apply_credit_current_month: float = INPUT(label='Apply earned credits to balance before rolling over excess        ', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_sell_eq_buy: float = INPUT(label='Set sell rate equal to buy rate', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='Optional override')
    ur_monthly_min_charge: float = INPUT(label='Monthly minimum charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_annual_min_charge: float = INPUT(label='Annual minimum charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_en_ts_sell_rate: float = INPUT(label='Enable time step sell rates', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_ts_sell_rate: Array = INPUT(label='Time step sell rates', units='$/kWh', type='ARRAY', group='Electricity Rates')
    ur_en_ts_buy_rate: float = INPUT(label='Enable time step buy rates', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_ts_buy_rate: Array = INPUT(label='Time step buy rates', units='$/kWh', type='ARRAY', group='Electricity Rates')
    ur_ec_sched_weekday: Matrix = INPUT(label='Energy charge weekday schedule', units='Periods defined in ur_ec_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_ec_sched_weekend: Matrix = INPUT(label='Energy charge weekend schedule', units='Periods defined in ur_ec_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_ec_tou_mat: Matrix = INPUT(label='Energy rates table', units='col 0=period no, col 1=tier no, col 2=max usage, col 3=max usage units (0=kWh, 1=kWh/kW, 2=kWh daily, 3=kWh/kW daily), col 4=buy rate ($/kWh), col 5=sell rate ($/kWh)', type='MATRIX', group='Electricity Rates', meta='nx6')
    ur_dc_enable: float = INPUT(label='Enable demand charge', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_dc_sched_weekday: Matrix = INPUT(label='Demand charge weekday schedule', units='Periods defined in ur_dc_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_dc_sched_weekend: Matrix = INPUT(label='Demand charge weekend schedule', units='Periods defined in ur_dc_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_dc_tou_mat: Matrix = INPUT(label='Demand rates (TOU) table', units='col 0=period no, col 1=tier no, col 2=tier peak (kW), col 3=charge ($/kW)', type='MATRIX', group='Electricity Rates', required='ur_dc_enable=1', meta='nx4')
    ur_dc_flat_mat: Matrix = INPUT(label='Demand rates (flat) table', units='col 0=month, col 1=tier no, col 2=tier peak (kW), col 3=charge ($/kW)', type='MATRIX', group='Electricity Rates', required='ur_dc_enable=1', meta='nx4')
    ur_enable_billing_demand: float = INPUT(label='Enable billing demand ratchets', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_billing_demand_minimum: float = INPUT(label='Minimum billing demand', units='kW', type='NUMBER', group='Electricity Rates', required='ur_enable_billing_demand=1')
    ur_billing_demand_lookback_period: float = INPUT(label='Billing demand lookback period', units='mn', type='NUMBER', group='Electricity Rates', required='ur_enable_billing_demand=1', constraints='INTEGER,MIN=0,MAX=12')
    ur_billing_demand_lookback_percentages: Matrix = INPUT(label='Billing demand lookback percentages by month and consider actual peak demand', units='%', type='MATRIX', group='Electricity Rates', required='ur_enable_billing_demand=1', meta='12x2')
    ur_dc_billing_demand_periods: Matrix = INPUT(label='Billing demand applicability to a given demand charge time of use period', type='MATRIX', group='Electricity Rates', required='ur_enable_billing_demand=1')
    ur_yearzero_usage_peaks: Array = INPUT(label='Peak usage by month for year zero', units='kW', type='ARRAY', group='Electricity Rates', required='ur_enable_billing_demand=1', meta='12')

    def __init__(self, *args: Mapping[str, Any],
                 sim_type: float = ...,
                 file_name: str = ...,
                 solar_mult_in: float = ...,
                 total_Ap_in: float = ...,
                 solar_mult_or_Ap: float = ...,
                 T_loop_in_des: float = ...,
                 T_loop_out: float = ...,
                 I_bn_des: float = ...,
                 tshours: float = ...,
                 q_pb_design: float = ...,
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
                 rec_su_delay: float = ...,
                 rec_qf_delay: float = ...,
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
                 pb_pump_coef: float = ...,
                 hs_type: float = ...,
                 hs_phys_N_sub: float = ...,
                 hs_phys_tol: float = ...,
                 hs_phys_f_mdot_steam_min: float = ...,
                 hs_phys_f_mdot_steam_max: float = ...,
                 hs_phys_T_steam_cold_des: float = ...,
                 hs_phys_P_steam_hot_des: float = ...,
                 hs_phys_Q_steam_hot_des: float = ...,
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
                 weekday_schedule: Matrix = ...,
                 weekend_schedule: Matrix = ...,
                 f_turb_tou_periods: Array = ...,
                 timestep_load_abs: Array = ...,
                 timestep_load_abs_factor: float = ...,
                 is_tod_pc_target_also_pc_max: float = ...,
                 pb_fixed_par: float = ...,
                 bop_array: Array = ...,
                 aux_array: Array = ...,
                 is_dispatch: float = ...,
                 disp_rsu_cost_rel: float = ...,
                 disp_horizon: float = ...,
                 disp_frequency: float = ...,
                 disp_max_iter: float = ...,
                 disp_timeout: float = ...,
                 disp_mip_gap: float = ...,
                 disp_time_weighting: float = ...,
                 disp_steps_per_hour: float = ...,
                 disp_spec_presolve: float = ...,
                 disp_spec_bb: float = ...,
                 disp_reporting: float = ...,
                 disp_spec_scaling: float = ...,
                 disp_inventory_incentive: float = ...,
                 q_rec_heattrace: float = ...,
                 q_rec_standby: float = ...,
                 csp_financial_model: float = ...,
                 ppa_multiplier_model: float = ...,
                 ppa_soln_mode: float = ...,
                 dispatch_factors_ts: Array = ...,
                 dispatch_sched_weekday: Matrix = ...,
                 dispatch_sched_weekend: Matrix = ...,
                 dispatch_tod_factors: Array = ...,
                 ppa_price_input_heat_btu: Array = ...,
                 site_improvements_spec_cost: float = ...,
                 solar_field_spec_cost: float = ...,
                 htf_system_spec_cost: float = ...,
                 storage_spec_cost: float = ...,
                 heat_sink_spec_cost: float = ...,
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
                 adjust_periods: Matrix = ...,
                 en_electricity_rates: float = ...,
                 inflation_rate: float = ...,
                 rate_escalation: Array = ...,
                 ur_metering_option: float = ...,
                 ur_nm_yearend_sell_rate: float = ...,
                 ur_nm_credit_month: float = ...,
                 ur_nm_credit_rollover: float = ...,
                 ur_monthly_fixed_charge: float = ...,
                 ur_nb_credit_expire: float = ...,
                 ur_nb_apply_credit_current_month: float = ...,
                 ur_sell_eq_buy: float = ...,
                 ur_monthly_min_charge: float = ...,
                 ur_annual_min_charge: float = ...,
                 ur_en_ts_sell_rate: float = ...,
                 ur_ts_sell_rate: Array = ...,
                 ur_en_ts_buy_rate: float = ...,
                 ur_ts_buy_rate: Array = ...,
                 ur_ec_sched_weekday: Matrix = ...,
                 ur_ec_sched_weekend: Matrix = ...,
                 ur_ec_tou_mat: Matrix = ...,
                 ur_dc_enable: float = ...,
                 ur_dc_sched_weekday: Matrix = ...,
                 ur_dc_sched_weekend: Matrix = ...,
                 ur_dc_tou_mat: Matrix = ...,
                 ur_dc_flat_mat: Matrix = ...,
                 ur_enable_billing_demand: float = ...,
                 ur_billing_demand_minimum: float = ...,
                 ur_billing_demand_lookback_period: float = ...,
                 ur_billing_demand_lookback_percentages: Matrix = ...,
                 ur_dc_billing_demand_periods: Matrix = ...,
                 ur_yearzero_usage_peaks: Array = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
