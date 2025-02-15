import streamlit as st
import input_elec

i=1

label_P=['Power Max Engine [W]', 'Engine Max Torque [N]', 'Engine Differential Efficiency', 'friction mean effective pressure [J]', 'Copper mean effect [1/(N.m.s)]', 'Converter mean effect [W]']
order=[[0,1],[2,3,4,5]]
parts=['Engine Sizing','Main Engine Losses']

help=[
'',
'',
'i.e. peak efficiency',
'size of the cylinder',
'coefficient for friction losses in the engine',
'coefficient for copper losses in the engine',
'coefficient for converter losses in the engine',
]

format=[
    '%.0f',
    '%.0f',
    '%.3f',
    '%.2f',
    '%.2f',
    '%.0f'
]

input_elec.details(i,order,parts,label_P,help,format)

