"""MCS-like profile definitions for Sionna link adaptation experiments."""
from __future__ import annotations
import numpy as np

EXPANDED_MCS_PROFILES = [
    {"profile_name":"QPSK_R030","mcs_like":"Very Low MCS","num_bits_per_symbol":2,"code_rate":0.30,"ebno_values":np.arange(-2,8,1)},
    {"profile_name":"QPSK_R050","mcs_like":"Low MCS","num_bits_per_symbol":2,"code_rate":0.50,"ebno_values":np.arange(0,10,1)},
    {"profile_name":"16QAM_R045","mcs_like":"Low-Medium MCS","num_bits_per_symbol":4,"code_rate":0.45,"ebno_values":np.arange(2,15,1)},
    {"profile_name":"16QAM_R060","mcs_like":"Medium MCS","num_bits_per_symbol":4,"code_rate":0.60,"ebno_values":np.arange(4,17,1)},
    {"profile_name":"64QAM_R050","mcs_like":"Medium-High MCS","num_bits_per_symbol":6,"code_rate":0.50,"ebno_values":np.arange(6,21,1)},
    {"profile_name":"64QAM_R065","mcs_like":"High MCS","num_bits_per_symbol":6,"code_rate":0.65,"ebno_values":np.arange(8,24,1)},
    {"profile_name":"64QAM_R080","mcs_like":"Very High 64QAM MCS","num_bits_per_symbol":6,"code_rate":0.80,"ebno_values":np.arange(10,27,1)},
    {"profile_name":"256QAM_R070","mcs_like":"256QAM Medium-High MCS","num_bits_per_symbol":8,"code_rate":0.70,"ebno_values":np.arange(12,30,1)},
    {"profile_name":"256QAM_R085","mcs_like":"256QAM High MCS","num_bits_per_symbol":8,"code_rate":0.85,"ebno_values":np.arange(14,33,1)},
]
