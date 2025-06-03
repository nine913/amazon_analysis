import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide',
    page_title='Forest Fire Analysis',
    page_icon=':fire:')

st.title('Forest Fire Analysis')

@st.cache_data
def load_data():
    fire = pd.read_csv(r'new_data/new_fire_incident.csv')
    forest = pd.read_csv(r'new_data/new_desforestation.csv')
    return fire, forest

fire, forest = load_data()

fire['el_nino_label'] = fire['el_nino'].map({True: 'Year with El Nino', False: 'Year without El Nino'})
forest['el_nino_label'] = forest['el_nino'].map({True: 'Year with El Nino', False: 'Year without El Nino'})

states = sorted(forest['state_abbrev'].unique())
state = st.sidebar.selectbox('Select State', states)

years = forest['year'].unique()
start_year, last_year = st.sidebar.slider('Select Year', int(min(years)), int(max(years)), (2004, 2014))

df_f = forest[
    (forest['state_abbrev'] == state) &
    (forest['year'].between(start_year, last_year))
]

df_i = fire[
    (fire['state_abbrev'] == state) & 
    (fire['year'].between(start_year, last_year))
]

st.subheader('Desforestation (km²)')
fig_f = px.line(
    df_f, x='year', y='desforestation_km2',
    color='el_nino_label',
    markers=True,
    labels={'year': 'Year', 'desforestation_km2': 'Desforestation (km²)', 'el_nino_label': 'Climatic condition'},
    color_discrete_map={'Year with El Nino': 'red', 'Year without El Nino': 'green'}
    
)
st.plotly_chart(fig_f)

st.subheader('Fire Incidents')

fig_i = px.line(
    df_i, x='year', y='firespots',
    color='el_nino_label',
    markers=True,
    labels={'year': 'Year', 'firespots': 'Fire Incidents', 'el_nino_label': 'Climatic condition'},
    color_discrete_map={'Year with El Nino': 'red', 'Year without El Nino': 'blue'}
)
st.plotly_chart(fig_i)


df_merge = pd.merge(
    df_f[['year', 'desforestation_km2']],
    df_i[['year', 'firespots']],
    on='year'
)

df_melted = df_merge.melt(
    id_vars='year',
    value_vars=['desforestation_km2', 'firespots'],
    var_name='type', value_name='value'
)

df_melted['type'] = df_melted['type'].map({
    'desforestation_km2': 'Desforestation (km²)',
    'firespots': 'Fire Incidents'
})

st.subheader('Side-by-Side Comparison: Deforestation vs Firespots')
fig_b = px.bar(
    df_melted,
    x='year', y='value', color='type',
    barmode='group',
    labels={'year': 'Year', 'value': 'Value', 'type': 'Type'},
    color_discrete_map={'Desforestation (km²)': 'green', 'Fire Incidents': 'orangered'}
)
st.plotly_chart(fig_b)