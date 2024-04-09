import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data(excel):
    df = pd.read_excel(excel)
    return df

NSICU_df = load_data('data/NSICU_ABGA_HDN.xlsx')

# NSICU_df = pd.read_excel('data/NSICU_ABGA_HDN.xlsx')
# #NSICU_df


st.title("Outcomes for Neurocritically Ill ICU Patients")
st.markdown('''
            "Neurocritical care medicine focuses on the diagnosis and treatment of life-threatening
             diseases of the nervous system, including: 
            - brain and spinal cord trauma
            - cerebral edema
            - ruptured aneurysms
            - severe strokes
            - encephalitis and meningitis
            - refractory seizures
            - complicated brain tumors" [1] 
            ''')  
st.markdown('''This data set is sourced from a study of 4,750 neurocritically ill patients 
        that were admitted to the ICU at a hospital in South Korea.''')


# multi = '''If you end a line with two spaces,
# a soft return is used for the next line.

# Two (or more) newline characters in a row will result in a hard return.
# '''
# st.markdown(multi)





