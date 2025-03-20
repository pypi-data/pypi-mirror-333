
# This is a generated file

"""trough_physical - Physical trough applications"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'sim_type': float,
    'time_start': float,
    'time_stop': float,
    'time_steps_per_hour': float,
    'vacuum_arrays': float,
    'file_name': str,
    'solar_resource_data': Table,
    'nHCEt': float,
    'nColt': float,
    'nHCEVar': float,
    'FieldConfig': float,
    'include_fixed_power_block_runner': float,
    'L_power_block_piping': float,
    'eta_pump': float,
    'Fluid': float,
    'accept_loc': float,
    'HDR_rough': float,
    'theta_stow': float,
    'theta_dep': float,
    'Row_Distance': float,
    'T_loop_in_des': float,
    'T_loop_out': float,
    'T_startup': float,
    'T_shutdown': float,
    'use_abs_or_rel_mdot_limit': float,
    'm_dot_htfmin': float,
    'm_dot_htfmax': float,
    'f_htfmin': float,
    'f_htfmax': float,
    'field_fl_props': Matrix,
    'T_fp': float,
    'I_bn_des': float,
    'Pipe_hl_coef': float,
    'SCA_drives_elec': float,
    'tilt': float,
    'azimuth': float,
    'wind_stow_speed': float,
    'accept_mode': float,
    'accept_init': float,
    'mc_bal_hot': float,
    'mc_bal_cold': float,
    'mc_bal_sca': float,
    'W_aperture': Array,
    'A_aperture': Array,
    'TrackingError': Array,
    'GeomEffects': Array,
    'Rho_mirror_clean': Array,
    'Dirt_mirror': Array,
    'Error': Array,
    'Ave_Focal_Length': Array,
    'L_SCA': Array,
    'L_aperture': Array,
    'ColperSCA': Array,
    'Distance_SCA': Array,
    'IAM_matrix': Matrix,
    'HCE_FieldFrac': Matrix,
    'D_2': Matrix,
    'D_3': Matrix,
    'D_4': Matrix,
    'D_5': Matrix,
    'D_p': Matrix,
    'Flow_type': Matrix,
    'Rough': Matrix,
    'alpha_env': Matrix,
    'epsilon_3_11': Matrix,
    'epsilon_3_12': Matrix,
    'epsilon_3_13': Matrix,
    'epsilon_3_14': Matrix,
    'epsilon_3_21': Matrix,
    'epsilon_3_22': Matrix,
    'epsilon_3_23': Matrix,
    'epsilon_3_24': Matrix,
    'epsilon_3_31': Matrix,
    'epsilon_3_32': Matrix,
    'epsilon_3_33': Matrix,
    'epsilon_3_34': Matrix,
    'epsilon_3_41': Matrix,
    'epsilon_3_42': Matrix,
    'epsilon_3_43': Matrix,
    'epsilon_3_44': Matrix,
    'alpha_abs': Matrix,
    'Tau_envelope': Matrix,
    'EPSILON_4': Matrix,
    'EPSILON_5': Matrix,
    'GlazingIntactIn': Matrix,
    'P_a': Matrix,
    'AnnulusGas': Matrix,
    'AbsorberMaterial': Matrix,
    'Shadowing': Matrix,
    'Dirt_HCE': Matrix,
    'Design_loss': Matrix,
    'p_start': float,
    'pc_config': float,
    'P_ref': float,
    'eta_ref': float,
    'cycle_max_frac': float,
    'cycle_cutoff_frac': float,
    'q_sby_frac': float,
    'startup_time': float,
    'startup_frac': float,
    'pb_pump_coef': float,
    'dT_cw_ref': float,
    'T_amb_des': float,
    'CT': float,
    'tech_type': float,
    'T_approach': float,
    'T_ITD_des': float,
    'P_cond_ratio': float,
    'pb_bd_frac': float,
    'P_cond_min': float,
    'n_pl_inc': float,
    'F_wc': Array,
    'ud_f_W_dot_cool_des': float,
    'ud_m_dot_water_cool_des': float,
    'ud_is_sco2_regr': float,
    'ud_ind_od': Matrix,
    'tes_type': float,
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
    'store_fluid': float,
    'store_fl_props': Matrix,
    'dt_hot': float,
    'tanks_in_parallel': float,
    'tes_cyl_tank_thick': float,
    'tes_cyl_tank_cp': float,
    'tes_cyl_tank_dens': float,
    'tes_cyl_piston_loss_poly': Array,
    'tes_cyl_tank_insul_percent': float,
    'tes_pb_n_xsteps': float,
    'tes_pb_k_eff': float,
    'tes_pb_void_frac': float,
    'tes_pb_dens_solid': float,
    'tes_pb_cp_solid': float,
    'tes_pb_T_hot_delta': float,
    'tes_pb_T_cold_delta': float,
    'tes_pb_T_charge_min': float,
    'tes_pb_f_oversize': float,
    'rec_op_mode_initial': float,
    'defocus_initial': float,
    'T_in_loop_initial': float,
    'T_out_loop_initial': float,
    'T_out_scas_initial': Array,
    'pc_op_mode_initial': float,
    'pc_startup_time_remain_init': float,
    'pc_startup_energy_remain_initial': float,
    'T_tank_cold_init': float,
    'T_tank_hot_init': float,
    'is_dispatch_targets': float,
    'q_pc_target_su_in': Array,
    'q_pc_target_on_in': Array,
    'q_pc_max_in': Array,
    'is_rec_su_allowed_in': Array,
    'is_pc_su_allowed_in': Array,
    'is_pc_sb_allowed_in': Array,
    'weekday_schedule': Matrix,
    'weekend_schedule': Matrix,
    'is_tod_pc_target_also_pc_max': float,
    'is_dispatch': float,
    'can_cycle_use_standby': float,
    'is_write_ampl_dat': float,
    'is_ampl_engine': float,
    'ampl_data_dir': str,
    'ampl_exec_call': str,
    'disp_frequency': float,
    'disp_steps_per_hour': float,
    'disp_horizon': float,
    'disp_max_iter': float,
    'disp_timeout': float,
    'disp_mip_gap': float,
    'disp_spec_presolve': float,
    'disp_spec_bb': float,
    'disp_reporting': float,
    'disp_spec_scaling': float,
    'disp_time_weighting': float,
    'disp_rsu_cost_rel': float,
    'disp_csu_cost_rel': float,
    'disp_pen_ramping': float,
    'disp_inventory_incentive': float,
    'q_rec_standby': float,
    'q_rec_heattrace': float,
    'f_turb_tou_periods': Array,
    'rec_su_delay': float,
    'rec_qf_delay': float,
    'csp_financial_model': float,
    'ppa_multiplier_model': float,
    'dispatch_factors_ts': Array,
    'ppa_soln_mode': float,
    'en_electricity_rates': float,
    'dispatch_sched_weekday': Matrix,
    'dispatch_sched_weekend': Matrix,
    'dispatch_tod_factors': Array,
    'is_timestep_load_fractions': float,
    'timestep_load_fractions': Array,
    'ppa_price_input': Array,
    'mp_energy_market_revenue': Matrix,
    'pb_fixed_par': float,
    'bop_array': Array,
    'aux_array': Array,
    'gross_net_conversion_factor': float,
    'water_usage_per_wash': float,
    'washing_frequency': float,
    'calc_design_pipe_vals': float,
    'V_hdr_cold_max': float,
    'V_hdr_cold_min': float,
    'V_hdr_hot_max': float,
    'V_hdr_hot_min': float,
    'N_max_hdr_diams': float,
    'L_rnr_pb': float,
    'L_rnr_per_xpan': float,
    'L_xpan_hdr': float,
    'L_xpan_rnr': float,
    'Min_rnr_xpans': float,
    'northsouth_field_sep': float,
    'N_hdr_per_xpan': float,
    'offset_xpan_hdr': float,
    'custom_sf_pipe_sizes': float,
    'sf_rnr_diams': Matrix,
    'sf_rnr_wallthicks': Matrix,
    'sf_rnr_lengths': Matrix,
    'sf_hdr_diams': Matrix,
    'sf_hdr_wallthicks': Matrix,
    'sf_hdr_lengths': Matrix,
    'has_hot_tank_bypass': float,
    'T_tank_hot_inlet_min': float,
    'tes_pump_coef': float,
    'V_tes_des': float,
    'custom_tes_p_loss': float,
    'k_tes_loss_coeffs': Matrix,
    'custom_tes_pipe_sizes': float,
    'tes_diams': Matrix,
    'tes_wallthicks': Matrix,
    'tes_lengths': Matrix,
    'DP_SGS': float,
    'use_solar_mult_or_aperture_area': float,
    'specified_solar_multiple': float,
    'specified_total_aperture': float,
    'non_solar_field_land_area_multiplier': float,
    'trough_loop_control': Array,
    'piping_loss': float,
    'disp_csu_cost': float,
    'disp_rsu_cost': float,
    'disp_pen_delta_w': float,
    'P_boil': float,
    'csp.dtr.cost.site_improvements.cost_per_m2': float,
    'csp.dtr.cost.solar_field.cost_per_m2': float,
    'csp.dtr.cost.htf_system.cost_per_m2': float,
    'csp.dtr.cost.storage.cost_per_kwht': float,
    'csp.dtr.cost.fossil_backup.cost_per_kwe': float,
    'csp.dtr.cost.power_plant.cost_per_kwe': float,
    'csp.dtr.cost.bop_per_kwe': float,
    'csp.dtr.cost.contingency_percent': float,
    'csp.dtr.cost.epc.per_acre': float,
    'csp.dtr.cost.epc.percent': float,
    'csp.dtr.cost.epc.per_watt': float,
    'csp.dtr.cost.epc.fixed': float,
    'csp.dtr.cost.plm.per_acre': float,
    'csp.dtr.cost.plm.percent': float,
    'csp.dtr.cost.plm.per_watt': float,
    'csp.dtr.cost.plm.fixed': float,
    'csp.dtr.cost.sales_tax.percent': float,
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
    'q_dot_cycle_des': float,
    'nameplate': float,
    'solar_mult': float,
    'nSCA': float,
    'field_htf_min_temp': float,
    'field_htf_max_temp': float,
    'field_htf_cp_avg_des': float,
    'single_loop_aperture': float,
    'min_inner_diameter': float,
    'csp_dtr_hce_design_heat_losses': Array,
    'csp_dtr_loop_hce_heat_loss': float,
    'csp_dtr_sca_calc_sca_effs': Array,
    'loop_optical_efficiency': float,
    'csp_dtr_hce_optical_effs': Array,
    'SCAInfoArray': Matrix,
    'SCADefocusArray': Array,
    'max_field_flow_velocity': float,
    'min_field_flow_velocity': float,
    'm_dot_htfmin_actual': float,
    'm_dot_htfmax_actual': float,
    'f_htfmin_actual': float,
    'f_htfmax_actual': float,
    'max_loop_flow_vel_des': float,
    'min_loop_flow_vel_des': float,
    'total_loop_conversion_efficiency': float,
    'total_required_aperture_for_SM1': float,
    'required_number_of_loops_for_SM1': float,
    'nLoops': float,
    'total_aperture': float,
    'fixed_land_area': float,
    'total_land_area': float,
    'total_tracking_power': float,
    'K_cpnt': Matrix,
    'D_cpnt': Matrix,
    'L_cpnt': Matrix,
    'Type_cpnt': Matrix,
    'field_thermal_output_actual': float,
    'field_thermal_output_ideal': float,
    'dP_sf_SS': float,
    'W_dot_pump_SS': float,
    'vol_tank': float,
    'q_tes': float,
    'csp_pt_tes_tank_height': float,
    'csp_pt_tes_tank_diameter': float,
    'q_dot_tes_est': float,
    'csp_pt_tes_htf_density': float,
    'tes_avail_vol': float,
    'is_hx': float,
    'vol_min': float,
    'V_tank_hot_ini': float,
    'tes_htf_avg_temp': float,
    'tes_htf_min_temp': float,
    'tes_htf_max_temp': float,
    'csp_dtr_sca_ap_lengths': Matrix,
    'csp_dtr_sca_calc_zenith': float,
    'csp_dtr_sca_calc_costh': float,
    'csp_dtr_sca_calc_theta': float,
    'csp_dtr_sca_calc_end_gains': Matrix,
    'csp_dtr_sca_calc_end_losses': Matrix,
    'csp_dtr_sca_calc_latitude': float,
    'csp_dtr_sca_calc_iams': Matrix,
    'm_dot_htf_cycle_des': float,
    'bop_design': float,
    'aux_design': float,
    'csp.dtr.cost.site_improvements': float,
    'csp.dtr.cost.solar_field': float,
    'csp.dtr.cost.htf_system': float,
    'csp.dtr.cost.storage': float,
    'csp.dtr.cost.fossil_backup': float,
    'csp.dtr.cost.power_plant': float,
    'csp.dtr.cost.bop': float,
    'csp.dtr.cost.contingency': float,
    'total_direct_cost': float,
    'direct_subtotal': float,
    'csp.dtr.cost.epc.total': float,
    'csp.dtr.cost.plm.total': float,
    'total_indirect_cost': float,
    'csp.dtr.cost.sales_tax.total': float,
    'total_installed_cost': float,
    'csp.dtr.cost.installed_per_capacity': float,
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
    'Theta_ave': Array,
    'CosTh_ave': Array,
    'IAM_ave': Array,
    'RowShadow_ave': Array,
    'EndLoss_ave': Array,
    'dni_costh': Array,
    'EqOpteff': Array,
    'SCAs_def': Array,
    'q_inc_sf_tot': Array,
    'qinc_costh': Array,
    'q_dot_rec_inc': Array,
    'q_dot_rec_thermal_loss': Array,
    'q_dot_rec_abs': Array,
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
    'vel_loop_min': Array,
    'vel_loop_max': Array,
    'W_dot_sca_track': Array,
    'W_dot_field_pump': Array,
    'pipe_header_diams': Array,
    'pipe_header_wallthk': Array,
    'pipe_header_lengths': Array,
    'pipe_header_expansions': Array,
    'pipe_header_mdot_dsn': Array,
    'pipe_header_vel_dsn': Array,
    'pipe_header_T_dsn': Array,
    'pipe_header_P_dsn': Array,
    'pipe_runner_diams': Array,
    'pipe_runner_wallthk': Array,
    'pipe_runner_lengths': Array,
    'pipe_runner_expansions': Array,
    'pipe_runner_mdot_dsn': Array,
    'pipe_runner_vel_dsn': Array,
    'pipe_runner_T_dsn': Array,
    'pipe_runner_P_dsn': Array,
    'pipe_loop_T_dsn': Array,
    'pipe_loop_P_dsn': Array,
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
    'vol_tes_cold': Array,
    'vol_tes_hot': Array,
    'vol_tes_tot': Array,
    'tes_piston_loc': Array,
    'tes_piston_frac': Array,
    'tes_cold_vol_frac': Array,
    'tes_mass_tot': Array,
    'tes_SA_cold': Array,
    'tes_SA_hot': Array,
    'tes_SA_tot': Array,
    'tes_error': Array,
    'tes_error_percent': Array,
    'tes_leak_error': Array,
    'tes_wall_error': Array,
    'tes_error_corrected': Array,
    'T_grad_0': Array,
    'T_grad_1': Array,
    'T_grad_2': Array,
    'T_grad_3': Array,
    'T_grad_4': Array,
    'T_grad_5': Array,
    'T_grad_6': Array,
    'T_grad_7': Array,
    'T_grad_8': Array,
    'T_grad_9': Array,
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
    'rec_op_mode_final': Array,
    'defocus_final': Array,
    'T_in_loop_final': Array,
    'T_out_loop_final': Array,
    'T_out_scas_last_final': Array,
    'pc_op_mode_final': Array,
    'pc_startup_time_remain_final': Array,
    'pc_startup_energy_remain_final': Array,
    'hot_tank_htf_percent_final': Array,
    'cycle_eff_load_table': Matrix,
    'cycle_Tdb_table': Matrix,
    'adjust_constant': float,
    'adjust_en_timeindex': float,
    'adjust_en_periods': float,
    'adjust_timeindex': Array,
    'adjust_periods': Matrix
}, total=False)

class Data(ssc.DataDict):
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='System Control', required='?=1')
    time_start: float = INPUT(label='Simulation start time', units='s', type='NUMBER', group='System Control', required='?=0')
    time_stop: float = INPUT(label='Simulation stop time', units='s', type='NUMBER', group='System Control', required='?=31536000')
    time_steps_per_hour: float = INPUT(label='Number of simulation time steps per hour', type='NUMBER', group='System Control', required='?=-1')
    vacuum_arrays: float = INPUT(label='Allocate arrays for only the required number of steps', type='NUMBER', group='System Control', required='?=0')
    file_name: str = INPUT(label='Local weather file with path', units='none', type='STRING', group='weather', required='?', constraints='LOCAL_FILE')
    solar_resource_data: Table = INPUT(label='Weather resource data in memory', type='TABLE', group='weather', required='?')
    nHCEt: float = INPUT(label='Number of HCE types', units='none', type='NUMBER', group='solar_field', required='*')
    nColt: float = INPUT(label='Number of collector types', units='none', type='NUMBER', group='solar_field', required='*', meta='constant=4')
    nHCEVar: float = INPUT(label='Number of HCE variants per type', units='none', type='NUMBER', group='solar_field', required='*')
    FieldConfig: float = INPUT(label='Number of subfield headers', units='none', type='NUMBER', group='solar_field', required='*')
    include_fixed_power_block_runner: float = INPUT(label='Should model consider piping through power block?', units='none', type='NUMBER', group='solar_field', required='*')
    L_power_block_piping: float = INPUT(label='Length of piping (full mass flow) through heat sink (if applicable)', units='none', type='NUMBER', group='solar_field', required='*')
    eta_pump: float = INPUT(label='HTF pump efficiency', units='none', type='NUMBER', group='solar_field', required='*')
    Fluid: float = INPUT(label='Field HTF fluid ID number', units='none', type='NUMBER', group='solar_field', required='*')
    accept_loc: float = INPUT(label='In acceptance testing mode - temperature sensor location', units='1/2', type='NUMBER', group='solar_field', required='*', meta='hx/loop')
    HDR_rough: float = INPUT(label='Header pipe roughness', units='m', type='NUMBER', group='solar_field', required='*')
    theta_stow: float = INPUT(label='Stow angle', units='deg', type='NUMBER', group='solar_field', required='*')
    theta_dep: float = INPUT(label='Deploy angle', units='deg', type='NUMBER', group='solar_field', required='*')
    Row_Distance: float = INPUT(label='Spacing between rows (centerline to centerline)', units='m', type='NUMBER', group='solar_field', required='*')
    T_loop_in_des: float = INPUT(label='Design loop inlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    T_loop_out: float = INPUT(label='Target loop outlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    T_startup: float = INPUT(label='Required temperature of the system before the power block can be switched on', units='C', type='NUMBER', group='solar_field', required='?')
    T_shutdown: float = INPUT(label='Temperature when solar field begins recirculating', units='C', type='NUMBER', group='solar_field', required='?')
    use_abs_or_rel_mdot_limit: float = INPUT(label='Use mass flow abs (0) or relative (1) limits', type='NUMBER', group='solar_field', required='?=0')
    m_dot_htfmin: float = INPUT(label='Minimum loop HTF flow rate', units='kg/s', type='NUMBER', group='solar_field', required='use_abs_or_rel_mdot_limit=0')
    m_dot_htfmax: float = INPUT(label='Maximum loop HTF flow rate', units='kg/s', type='NUMBER', group='solar_field', required='use_abs_or_rel_mdot_limit=0')
    f_htfmin: float = INPUT(label='Minimum loop mass flow rate fraction of design', type='NUMBER', group='solar_field', required='use_abs_or_rel_mdot_limit=1')
    f_htfmax: float = INPUT(label='Maximum loop mass flow rate fraction of design', type='NUMBER', group='solar_field', required='use_abs_or_rel_mdot_limit=1')
    field_fl_props: Matrix = INPUT(label='User defined field fluid property data', units='-', type='MATRIX', group='solar_field', required='*')
    T_fp: float = INPUT(label='Freeze protection temperature (heat trace activation temperature)', units='none', type='NUMBER', group='solar_field', required='*')
    I_bn_des: float = INPUT(label='Solar irradiation at design', units='C', type='NUMBER', group='solar_field', required='*')
    Pipe_hl_coef: float = INPUT(label='Loss coefficient from the header, runner pipe, and non-HCE piping', units='m/s', type='NUMBER', group='solar_field', required='*')
    SCA_drives_elec: float = INPUT(label='Tracking power, in Watts per SCA drive', units='W/m2-K', type='NUMBER', group='solar_field', required='*')
    tilt: float = INPUT(label='Tilt angle of surface/axis', units='none', type='NUMBER', group='solar_field', required='*')
    azimuth: float = INPUT(label='Azimuth angle of surface/axis', units='none', type='NUMBER', group='solar_field', required='*')
    wind_stow_speed: float = INPUT(label='Trough wind stow speed', units='m/s', type='NUMBER', group='solar_field', required='?=50')
    accept_mode: float = INPUT(label='Acceptance testing mode?', units='0/1', type='NUMBER', group='solar_field', required='*', meta='no/yes')
    accept_init: float = INPUT(label='In acceptance testing mode - require steady-state startup', units='none', type='NUMBER', group='solar_field', required='*')
    mc_bal_hot: float = INPUT(label='Heat capacity of the balance of plant on the hot side', units='kWht/K-MWt', type='NUMBER', group='solar_field', required='*', meta='none')
    mc_bal_cold: float = INPUT(label='Heat capacity of the balance of plant on the cold side', units='kWht/K-MWt', type='NUMBER', group='solar_field', required='*')
    mc_bal_sca: float = INPUT(label='Non-HTF heat capacity associated with each SCA - per meter basis', units='Wht/K-m', type='NUMBER', group='solar_field', required='*')
    W_aperture: Array = INPUT(label='The collector aperture width (Total structural area used for shadowing)', units='m', type='ARRAY', group='solar_field', required='*')
    A_aperture: Array = INPUT(label='Reflective aperture area of the collector', units='m2', type='ARRAY', group='solar_field', required='*')
    TrackingError: Array = INPUT(label='User-defined tracking error derate', units='none', type='ARRAY', group='solar_field', required='*')
    GeomEffects: Array = INPUT(label='User-defined geometry effects derate', units='none', type='ARRAY', group='solar_field', required='*')
    Rho_mirror_clean: Array = INPUT(label='User-defined clean mirror reflectivity', units='none', type='ARRAY', group='solar_field', required='*')
    Dirt_mirror: Array = INPUT(label='User-defined dirt on mirror derate', units='none', type='ARRAY', group='solar_field', required='*')
    Error: Array = INPUT(label='User-defined general optical error derate ', units='none', type='ARRAY', group='solar_field', required='*')
    Ave_Focal_Length: Array = INPUT(label='Average focal length of the collector ', units='m', type='ARRAY', group='solar_field', required='*')
    L_SCA: Array = INPUT(label='Length of the SCA ', units='m', type='ARRAY', group='solar_field', required='*')
    L_aperture: Array = INPUT(label='Length of a single mirror/HCE unit', units='m', type='ARRAY', group='solar_field', required='*')
    ColperSCA: Array = INPUT(label='Number of individual collector sections in an SCA ', units='none', type='ARRAY', group='solar_field', required='*')
    Distance_SCA: Array = INPUT(label="Piping distance between SCA's in the field", units='m', type='ARRAY', group='solar_field', required='*')
    IAM_matrix: Matrix = INPUT(label='IAM coefficients, matrix for 4 collectors', units='none', type='MATRIX', group='solar_field', required='*')
    HCE_FieldFrac: Matrix = INPUT(label='Fraction of the field occupied by this HCE type ', units='none', type='MATRIX', group='solar_field', required='*')
    D_2: Matrix = INPUT(label='Inner absorber tube diameter', units='m', type='MATRIX', group='solar_field', required='*')
    D_3: Matrix = INPUT(label='Outer absorber tube diameter', units='m', type='MATRIX', group='solar_field', required='*')
    D_4: Matrix = INPUT(label='Inner glass envelope diameter ', units='m', type='MATRIX', group='solar_field', required='*')
    D_5: Matrix = INPUT(label='Outer glass envelope diameter ', units='m', type='MATRIX', group='solar_field', required='*')
    D_p: Matrix = INPUT(label='Diameter of the absorber flow plug (optional) ', units='m', type='MATRIX', group='solar_field', required='*')
    Flow_type: Matrix = INPUT(label='Flow type through the absorber', units='none', type='MATRIX', group='solar_field', required='*')
    Rough: Matrix = INPUT(label='Relative roughness of the internal HCE surface ', units='-', type='MATRIX', group='solar_field', required='*')
    alpha_env: Matrix = INPUT(label='Envelope absorptance ', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_11: Matrix = INPUT(label='Absorber emittance for receiver type 1 variation 1', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_12: Matrix = INPUT(label='Absorber emittance for receiver type 1 variation 2', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_13: Matrix = INPUT(label='Absorber emittance for receiver type 1 variation 3', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_14: Matrix = INPUT(label='Absorber emittance for receiver type 1 variation 4', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_21: Matrix = INPUT(label='Absorber emittance for receiver type 2 variation 1', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_22: Matrix = INPUT(label='Absorber emittance for receiver type 2 variation 2', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_23: Matrix = INPUT(label='Absorber emittance for receiver type 2 variation 3', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_24: Matrix = INPUT(label='Absorber emittance for receiver type 2 variation 4', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_31: Matrix = INPUT(label='Absorber emittance for receiver type 3 variation 1', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_32: Matrix = INPUT(label='Absorber emittance for receiver type 3 variation 2', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_33: Matrix = INPUT(label='Absorber emittance for receiver type 3 variation 3', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_34: Matrix = INPUT(label='Absorber emittance for receiver type 3 variation 4', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_41: Matrix = INPUT(label='Absorber emittance for receiver type 4 variation 1', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_42: Matrix = INPUT(label='Absorber emittance for receiver type 4 variation 2', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_43: Matrix = INPUT(label='Absorber emittance for receiver type 4 variation 3', units='none', type='MATRIX', group='solar_field', required='*')
    epsilon_3_44: Matrix = INPUT(label='Absorber emittance for receiver type 4 variation 4', units='none', type='MATRIX', group='solar_field', required='*')
    alpha_abs: Matrix = INPUT(label='Absorber absorptance ', units='none', type='MATRIX', group='solar_field', required='*')
    Tau_envelope: Matrix = INPUT(label='Envelope transmittance', units='none', type='MATRIX', group='solar_field', required='*')
    EPSILON_4: Matrix = INPUT(label='Inner glass envelope emissivities (Pyrex) ', units='none', type='MATRIX', group='solar_field', required='*')
    EPSILON_5: Matrix = INPUT(label='Outer glass envelope emissivities (Pyrex) ', units='none', type='MATRIX', group='solar_field', required='*')
    GlazingIntactIn: Matrix = INPUT(label='Glazing intact (broken glass) flag {1=true, else=false}', units='none', type='MATRIX', group='solar_field', required='*')
    P_a: Matrix = INPUT(label='Annulus gas pressure', units='torr', type='MATRIX', group='solar_field', required='*')
    AnnulusGas: Matrix = INPUT(label='Annulus gas type (1=air, 26=Ar, 27=H2)', units='none', type='MATRIX', group='solar_field', required='*')
    AbsorberMaterial: Matrix = INPUT(label='Absorber material type', units='none', type='MATRIX', group='solar_field', required='*')
    Shadowing: Matrix = INPUT(label='Receiver bellows shadowing loss factor', units='none', type='MATRIX', group='solar_field', required='*')
    Dirt_HCE: Matrix = INPUT(label='Loss due to dirt on the receiver envelope', units='none', type='MATRIX', group='solar_field', required='*')
    Design_loss: Matrix = INPUT(label='Receiver heat loss at design', units='W/m', type='MATRIX', group='solar_field', required='*')
    p_start: float = INPUT(label='Collector startup energy, per SCA', units='kWhe', type='NUMBER', group='solar_field', required='*')
    pc_config: float = INPUT(label='0: Steam Rankine (224), 1: user defined', units='-', type='NUMBER', group='powerblock', required='?=0', constraints='INTEGER')
    P_ref: float = INPUT(label='Rated plant capacity', units='MWe', type='NUMBER', group='powerblock', required='*')
    eta_ref: float = INPUT(label='Power cycle efficiency at design', units='none', type='NUMBER', group='powerblock', required='*')
    cycle_max_frac: float = INPUT(label='Maximum turbine over design operation fraction', units='-', type='NUMBER', group='powerblock', required='*')
    cycle_cutoff_frac: float = INPUT(label='Minimum turbine operation fraction before shutdown', units='-', type='NUMBER', group='powerblock', required='*')
    q_sby_frac: float = INPUT(label='Fraction of thermal power required for standby mode', units='none', type='NUMBER', group='powerblock', required='*')
    startup_time: float = INPUT(label='Time needed for power block startup', units='hr', type='NUMBER', group='powerblock', required='*')
    startup_frac: float = INPUT(label='Fraction of design thermal power needed for startup', units='none', type='NUMBER', group='powerblock', required='*')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='powerblock', required='*')
    dT_cw_ref: float = INPUT(label='Reference condenser cooling water inlet/outlet T diff', units='C', type='NUMBER', group='powerblock', required='pc_config=0')
    T_amb_des: float = INPUT(label='Reference ambient temperature at design point', units='C', type='NUMBER', group='powerblock', required='pc_config=0')
    CT: float = INPUT(label='Flag for using dry cooling or wet cooling system', units='none', type='NUMBER', group='powerblock', required='pc_config=0')
    tech_type: float = INPUT(label='Turbine inlet pressure control flag (sliding=user, fixed=trough)', units='1/2/3', type='NUMBER', group='powerblock', required='pc_config=0', meta='tower/trough/user')
    T_approach: float = INPUT(label='Cooling tower approach temperature', units='C', type='NUMBER', group='powerblock', required='pc_config=0')
    T_ITD_des: float = INPUT(label='ITD at design for dry system', units='C', type='NUMBER', group='powerblock', required='pc_config=0')
    P_cond_ratio: float = INPUT(label='Condenser pressure ratio', units='none', type='NUMBER', group='powerblock', required='pc_config=0')
    pb_bd_frac: float = INPUT(label='Power block blowdown steam fraction ', units='none', type='NUMBER', group='powerblock', required='pc_config=0')
    P_cond_min: float = INPUT(label='Minimum condenser pressure', units='inHg', type='NUMBER', group='powerblock', required='pc_config=0')
    n_pl_inc: float = INPUT(label='Number of part-load increments for the heat rejection system', units='none', type='NUMBER', group='powerblock', required='pc_config=0')
    F_wc: Array = INPUT(label='Fraction indicating wet cooling use for hybrid system', units='none', type='ARRAY', group='powerblock', required='pc_config=0', meta='constant=[0,0,0,0,0,0,0,0,0]')
    ud_f_W_dot_cool_des: float = INPUT(label='Percent of user-defined power cycle design gross output consumed by cooling', units='%', type='NUMBER', group='powerblock', required='pc_config=1')
    ud_m_dot_water_cool_des: float = INPUT(label='Mass flow rate of water required at user-defined power cycle design point', units='kg/s', type='NUMBER', group='powerblock', required='pc_config=1')
    ud_is_sco2_regr: float = INPUT(label='0: (default) simple max htf mass flow correction; 1: sco2 heuristic regression; 2: no correction', type='NUMBER', group='powerblock', required='?=0')
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='powerblock', required='pc_config=1')
    tes_type: float = INPUT(label='Standard two tank (1), Packed Bed (2), Piston Cylinder (3)', units='-', type='NUMBER', group='TES', required='?=1')
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
    store_fluid: float = INPUT(label='Material number for storage fluid', units='-', type='NUMBER', group='TES', required='tes_type=1')
    store_fl_props: Matrix = INPUT(label='User defined storage fluid property data', units='-', type='MATRIX', group='TES', required='tes_type=1')
    dt_hot: float = INPUT(label='Hot side HX approach temp', units='C', type='NUMBER', group='TES', required='tes_type=1')
    tanks_in_parallel: float = INPUT(label='Tanks are in parallel, not in series, with solar field', units='-', type='NUMBER', group='controller', required='tes_type=1')
    tes_cyl_tank_thick: float = INPUT(label='Tank wall thickness (used for Piston Cylinder)', units='m', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_tank_cp: float = INPUT(label='Tank wall cp (used for Piston Cylinder)', units='kJ/kg-K', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_tank_dens: float = INPUT(label='Tank wall thickness (used for Piston Cylinder)', units='kg/m3', type='NUMBER', group='TES', required='tes_type=3')
    tes_cyl_piston_loss_poly: Array = INPUT(label='Polynomial coefficients describing piston heat loss function (f(kg/s)=%)', type='ARRAY', group='TES', required='tes_type=3')
    tes_cyl_tank_insul_percent: float = INPUT(label='Percent additional wall mass due to insulation (used for Piston Cylinder)', units='%', type='NUMBER', group='TES', required='?=0')
    tes_pb_n_xsteps: float = INPUT(label='Number of spatial segments', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_k_eff: float = INPUT(label='TES packed bed effective conductivity', units='W/m K', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_void_frac: float = INPUT(label='TES packed bed void fraction', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_dens_solid: float = INPUT(label='TES packed bed media density', units='kg/m3', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_cp_solid: float = INPUT(label='TES particle specific heat', units='kJ/kg K', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_hot_delta: float = INPUT(label='Max allowable decrease in hot discharge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_cold_delta: float = INPUT(label='Max allowable increase in cold discharge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_T_charge_min: float = INPUT(label='Min charge temp', units='C', type='NUMBER', group='TES', required='tes_type=2')
    tes_pb_f_oversize: float = INPUT(label='Packed bed oversize factor', type='NUMBER', group='TES', required='tes_type=2')
    rec_op_mode_initial: float = INPUT(label='Initial receiver operating mode 0: off, 1: startup, 2: on', units='-', type='NUMBER', group='System Control')
    defocus_initial: float = INPUT(label='Initial receiver defocus', units='-', type='NUMBER', group='System Control')
    T_in_loop_initial: float = INPUT(label='Initial loop inlet, cold header and cold runner fluid temperature', units='-', type='NUMBER', group='System Control')
    T_out_loop_initial: float = INPUT(label='Initial loop outlet, hot header and hot runner fluid temperature', units='-', type='NUMBER', group='System Control')
    T_out_scas_initial: Array = INPUT(label='Initial SCA outlet temperatures', units='-', type='ARRAY', group='System Control')
    pc_op_mode_initial: float = INPUT(label='Initial cycle operation mode 0:startup, 1:on, 2:standby, 3:off, 4:startup_controlled', units='-', type='NUMBER', group='System Control')
    pc_startup_time_remain_init: float = INPUT(label='Initial cycle startup time remaining', units='hr', type='NUMBER', group='System Control')
    pc_startup_energy_remain_initial: float = INPUT(label='Initial cycle startup energy remaining', units='kwh', type='NUMBER', group='System Control')
    T_tank_cold_init: float = INPUT(label='Initial cold tank fluid temperature', units='C', type='NUMBER', group='System Control')
    T_tank_hot_init: float = INPUT(label='Initial hot tank fluid temperate', units='C', type='NUMBER', group='System Control')
    is_dispatch_targets: float = INPUT(label='Run solution from user-specified dispatch targets?', units='-', type='NUMBER', group='System Control', required='?=0')
    q_pc_target_su_in: Array = INPUT(label='User-provided target thermal power to PC', units='MWt', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    q_pc_target_on_in: Array = INPUT(label='User-provided target thermal power to PC', units='MWt', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    q_pc_max_in: Array = INPUT(label='User-provided max thermal power to PC', units='MWt', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    is_rec_su_allowed_in: Array = INPUT(label='User-provided is receiver startup allowed?', units='-', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    is_pc_su_allowed_in: Array = INPUT(label='User-provided is power cycle startup allowed?', units='-', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    is_pc_sb_allowed_in: Array = INPUT(label='User-provided is power cycle standby allowed?', units='-', type='ARRAY', group='System Control', required='is_dispatch_targets=1')
    weekday_schedule: Matrix = INPUT(label='12x24 CSP operation Time-of-Use Weekday schedule', units='-', type='MATRIX', group='tou', required='*')
    weekend_schedule: Matrix = INPUT(label='12x24 CSP operation Time-of-Use Weekend schedule', units='-', type='MATRIX', group='tou', required='*')
    is_tod_pc_target_also_pc_max: float = INPUT(label='Is the TOD target cycle heat input also the max cycle heat input?', type='NUMBER', group='tou', required='?=0')
    is_dispatch: float = INPUT(label='Allow dispatch optimization?', units='-', type='NUMBER', group='tou', required='?=0')
    can_cycle_use_standby: float = INPUT(label='Can the cycle use standby operation?', type='NUMBER', group='tou', required='?=0')
    is_write_ampl_dat: float = INPUT(label='Write AMPL data files for dispatch run', units='-', type='NUMBER', group='tou', required='?=0')
    is_ampl_engine: float = INPUT(label='Run dispatch optimization with external AMPL engine', units='-', type='NUMBER', group='tou', required='?=0')
    ampl_data_dir: str = INPUT(label='AMPL data file directory', units='-', type='STRING', group='tou', required="?=''")
    ampl_exec_call: str = INPUT(label='System command to run AMPL code', units='-', type='STRING', group='tou', required="?='ampl sdk_solution.run'")
    disp_frequency: float = INPUT(label='Frequency for dispatch optimization calculations', units='hour', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_steps_per_hour: float = INPUT(label='Time steps per hour for dispatch optimization calculations', units='-', type='NUMBER', group='tou', required='?=1')
    disp_horizon: float = INPUT(label='Time horizon for dispatch optimization', units='hour', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_max_iter: float = INPUT(label='Max. no. dispatch optimization iterations', units='-', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_timeout: float = INPUT(label='Max. dispatch optimization solve duration', units='s', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_mip_gap: float = INPUT(label='Dispatch optimization solution tolerance', units='-', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_spec_presolve: float = INPUT(label='Dispatch optimization presolve heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_bb: float = INPUT(label='Dispatch optimization B&B heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_reporting: float = INPUT(label='Dispatch optimization reporting level', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_spec_scaling: float = INPUT(label='Dispatch optimization scaling heuristic', units='-', type='NUMBER', group='tou', required='?=-1')
    disp_time_weighting: float = INPUT(label='Dispatch optimization future time discounting factor', units='-', type='NUMBER', group='tou', required='?=0.99')
    disp_rsu_cost_rel: float = INPUT(label='Receiver startup cost', units='$/MWt/start', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_csu_cost_rel: float = INPUT(label='Cycle startup cost', units='$/MWe-cycle/start', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_pen_ramping: float = INPUT(label='Dispatch cycle production change penalty', units='$/MWe-change', type='NUMBER', group='tou', required='is_dispatch=1')
    disp_inventory_incentive: float = INPUT(label='Dispatch storage terminal inventory incentive multiplier', type='NUMBER', group='System Control', required='?=0.0')
    q_rec_standby: float = INPUT(label='Receiver standby energy consumption', units='kWt', type='NUMBER', group='tou', required='?=9e99')
    q_rec_heattrace: float = INPUT(label='Receiver heat trace energy consumption during startup', units='kWhe', type='NUMBER', group='tou', required='?=0.0')
    f_turb_tou_periods: Array = INPUT(label='Dispatch logic for turbine load fraction', units='-', type='ARRAY', group='tou', required='*')
    rec_su_delay: float = INPUT(label='Fixed startup delay time for the receiver', units='hr', type='NUMBER', group='System Control', required='*')
    rec_qf_delay: float = INPUT(label='Energy-based receiver startup delay (fraction of rated thermal power)', units='-', type='NUMBER', group='System Control', required='*')
    csp_financial_model: float = INPUT(units='1-8', type='NUMBER', group='Financial Model', required='?=1', constraints='INTEGER,MIN=0')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model 0: dispatch factors dispatch_factorX, 1: hourly multipliers dispatch_factors_ts', units='0/1', type='NUMBER', group='tou', required='?=0', constraints='INTEGER,MIN=0', meta='0=diurnal,1=timestep')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor array', type='ARRAY', group='tou', required='sim_type=1&ppa_multiplier_model=1&csp_financial_model<5&is_dispatch=1')
    ppa_soln_mode: float = INPUT(label='PPA solution mode (0=Specify IRR target, 1=Specify PPA price)', type='NUMBER', group='Financial Solution Mode', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
    en_electricity_rates: float = INPUT(label='Enable electricity rates for grid purchase', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0')
    dispatch_sched_weekday: Matrix = INPUT(label='12x24 PPA pricing Weekday schedule', type='MATRIX', group='tou', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
    dispatch_sched_weekend: Matrix = INPUT(label='12x24 PPA pricing Weekend schedule', type='MATRIX', group='tou', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
    dispatch_tod_factors: Array = INPUT(label='TOD factors for periods 1 through 9', type='ARRAY', group='Time of Delivery Factors', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1', meta='We added this array input after SAM 2022.12.21 to replace the functionality of former single value inputs dispatch_factor1 through dispatch_factor9')
    is_timestep_load_fractions: float = INPUT(label='Use turbine load fraction for each timestep instead of block dispatch?', type='NUMBER', group='tou', required='?=0')
    timestep_load_fractions: Array = INPUT(label='Turbine load fraction for each timestep, alternative to block dispatch', type='ARRAY', group='tou', required='?')
    ppa_price_input: Array = INPUT(label='PPA prices - yearly', units='$/kWh', type='ARRAY', group='Revenue', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1')
    mp_energy_market_revenue: Matrix = INPUT(label='Energy market revenue input', type='MATRIX', group='Revenue', required='sim_type=1&csp_financial_model=6&is_dispatch=1', meta='Lifetime x 2[Cleared Capacity(MW),Price($/MWh)]')
    pb_fixed_par: float = INPUT(label='Fraction of rated gross power constantly consumed', units='MWe/MWcap', type='NUMBER', group='system', required='*')
    bop_array: Array = INPUT(label='Balance of plant parasitic power fraction, mult frac and const, linear and quad coeff', type='ARRAY', group='system', required='*')
    aux_array: Array = INPUT(label='Auxiliary heater, mult frac and const, linear and quad coeff', type='ARRAY', group='system', required='*')
    gross_net_conversion_factor: float = INPUT(label='Estimated gross to net conversion factor', type='NUMBER', group='system', required='*')
    water_usage_per_wash: float = INPUT(label='Water usage per wash', units='L/m2_aper', type='NUMBER', group='system', required='*')
    washing_frequency: float = INPUT(label='Mirror washing frequency', units='-/year', type='NUMBER', group='system', required='*')
    calc_design_pipe_vals: float = INPUT(label='Calculate temps and pressures at design conditions for runners and headers', units='none', type='NUMBER', group='solar_field', required='*')
    V_hdr_cold_max: float = INPUT(label='Maximum HTF velocity in the cold headers at design', units='m/s', type='NUMBER', group='solar_field', required='*')
    V_hdr_cold_min: float = INPUT(label='Minimum HTF velocity in the cold headers at design', units='m/s', type='NUMBER', group='solar_field', required='*')
    V_hdr_hot_max: float = INPUT(label='Maximum HTF velocity in the hot headers at design', units='m/s', type='NUMBER', group='solar_field', required='*')
    V_hdr_hot_min: float = INPUT(label='Minimum HTF velocity in the hot headers at design', units='m/s', type='NUMBER', group='solar_field', required='*')
    N_max_hdr_diams: float = INPUT(label='Maximum number of diameters in each of the hot and cold headers', units='none', type='NUMBER', group='solar_field', required='*')
    L_rnr_pb: float = INPUT(label='Length of runner pipe in power block', units='m', type='NUMBER', group='powerblock', required='*')
    L_rnr_per_xpan: float = INPUT(label='Threshold length of straight runner pipe without an expansion loop', units='m', type='NUMBER', group='solar_field', required='*')
    L_xpan_hdr: float = INPUT(label='Compined perpendicular lengths of each header expansion loop', units='m', type='NUMBER', group='solar_field', required='*')
    L_xpan_rnr: float = INPUT(label='Compined perpendicular lengths of each runner expansion loop', units='m', type='NUMBER', group='solar_field', required='*')
    Min_rnr_xpans: float = INPUT(label='Minimum number of expansion loops per single-diameter runner section', units='none', type='NUMBER', group='solar_field', required='*')
    northsouth_field_sep: float = INPUT(label='North/south separation between subfields. 0 = SCAs are touching', units='m', type='NUMBER', group='solar_field', required='*')
    N_hdr_per_xpan: float = INPUT(label='Number of collector loops per expansion loop', units='none', type='NUMBER', group='solar_field', required='*')
    offset_xpan_hdr: float = INPUT(label='Location of first header expansion loop. 1 = after first collector loop', units='none', type='NUMBER', group='solar_field', required='*')
    custom_sf_pipe_sizes: float = INPUT(label='Use custom solar field pipe diams, wallthks, and lengths', units='none', type='NUMBER', group='solar_field', required='*')
    sf_rnr_diams: Matrix = INPUT(label='Custom runner diameters', units='m', type='MATRIX', group='solar_field', required='*')
    sf_rnr_wallthicks: Matrix = INPUT(label='Custom runner wall thicknesses', units='m', type='MATRIX', group='solar_field', required='*')
    sf_rnr_lengths: Matrix = INPUT(label='Custom runner lengths', units='m', type='MATRIX', group='solar_field', required='*')
    sf_hdr_diams: Matrix = INPUT(label='Custom header diameters', units='m', type='MATRIX', group='solar_field', required='*')
    sf_hdr_wallthicks: Matrix = INPUT(label='Custom header wall thicknesses', units='m', type='MATRIX', group='solar_field', required='*')
    sf_hdr_lengths: Matrix = INPUT(label='Custom header lengths', units='m', type='MATRIX', group='solar_field', required='*')
    has_hot_tank_bypass: float = INPUT(label='Bypass valve connects field outlet to cold tank', units='-', type='NUMBER', group='controller', required='*')
    T_tank_hot_inlet_min: float = INPUT(label='Minimum hot tank htf inlet temperature', units='C', type='NUMBER', group='controller', required='*')
    tes_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through tes loop', units='kW/(kg/s)', type='NUMBER', group='controller', required='*')
    V_tes_des: float = INPUT(label='Design-point velocity to size the TES pipe diameters', units='m/s', type='NUMBER', group='controller', required='*')
    custom_tes_p_loss: float = INPUT(label='TES pipe losses are based on custom lengths and coeffs', units='-', type='NUMBER', group='controller', required='*')
    k_tes_loss_coeffs: Matrix = INPUT(label='Minor loss coeffs for the coll, gen, and bypass loops', units='-', type='MATRIX', group='controller', required='*')
    custom_tes_pipe_sizes: float = INPUT(label='Use custom TES pipe diams, wallthks, and lengths', units='-', type='NUMBER', group='controller', required='*')
    tes_diams: Matrix = INPUT(label='Custom TES diameters', units='m', type='MATRIX', group='controller', required='custom_tes_pipe_sizes=1')
    tes_wallthicks: Matrix = INPUT(label='Custom TES wall thicknesses', units='m', type='MATRIX', group='controller', required='custom_tes_pipe_sizes=1')
    tes_lengths: Matrix = INPUT(label='Custom TES lengths', units='m', type='MATRIX', group='controller', required='custom_tes_pipe_sizes=1')
    DP_SGS: float = INPUT(label='Pressure drop within the steam generator', units='bar', type='NUMBER', group='controller', required='*')
    use_solar_mult_or_aperture_area: float = INPUT(label='Use solar multiple or total field aperture area', units='-', type='NUMBER', group='controller', required='?=0')
    specified_solar_multiple: float = INPUT(label='specified_solar_multiple', units='-', type='NUMBER', group='controller', required='*')
    specified_total_aperture: float = INPUT(label='specified_total_aperture', units='-', type='NUMBER', group='controller', required='*')
    non_solar_field_land_area_multiplier: float = INPUT(label='non_solar_field_land_area_multiplier', units='-', type='NUMBER', group='controller', required='*')
    trough_loop_control: Array = INPUT(label='trough_loop_control', units='-', type='ARRAY', group='controller', required='*')
    piping_loss: float = INPUT(label='Thermal loss per meter of piping', units='Wt/m', type='NUMBER', group='Tower and Receiver')
    disp_csu_cost: float = INPUT(label='Cycle startup cost', units='$', type='NUMBER', group='System Control')
    disp_rsu_cost: float = INPUT(label='Receiver startup cost', units='$', type='NUMBER', group='System Control')
    disp_pen_delta_w: float = INPUT(label='Dispatch cycle production change penalty', units='$/kWe-change', type='NUMBER', group='tou')
    P_boil: float = INPUT(label='Boiler operating pressure', units='bar', type='NUMBER', group='powerblock')
    csp_dtr_cost_site_improvements_cost_per_m2: float = INPUT(name='csp.dtr.cost.site_improvements.cost_per_m2', label='Site Improvement Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_solar_field_cost_per_m2: float = INPUT(name='csp.dtr.cost.solar_field.cost_per_m2', label='Solar Field Cost per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_htf_system_cost_per_m2: float = INPUT(name='csp.dtr.cost.htf_system.cost_per_m2', label='HTF System Cost Per m2', units='$/m2', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_storage_cost_per_kwht: float = INPUT(name='csp.dtr.cost.storage.cost_per_kwht', label='Storage cost per kWht', units='$/kWht', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_fossil_backup_cost_per_kwe: float = INPUT(name='csp.dtr.cost.fossil_backup.cost_per_kwe', label='Fossil Backup Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_power_plant_cost_per_kwe: float = INPUT(name='csp.dtr.cost.power_plant.cost_per_kwe', label='Power Plant Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_bop_per_kwe: float = INPUT(name='csp.dtr.cost.bop_per_kwe', label='Balance of Plant Cost per kWe', units='$/kWe', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_contingency_percent: float = INPUT(name='csp.dtr.cost.contingency_percent', label='Contingency Percent', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_epc_per_acre: float = INPUT(name='csp.dtr.cost.epc.per_acre', label='EPC Costs per acre', units='$/acre', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_epc_percent: float = INPUT(name='csp.dtr.cost.epc.percent', label='EPC Costs % direct', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_epc_per_watt: float = INPUT(name='csp.dtr.cost.epc.per_watt', label='EPC Cost Wac', units='$/Wac', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_epc_fixed: float = INPUT(name='csp.dtr.cost.epc.fixed', label='Fixed EPC Cost', units='$', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_plm_per_acre: float = INPUT(name='csp.dtr.cost.plm.per_acre', label='Land Cost per acre', units='$/acre', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_plm_percent: float = INPUT(name='csp.dtr.cost.plm.percent', label='Land Cost % direct', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_plm_per_watt: float = INPUT(name='csp.dtr.cost.plm.per_watt', label='Land Cost Wac', units='$/Wac', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_plm_fixed: float = INPUT(name='csp.dtr.cost.plm.fixed', label='Fixed Land Cost', units='$', type='NUMBER', group='Capital_Costs', required='?=0')
    csp_dtr_cost_sales_tax_percent: float = INPUT(name='csp.dtr.cost.sales_tax.percent', label='Sales Tax Percentage of Direct Cost', units='%', type='NUMBER', group='Capital_Costs', required='?=0')
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
    system_capacity: Final[float] = OUTPUT(label='System capacity', units='kWe', type='NUMBER', group='System Costs', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWe', type='NUMBER', group='System Costs', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWe', type='NUMBER', group='System Costs', required='*')
    q_dot_cycle_des: Final[float] = OUTPUT(label='Cycle thermal power at design', units='MWt', type='NUMBER', group='Power Cycle', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    solar_mult: Final[float] = OUTPUT(label='Actual solar multiple', type='NUMBER', group='System Design Calc', required='*')
    nSCA: Final[float] = OUTPUT(label='Number of SCAs in a loop', units='none', type='NUMBER', group='solar_field', required='*')
    field_htf_min_temp: Final[float] = OUTPUT(label='Minimum field htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    field_htf_max_temp: Final[float] = OUTPUT(label='Maximum field htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    field_htf_cp_avg_des: Final[float] = OUTPUT(label='Field average htf cp at design', units='kJ/kgK', type='NUMBER', group='Solar Field', required='*')
    single_loop_aperture: Final[float] = OUTPUT(label='Single loop aperture', units='m2', type='NUMBER', group='Solar Field', required='*')
    min_inner_diameter: Final[float] = OUTPUT(label='Minimum absorber inner diameter in loop', units='m', type='NUMBER', group='Solar Field', required='*')
    csp_dtr_hce_design_heat_losses: Final[Array] = OUTPUT(label='Heat loss at design', units='W/m', type='ARRAY', group='Solar Field', required='*')
    csp_dtr_loop_hce_heat_loss: Final[float] = OUTPUT(label='Loop Heat Loss from HCE at Design', units='W/m', type='NUMBER', group='Solar Field', required='*')
    csp_dtr_sca_calc_sca_effs: Final[Array] = OUTPUT(label='SCA optical efficiencies at design', type='ARRAY', group='Solar Field', required='*')
    loop_optical_efficiency: Final[float] = OUTPUT(label='Loop total optical effiency at design', type='NUMBER', group='Solar Field', required='*')
    csp_dtr_hce_optical_effs: Final[Array] = OUTPUT(label='HCE optical efficiencies at design', type='ARRAY', group='Solar Field', required='*')
    SCAInfoArray: Final[Matrix] = OUTPUT(label='Receiver (,1) and collector (,2) type for each assembly in loop', type='MATRIX', group='Solar Field', required='*')
    SCADefocusArray: Final[Array] = OUTPUT(label="Order in which the SCA's should be defocused", type='ARRAY', group='Solar Field', required='*')
    max_field_flow_velocity: Final[float] = OUTPUT(label='Maximum field flow velocity', units='m/s', type='NUMBER', group='Solar Field', required='*')
    min_field_flow_velocity: Final[float] = OUTPUT(label='Minimum field flow velocity', units='m/s', type='NUMBER', group='Solar Field', required='*')
    m_dot_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop HTF flow rate', units='kg/s', type='NUMBER', group='solar_field', required='*')
    m_dot_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop HTF flow rate', units='kg/s', type='NUMBER', group='solar_field', required='*')
    f_htfmin_actual: Final[float] = OUTPUT(label='Actual minimum loop mass flow rate fraction of design', type='NUMBER', group='solar_field', required='*')
    f_htfmax_actual: Final[float] = OUTPUT(label='Actual maximum loop mass flow rate fraction of design', type='NUMBER', group='solar_field', required='*')
    max_loop_flow_vel_des: Final[float] = OUTPUT(label='Maximum loop flow velocity at design', units='m/s', type='NUMBER', group='Solar Field', required='*')
    min_loop_flow_vel_des: Final[float] = OUTPUT(label='Minimum loop flow velocity at design', units='m/s', type='NUMBER', group='Solar Field', required='*')
    total_loop_conversion_efficiency: Final[float] = OUTPUT(label='Total Loop Conversion Efficiency at Design', type='NUMBER', group='Solar Field', required='*')
    total_required_aperture_for_SM1: Final[float] = OUTPUT(label='Aperture required for solar mult = 1', units='m2', type='NUMBER', group='Solar Field', required='*')
    required_number_of_loops_for_SM1: Final[float] = OUTPUT(label='Heat loss at design', type='NUMBER', group='Solar Field', required='*')
    nLoops: Final[float] = OUTPUT(label='Number of loops in the field', type='NUMBER', group='Solar Field', required='*')
    total_aperture: Final[float] = OUTPUT(label='Total field aperture area', units='m2', type='NUMBER', group='Solar Field', required='*')
    fixed_land_area: Final[float] = OUTPUT(label='Fixed Land Area', units='acre', type='NUMBER', group='Solar Field', required='*')
    total_land_area: Final[float] = OUTPUT(label='Total Land Area', units='acre', type='NUMBER', group='Solar Field', required='*')
    total_tracking_power: Final[float] = OUTPUT(label='Total Tracking Power', units='MWe', type='NUMBER', group='Solar Field', required='*')
    K_cpnt: Final[Matrix] = OUTPUT(label='Minor loss coefficients of the components in each loop interconnect', type='MATRIX', group='Solar Field', required='*')
    D_cpnt: Final[Matrix] = OUTPUT(label='Inner diameters of the components in each loop interconnect', units='m', type='MATRIX', group='Solar Field', required='*')
    L_cpnt: Final[Matrix] = OUTPUT(label='Lengths of the components in each loop interconnect', units='m', type='MATRIX', group='Solar Field', required='*')
    Type_cpnt: Final[Matrix] = OUTPUT(label='Type of component in each loop interconnect [0=fitting | 1=pipe | 2=flex_hose]', units='Wm', type='MATRIX', group='Solar Field', required='*')
    field_thermal_output_actual: Final[float] = OUTPUT(label='Design-point thermal power from the solar field limited by mass flow', units='MW', type='NUMBER', group='Solar Field', required='*')
    field_thermal_output_ideal: Final[float] = OUTPUT(label='Design-point thermal power from the solar field with no limit', units='MW', type='NUMBER', group='Solar Field', required='*')
    dP_sf_SS: Final[float] = OUTPUT(label='Steady State field pressure drop', units='bar', type='NUMBER', group='Solar Field', required='*')
    W_dot_pump_SS: Final[float] = OUTPUT(label='Steady State pumping power', units='MWe', type='NUMBER', group='Solar Field', required='*')
    vol_tank: Final[float] = OUTPUT(label='Total tank volume', units='m3', type='NUMBER', group='Thermal Storage', required='*')
    q_tes: Final[float] = OUTPUT(label='TES design capacity', units='MWt-hr', type='NUMBER', group='Thermal Storage', required='*')
    csp_pt_tes_tank_height: Final[float] = OUTPUT(label='Tank height', units='m', type='NUMBER', group='Thermal Storage', required='*')
    csp_pt_tes_tank_diameter: Final[float] = OUTPUT(label='Tank diameter', units='m', type='NUMBER', group='Thermal Storage', required='*')
    q_dot_tes_est: Final[float] = OUTPUT(label='Estimated TES Heat Loss', units='MW', type='NUMBER', group='Thermal Storage', required='*')
    csp_pt_tes_htf_density: Final[float] = OUTPUT(label='Storage htf density', units='kg/m3', type='NUMBER', group='Thermal Storage', required='*')
    tes_avail_vol: Final[float] = OUTPUT(label='Available HTF volume', units='m3', type='NUMBER', group='Thermal Storage', required='*')
    is_hx: Final[float] = OUTPUT(label='System has heat exchanger no/yes (0/1)', type='NUMBER', group='Thermal Storage', required='*')
    vol_min: Final[float] = OUTPUT(label='Minimum Fluid Volume', units='m3', type='NUMBER', group='Thermal Storage', required='*')
    V_tank_hot_ini: Final[float] = OUTPUT(label='Initial hot tank volume', units='m3', type='NUMBER', group='Thermal Storage', required='*')
    tes_htf_avg_temp: Final[float] = OUTPUT(label='HTF Average Temperature at Design', units='C', type='NUMBER', group='Thermal Storage', required='*')
    tes_htf_min_temp: Final[float] = OUTPUT(label='Minimum storage htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    tes_htf_max_temp: Final[float] = OUTPUT(label='Maximum storage htf temp', units='C', type='NUMBER', group='Power Cycle', required='*')
    csp_dtr_sca_ap_lengths: Final[Matrix] = OUTPUT(label='Length of single module', units='m', type='MATRIX', group='Collector', required='?=0')
    csp_dtr_sca_calc_zenith: Final[float] = OUTPUT(label='Calculated zenith', units='degree', type='NUMBER', group='Collector', required='?=0')
    csp_dtr_sca_calc_costh: Final[float] = OUTPUT(label='Calculated costheta', type='NUMBER', group='Collector', required='?=0')
    csp_dtr_sca_calc_theta: Final[float] = OUTPUT(label='Calculated theta', units='degree', type='NUMBER', group='Collector', required='?=0')
    csp_dtr_sca_calc_end_gains: Final[Matrix] = OUTPUT(label='End gain factor', type='MATRIX', group='Collector', required='?=0')
    csp_dtr_sca_calc_end_losses: Final[Matrix] = OUTPUT(label='Use time-series net electricity generation limits', type='MATRIX', group='Collector', required='?=0')
    csp_dtr_sca_calc_latitude: Final[float] = OUTPUT(label='Latitude', units='degree', type='NUMBER', group='Collector', required='?=0')
    csp_dtr_sca_calc_iams: Final[Matrix] = OUTPUT(label='IAM at summer solstice', type='MATRIX', group='Collector', required='?=0')
    m_dot_htf_cycle_des: Final[float] = OUTPUT(label='PC mass flow rate at design', units='kg/s', type='NUMBER', group='Power Cycle', required='*')
    bop_design: Final[float] = OUTPUT(label='BOP parasitic at design', units='MWe', type='NUMBER', group='System Control', required='*')
    aux_design: Final[float] = OUTPUT(label='Aux parasitic at design', units='MWe', type='NUMBER', group='System Control', required='*')
    csp_dtr_cost_site_improvements: Final[float] = OUTPUT(name='csp.dtr.cost.site_improvements', label='Site improvements cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_solar_field: Final[float] = OUTPUT(name='csp.dtr.cost.solar_field', label='Solar field cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_htf_system: Final[float] = OUTPUT(name='csp.dtr.cost.htf_system', label='HTF system cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_storage: Final[float] = OUTPUT(name='csp.dtr.cost.storage', label='Thermal storage cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_fossil_backup: Final[float] = OUTPUT(name='csp.dtr.cost.fossil_backup', label='Fossil backup cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_power_plant: Final[float] = OUTPUT(name='csp.dtr.cost.power_plant', label='Power plant cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_bop: Final[float] = OUTPUT(name='csp.dtr.cost.bop', label='Balance of plant cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_contingency: Final[float] = OUTPUT(name='csp.dtr.cost.contingency', label='Contingency cost', units='$', type='NUMBER', group='Capital Costs')
    total_direct_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    direct_subtotal: Final[float] = OUTPUT(label='Direct subtotal', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_epc_total: Final[float] = OUTPUT(name='csp.dtr.cost.epc.total', label='EPC total cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_plm_total: Final[float] = OUTPUT(name='csp.dtr.cost.plm.total', label='Total land cost', units='$', type='NUMBER', group='Capital Costs')
    total_indirect_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_sales_tax_total: Final[float] = OUTPUT(name='csp.dtr.cost.sales_tax.total', label='Sales tax total', units='$', type='NUMBER', group='Capital Costs')
    total_installed_cost: Final[float] = OUTPUT(label='Total installed cost', units='$', type='NUMBER', group='Capital Costs')
    csp_dtr_cost_installed_per_capacity: Final[float] = OUTPUT(name='csp.dtr.cost.installed_per_capacity', label='Estimated total installed cost per net capacity ($/kW)', units='$/kW', type='NUMBER', group='Capital Costs')
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
    Theta_ave: Final[Array] = OUTPUT(label='Field collector solar incidence angle', units='deg', type='ARRAY', group='solar_field', required='sim_type=1')
    CosTh_ave: Final[Array] = OUTPUT(label='Field collector cosine efficiency', type='ARRAY', group='solar_field', required='sim_type=1')
    IAM_ave: Final[Array] = OUTPUT(label='Field collector incidence angle modifier', type='ARRAY', group='solar_field', required='sim_type=1')
    RowShadow_ave: Final[Array] = OUTPUT(label='Field collector row shadowing loss', type='ARRAY', group='solar_field', required='sim_type=1')
    EndLoss_ave: Final[Array] = OUTPUT(label='Field collector optical end loss', type='ARRAY', group='solar_field', required='sim_type=1')
    dni_costh: Final[Array] = OUTPUT(label='Field collector DNI-cosine product', units='W/m2', type='ARRAY', group='solar_field', required='sim_type=1')
    EqOpteff: Final[Array] = OUTPUT(label='Field optical efficiency before defocus', type='ARRAY', group='solar_field', required='sim_type=1')
    SCAs_def: Final[Array] = OUTPUT(label='Field fraction of focused SCAs', type='ARRAY', group='solar_field', required='sim_type=1')
    q_inc_sf_tot: Final[Array] = OUTPUT(label='Field thermal power incident', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    qinc_costh: Final[Array] = OUTPUT(label='Field thermal power incident after cosine', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_rec_inc: Final[Array] = OUTPUT(label='Receiver thermal power incident', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_rec_thermal_loss: Final[Array] = OUTPUT(label='Receiver thermal losses', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_rec_abs: Final[Array] = OUTPUT(label='Receiver thermal power absorbed', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_piping_loss: Final[Array] = OUTPUT(label='Field piping thermal losses', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    e_dot_field_int_energy: Final[Array] = OUTPUT(label='Field change in material/htf internal energy', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_htf_sf_out: Final[Array] = OUTPUT(label='Field thermal power leaving in HTF', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    q_dot_freeze_prot: Final[Array] = OUTPUT(label='Field freeze protection required', units='MWt', type='ARRAY', group='solar_field', required='sim_type=1')
    m_dot_loop: Final[Array] = OUTPUT(label='Receiver mass flow rate', units='kg/s', type='ARRAY', group='solar_field', required='sim_type=1')
    m_dot_field_recirc: Final[Array] = OUTPUT(label='Field total mass flow recirculated', units='kg/s', type='ARRAY', group='solar_field', required='sim_type=1')
    m_dot_field_delivered: Final[Array] = OUTPUT(label='Field total mass flow delivered', units='kg/s', type='ARRAY', group='solar_field', required='sim_type=1')
    T_field_cold_in: Final[Array] = OUTPUT(label='Field timestep-averaged inlet temperature', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    T_rec_cold_in: Final[Array] = OUTPUT(label='Loop timestep-averaged inlet temperature', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    T_rec_hot_out: Final[Array] = OUTPUT(label='Loop timestep-averaged outlet temperature', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    T_field_hot_out: Final[Array] = OUTPUT(label='Field timestep-averaged outlet temperature', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    deltaP_field: Final[Array] = OUTPUT(label='Field pressure drop', units='bar', type='ARRAY', group='solar_field', required='sim_type=1')
    vel_loop_min: Final[Array] = OUTPUT(label='Receiver min HTF velocity in loop', units='m/s', type='ARRAY', group='solar_field', required='sim_type=1')
    vel_loop_max: Final[Array] = OUTPUT(label='Receiver max HTF velocity in loop', units='m/s', type='ARRAY', group='solar_field', required='sim_type=1')
    W_dot_sca_track: Final[Array] = OUTPUT(label='Field collector tracking power', units='MWe', type='ARRAY', group='solar_field', required='sim_type=1')
    W_dot_field_pump: Final[Array] = OUTPUT(label='Field htf pumping power', units='MWe', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_diams: Final[Array] = OUTPUT(label='Field piping header diameters', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_wallthk: Final[Array] = OUTPUT(label='Field piping header wall thicknesses', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_lengths: Final[Array] = OUTPUT(label='Field piping header lengths', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_expansions: Final[Array] = OUTPUT(label='Number of field piping header expansions', units='-', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_mdot_dsn: Final[Array] = OUTPUT(label='Field piping header mass flow at design', units='kg/s', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_vel_dsn: Final[Array] = OUTPUT(label='Field piping header velocity at design', units='m/s', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_T_dsn: Final[Array] = OUTPUT(label='Field piping header temperature at design', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_header_P_dsn: Final[Array] = OUTPUT(label='Field piping header pressure at design', units='bar', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_diams: Final[Array] = OUTPUT(label='Field piping runner diameters', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_wallthk: Final[Array] = OUTPUT(label='Field piping runner wall thicknesses', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_lengths: Final[Array] = OUTPUT(label='Field piping runner lengths', units='m', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_expansions: Final[Array] = OUTPUT(label='Number of field piping runner expansions', units='-', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_mdot_dsn: Final[Array] = OUTPUT(label='Field piping runner mass flow at design', units='kg/s', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_vel_dsn: Final[Array] = OUTPUT(label='Field piping runner velocity at design', units='m/s', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_T_dsn: Final[Array] = OUTPUT(label='Field piping runner temperature at design', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_runner_P_dsn: Final[Array] = OUTPUT(label='Field piping runner pressure at design', units='bar', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_loop_T_dsn: Final[Array] = OUTPUT(label='Field piping loop temperature at design', units='C', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_loop_P_dsn: Final[Array] = OUTPUT(label='Field piping loop pressure at design', units='bar', type='ARRAY', group='solar_field', required='sim_type=1')
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
    vol_tes_cold: Final[Array] = OUTPUT(label='TES cold fluid volume', units='m3', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    vol_tes_hot: Final[Array] = OUTPUT(label='TES hot fluid volume', units='m3', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    vol_tes_tot: Final[Array] = OUTPUT(label='TES total fluid volume', units='m3', type='ARRAY', group='TES', required='sim_type=1')
    tes_piston_loc: Final[Array] = OUTPUT(label='TES piston distance from left (cold) side', units='m', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_piston_frac: Final[Array] = OUTPUT(label='TES piston fraction of cold distance over total', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_cold_vol_frac: Final[Array] = OUTPUT(label='TES volume fraction of cold over total', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_mass_tot: Final[Array] = OUTPUT(label='TES total fluid mass', units='kg', type='ARRAY', group='TES', required='sim_type=1')
    tes_SA_cold: Final[Array] = OUTPUT(label='TES cold side surface area', units='m2', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_SA_hot: Final[Array] = OUTPUT(label='TES hot side surface area', units='m2', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_SA_tot: Final[Array] = OUTPUT(label='TES total surface area', units='m2', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_error: Final[Array] = OUTPUT(label='TES energy balance error', units='MWt', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_error_percent: Final[Array] = OUTPUT(label='TES energy balance error percent', units='%', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_leak_error: Final[Array] = OUTPUT(label='TES energy balance error due to leakage assumption', units='MWt', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_wall_error: Final[Array] = OUTPUT(label='TES energy balance error due to wall temperature assumption', units='MWt', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    tes_error_corrected: Final[Array] = OUTPUT(label='TES energy balance error, accounting for wall and temperature assumption error', units='MWt', type='ARRAY', group='TES', required='sim_type=1&tes_type=3')
    T_grad_0: Final[Array] = OUTPUT(label='TES Temperature gradient 0 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_1: Final[Array] = OUTPUT(label='TES Temperature gradient 1 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_2: Final[Array] = OUTPUT(label='TES Temperature gradient 2 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_3: Final[Array] = OUTPUT(label='TES Temperature gradient 3 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_4: Final[Array] = OUTPUT(label='TES Temperature gradient 4 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_5: Final[Array] = OUTPUT(label='TES Temperature gradient 5 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_6: Final[Array] = OUTPUT(label='TES Temperature gradient 6 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_7: Final[Array] = OUTPUT(label='TES Temperature gradient 7 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_8: Final[Array] = OUTPUT(label='TES Temperature gradient 8 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    T_grad_9: Final[Array] = OUTPUT(label='TES Temperature gradient 9 indice', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=2')
    op_mode_1: Final[Array] = OUTPUT(label='1st operating mode', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_2: Final[Array] = OUTPUT(label='2nd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    op_mode_3: Final[Array] = OUTPUT(label='3rd op. mode, if applicable', type='ARRAY', group='solver', required='sim_type=1')
    m_dot_balance: Final[Array] = OUTPUT(label='Relative mass flow balance error', type='ARRAY', group='solver', required='sim_type=1')
    q_balance: Final[Array] = OUTPUT(label='Relative energy balance error', type='ARRAY', group='solver', required='sim_type=1')
    monthly_energy: Final[Array] = OUTPUT(label='Monthly AC energy in Year 1', units='kWh', type='ARRAY', group='Post-process', required='sim_type=1', constraints='LENGTH=12')
    annual_energy: Final[float] = OUTPUT(label='Annual net electrical energy w/ avail. derate', units='kWhe', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_thermal_consumption: Final[float] = OUTPUT(label='Annual thermal freeze protection required', units='kWht', type='NUMBER', group='Post-process', required='sim_type=1')
    annual_total_water_use: Final[float] = OUTPUT(label='Total Annual Water Usage', units='m^3', type='NUMBER', group='Post-process', required='sim_type=1')
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
    disp_qsfsu_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field startup energy', units='MWt', type='ARRAY', group='tou', required='sim_type=1')
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
    P_out_net: Final[Array] = OUTPUT(label='System net electrical power', units='MWe', type='ARRAY', group='system', required='sim_type=1')
    gen: Final[Array] = OUTPUT(label='System net electrical power w/ avail. derate', units='kWe', type='ARRAY', group='system', required='sim_type=1')
    annual_W_cycle_gross: Final[float] = OUTPUT(label='Electrical source - Power cycle gross output', units='kWhe', type='NUMBER', group='system', required='sim_type=1')
    conversion_factor: Final[float] = OUTPUT(label='Gross to Net Conversion Factor', units='%', type='NUMBER', group='system', required='sim_type=1')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='system', required='sim_type=1')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', group='system', required='sim_type=1')
    sim_duration: Final[float] = OUTPUT(label='Computational time of timeseries simulation', units='s', type='NUMBER', group='system', required='sim_type=1')
    recirculating: Final[Array] = OUTPUT(label='Field recirculating (bypass valve open)', units='-', type='ARRAY', group='solar_field', required='sim_type=1')
    pipe_tes_diams: Final[Array] = OUTPUT(label='Pipe diameters in TES', units='m', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_wallthk: Final[Array] = OUTPUT(label='Pipe wall thickness in TES', units='m', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_lengths: Final[Array] = OUTPUT(label='Pipe lengths in TES', units='m', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_mdot_dsn: Final[Array] = OUTPUT(label='Mass flow TES pipes at design conditions', units='kg/s', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_vel_dsn: Final[Array] = OUTPUT(label='Velocity in TES pipes at design conditions', units='m/s', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_T_dsn: Final[Array] = OUTPUT(label='Temperature in TES pipes at design conditions', units='C', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    pipe_tes_P_dsn: Final[Array] = OUTPUT(label='Pressure in TES pipes at design conditions', units='bar', type='ARRAY', group='TES', required='sim_type=1&tes_type=1')
    rec_op_mode_final: Final[Array] = OUTPUT(label='Final receiver operating mode 0: off, 1: startup, 2: on', units='-', type='ARRAY', group='System Control')
    defocus_final: Final[Array] = OUTPUT(label='Defocus final', units='-', type='ARRAY', group='System Control')
    T_in_loop_final: Final[Array] = OUTPUT(label='Final loop inlet, cold header and cold runner fluid temperature', units='-', type='ARRAY', group='System Control')
    T_out_loop_final: Final[Array] = OUTPUT(label='Final loop outlet, hot header and hot runner fluid temperature', units='-', type='ARRAY', group='System Control')
    T_out_scas_last_final: Final[Array] = OUTPUT(label='Final SCA outlet temperatures', units='-', type='ARRAY', group='System Control')
    pc_op_mode_final: Final[Array] = OUTPUT(label='Final cycle operation mode 0:startup, 1:on, 2:standby, 3:off, 4:startup_controlled', units='-', type='ARRAY', group='System Control')
    pc_startup_time_remain_final: Final[Array] = OUTPUT(label='Final cycle startup time remaining', units='hr', type='ARRAY', group='System Control')
    pc_startup_energy_remain_final: Final[Array] = OUTPUT(label='Final cycle startup energy remaining', units='kwh', type='ARRAY', group='System Control')
    hot_tank_htf_percent_final: Final[Array] = OUTPUT(label='Final percent fill of available hot tank mass', units='%', type='ARRAY', group='System Control')
    cycle_eff_load_table: Final[Matrix] = OUTPUT(label='Cycle efficiency vs. load', type='MATRIX', required='sim_type=1')
    cycle_Tdb_table: Final[Matrix] = OUTPUT(label='Normalized cycle efficiency and condenser power vs. ambient temperature', type='MATRIX', required='sim_type=1')
    adjust_constant: float = INPUT(label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='MAX=100', meta="'adjust' and 'constant' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_timeindex: float = INPUT(label='Enable lifetime adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_en_periods: float = INPUT(label='Enable period-based adjustment factors', units='0/1', type='NUMBER', group='Adjustment Factors', required='?=0', constraints='BOOLEAN', meta="'adjust' and 'en_periods' separated by _ instead of : after SAM 2022.12.21")
    adjust_timeindex: Array = INPUT(label='Lifetime adjustment factors', units='%', type='ARRAY', group='Adjustment Factors', required='adjust_en_timeindex=1', meta="'adjust' and 'timeindex' separated by _ instead of : after SAM 2022.12.21")
    adjust_periods: Matrix = INPUT(label='Period-based adjustment factors', units='%', type='MATRIX', group='Adjustment Factors', required='adjust_en_periods=1', constraints='COLS=3', meta="Syntax: n x 3 matrix [ start, end, loss ]; Version upgrade: 'adjust' and 'periods' separated by _ instead of : after SAM 2022.12.21")

    def __init__(self, *args: Mapping[str, Any],
                 sim_type: float = ...,
                 time_start: float = ...,
                 time_stop: float = ...,
                 time_steps_per_hour: float = ...,
                 vacuum_arrays: float = ...,
                 file_name: str = ...,
                 solar_resource_data: Table = ...,
                 nHCEt: float = ...,
                 nColt: float = ...,
                 nHCEVar: float = ...,
                 FieldConfig: float = ...,
                 include_fixed_power_block_runner: float = ...,
                 L_power_block_piping: float = ...,
                 eta_pump: float = ...,
                 Fluid: float = ...,
                 accept_loc: float = ...,
                 HDR_rough: float = ...,
                 theta_stow: float = ...,
                 theta_dep: float = ...,
                 Row_Distance: float = ...,
                 T_loop_in_des: float = ...,
                 T_loop_out: float = ...,
                 T_startup: float = ...,
                 T_shutdown: float = ...,
                 use_abs_or_rel_mdot_limit: float = ...,
                 m_dot_htfmin: float = ...,
                 m_dot_htfmax: float = ...,
                 f_htfmin: float = ...,
                 f_htfmax: float = ...,
                 field_fl_props: Matrix = ...,
                 T_fp: float = ...,
                 I_bn_des: float = ...,
                 Pipe_hl_coef: float = ...,
                 SCA_drives_elec: float = ...,
                 tilt: float = ...,
                 azimuth: float = ...,
                 wind_stow_speed: float = ...,
                 accept_mode: float = ...,
                 accept_init: float = ...,
                 mc_bal_hot: float = ...,
                 mc_bal_cold: float = ...,
                 mc_bal_sca: float = ...,
                 W_aperture: Array = ...,
                 A_aperture: Array = ...,
                 TrackingError: Array = ...,
                 GeomEffects: Array = ...,
                 Rho_mirror_clean: Array = ...,
                 Dirt_mirror: Array = ...,
                 Error: Array = ...,
                 Ave_Focal_Length: Array = ...,
                 L_SCA: Array = ...,
                 L_aperture: Array = ...,
                 ColperSCA: Array = ...,
                 Distance_SCA: Array = ...,
                 IAM_matrix: Matrix = ...,
                 HCE_FieldFrac: Matrix = ...,
                 D_2: Matrix = ...,
                 D_3: Matrix = ...,
                 D_4: Matrix = ...,
                 D_5: Matrix = ...,
                 D_p: Matrix = ...,
                 Flow_type: Matrix = ...,
                 Rough: Matrix = ...,
                 alpha_env: Matrix = ...,
                 epsilon_3_11: Matrix = ...,
                 epsilon_3_12: Matrix = ...,
                 epsilon_3_13: Matrix = ...,
                 epsilon_3_14: Matrix = ...,
                 epsilon_3_21: Matrix = ...,
                 epsilon_3_22: Matrix = ...,
                 epsilon_3_23: Matrix = ...,
                 epsilon_3_24: Matrix = ...,
                 epsilon_3_31: Matrix = ...,
                 epsilon_3_32: Matrix = ...,
                 epsilon_3_33: Matrix = ...,
                 epsilon_3_34: Matrix = ...,
                 epsilon_3_41: Matrix = ...,
                 epsilon_3_42: Matrix = ...,
                 epsilon_3_43: Matrix = ...,
                 epsilon_3_44: Matrix = ...,
                 alpha_abs: Matrix = ...,
                 Tau_envelope: Matrix = ...,
                 EPSILON_4: Matrix = ...,
                 EPSILON_5: Matrix = ...,
                 GlazingIntactIn: Matrix = ...,
                 P_a: Matrix = ...,
                 AnnulusGas: Matrix = ...,
                 AbsorberMaterial: Matrix = ...,
                 Shadowing: Matrix = ...,
                 Dirt_HCE: Matrix = ...,
                 Design_loss: Matrix = ...,
                 p_start: float = ...,
                 pc_config: float = ...,
                 P_ref: float = ...,
                 eta_ref: float = ...,
                 cycle_max_frac: float = ...,
                 cycle_cutoff_frac: float = ...,
                 q_sby_frac: float = ...,
                 startup_time: float = ...,
                 startup_frac: float = ...,
                 pb_pump_coef: float = ...,
                 dT_cw_ref: float = ...,
                 T_amb_des: float = ...,
                 CT: float = ...,
                 tech_type: float = ...,
                 T_approach: float = ...,
                 T_ITD_des: float = ...,
                 P_cond_ratio: float = ...,
                 pb_bd_frac: float = ...,
                 P_cond_min: float = ...,
                 n_pl_inc: float = ...,
                 F_wc: Array = ...,
                 ud_f_W_dot_cool_des: float = ...,
                 ud_m_dot_water_cool_des: float = ...,
                 ud_is_sco2_regr: float = ...,
                 ud_ind_od: Matrix = ...,
                 tes_type: float = ...,
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
                 store_fluid: float = ...,
                 store_fl_props: Matrix = ...,
                 dt_hot: float = ...,
                 tanks_in_parallel: float = ...,
                 tes_cyl_tank_thick: float = ...,
                 tes_cyl_tank_cp: float = ...,
                 tes_cyl_tank_dens: float = ...,
                 tes_cyl_piston_loss_poly: Array = ...,
                 tes_cyl_tank_insul_percent: float = ...,
                 tes_pb_n_xsteps: float = ...,
                 tes_pb_k_eff: float = ...,
                 tes_pb_void_frac: float = ...,
                 tes_pb_dens_solid: float = ...,
                 tes_pb_cp_solid: float = ...,
                 tes_pb_T_hot_delta: float = ...,
                 tes_pb_T_cold_delta: float = ...,
                 tes_pb_T_charge_min: float = ...,
                 tes_pb_f_oversize: float = ...,
                 rec_op_mode_initial: float = ...,
                 defocus_initial: float = ...,
                 T_in_loop_initial: float = ...,
                 T_out_loop_initial: float = ...,
                 T_out_scas_initial: Array = ...,
                 pc_op_mode_initial: float = ...,
                 pc_startup_time_remain_init: float = ...,
                 pc_startup_energy_remain_initial: float = ...,
                 T_tank_cold_init: float = ...,
                 T_tank_hot_init: float = ...,
                 is_dispatch_targets: float = ...,
                 q_pc_target_su_in: Array = ...,
                 q_pc_target_on_in: Array = ...,
                 q_pc_max_in: Array = ...,
                 is_rec_su_allowed_in: Array = ...,
                 is_pc_su_allowed_in: Array = ...,
                 is_pc_sb_allowed_in: Array = ...,
                 weekday_schedule: Matrix = ...,
                 weekend_schedule: Matrix = ...,
                 is_tod_pc_target_also_pc_max: float = ...,
                 is_dispatch: float = ...,
                 can_cycle_use_standby: float = ...,
                 is_write_ampl_dat: float = ...,
                 is_ampl_engine: float = ...,
                 ampl_data_dir: str = ...,
                 ampl_exec_call: str = ...,
                 disp_frequency: float = ...,
                 disp_steps_per_hour: float = ...,
                 disp_horizon: float = ...,
                 disp_max_iter: float = ...,
                 disp_timeout: float = ...,
                 disp_mip_gap: float = ...,
                 disp_spec_presolve: float = ...,
                 disp_spec_bb: float = ...,
                 disp_reporting: float = ...,
                 disp_spec_scaling: float = ...,
                 disp_time_weighting: float = ...,
                 disp_rsu_cost_rel: float = ...,
                 disp_csu_cost_rel: float = ...,
                 disp_pen_ramping: float = ...,
                 disp_inventory_incentive: float = ...,
                 q_rec_standby: float = ...,
                 q_rec_heattrace: float = ...,
                 f_turb_tou_periods: Array = ...,
                 rec_su_delay: float = ...,
                 rec_qf_delay: float = ...,
                 csp_financial_model: float = ...,
                 ppa_multiplier_model: float = ...,
                 dispatch_factors_ts: Array = ...,
                 ppa_soln_mode: float = ...,
                 en_electricity_rates: float = ...,
                 dispatch_sched_weekday: Matrix = ...,
                 dispatch_sched_weekend: Matrix = ...,
                 dispatch_tod_factors: Array = ...,
                 is_timestep_load_fractions: float = ...,
                 timestep_load_fractions: Array = ...,
                 ppa_price_input: Array = ...,
                 mp_energy_market_revenue: Matrix = ...,
                 pb_fixed_par: float = ...,
                 bop_array: Array = ...,
                 aux_array: Array = ...,
                 gross_net_conversion_factor: float = ...,
                 water_usage_per_wash: float = ...,
                 washing_frequency: float = ...,
                 calc_design_pipe_vals: float = ...,
                 V_hdr_cold_max: float = ...,
                 V_hdr_cold_min: float = ...,
                 V_hdr_hot_max: float = ...,
                 V_hdr_hot_min: float = ...,
                 N_max_hdr_diams: float = ...,
                 L_rnr_pb: float = ...,
                 L_rnr_per_xpan: float = ...,
                 L_xpan_hdr: float = ...,
                 L_xpan_rnr: float = ...,
                 Min_rnr_xpans: float = ...,
                 northsouth_field_sep: float = ...,
                 N_hdr_per_xpan: float = ...,
                 offset_xpan_hdr: float = ...,
                 custom_sf_pipe_sizes: float = ...,
                 sf_rnr_diams: Matrix = ...,
                 sf_rnr_wallthicks: Matrix = ...,
                 sf_rnr_lengths: Matrix = ...,
                 sf_hdr_diams: Matrix = ...,
                 sf_hdr_wallthicks: Matrix = ...,
                 sf_hdr_lengths: Matrix = ...,
                 has_hot_tank_bypass: float = ...,
                 T_tank_hot_inlet_min: float = ...,
                 tes_pump_coef: float = ...,
                 V_tes_des: float = ...,
                 custom_tes_p_loss: float = ...,
                 k_tes_loss_coeffs: Matrix = ...,
                 custom_tes_pipe_sizes: float = ...,
                 tes_diams: Matrix = ...,
                 tes_wallthicks: Matrix = ...,
                 tes_lengths: Matrix = ...,
                 DP_SGS: float = ...,
                 use_solar_mult_or_aperture_area: float = ...,
                 specified_solar_multiple: float = ...,
                 specified_total_aperture: float = ...,
                 non_solar_field_land_area_multiplier: float = ...,
                 trough_loop_control: Array = ...,
                 piping_loss: float = ...,
                 disp_csu_cost: float = ...,
                 disp_rsu_cost: float = ...,
                 disp_pen_delta_w: float = ...,
                 P_boil: float = ...,
                 csp_dtr_cost_site_improvements_cost_per_m2: float = ...,
                 csp_dtr_cost_solar_field_cost_per_m2: float = ...,
                 csp_dtr_cost_htf_system_cost_per_m2: float = ...,
                 csp_dtr_cost_storage_cost_per_kwht: float = ...,
                 csp_dtr_cost_fossil_backup_cost_per_kwe: float = ...,
                 csp_dtr_cost_power_plant_cost_per_kwe: float = ...,
                 csp_dtr_cost_bop_per_kwe: float = ...,
                 csp_dtr_cost_contingency_percent: float = ...,
                 csp_dtr_cost_epc_per_acre: float = ...,
                 csp_dtr_cost_epc_percent: float = ...,
                 csp_dtr_cost_epc_per_watt: float = ...,
                 csp_dtr_cost_epc_fixed: float = ...,
                 csp_dtr_cost_plm_per_acre: float = ...,
                 csp_dtr_cost_plm_percent: float = ...,
                 csp_dtr_cost_plm_per_watt: float = ...,
                 csp_dtr_cost_plm_fixed: float = ...,
                 csp_dtr_cost_sales_tax_percent: float = ...,
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
