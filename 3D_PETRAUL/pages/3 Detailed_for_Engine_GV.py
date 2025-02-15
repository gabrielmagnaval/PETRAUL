import streamlit as st
import input_th

i=1

label_P=['Power Max Engine [W]', 'Engine Differential Efficiency', 'Engine Displacement [L]', 'friction mean effective pressure [kPa]', 'Pumping mean effect [kPa.s2]', 'Thermal mean effect [kPa/s]', 'Engine speed during idling [rpm]', 'cold start coefficient [s] ', 'Fraction of idling remaining (start-and-stop) [-]']
order=[[0,2],[1,3,4,5],[6,8,7]]
parts=['Engine Sizing','Main Engine Losses','Additional Losses Parameters']
help=[
'',
'i.e. peak efficiency',
'size of the cylinder',
'coefficient for friction losses in the engine',
'coefficient for pumping losses in the engine',
'coefficient for thermal losses in the engine',
'',
'coefficient for cold start additional losses',
'1: no start and stop ; 0: start and stop implemented']

format=[
    '%.0f',
    '%.3f',
    '%.2f',
    '%.0f',
    '%.2e',
    '%.0f',
    '%.0f',
    '%.1f',
    '%.2f'
]


input_th.details(i,order,parts,label_P,help,format)


                   

