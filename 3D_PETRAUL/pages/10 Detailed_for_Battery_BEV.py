import streamlit as st
import input_elec

i=5

label_P=['Internal Resistance Battery [Ohm]', 'Voltage Battery [V]', 'Mass Battery [kg]', 'Differential Efficiency Battery [-]']
order=[[3,0,1],[2]]
parts=['Battery losses', 'Additional Characteristics']
help=[
'Overall average resistance of the battery',
'',
'',
'charging efficiency',
]

format=[
    '%.2f',
    '%.0f',
    '%.0f',
    '%.3f'
]

input_elec.details(i,order,parts,label_P,help,format)
