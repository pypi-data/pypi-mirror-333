# -*- coding: utf-8 -*-
"""
This script performs voltage sweep experiments using a Nanonis instance.
"""
from nanonis_tramea import Nanonis
from gate_manager.gate import Gate, GatesGroup
from gate_manager.connection import NanonisSourceConnection, SemiqonLinesConnection
from gate_manager.sweeper import Sweeper
import socket
import os


# Choose the currents folder
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Create a socket connection to Nanonis
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.236.1", 6501))

# Create Nanonis instance for controlling the device
nanonisInstance = Nanonis(connection)

# Connection
nanonis_o = NanonisSourceConnection(nanonisInstance).outputs
nanonis_i = NanonisSourceConnection(nanonisInstance).inputs
lines = SemiqonLinesConnection().lines


# %% Define gates

# top channel 
t_P1 = Gate(source=nanonis_o[1], lines=[lines[9]])  # tP1: 9
t_bar_S1 = Gate(source=nanonis_o[2], lines=[lines[10]])  #t_bar_S1
t_bar_12 = Gate(source=nanonis_o[3], lines=[lines[8]])  #t_bar_1-2
t_global =  Gate(source=nanonis_o[5], lines=[lines[2], lines[3], lines[4], lines[5], lines[6], lines[7]])

# sources and reservoirs
t_b_s = Gate(source=nanonis_o[7], lines=[lines[11], lines[13]])  # bs,ts: 11,13
res_S_D = Gate(source=nanonis_o[8], lines=[lines[12], lines[24]])  # resS,resD: 12,24

# Grouping gates for easier voltage control
outputs = GatesGroup([t_P1, t_bar_S1, t_bar_12, t_global, t_b_s, res_S_D])
fingers = GatesGroup([t_P1, t_bar_S1, t_bar_12, t_global])


# %% Define input gates for reading currents measurements

t_D = Gate(source=nanonis_i[1], lines=[lines[1]])
b_D = Gate(source=nanonis_i[2], lines=[lines[23]])
SD3 = Gate(source=nanonis_i[3])
SD4 = Gate(source=nanonis_i[4])
SD5 = Gate(source=nanonis_i[5])
SD6 = Gate(source=nanonis_i[6])
SD7 = Gate(source=nanonis_i[7])
SD8 = Gate(source=nanonis_i[8])

# this should be automatic for the input gates grouping. maybe call it 'inputs' only?
inputs = GatesGroup([t_D, b_D, SD4, SD5, SD6, SD7, SD8])


# %% Define parameters for the experiment
slew_rate = 0.1 
for i in range(8):
    nanonisInstance.UserOut_SlewRateSet(i+1, slew_rate)
params = {
    'device': "Semiqon 36",
    'temperature': "CT",
    'amplification': (-1) * 10 ** 7, #-1 because of the inverting amplifier
    }
sweeper = Sweeper(outputs, inputs, **params)


# %% 1D sweep

param = {
    'swept_outputs': GatesGroup([t_P1]),
    'measured_inputs': GatesGroup([t_D]),
    'start_voltage': -0.6,
    'end_voltage': 0,
    'step': 0.5 * 1e-3,
    'initial_state': [
        [t_b_s, 0.4 * 1e-3],
        [res_S_D, 2],
        [t_bar_S1, 1.0],
        [t_bar_12, 1.0],
        [t_global, 0.8]
        ],
    'comments': 'test'
    }
    
sweeper.sweep1D(**param)


# %% 2D sweep

param = {
        'X_swept_outputs': GatesGroup([t_P1]),
        'X_start_voltage': -0.3,
        'X_end_voltage': 0.3,
        'X_step': 2 * 1e-3,
        'Y_swept_outputs': GatesGroup([res_S_D]),
        'Y_start_voltage': 0.1,
        'Y_end_voltage': 1.0,
        'Y_step': 0.1,
        'measured_inputs': GatesGroup([t_D]),
        'initial_state': [
            [t_b_s, 0.4 * 1e-3], 
            [t_bar_S1, 1],
            [t_bar_12, 1],
            [t_global, 0.8]
        ],
        'voltage_unit': 'V',
        'current_unit': 'nA',
        'comments': f'diamond'
        }
sweeper.sweep2D(**params)


# %% Turn off
fingers.turn_off()
GatesGroup([t_b_s, res_S_D]).turn_off()
