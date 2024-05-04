import streamlit as st
import altair as alt
import seaborn as sns
import plotly.express as px
import pandas as pd

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

#----TITLE & IMAGE TABS-------------------------------------------------------------------------------------------------------------

title_col, image_col = st.columns(2)

with title_col:
    st.title('Patient Statistics :stethoscope:')
    st.markdown(''' Health and health outcomes are influenced by many things. Broadly, most factors can be organized into categories:''')
    st.markdown('''
                :dna: Genetics  
                :wave: Behavior  
                :leaves: Environmental  
                :muscle: Physical Influences  
                :ambulance: Medical Care & Social Factors  
                ''')
    st.markdown('''
                Although this dataset does not include social, environmental, or behavioral factors, genetic and medical factors as well as physical influences are represented in the data.''')  
    st.markdown(''' ###### Explore some determinants of health using the tabs below:  ''')
with image_col:
    st.markdown('''
                #  
                #''')
    st.image('images/kristine-wook-ZyxNWi3JCto-unsplash.jpg', caption='Image from Kristine Wook on Unsplash')





#------TABS-------------------------------------------------------------------------------------------------------------
age_tab, sex_tab, comorbidity_tab, stay_duration_tab = st.tabs(["Age", "Sex", "Comorbidities", "Admission Duration"])

with age_tab:
   
   age_intro_col, age_df_col = st.columns([4.5, 1], gap='medium')

   with age_intro_col:
       st.markdown(" ### Patient Age")
       st.markdown(''' Age has been observed to be a factor in patient outcomes in a number of ways. 
               Oftentimes, very young or very old patients can be more vulnerable to serious illness and injury and 
               can be more at risk of contracting infectious illnesses.  
               Children are at higher risk for a variety of reasons. For example, they are more likely to come in contact with environmental hazards, as young children often put their hands in their
               mouths and spend more time on the ground and outdoors than most people in other age groups. Children have weaker immune
               systems and at the same time have frequent contact with others through places like school or daycare, and are therefore
               more likely to catch infectious diseases. Very young children are also unable to communicate how they are feeling, 
               which can make assessing their condition and accessing care in a timely manner more difficult than it would be for someone
               who can communicate an issue. [2].  
                   Older adults are more often to have one or more chronic conditions, which can complicate care, and are more likely
               than other age groups to be hospitalized for some infectious illnesses. [3]  
               For neurocritically ill patients, mortality and otherwise unfavorable outcomes are associated with ages 60 years and above. 
               These patients also have higher clinical severity on average than other age groups. [4]  
                    ''')
   with age_df_col: 
       st.markdown('#### Age Ranges Represented:')
       age_df = nsicu_df[['Age Group']].value_counts().sort_index()
       age_df = age_df.rename(index={'80':'80+'}).to_frame("Patients")
       
       st.dataframe(age_df)

  
   
   selected_age = st.multiselect('Filter Diseases by Age Group:', nsicu_df['Age Group'].unique())
   if selected_age:
      age_filtered =  nsicu_df[nsicu_df['Age Group'].isin(selected_age)]
   else: age_filtered = nsicu_df

   age_filtered = age_filtered.sort_index().rename(index={'80':'80+'})


   age_chart = alt.Chart(age_filtered).mark_bar().encode(
    x=alt.X('count()', title='Number of Patients'),
    y=alt.Y('Category1', title='Disease', ).sort('-x')
    ).configure_axis(labelLimit=300, grid=False, ticks=False
    ).properties(width=900, height=300)
   
   
   st.altair_chart(age_chart)




    # st.markdown(f'### Graph')
    # st.subheader('Plotly Chart')
    # age_fig = px.histogram(nsicu_df['Age Group'])
    # st.plotly_chart(age_fig)


with sex_tab:
   st.header("Patient Sex")
   
   vio_graph_col, sex_intro = st.columns(2)
   
   #---SEX VIOLIN PLOT------------------------
   st.markdown(f'###### Age and Sex Distrubution')
   with vio_graph_col:
      # Color
        domain = ['Male', 'Female']
        range_ = ['#6fa8dc', '#ecc6d9']

        # Violin plot
        sex_violin = alt.Chart(nsicu_df).transform_density(
            'Age',
            as_=['Age', 'density'],    
            groupby=['Sex']
        ).mark_area(orient='horizontal').encode(
            y='Age:Q',
            color=alt.Color('Sex:N', scale=alt.Scale(domain=domain, range=range_)),
            x=alt.X(
                'density:Q',
                stack='center',
                impute=None,
                title=None,
                axis=alt.Axis(labels=False, values=[0],grid=False, ticks=False)        
            ),
            column=alt.Column(
                'Sex:N'
            ),
            tooltip=alt.value(None)
        ).properties(
            width=100
        ).configure_facet(
            spacing=0
        ).configure_axis(
            grid=False
        ).configure_view(
            stroke=None
        )
        st.altair_chart(sex_violin)
        st.caption('This violin plot provides a quick visual representation of the distribution of males and females in this study by their age groups.')


with comorbidity_tab:
    st.header('Comorbidities')

with stay_duration_tab:
   st.header("Duration of Time Admitted")

   #---MED DURATION/AGE GRAPH----------------------------------------------
   age_group_median_duration = (
       nsicu_df.groupby(["Age Group", "death"])["Hospital Duration (Days)"]
        .median()
        .reset_index()
    ) 
   
   age_group_median_duration.columns = ["age_Group", "death", "med_stay"]

   domain = ['Died', 'Survived']
   range_ = ['#0D0630', '#C1EEFF']

#create chart
#cornerRadius round corners

   age_duration = alt.Chart(age_group_median_duration).mark_bar(
       cornerRadiusTopLeft=3,
       cornerRadiusTopRight=3
   ).encode(
      x=alt.X('age_Group', title= 'Age Group'),
      y=alt.Y('med_stay', title='Median Admission Duration (Days)'),
      color=alt.Color('death', scale=alt.Scale(domain=domain, range=range_)),
      tooltip=['count()']
   ).properties(width=400
   )

   st.altair_chart(age_duration)
