import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import model
import input_th
import input_elec
import pandas as pd
import plotly.graph_objects as go



def file_opening_dict(name):
    with open(name) as file_name:
        df = pd.read_csv(file_name, index_col=0, sep=';')
        scenarios = df.to_dict(orient='list')
    return scenarios
    
    

colors = ['#2c3e50', '#f1c40f', '#2ecc71', '#e67e22', '#e74c3c', '#1abc9c', 
              '#9b59b6', '#34495e', '#f39c12', '#27ae60', '#d35400', '#c0392b', 
              '#3498db', '#2980b9', '#8e44ad', '#bdc3c7']



### plot coding ###

def comparison_window(title, EC, labels,unit,limit):
    fig, ax = plt.subplots(figsize=(10, 5))
    sums = EC[0]
    sums = np.round(sums, 2)
    losses = EC[1]
    if limit<sums:
        limit=sums*1.1


    ax.set_xlim(0, limit)
    left = 0
    for k in range(len(losses)):
        ax.barh(0, losses[k], left=left, color='black')
        left += losses[k]

    ax.text(sums+0.2,0, f'{sums} {unit}', ha='left', va='center', fontsize=18)  
    ax.set_xlabel('Contribution [' + unit + ']')
    ax.set_yticks([])
    ax.set_title(title)
    ax.legend(loc='upper right')

    return fig
    
    
def fig_interactive (title, EC, labels,unit):    
    fig = go.Figure()
    sums = EC[0]
    sums = np.round(sums, 2)
    losses = EC[1]

    for k in range(len(losses)):  
        fig.add_trace(go.Bar(
                y=[f"{sums}" + unit],  # Une seule catégorie sur l'axe des Y
                x=[losses[k]],  # Valeur de la contribution
                name=labels[k],  # Nom de la section
                marker_color=colors[k],
                width=0.6,  # Ajuster la largeur des barres
                orientation='h',
                hoverinfo="x+name"  # Afficher la valeur et le nom au survol
            ))

        
        
    # Configuration du graphique
    fig.update_layout(
            barmode='stack',
            title=title,
            xaxis=dict(title='Contribution [' + unit + ']'),
            showlegend=True
        )

    # Affichage
    st.plotly_chart(fig, use_container_width=True)
            



### button for ICEV vs BEV ###


col1, col2,col3,col4 = st.columns(4)

with col1:
    if st.button("Reset All"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("All session state values have been reset to default.")
        st.rerun()

with col4:
    if "model_choice" not in st.session_state:
        st.session_state.model_choice ='ICEV'
    
    st.session_state.model_choice = st.select_slider(
        "Select the powertrain :",
        options=["ICEV", "BEV"],
        value=st.session_state.model_choice,
    )
    
if st.session_state.model_choice == 'ICEV':

    st.title("Powertrain selected: ICEV (gasoline)")
    
    labels = ['rolling', 'drag', 'inertia', 'grade', 'wind', 'friction', 'pumping',
              'thermal', 'accessories', 'transmission', 'synchronization', 'cold_engine',
              'idling']
    unit= 'L/100km'
    limit=20

    st.session_state.parameters_ICEV=input_th.ask()
    if st.session_state.parameters_ICEV==None:
        st.warning('You must select all options to continue')
    
    else:
        
        EC = model.EC_th(*st.session_state.parameters_ICEV)
        fig = comparison_window("Energy Consumption Calculation", EC, labels,unit,limit)
        st.pyplot(fig)
        
        fig_interactive ("Energy Consumption Contributions", EC, labels,unit)
            

        col1,col2=st.columns(2)
        with col1:
            with st.expander("efficiencies of the powertrain elements"):

                label_nop = ['nop_engine = ', 'nop_trans = ', 'nop = ']
    
                for n in range(len(EC[2])):
                    op = round(EC[2][n], 2)
                    st.write(f"{label_nop[n]}{op}")
            
    
        with col2:
        
            with st.expander("Process PIEC"):

                col1,col2=st.columns(2)
                with col1:
                    P_options=['--Select--','MIEC','r0IEC','CdIEC','AIEC','DIEC','σIEC','f0IEC','p0IEC','PaccIEC']
                    unit_PIEC=['100kg','0.001-','0.1-','m2','L','unit','kPa','(1e-3 kPa.s2)','kW','100kg']
                    selected_P = st.selectbox(f'Which Parameter?', options=P_options, key='selected_P')
                    selected_index = P_options.index(selected_P)-1
                    if selected_P=='MIEC':
                        with col2:
                            secondary_MIEC = st.selectbox(f'With Secondary Reduction Included?', options=['No','Yes'], key=f'MIEC_SE')
                            if secondary_MIEC=='Yes':
                                selected_index=-1
                if selected_P=='--Select--':
                        st.warning('You must select an option to continue')

                else:
                        PIEC=model.PIEC_th(*st.session_state.parameters_ICEV)[selected_index]
                        PIEC=np.round(PIEC,2)
                        st.write(f"{selected_P} = {PIEC} kWh/100km/{unit_PIEC[selected_index]}")
                        st.write(f"(i.e., {selected_P} = {np.round(PIEC/8.9,2)} l/100km/{unit_PIEC[selected_index]})")
                        
                            
            

     
        
            
            

if st.session_state.model_choice == 'BEV':

    st.title("Powertrain selected: BEV (electric)")
    
    labels = ['rolling','drag','inertia','grade','wind','friction','copper','converter','accessories','transmission','battery']     
    unit= 'kWh/100km'
    limit=100

    st.session_state.parameters_BEV=input_elec.ask()
    if st.session_state.parameters_BEV==None:
        st.warning('You must select all options to continue')
    
    else:
            EC = model.EC_el(*st.session_state.parameters_BEV)
            fig = comparison_window("Energy Consumption Calculation", EC, labels,unit,limit)
            st.pyplot(fig)
            
            fig_interactive ("Energy Consumption Contributions", EC, labels,unit)
            
            
            col1,col2=st.columns(2)
            with col1:
                with st.expander("operating efficiencies of the powertrain elements"):

                    label_nop = ['nop_engine = ', 'nop_trans = ','nop_battery = ', 'nop = ']
    
                    for n in range(len(EC[2])):
                        op = round(EC[2][n], 2)
                        st.write(f"{label_nop[n]}{op}")
            
    
            with col2:
        
                with st.expander("Process PIEC"):

                    col1,col2=st.columns(2)
                    with col1:
                        P_options=['--Select--','MIEC','r0IEC','CdIEC','AIEC','PeIEC','σIEC','PaccIEC']
                        unit_PIEC=['100kg','0.001-','0.1-','m2','100kW','unit','kW','100kg']
                        selected_P = st.selectbox(f'Which Parameter?', options=P_options, key='selected_P')
                        selected_index = P_options.index(selected_P)-1
                        if selected_P=='MIEC':
                            with col2:
                                secondary_MIEC = st.selectbox(f'With Secondary Reduction Included?', options=['No','Yes'], key=f'MIEC_SE')
                                if secondary_MIEC=='Yes':
                                    selected_index=-1
                    if selected_P=='--Select--':
                        st.warning('You must select an option to continue')
                    else:
                        PIEC=model.PIEC_el(*st.session_state.parameters_BEV)[selected_index]
                        PIEC=np.round(PIEC,2)
                       
                        st.write(f"{selected_P} = {PIEC} {unit}/{unit_PIEC[selected_index]}")

