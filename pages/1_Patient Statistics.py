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
    st.markdown('''
                #
                ''')
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
with image_col:
    st.image('images/kristine-wook-ZyxNWi3JCto-unsplash.jpg', caption='Image from Kristine Wook on Unsplash')


st.markdown(''' #### Explore some determinants of health using the tabs below:  ''')
#------TABS-------------------------------------------------------------------------------------------------------------
age_tab, sex_tab, stay_duration_tab = st.tabs(["Age", "Sex", "Admission Duration"])


#---AGE----------------------------------------------------------------------------------------------------------------------------
with age_tab:
   

 #--AGE COLUMNS--------------------------------  
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
    
# multiselect-----
   selected_age = st.multiselect('Filter Diseases by Age Group:', nsicu_df['Age Group'].unique())
   if selected_age:
      age_filtered =  nsicu_df[nsicu_df['Age Group'].isin(selected_age)]
   else: age_filtered = nsicu_df

   age_filtered = age_filtered.sort_index().rename(index={'80':'80+'})

# graph-----------
   age_chart = alt.Chart(age_filtered).mark_bar(cornerRadiusTopRight=15, cornerRadiusBottomRight=15).encode(
    x=alt.X('count()', title='Number of Patients'),
    y=alt.Y('Category1', title='Disease' ).sort('-x')
    ).configure_axis(labelLimit=300, grid=False, ticks=False
    ).properties(width=900, height=300)
   
   st.altair_chart(age_chart)

#--SEX--------------------------------------------------------------------------------------------------------------------------
with sex_tab:
   st.markdown(''' ### Sex as an Influence on Patients ''')
   st.markdown('''
               # 
               ''')
   
   vio_graph_col, sex_intro_col = st.columns(2)
   
   #---SEX VIOLIN PLOT------------------------
   with sex_intro_col:
       
       st.markdown('''Many diseases can manifest differently in men and women and a patient's gender can put them at higher risk for some diseases and lower risk for others.   
               Many neurological disorders have been found to have strong associations with sex in terms of incidence and manifestation.   
               For example, young men are at higher risk for stroke than women. As age increases, however, women's risk outpaces men's.    
               Animal studies have found some evidence that men and women might respond differently to treatment after stroke as well. [5] ''')
       st.markdown('''
                   #   
                   ''')
    
       selected_disease = st.multiselect('Filter by disease to compare incidence in men and women:', nsicu_df['Category1'].unique())
       if selected_disease:
           disease_filtered = nsicu_df[nsicu_df['Category1'].isin(selected_disease)]
       else: disease_filtered = nsicu_df

       domain = ['Male', 'Female']
       range_ = ['#6fa8dc', '#ecc6d9']

       sex_chart = alt.Chart(disease_filtered).mark_bar(cornerRadiusTopRight=50, cornerRadiusBottomRight=50).encode(
           x=alt.X('count()', title = 'Number of Patients'),
           y=alt.Y('Sex', title=''),
           color=alt.Color('Sex', scale=alt.Scale(domain=domain, range=range_))
       ).configure_axis(grid=False, ticks=False).properties(width=450, height=150)

       st.altair_chart(sex_chart)

   with vio_graph_col:
      # Color
        domain = ['Male', 'Female']
        range_ = ['#6fa8dc', '#ecc6d9']

        # Violin plot
        sex_violin = alt.Chart(disease_filtered).transform_density(
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

#--STAY DURATION--------------------------------------------------------------------------------------------------------------------

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
