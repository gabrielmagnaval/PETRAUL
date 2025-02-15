import streamlit as st
import input_th

i=0

label_P=['Mass [kg]', 'rolling factor [-]', 'Drag Resistance [-]', 'Frontal Area [m2]', 'Wheel Inertia [kg.m2]', 'Wheel radius [m]', 'Total (Overall) reduction ratio of the gearbox on highway [-]', 'Power accessories [W]', 'Additional Mass of Equipment [kg]', 'Increase factor of Drag Resistance due to Equipment [-]']
order=[[0,2,3],[1,4,5],[6],[7,8,9]]
parts=['Structure','Wheels','Gearbox Settings','Equipment']
help=[
'Total mass of the vehicle without equipment, passengers and cargo',
'average rolling factor of the tires',
'drag resistance of the automobile without equipment',
'Frontal Area of the automobile without equipment',
'',
'',
'Product of the transmission ratio of the highest gear and the final transmission ratio',
'',
'',
'']

format=[
    '%.0f',
    '%.3f',
    '%.2f',
    '%.2f',
    '%.2f',
    '%.2f',
    '%.2f',
    '%.0f',
    '%.0f',
    '%.2f'
]

input_th.details(i,order,parts,label_P,help,format)


                   

