import streamlit as st


# Streamlit app layout
st.title("Welcome to the Energy Consumption Comparison Tool")



st.write("This app is the first version of the PETRAUL . It aims to be used for accurately model the energy consumption of automobile in LCA, for foreground application (calculation of Parameter Induced Energy Consumption) or for background application (representativeness of energy consumption).")
st.write("Warning: The app is still under development. In case of problem, please contact app owner at gabriel.magnaval@hevs.ch. Any feedback is valuable to help us in further developing the app.")

st.write('Details on the equations and the pre-set configurations can be found in the supplementary information, available here: ')

with st.expander("How to use this tool?"):

    st.write("Calculation of your personalized energy consumption can be done on the Energy Consumption page for ICEV (gasoline vehicles) and BEV (battery vehicles). You can select on the upper right of the page your powertrain.")
    st.write("Pre-set configurations for the main contributors to Energy Consumption have been collected and computed. Select the configuration you want for each contributor to compute a first round of calculation.")
    st.write("Results page show the energy consumption per 100km, and the contribution of each loss over the results. You can also calculate the desired PIEC using the expander on the Energy Consumption page.")
    st.write("You can improve the preciseness of the model by changing the parameters of the model in the different detailed pages you can find in the lateral window, or by clicking on 'detailed' boxes. Save your work to compute the changes. You can either create your new scenario or update an existing one. Click on 'Reset the scenarios' to restart from scratch teh scenario modeling.")
    st.write("If a problem occurs, do not hesitate to clean the session by clicking on 'Reset All' in the EnergyConsumption page.")


if st.button("Open Model"):

    st.switch_page("pages/1 EnergyConsumption.py")