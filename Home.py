

# Author: Sophia Gucciardi
# Streamlit App
# DSBA 5122 Final Project

#-----IMPORTS AND PAGE CONFIGS-------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import base64 

#set page configs
st.set_page_config(
    page_title="Home", 
    layout='wide',
    page_icon=':brain:'
    )

#----CACHE DATA & FIX COLUMN NAMES--------------------------------------------------------------------------------------------------------------------------------------

# cache data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, encoding='utf8')
    return df

nsicu_df = load_data('data/nsicu_data_new.csv')

# fix name in death column
nsicu_df.rename(columns={'Death ': 'death'}, inplace=True)

# -----2 COLUMNS WITH INTRO AND FILTERABLE STATS---------------------------------------------------------------------------------------------                         
## shows introduction and creates a multiselect filter on sidebar to filter overview by disease ##

st.title("Outcomes for Neurocritically Ill ICU Patients")

#create columns, col1 should be wider
intro, pt_breakdown = st.columns([3,1])

#col1 introduction
with intro:
    st.header('Introduction')
    st.markdown('''
            "*Neurocritical care medicine focuses on the diagnosis and treatment of life-threatening
             diseases of the nervous system, including:* 
            - brain and spinal cord trauma
            - cerebral edema
            - ruptured aneurysms
            - severe strokes
            - encephalitis and meningitis
            - refractory seizures
            - complicated brain tumors\"[1] 
            ''')

#col2 pt breakdown, includes sidebar multiselect

with pt_breakdown:
    def show_outcomes(data):

        st.header('  ')
        
        ## disease selection sidebar 
        selected_disease = st.multiselect('Select Disease:', nsicu_df['Category1'].unique())
        if selected_disease:
            disease_filtered =  nsicu_df[nsicu_df['Category1'].isin(selected_disease)]
        else: 
            disease_filtered = nsicu_df

        ## calculations for pt breakdown
        num_patients = len(disease_filtered)
        median_age = disease_filtered['Age'].median() if num_patients > 0 else 'No Patients'
        median_stay = disease_filtered['Hospital Duration (Days)'].median() if num_patients > 0 else 'No Patients'
        mortality_rate = sum(disease_filtered['death'] == 'Died') / num_patients * 100 if num_patients > 0 else 0
   
        ## markdown for breakdown calculations
        st.markdown(f'#### {num_patients} Patients')
        st.markdown(f" ##### Median Patient Age **{median_age} years**")
        st.markdown(f" ##### Median Stay: **{median_stay} days**")
        st.markdown(f" ##### Mortality Rate: **{mortality_rate:.2f}%**") 

    ## show 
    if __name__ == "__main__":
        show_outcomes(nsicu_df)


st.markdown('''This data set is sourced from a study of 4,750 neurocritically ill patients admitted to the ICU at Samsung Medical Center in Seoul, South Korea.
            The data spans from 2011 to 2023, with one outlier being admitted in 2004.  
            ''')

st.image('images/milad-fakurian-58Z17lnVS4U-unsplash-2-scaled.jpg', caption='Source: Milad Fakurian on Unsplash')


                                      



