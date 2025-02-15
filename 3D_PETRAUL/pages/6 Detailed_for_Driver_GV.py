import streamlit as st
import input_th

i=4

label_P=['Braking deceleration Rate [m/s2]', "Driver's aggressiveness factor with speed regulations [-]", "Driver's aggressiveness factor with use of the engine power during acceleration [-]", "Driver's aggressiveness factor with engine speed [-]", 'Cargo Additional Mass [kg] (passenger and load)']
order=[[0,1,2],[3]]
parts=["Driver's Aggressivity","Driver's Needs"]

help=[
'Average deceleration imposed by the driver',
'Multiplicative factor to path speed',
'Multiplicative factor to maximum power of the engine to characterize average power used during acceleration',
'Multiplicative factor to average engine speed in town',
''
]

format=[
    '%.2f',
    '%.2f',
    '%.2f',
    '%.2f',
    '%.0f'
]

input_th.details(i,order,parts,label_P,help,format)


                   