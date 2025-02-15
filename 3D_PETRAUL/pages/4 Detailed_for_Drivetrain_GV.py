import streamlit as st
import input_th


i=2

label_P=['Transmission/Drivetrain Differential Efficiency [-]', 'Transmission mean effect [s]', 'Synchronization loss factor [J/m]', 'Ideal engine speed in town [rpm]']
order=[[0,1,2],[3]]
parts=['Transmission Losses','Transmission Settings']

help=[
'i.e. peak efficiency',
'coefficient for friction losses in the drivetrain',
'coefficient for synchronization losses in the gearbox',
'']

format=[
"%.3f",
"%.2e",
"%.1f",
"%.0f"
]

input_th.details(i,order,parts,label_P,help,format)


                   