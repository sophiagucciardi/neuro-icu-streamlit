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

domain = ['Died', 'Survived']
range_ = ['#0D0630', '#C1EEFF']


#---SIDE BAR FILTER-------------------------------------------------------------------------------------------------------------------------------------------

# side bar:
with st.sidebar:
    st.markdown('''
    ## Select Diseases
    ''')

    # add checkboxes to sidebar, but with labels for filtering
    checkboxes = [(disease, st.checkbox(disease)) for disease in nsicu_df['Category1'].unique() ]

    # find which diseases are selected
    diseases_selected = [checkbox[0] for checkbox in checkboxes if checkbox[1]]

    #filter down dataframe
    if diseases_selected:
        disease_filtered = nsicu_df[nsicu_df['Category1'].isin(diseases_selected)]
    else:
        disease_filtered = nsicu_df


#---INTRO AND GRAPH-------------------------------------------------------------------------------------------------------------------------------------------

#create columns
mort_pie_col, intro_col = st.columns([1, 1.5])


#---MORTALITY PIE------------------------------------

with mort_pie_col:

    st.markdown(''' # ''')
    
    mortality_pie = alt.Chart(disease_filtered).mark_arc(innerRadius=120).encode(
        theta='count()',
        color=alt.Color('death:N').scale(domain=domain, range=range_),
        tooltip=[alt.Tooltip('death:N', title="Status:"), alt.Tooltip('count()', title="Number of Patients:")]
    ).configure_header(
        titleColor='#f9f7fb',
        titleFontSize=14,
        titleAlign='center'
    )

    # show graph 
    st.altair_chart(mortality_pie)


#---INTRO------------------------------------

with intro_col:

    # page title
    st.title('Patient Mortality')

    st.markdown('''Mortality is tracked for a multitude of reasons. For example, tracking mortality can give insights into how severe an illness or type of injury generally is, it can highlight discrepancies in care, or it can be used to evaluate the effectiveness of different treatments or preventions, and can inform public health initiatives. [9]  
                Monitoring mortality is a critical part of healthcare around the world, and many countries have done so for a long time [8].  
                A study following ICU patients in Brazil found a mean mortality rate about 1.7 times higher in patients requiring neurocritical care than ICU patients who did not (17.21\% and 10.1\% respectively). ''')
    st.markdown(''' There are a number of risk factors and predictors for mortality and unfavorable outcomes in patients. Some of these are advanced age, a higher number of possible secondary injuries, emergency admission, 
                and worse APACHE II and Glasgow coma scale scores. [9] ''')

#---CHECKBOX AND GRAPH-------------------------------------------------------------------------------------------------------------------------------------------

# create columns
numbers_col, graph_col = st.columns([2,3])

#--NUMBERS COL-------------------------------

with numbers_col:

    # mortality statistics calculations:
    num_patients = len(disease_filtered)
    num_patients_dec = len(disease_filtered[disease_filtered['death'] == 'Died'])
    mort_rate = num_patients_dec/num_patients * 100 if num_patients_dec > 0 else '0'
    median_age_dec = disease_filtered['Age'].median() if num_patients_dec > 0 else 'No Patients Died'
    med_death_days = disease_filtered[disease_filtered['death'] == 'Died']['Hospital Duration (Days)'].median() if num_patients_dec > 0 else 'No Patients Died'
    percent_icu_deaths = round((len(disease_filtered[disease_filtered['ICU mortality'] == 'Y'])/num_patients_dec)*100, 2)

    # mortaliy statistics markdowns
    st.subheader('Mortality Statistics')
    st.markdown(f'''  * **{num_patients} Patients Total**''')
    st.markdown(f'''  * **{num_patients_dec} Patients** Died''')
    st.markdown(f'''  * **{mort_rate:.2f} %** Mortality Rate''')
    st.markdown(f'''  * Median Age of Deceased Patients: **{median_age_dec} Years**''')
    st.markdown(f'''  * **{percent_icu_deaths} %** of hospital deaths occured in the ICU''')
    st.markdown(f'''  * 50 % of all deaths occured within **{med_death_days} days** of admission''')


#---GRAPH COL-------------------------------

with graph_col: 

    age_death = alt.Chart(disease_filtered).mark_bar(cornerRadiusTopLeft=50, cornerRadiusTopRight=50, cornerRadiusBottomLeft=50, cornerRadiusBottomRight=50
            ).encode(
            x=alt.X('Age Group:N'),
            y=alt.Y('count()', title='Number of Patients').stack('normalize'),
            color=alt.Color('death:N').scale(domain=domain, range=range_),
            tooltip=[
                        alt.Tooltip('death:N', title="Status\:"), 
                        alt.Tooltip('count()', title="Number of Patients\:"), 
                        alt.Tooltip('Age Group', title='Age Group\:')
                     ]
        ).configure_axis(labelLimit=300, grid=False, ticks=False
        ).properties(width=700, height=300
        ).configure_mark(width=28)
    
    st.subheader('Deaths by Age Group')

    st.altair_chart(age_death)

