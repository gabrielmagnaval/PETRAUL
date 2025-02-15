import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import model
import pandas as pd
from PIL import Image


def file_opening_dict(name):
    with open(name) as file_name:
        df = pd.read_csv(file_name, index_col=0, sep=';')
        scenarios = df.to_dict(orient='list')
    return scenarios

# Load data
body_dict = file_opening_dict('3D_PETRAUL/body.csv')
engine_dict = file_opening_dict('3D_PETRAUL/thermal.csv')
trans_dict = file_opening_dict('3D_PETRAUL/transmission.csv')
path_dict = file_opening_dict('3D_PETRAUL/path.csv')
driver_dict = file_opening_dict('3D_PETRAUL/driver.csv')

st.session_state.dictionary_ICEV = [body_dict, engine_dict, trans_dict, path_dict, driver_dict]
element = ['Body', 'Engine', 'Drivetrain', 'Path', 'Driver']
st.session_state.label_parameters = [['Mass [kg]', 'rolling factor [-]', 'Drag Resistance [-]', 'Frontal Area [m2]', 'Wheel Inertia', 'Wheel radius [m]', 'transf', 'Power accessories [W]', 'Additional Mass of Equipment [kg]', 'Additional Drag Resistance of Equipment [-]'],
                    ['Power Max Engine [W]', 'Engine Differential Efficiency (i.e. peak efficiency)', 'Engine Displacement [L]', 'friction mean effective pressure [kPa]', 'Pumping mean effect [kPa/s3]', 'Thermal mean effect [kPa.s]', 'Engine speed during idling [rpm]', 'cs', 'share of start and stop technology in the fleet'],
                    ['Transmission Differential Efficiency (i.e. peak efficiency)', 'Transmission mean effect', 'Synchronization loss factor', 'Ideal engine speed in town [rpm]'],
                    ['J3p', 'K1p', 'K2p', 'r_acc', 'J0p', 'H', 'w', 'urb', 'd', 't_idle'],
                    ['B', 'mu_v', 'mu_a', 'mu_N', 'M_load']]

def category_to_parameter(categories, dictionary):
    parameters = []
    for k in range(len(categories)):
        dic = dictionary[k]
        cat = categories[k]
        parameters += [dic[cat]]
    return parameters

def reset_current_dictionary(index):
    st.session_state.dictionary_ICEV[index] = file_opening_dict(
        ['3D_PETRAUL/body.csv', '3D_PETRAUL/thermal.csv', '3D_PETRAUL/trans.csv', '3D_PETRAUL/path.csv', '3D_PETRAUL/driver.csv'][index]
    )
    st.session_state.options_ICEV[index] = '--Select--'
    st.success("Current dictionary has been reset and selection cleared!")



def ask ():

    if "dictionary_ICEV" not in st.session_state:
        st.session_state.dictionary_ICEV = [body_dict, engine_dict, trans_dict, path_dict, driver_dict]
    if "options_ICEV" not in st.session_state:
        st.session_state.options_ICEV =['--Select--']*5


    # Create dropdown menus for categories
    entries = []
    all_selected=True
    
    columns = st.columns(len(st.session_state.dictionary_ICEV))
    for i in range(len(st.session_state.dictionary_ICEV)):
        
        with columns[i]:
            st.write(element[i])
            image_name="3D_PETRAUL/pictures/picture_"+element[i]+".png"
            image=Image.open(image_name)
            resized_image = image.resize((300, 250))
            st.image(resized_image)
            
            options=['--Select--'] +list(st.session_state.dictionary_ICEV[i].keys())
            index=options.index(st.session_state.options_ICEV[i])
            st.session_state.options_ICEV[i] = st.selectbox(f'Select Option', options=options, index=index ,key=f'option_{i}')
            
            if st.session_state.options_ICEV[i]=='--Select--':
                all_selected=False
                
            else:
                entries.append(category_to_parameter([st.session_state.options_ICEV[i]], [st.session_state.dictionary_ICEV[i]])[0])
            
            
            if st.button("Go to Detailed Page", key=f"alt_{i}"):
                st.switch_page(f"pages/{i+2} Detailed_for_{element[i]}_GV.py")
              
                
    if all_selected:
        return entries
    else:
        return None
    
    
    
def details (i, order, parts, label_P, help, format):
    if "parameters_ICEV" not in st.session_state:
        st.session_state.parameters_ICEV = [[] for _ in range(len(element))]
    if "dictionary_ICEV" not in st.session_state:
        st.session_state.dictionary_ICEV = [body_dict, engine_dict, trans_dict, path_dict, driver_dict]
    if "options_ICEV" not in st.session_state:
        st.session_state.options_ICEV =['--Select--']*5

    st.title("Welcome to the Detailed Page for " + element[i])
    image_name = "3D_PETRAUL/pictures/picture_" + element[i] + ".png"
    image = Image.open(image_name)
    resized_image = image.resize((300, 250))
    st.image(resized_image)

    options = ['--Select--'] + list(st.session_state.dictionary_ICEV[i].keys())
    index = options.index(st.session_state.options_ICEV[i])
    st.session_state.options_ICEV[i] = st.selectbox(f'Select Option', options=options, index=index ,key=f'optionICEV_{i}')
    
    if st.session_state.options_ICEV[i] == '--Select--':
        st.warning("You must select an option to continue.")
    else:
        selected_category = st.session_state.options_ICEV[i]
        local_entries = [category_to_parameter([selected_category], [st.session_state.dictionary_ICEV[i]])[0].copy()]     
        
        for x in range(len(order)):
            st.markdown("---")
            st.write(f"**{parts[x]}**")
            for j in order[x]:
                local_entries[0][j] = st.number_input(f"{label_P[j]}", key=f'param_{i}_{j}', value=local_entries[0][j], format=format[j], help=help[j])
        
        scenario_name = ""
        if st.button("Save to Current Scenario"):
            st.session_state.dictionary_ICEV[i][selected_category] = local_entries[0]
            st.success(f"Changes saved for {selected_category}.")
            st.switch_page("pages/1 EnergyConsumption.py")
        
        with st.expander("Create New Scenario"):
            scenario_name = st.text_input("Enter a name for the new scenario:", key=f'scenario_name_ICEV_{i}')
            if st.button("Confirm name and Create New Scenario"):
                if scenario_name:
                
                    st.session_state.dictionary_ICEV[i][scenario_name] = local_entries[0]
                    st.session_state.options_ICEV[i] = scenario_name  # Sélectionner le nouveau scénario
                    st.success(f"Scenario '{scenario_name}' has been saved and selected.")
                    st.switch_page("pages/1 EnergyConsumption.py")
                else:
                    st.warning("Please enter a name for the scenario before saving.")
        
        if st.button(f"Reset the scenarios of {element[i]}"):
            reset_current_dictionary(i)
            st.rerun()