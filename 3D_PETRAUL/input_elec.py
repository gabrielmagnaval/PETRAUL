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
body_dict = file_opening_dict('3D_PETRAUL/body_EV.csv')
engine_dict = file_opening_dict('3D_PETRAUL/electric.csv')
trans_dict = file_opening_dict('3D_PETRAUL/trans_EV.csv')
path_dict = file_opening_dict('3D_PETRAUL/path.csv')
driver_dict = file_opening_dict('3D_PETRAUL/driver.csv')
battery_dict = file_opening_dict('3D_PETRAUL/battery.csv')

st.session_state.dictionary_BEV=[body_dict,engine_dict,trans_dict,path_dict,driver_dict,battery_dict]
element = ['Body', 'Engine', 'Drivetrain', 'Path', 'Driver','Battery']
page=[7,8,9,11,12,10]

def category_to_parameter(categories, dictionary):
    parameters = []
    for k in range(len(categories)):
        dic = dictionary[k]
        cat = categories[k]
        parameters += [dic[cat]]
    return parameters

def reset_current_dictionary(index):
    st.session_state.dictionary_BEV[index] = file_opening_dict(
        ['3D_PETRAUL/body_EV.csv', '3D_PETRAUL/electric.csv', '3D_PETRAUL/trans_EV.csv', '3D_PETRAUL/path.csv', '3D_PETRAUL/driver.csv', '3D_PETRAUL/battery.csv'][index]
    )
    st.session_state.options_BEV[index] = '--Select--'
    st.success("Current dictionary has been reset and selection cleared!")

def ask ():
    if "dictionary_BEV" not in st.session_state:
        st.session_state.dictionary_BEV = [body_dict, engine_dict, trans_dict, path_dict, driver_dict,battery_dict]
    if "options_BEV" not in st.session_state:
        st.session_state.options_BEV =['--Select--']*6


    # Create dropdown menus for categories
    entries = []
    all_selected=True
    
    columns = st.columns(len(st.session_state.dictionary_BEV))
    for i in range(len(st.session_state.dictionary_BEV)):
        
        with columns[i]:
            st.write(element[i])
            image_name="3D_PETRAUL/pictures/picture_"+element[i]+".png"
            image=Image.open(image_name)
            resized_image = image.resize((300, 250))
            st.image(resized_image)
            
            options=['--Select--'] +list(st.session_state.dictionary_BEV[i].keys())
            index=options.index(st.session_state.options_BEV[i])
            st.session_state.options_BEV[i] = st.selectbox(f'Select Option', options=options, index=index ,key=f'optionBEV_{i}')
            
            if st.session_state.options_BEV[i]=='--Select--':
                all_selected=False
                
            else:
                entries.append(category_to_parameter([st.session_state.options_BEV[i]], [st.session_state.dictionary_BEV[i]])[0])
            
            
            if st.button("Go to Detailed Page", key=f"altBEV_{i}"):
                st.switch_page(f"pages/{page[i]} Detailed_for_{element[i]}_BEV.py")
              
                
    if all_selected:
        return entries
    else:
        return None
    
    
    
def details (i, order, parts, label_P, help, format):
    if "parameters_BEV" not in st.session_state:
        st.session_state.parameters_BEV = [[] for _ in range(len(element))]
    if "dictionary_BEV" not in st.session_state:
        st.session_state.dictionary_BEV = [body_dict, engine_dict, trans_dict, path_dict, driver_dict,battery_dict]
    if "options_BEV" not in st.session_state:
        st.session_state.options_BEV =['--Select--']*6

    st.title("Welcome to the Detailed Page for " + element[i])
    image_name = "3D_PETRAUL/pictures/picture_" + element[i] + ".png"
    image = Image.open(image_name)
    resized_image = image.resize((300, 250))
    st.image(resized_image)

    options = ['--Select--'] + list(st.session_state.dictionary_BEV[i].keys())
    index = options.index(st.session_state.options_BEV[i])
    st.session_state.options_BEV[i] = st.selectbox(f'Select Option', options=options, index=index ,key=f'optionBEV_{i}')
    
    if st.session_state.options_BEV[i] == '--Select--':
        st.warning("You must select an option to continue.")
    else:
        selected_category = st.session_state.options_BEV[i]
        local_entries = [category_to_parameter([selected_category], [st.session_state.dictionary_BEV[i]])[0].copy()]     
        
        for x in range(len(order)):
            st.markdown("---")
            st.write(f"**{parts[x]}**")
            for j in order[x]:
                local_entries[0][j] = st.number_input(f"{label_P[j]}", key=f'paramBEV_{i}_{j}', value=local_entries[0][j], format=format[j], help=help[j])
        
        scenario_name = ""
        if st.button("Save to Current Scenario"):
            st.session_state.dictionary_BEV[i][selected_category] = local_entries[0]
            st.success(f"Changes saved for {selected_category}.")
            st.switch_page("pages/1 EnergyConsumption.py")
        
        with st.expander("Create New Scenario"):
            scenario_name = st.text_input("Enter a name for the new scenario:", key=f'scenario_name_{i}')
            if st.button("Confirm name and Create New Scenario"):
                if scenario_name:
                
                    st.session_state.dictionary_BEV[i][scenario_name] = local_entries[0]
                    st.session_state.options_BEV[i] = scenario_name  # Sélectionner le nouveau scénario
                    st.success(f"Scenario '{scenario_name}' has been saved and selected.")
                    st.switch_page("pages/1 EnergyConsumption.py")
                else:
                    st.warning("Please enter a name for the scenario before saving.")
        
        if st.button(f"Reset the scenarios of {element[i]}"):
            reset_current_dictionary(i)
            st.rerun()



