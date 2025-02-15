import streamlit as st


# Streamlit app layout
st.title("Welcome to the Energy Consumption Comparison Tool")



st.write("This app is the first version of the PETRAUL .It is designed to accurately model the energy consumption of automobile in LCA, for foreground application (calculation of Parameter Influence on Energy Consumption) or for background application (representativeness of energy consumption).")
st.write("Warning: The app is still under development. If you encounter any issues, please contact app owner at gabriel.magnaval@hevs.ch. Any feedback is valuable to help us further improve the app.")

st.write('Details on the equations and the pre-set configurations can be found in the supplementary information, available here: 10.5281/zenodo.14874993')

with st.expander("How to use this tool?"):
    st.write(
        "You can calculate personalized energy consumption on the **Energy Consumption** page for **ICEV (gasoline vehicles)** and **BEV (battery electric vehicles)**. Select your powertrain from the upper right corner of the page."
    )
    st.write(
        "Pre-set configurations for key contributors to energy consumption have been collected and computed. Select the desired configuration for each contributor to perform an initial calculation."
    )
    st.write(
        "The **Results** page displays energy consumption per 100 km and the contribution of each loss category. You can also calculate the desired **PIEC** using the expander on the Energy Consumption page."
    )
    st.write(
        "You can improve model accuracy by adjusting parameters in the detailed pages available in the side menu or by clicking on 'Detailed' boxes. Save your work to apply changes. You can either create a new scenario or update an existing one. Click **'Reset the scenarios'** to restart scenario modeling from scratch."
    )
    st.write(
        "If a problem occurs, try clearing the session by clicking **'Reset All'** on the Energy Consumption page."
    )

if st.button("Open Model"):

    st.switch_page("pages/1 EnergyConsumption.py")