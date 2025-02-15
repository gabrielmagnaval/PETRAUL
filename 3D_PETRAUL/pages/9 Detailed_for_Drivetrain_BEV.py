import streamlit as st
import input_elec


i=2

label_P=['Transmission mean effect [s]','Transmission Differential Efficiency [-]']
order=[[1,0]]
parts=['Transmission Losses']

help=[
'coefficient for friction losses in the drivetrain',
'i.e. peak efficiency',
]

format=[
'%.2e',
'%.3f'
]

input_elec.details(i,order,parts,label_P,help,format)


                   