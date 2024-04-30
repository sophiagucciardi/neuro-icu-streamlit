import streamlit as st
import altair as alt
import seaborn as sns

# cache data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, encoding='utf8')
    return df

nsicu_df = load_data('data/nsicu_data_new.csv')

# fix name in death column
nsicu_df.rename(columns={'Death ': 'death'}, inplace=True)

#----SEX VIOLIN PLOT------------------------------------------------------------------------------------------------------------------------

## REMOVE LINES OR MAKE WHITE 

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
    )
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


# -----MEDIAN STAYS BY AGE GROUPS---------------------------------------------------------------------------------------------------------                         
## graph showing the median stays for age groups ##

#group by for graph 
age_group_median_duration = (
    nsicu_df.groupby(["Age Group", "death"])["Hospital Duration (Days)"]
    .median()
    .reset_index()
)
age_group_median_duration.columns = ["age_Group", "death", "med_stay"]

#colors for died and survived
domain = ['Died', 'Survived']
range_ = ['red', 'green']

#create chart
age_duration = alt.Chart(age_group_median_duration).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x='age_Group', 
    y='med_stay', 
    color=alt.Color('death', scale=alt.Scale(domain=domain, range=range_)),
).properties(
        width=400
)
st.altair_chart(age_duration)