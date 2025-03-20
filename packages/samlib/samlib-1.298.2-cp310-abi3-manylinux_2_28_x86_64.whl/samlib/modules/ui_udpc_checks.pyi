
# This is a generated file

"""ui_udpc_checks - Calculates the levels and number of paramteric runs for 3 udpc ind variables"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'ud_ind_od': Matrix,
    'T_htf_des_in': float,
    'is_calc_m_dot_vs_T_amb': float,
    'W_dot_net_des': float,
    'cooler_tot_W_dot_fan': float,
    'T_htf_cold_des': float,
    'n_T_htf_pars': float,
    'T_htf_low': float,
    'T_htf_des': float,
    'T_htf_high': float,
    'T_htf_pars': Array,
    'n_T_amb_pars': float,
    'T_amb_low': float,
    'T_amb_des': float,
    'T_amb_high': float,
    'T_amb_pars': Array,
    'n_m_dot_pars': float,
    'm_dot_low': float,
    'm_dot_des': float,
    'm_dot_high': float,
    'm_dot_pars': Array,
    'W_dot_gross_ND_des': float,
    'Q_dot_HTF_ND_des': float,
    'W_dot_cooling_ND_des': float,
    'm_dot_water_ND_des': float,
    'T_amb_sweep': Array,
    'm_dot_htf_ND_max_vs_T_amb_rule0': Array,
    'T_amb_LT': float,
    'q_dot_ND_vs_m_dot__T_amb_LT': Array,
    'W_dot_ND_vs_m_dot__T_amb_LT': Array,
    'eta_ND_vs_m_dot__T_amb_LT': Array,
    'm_dot_htf_ND_max_at_T_amb_LT_rule0': float,
    'q_dot_htf_ND_max_at_T_amb_LT_rule0': float,
    'W_dot_htf_ND_max_at_T_amb_LT_rule0': float,
    'eta_ND_max_at_T_amb_LT_rule0': float,
    'T_amb_HT': float,
    'q_dot_ND_vs_m_dot__T_amb_HT': Array,
    'W_dot_ND_vs_m_dot__T_amb_HT': Array,
    'eta_ND_vs_m_dot__T_amb_HT': Array,
    'm_dot_htf_ND_max_at_T_amb_HT_rule0': float,
    'q_dot_htf_ND_max_at_T_amb_HT_rule0': float,
    'W_dot_htf_ND_max_at_T_amb_HT_rule0': float,
    'eta_ND_max_at_T_amb_HT_rule0': float,
    'q_dot_ND_regr_vs_m_dot__T_amb_high_level': Array,
    'W_dot_ND_regr_vs_m_dot__T_amb_high_level': Array,
    'eta_ND_regr_vs_m_dot__T_amb_high_level': Array,
    'q_dot_ND_regr_vs_m_dot__T_amb_design': Array,
    'W_dot_ND_regr_vs_m_dot__T_amb_design': Array,
    'eta_ND_regr_vs_m_dot__T_amb_design': Array,
    'q_dot_ND_regr_vs_m_dot__T_amb_low_level': Array,
    'W_dot_ND_regr_vs_m_dot__T_amb_low_level': Array,
    'eta_ND_regr_vs_m_dot__T_amb_low_level': Array,
    'q_dot_ND_regr_vs_m_dot__T_amb_LT': Array,
    'W_dot_ND_regr_vs_m_dot__T_amb_LT': Array,
    'eta_ND_regr_vs_m_dot__T_amb_LT': Array,
    'q_dot_ND_regr_vs_m_dot__T_amb_HT': Array,
    'W_dot_ND_regr_vs_m_dot__T_amb_HT': Array,
    'eta_ND_regr_vs_m_dot__T_amb_HT': Array,
    'q_dot_ND_regr_vs_T_amb__T_HTF_low_level': Array,
    'W_dot_ND_regr_vs_T_amb__T_HTF_low_level': Array,
    'eta_ND_regr_vs_T_amb__T_HTF_low_level': Array,
    'm_dot_htf_ND_max_at_T_amb_low_level_rule0': float,
    'q_dot_htf_ND_max_at_T_amb_low_level_rule0': float,
    'W_dot_htf_ND_max_at_T_amb_low_level_rule0': float,
    'eta_ND_max_at_T_amb_low_level_rule0': float,
    'm_dot_htf_ND_max_at_T_amb_design_rule0': float,
    'q_dot_htf_ND_max_at_T_amb_design_rule0': float,
    'W_dot_htf_ND_max_at_T_amb_design_rule0': float,
    'eta_ND_max_at_T_amb_design_rule0': float,
    'm_dot_htf_ND_max_at_T_amb_high_level_rule0': float,
    'q_dot_htf_ND_max_at_T_amb_high_level_rule0': float,
    'W_dot_htf_ND_max_at_T_amb_high_level_rule0': float,
    'eta_ND_max_at_T_amb_high_level_rule0': float,
    'm_dot_htf_ND_max_at_T_amb_low_level_regr': float,
    'q_dot_htf_ND_max_at_T_amb_low_level_regr': float,
    'W_dot_htf_ND_max_at_T_amb_low_level_regr': float,
    'eta_ND_max_at_T_amb_low_level_regr': float,
    'm_dot_htf_ND_max_at_T_amb_design_regr': float,
    'q_dot_htf_ND_max_at_T_amb_design_regr': float,
    'W_dot_htf_ND_max_at_T_amb_design_regr': float,
    'eta_ND_max_at_T_amb_design_regr': float,
    'm_dot_htf_ND_max_at_T_amb_high_level_regr': float,
    'q_dot_htf_ND_max_at_T_amb_high_level_regr': float,
    'W_dot_htf_ND_max_at_T_amb_high_level_regr': float,
    'eta_ND_max_at_T_amb_high_level_regr': float,
    'm_dot_htf_ND_max_at_T_amb_LT_regr': float,
    'q_dot_htf_ND_max_at_T_amb_LT_regr': float,
    'W_dot_htf_ND_max_at_T_amb_LT_regr': float,
    'eta_ND_max_at_T_amb_LT_regr': float,
    'm_dot_htf_ND_max_at_T_amb_HT_regr': float,
    'q_dot_htf_ND_max_at_T_amb_HT_regr': float,
    'W_dot_htf_ND_max_at_T_amb_HT_regr': float,
    'eta_ND_max_at_T_amb_HT_regr': float
}, total=False)

class Data(ssc.DataDict):
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='User Defined Power Cycle', required='?=[[0]]')
    T_htf_des_in: float = INPUT(label='Input HTF design temperature', units='C', type='NUMBER', required='*')
    is_calc_m_dot_vs_T_amb: float = INPUT(label='0 (defalt) no; 1: return array of max m_dot vs T_amb', type='NUMBER', required='?=0')
    W_dot_net_des: float = INPUT(label='Design cycle power output (no cooling parasitics)', units='MWe', type='NUMBER', group='System Design', required='is_calc_m_dot_vs_T_amb=1')
    cooler_tot_W_dot_fan: float = INPUT(label='Total cooler fan power', units='MWe', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1', meta='Cooler Totals')
    T_htf_cold_des: float = INPUT(label='Cold outlet HTF design temperature', units='C', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    n_T_htf_pars: Final[float] = OUTPUT(label='Number of HTF parametrics', units='-', type='NUMBER', required='*')
    T_htf_low: Final[float] = OUTPUT(label='HTF low temperature', units='C', type='NUMBER', required='*')
    T_htf_des: Final[float] = OUTPUT(label='HTF design temperature', units='C', type='NUMBER', required='*')
    T_htf_high: Final[float] = OUTPUT(label='HTF high temperature', units='C', type='NUMBER', required='*')
    T_htf_pars: Final[Array] = OUTPUT(label='HTF temperature parametric values', units='C', type='ARRAY', required='*')
    n_T_amb_pars: Final[float] = OUTPUT(label='Number of ambient temperature parametrics', units='-', type='NUMBER', required='*')
    T_amb_low: Final[float] = OUTPUT(label='Low ambient temperature', units='C', type='NUMBER', required='*')
    T_amb_des: Final[float] = OUTPUT(label='Design ambient temperature', units='C', type='NUMBER', required='*')
    T_amb_high: Final[float] = OUTPUT(label='High ambient temperature', units='C', type='NUMBER', required='*')
    T_amb_pars: Final[Array] = OUTPUT(label='Ambient temperature parametric values', units='C', type='ARRAY', required='*')
    n_m_dot_pars: Final[float] = OUTPUT(label='Number of HTF mass flow parametrics', type='NUMBER', required='*')
    m_dot_low: Final[float] = OUTPUT(label='Low normalized HTF mass flow rate', type='NUMBER', required='*')
    m_dot_des: Final[float] = OUTPUT(label='Design normalized HTF mass flow rate', type='NUMBER', required='*')
    m_dot_high: Final[float] = OUTPUT(label='High normalized HTF mass flow rate', type='NUMBER', required='*')
    m_dot_pars: Final[Array] = OUTPUT(label='Normalized mass flow parametric values', type='ARRAY', required='*')
    W_dot_gross_ND_des: Final[float] = OUTPUT(label='ND cycle power output at design values of independent parameters', units='-', type='NUMBER', required='*')
    Q_dot_HTF_ND_des: Final[float] = OUTPUT(label='ND cycle heat input at design values of independent parameters', units='-', type='NUMBER', required='*')
    W_dot_cooling_ND_des: Final[float] = OUTPUT(label='ND cycle cooling power at design values of independent parameters', units='C', type='NUMBER', required='*')
    m_dot_water_ND_des: Final[float] = OUTPUT(label='ND cycle water use at design values of independent parameters', units='C', type='NUMBER', required='*')
    T_amb_sweep: Final[Array] = OUTPUT(label='Ambient temperature sweep for max mass flow calcs', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_vs_T_amb_rule0: Final[Array] = OUTPUT(label='Calculated ND max htf mass flow rate vs ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    T_amb_LT: Final[float] = OUTPUT(label='Low temp ambient temp of calculated ND outputs', units='C', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Calculated ND heat in vs mass flow at LT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Calculated ND power in vs mass flow at LT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Calculated ND efficiency in vs mass flow at LT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_LT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_LT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_LT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_LT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    T_amb_HT: Final[float] = OUTPUT(label='High temp ambient temp of calculated ND outputs', units='C', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Calculated ND heat in vs mass flow at HT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Calculated ND power in vs mass flow at HT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Calculated ND efficiency in vs mass flow at HT ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_HT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_HT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_HT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_HT_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_m_dot__T_amb_high_level: Final[Array] = OUTPUT(label='Regression heat ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_m_dot__T_amb_high_level: Final[Array] = OUTPUT(label='Regression net power ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_m_dot__T_amb_high_level: Final[Array] = OUTPUT(label='Regression net efficiency ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_m_dot__T_amb_design: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_m_dot__T_amb_design: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_m_dot__T_amb_design: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_m_dot__T_amb_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_m_dot__T_amb_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_m_dot__T_amb_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_m_dot__T_amb_LT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_m_dot__T_amb_HT: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_ND_regr_vs_T_amb__T_HTF_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_ND_regr_vs_T_amb__T_HTF_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_regr_vs_T_amb__T_HTF_low_level: Final[Array] = OUTPUT(label='Regression max ND HTF mass flow at low level ambient temp', type='ARRAY', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_low_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_low_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_low_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_low_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_design_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_design_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_design_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_design_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_high_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_high_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_high_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_high_level_rule0: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_low_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_low_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_low_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_low_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_design_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_design_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_design_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_design_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_high_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_high_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_high_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_high_level_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at low level ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_LT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_LT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_LT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_LT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at LT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    m_dot_htf_ND_max_at_T_amb_HT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    q_dot_htf_ND_max_at_T_amb_HT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    W_dot_htf_ND_max_at_T_amb_HT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')
    eta_ND_max_at_T_amb_HT_regr: Final[float] = OUTPUT(label='Calculated max ND HTF mass flow at HT ambient temp', type='NUMBER', required='is_calc_m_dot_vs_T_amb=1')

    def __init__(self, *args: Mapping[str, Any],
                 ud_ind_od: Matrix = ...,
                 T_htf_des_in: float = ...,
                 is_calc_m_dot_vs_T_amb: float = ...,
                 W_dot_net_des: float = ...,
                 cooler_tot_W_dot_fan: float = ...,
                 T_htf_cold_des: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
