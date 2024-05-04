import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

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

# #---FILTER AGE/SEX-----------------------------------------------------------------------------------------------------------------

def show_mortality(data): 
    # st.subheader('Patient Breakdown')
    # st.markdown(f"Use the side bar to filter the patient breakdown by disease category.")
    
    ## disease selection sidebar 
    selected_age_group = st.sidebar.multiselect('Select Age Group:', nsicu_df['Age Group'].unique())
    if selected_age_group:
        selected_age_group =  nsicu_df[nsicu_df['Category1'].isin(selected_age_group)]
    else: 
        selected_age_group = nsicu_df

    ## calculations for pt breakdown
    num_patients = len(selected_age_group)
    median_age = selected_age_group['Age'].median() if num_patients > 0 else 'No Patients'
    median_stay = selected_age_group['Hospital Duration (Days)'].median() if num_patients > 0 else 'No Patients'
    mortality_rate = sum(selected_age_group['death'] == 'Died') / num_patients * 100 if num_patients > 0 else 0
   
    ## markdown for breakdown calculations
    st.markdown(f'#### {num_patients} Patients')
    st.markdown(f" ##### Median Patient Age **{median_age} years**")
    st.markdown(f" ##### Median Stay: **{median_stay} days**")
    st.markdown(f" ##### Mortality Rate: **{mortality_rate:.2f}%**") 
    

## show 
if __name__ == "__main__":
    show_mortality(nsicu_df)



#---PERCENT HOSPITAL DEATHS-----------------------------------------------------------------------------------------------------------------

# hospital mortality
hosp_mortality_yes = nsicu_df[nsicu_df["In hospital mortality"] == "Y"].count().max()
hosp_mortality_no = nsicu_df[nsicu_df["In hospital mortality"] == "N"].count().max()

# icu mortality
icu_mortality_yes = nsicu_df[nsicu_df["ICU mortality"] == "Y"].count().max()
icu_mortality_no = nsicu_df[nsicu_df["ICU mortality"] == "N"].count().max()

# number deaths
death_count =  nsicu_df[nsicu_df['death'] == 'Died'].count().max()

# percent icu and hospital deaths
percent_hosp_deaths = round((hosp_mortality_yes/death_count)*100, 2)
percent_icu_deaths = round((hosp_mortality_yes/icu_mortality_yes)*100 , 2)

# markdowns
st.markdown(f'#### {percent_hosp_deaths}% of deaths occured in the hospital.')
st.markdown(f'#### {percent_icu_deaths}% of deaths that occured in the hospital were in the ICU.') 


#---CREATE hosp_mortality_adj TO SHOW ALL HOSPITAL DEATHS------------------------------------------------------------------------------------------------------------------------------------------------

hosp_mortality = (
    nsicu_df[["In hospital mortality", "ICU mortality", "death"]]
)

hosp_mortality_adj = hosp_mortality[ hosp_mortality['In hospital mortality'] == 'Y' ]

# #---MORTALITY DONUT CHART------------------------------------------------------------------------------------------------------------------------------------------------

mortality_df = nsicu_df[["death", 'Age Group']]

domain = ['Died', 'Survived']
range_ = ['#0D0630', '#C1EEFF']

mortality_pie = alt.Chart(mortality_df).mark_arc(innerRadius=120).encode(
    theta="count()",
    color=alt.Color('death:N').scale(domain=domain, range=range_)
)
 
st.altair_chart(mortality_pie)



# st.dataframe(nsicu_df['death'],['Age Group'])


# def get_chart_57737(use_container_width: bool):

#     source = nsicu_df.groupby("Age Group")["Hospital Duration (Days)"].value_counts()

#     chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
#         theta=alt.Theta(field="value", type="quantitative"),
#         color=alt.Color(field="category", type="nominal"),
#     )

#     tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

#     with tab1:
#         st.altair_chart(chart, theme="streamlit", use_container_width=True)
#     with tab2:
#         st.altair_chart(chart, theme=None, use_container_width=True)

