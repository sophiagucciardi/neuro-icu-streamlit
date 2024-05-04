import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Home", 
    layout='wide',
    page_icon=':brain:'
    )

# cache data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, encoding='utf8')
    return df

nsicu_df = load_data('data/nsicu_data_new.csv')

# fix name in death column
nsicu_df.rename(columns={'Death ': 'death'}, inplace=True)


#tabs with different groups (i.e. stroke, tumor)

#mvd = microvascular decompression

# # Calculate the correlation matrix
# correlation_matrix = filtered_df.corr()

disease_counts = nsicu_df["Category1"].value_counts()
