import streamlit as st
import altair as alt
import seaborn as sns
import plotly.express as px

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


# Custom CSS to inject
custom_css = """
<style>
    /* Custom style for the active tab */
    .stTabs > .tablist > .react-tabs__tab--selected {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Custom style for all tabs */
    .stTabs > .tablist > .react-tabs__tab {
        background-color: #e8e8e8;
        color: #4f4f4f;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

age_tab, sex_tab, comorbidity_tab, stay_duration_tab = st.tabs(["Age", "Sex", "Comorbidities", "Admission Duration"])

with age_tab:
   st.markdown("Patient Age")
   
   graph_col, intro_col = st.columns(2)

   with graph_col:
      st.markdown(f'### Graph')
      st.subheader('Plotly Chart')
      age_fig = px.histogram(nsicu_df['Age Group'])
      st.plotly_chart(age_fig)

  

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
                axis=alt.Axis(labels=False, values=[0],grid=False, ticks=True)        
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
