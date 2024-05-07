# Analysis of Neurocritical ICU Patient Data 🩺
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nsicu-data.streamlit.app/)

## 📖 Introduction

This streamlit app explores a dataset containing data from 4750 neurocritical ICU patients. It allows users to interact with graphs to investigate relationships between factors such as age, sex, and disease inform one another and explore statistics associated with different variables. 
The purpose of this app was not to draw conclusions with, rather to provide the user tools with which to examine correlations, general trends, and relationships. 

The app has four main pages:

1️⃣ **Home:** Includes an introduction to the dataset used and outlines what neurocritical care is. 

2️⃣ **Patient Statistics:** Describes what determinants of health are and contains tabs to view data in relation to patient age and sex.

3️⃣ **Mortality:** Establishes the importance and possible use cases of tracking mortality data and shows some basic mortality statistics as well as graphs showing mortality across varying factors. It also includes tabs for several established and proposed prognostic tools.

4️⃣ **Sources:** Includes all sources cited in this app as well as the data source.  


## 🔬 Data Source & Preparation

### Preparation
Because the dataset used was very clean to begin with, most of the preparation for this project involved creating columns calculated from the existing data as well as several smaller dataframes for specific use cases. 

### Source
Ryu, Jeong-Am, 2024, "The association between arterial oxygen level and clinical outcome in neurocritically ill patients with brain tumor", https://doi.org/10.7910/DVN/89MI66, Harvard Dataverse, V1 


## 💡 Future Work
A possible direction for this project to go in the future would be comparing ICU data from the same hospital this data is sourced from to investigate whether neurocritical patients there have better, worse, or similar outcomes. Additionally, comparing this data to other hospitals may also be interesting. 