#Classically, prognosis is defined as a forecast or prediction. 
#Medically, prognosis may be defined as the prospect of recovering from injury or disease, or a prediction or 
#forecast of the course and outcome of a medical condition. As such, prognosis may vary according to injury, disease, age, sex, race and treatment.

#The prognosis is a key element, not only in deciding on appropriate treatment,
#but also in discussing the opinions of patients or relatives concerning management.

st.markdown(''' #### Prognostic Tools ''')
st.markdown(''' A prognosis is a prediction about the outcome of an injury or disease and can be a key element in determining appropriate ailment for an illness. A prognosis will vary according to variables such as age, sex, race, disease, injury, and treatment. [10]  
            Prognostic tools can be used to assess a patient and inform a patient's prognosis.  
            ''')
st.markdown( ''' ##### Explore proposed and established prognostic tools below:''')
#--PROGNOSTIC TOOLS------------------------------------------------------------------------------------------------------------------------------------------------

#create tabs
crp_tab, apache_tab = st.tabs(['C-Reactive Protein', 'Apache II'])

#---CRP TAB---------------------------------------------------------
with crp_tab:

    st.header('C-Reactive Protein as a Proposed Prognostic Tool')

    crp_desc_col, crp_graph_col = st.columns(2)

#--CRP DESCRIPTION------------------
    with crp_desc_col:
        st.markdown('''C-Reactive Protein, or CRP, is made in the liver and released into the bloodstream in response to inflammation.  
                    Moderate to Severe CRP elevation will be seen in cases such as major trauma, serious infection, and heart attack, among other cuases.[5]  
                    In a study of neurocritically ill ICU patients, Dr. Jeong Am Ryu examined acute stroke patients and found that C-Reactive protein is significantly higher in non-survivors than survivors. He concluded that for some patients it can be used as an early predictor of mortality. [6]
                    ''')
#--CRP GRAPH------------------------
    with crp_graph_col:
        st.markdown(''' ##### Mortality Associated with Max CRP Levels''')

        domain = ['Died', 'Survived']
        range_ = ['#0D0630', '#C1EEFF']

        crp_graph = alt.Chart(disease_filtered).mark_bar(cornerRadiusTopRight=50, cornerRadiusBottomRight=50
        ).encode(
            x=alt.X('Crp Max:Q', title='Max CRP'),
            y=alt.Y('death:N', title=''),
            color=alt.Color('death:N', legend=None).scale(domain=domain, range=range_),
        tooltip=([
            alt.Tooltip('death:N', title="Status\:"), 
            alt.Tooltip('count()', title="Number of Patients\:"), 
            alt.Tooltip('median(CRP Max):Q', title='Median CRP Max\:')])
        ).configure_axis(
            grid=False
        ).configure_view(
            stroke=None
        ).properties(width=550, height=180)

        st.altair_chart(crp_graph)


#---APACHE II---------------------------------------------------

with apache_tab:

    st.header('APACHE II Score as an Established Prognostic Tool')

    apache_desc_col, apache_graph_col = st.columns(2)

#--APACHE II DESC------------------------
    with apache_desc_col:
        st.markdown('''The APACHE II score is a general measure of disease severity based on current physiologic measurements, age & previous health conditions. It can help in the assessment of patients to determine the level & degree of diagnostic & therapeutic intervention.''') 
        st.markdown(''' **Interpretation of APACHE II** : the score has a minimum of 0 and maximum of 71. An increasing score is associated with an increasing risk of hospital death. ''')  
        st.markdown('''The advantage of the APACHE is that it can be used throughout the patient’s hospital course in monitoring the patient’s response to therapy.  
                    The accuracy of the APACHE II at admission as an early prognostic indicator of disease severity is about 75%.[7]
                    ''')
#--APACHE II GRAPH-----------------------
    with apache_graph_col:
        st.markdown(''' ##### APACHE II Scores and Associated Mortality''')

        apache_chart = alt.Chart(disease_filtered).mark_area().encode(
            x=alt.X("APACHE2 score:Q", title='APACHE II Score'),
            y=alt.Y("count():Q", title='Percent of Patients').stack('normalize'),
            color=alt.Color("death:N", legend=None).scale(domain=domain, range=range_),
            tooltip=[
                alt.Tooltip('death:N', title="Status\:"), 
                alt.Tooltip('count():Q', title="Percent of Patients\:"), 
                alt.Tooltip('APACHE2 score:Q', title='APACHE II Score\:')]
            ).configure_axis(
            grid=False
            ).properties(width=600, height=280
            ).configure_mark(width=13
            )
        
        st.altair_chart(apache_chart)

