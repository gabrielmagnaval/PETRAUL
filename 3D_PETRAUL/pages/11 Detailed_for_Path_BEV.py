import streamlit as st
import input_elec


i=3

label_P=['J3p [m2/s2]', 'K1p [m/s2]', 'K2p [m2/s3]', 'r_acc', 'J0p [s/m] ', 'H [-] ', 'w [m/s]', 'urban rate [-]', 'average length of the journeys [m]', 'time spent at idling [s/m]']
order=[[0,1,4,7],[5,6],[2,3],[8,9]]
parts=['Main Path characteristics','Environmental characteristics','Additional parameters for acceleration modelling','Additional parameters for idling and cold start']
help=[
'characterizing speed (average_speed^2)',
'characterizing inertia ',
'characterizing acceleration',
'characterizing acceleration',
'characterizing duration (1/average speed)',
'characterizing average slope over the journey',
'characterizing average wind speed',
'',
'',
''
]

format=[
    '%.0f',
    '%.3f',
    '%.2f',
    '%.2f',
    '%.3f',
    '%.3f',
    '%.0f',
    '%.2f',
    '%.0f',
    '%.2f'
]

input_elec.details(i,order,parts,label_P,help,format)

