import streamlit as st
import plotly.express as px
import pandas as pd

child_mortality_africa = pd.read_csv('child-mortality-africa.csv')

child_mortality_africa.rename(columns={
    'Under-five mortality rate': 'Under-five mortality rate (per 100 live births)'
}, inplace=True)

# Plot child and infant mortality rates
fig_mortality = px.line(
    child_mortality_africa, 
    x='Year', 
    y='Under-five mortality rate (per 100 live births)', 
    title='Trends in Child and Infant Mortality Rates in Africa (1932–2022)',
    labels={'Under-five mortality rate (per 100 live births)': 'Deaths per 100 live births'},
    markers=True
)

fig_mortality.update_layout(
    xaxis_title='Year',
    yaxis_title='Deaths per 100 live births',
    template='plotly_white'
)


infant_deaths_africa = pd.read_csv('infant-deaths-africa.csv')

infant_deaths_africa['Deaths (millions)'] = infant_deaths_africa['Deaths'] / 1e6

# Plot child and infant deaths
fig_infant_deaths = px.line(
    infant_deaths_africa,
    x='Year',
    y='Deaths (millions)',
    title='Infant Deaths in Africa (1950–2023)',
    labels={'Deaths (millions)': 'Deaths (in millions)'},
    markers=True
)

fig_infant_deaths.update_layout(
    xaxis_title='Year',
    yaxis_title='Deaths (in millions)',
    template='plotly_white'
)


child_mortality = pd.read_csv('child-mortality.csv')

african_countries = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", 
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", 
    "Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eswatini", 
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", 
    "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", 
    "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", 
    "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", 
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", 
    "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", 
    "Zambia", "Zimbabwe"
]

africa_2022 = child_mortality[
    (child_mortality['Year'] == 2022) & 
    (child_mortality['Entity'].isin(african_countries))
]

africa_2022.rename(columns={'Under-five mortality rate': 'Mortality Rate'}, inplace=True)

# Create map visualization
fig_map = px.choropleth(
    africa_2022,
    locations='Entity',  # Column with country names
    locationmode='country names',
    color='Mortality Rate',
    hover_name='Entity',
    title='Under-Five Mortality Rates in Africa (2022)',
    color_continuous_scale='Reds',
    labels={'Mortality Rate': 'Deaths per 100 live births'}
)

# Update layout for focusing on Africa
fig_map.update_geos(
    visible=True,
    resolution=50,
    showcountries=True,
    countrycolor="Black",
    fitbounds="locations",
    projection_type="mercator"
)

fig_map.update_layout(
    template='plotly_white',
    title_x=0.5,
    width=1200,  
    height=900,  
    margin={"r":0, "t":50, "l":0, "b":0} 
)

df = pd.read_csv('causes-of-death.csv')

# Filter for African countries, Period=2017, and relevant age groups (0-27 days, 1-9 months, 0-4 years)
african_countries = df[df['Location'].isin([
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 
    'Comoros', 'Congo', 'Congo (Democratic Republic)', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 
    'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 
    'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'São Tomé and Príncipe', 
    'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
])]

# Further filter for periods 2017 and age groups of interest
age_groups = ['0-27 days', '1-9 months', '0-4 years']
df_filtered = african_countries[(df['Period'] == 2017) & (df['Dim1'].isin(age_groups))]

# Find the cause of death with the highest value for each country and age group
df_max_cause = df_filtered.loc[df_filtered.groupby(['Location', 'Dim1'])['FactValueNumeric'].idxmax()]

fig_causes_of_death = px.bar(df_max_cause, 
             x='Location', 
             y='FactValueNumeric', 
             color='Dim2', 
             title='Leading Causes of Death in African Countries (2017)', 
             labels={'FactValueNumeric': 'Cause of Death (%)', 'Location': 'Country'},
             color_discrete_sequence=px.colors.qualitative.Set1)

fig_causes_of_death.update_layout(
    xaxis_title='Country',
    yaxis_title='Percentage of Deaths Due to Cause (%)',
    xaxis_tickangle=-45,
    showlegend=True
)

births_df = pd.read_csv('births-attended.csv')

regions = [
    'East Asia and Pacific (WB)', 'Europe and Central Asia (WB)', 
    'Latin America & the Caribbean (WB)', 'Middle East and North Africa (WB)', 
    'North America (WB)', 'South Asia (WB)', 'Sub-Saharan Africa (WB)'
]

# Filter for 2019 data and the relevant regions
births_2019 = births_df[(births_df['Year'] == 2019) & (births_df['Entity'].isin(regions))]

mortality_df = pd.read_csv('child-mortality.csv')

# Mapping for the regions in child-mortality.csv to match the names in births-attended.csv
region_mapping = {
    'East Asia and Pacific (WB)': 'Eastern Asia and South-Eastern Asia (SDG)',
    'Europe and Central Asia (WB)': 'Europe (SDG)',
    'Latin America & the Caribbean (WB)': 'Latin America and the Caribbean (SDG)',
    'Middle East and North Africa (WB)': 'Northern Africa (SDG)',
    'North America (WB)': 'Northern America (SDG)',
    'South Asia (WB)': 'Southern Asia (SDG)',
    'Sub-Saharan Africa (WB)': 'Sub-Saharan Africa (SDG)'
}

# Apply the mapping to align regions
births_2019['Mapped_Region'] = births_2019['Entity'].map(region_mapping)

mortality_2019 = mortality_df[(mortality_df['Year'] == 2019) & (mortality_df['Entity'].isin(region_mapping.values()))]

merged_df = pd.merge(births_2019, mortality_2019, left_on='Mapped_Region', right_on='Entity', suffixes=('_births', '_mortality'))

# Create the scatter plot to compare healthcare attendance with mortality rates
fig_healthcare_vs_mortality = px.scatter(
    merged_df,
    x='Births attended by skilled health staff (% of total)',  # X-axis: healthcare attendance percentage
    y='Under-five mortality rate',  # Y-axis: mortality rate
    color='Mapped_Region',  # Color by region
    title='Healthcare Attendance vs Under-five Mortality Rate (2019)',
    labels={'Births attended by skilled health staff (% of total)': 'Percentage of Births Attended',
            'Under-five mortality rate': 'Under-five Mortality Rate (per 1,000 live births)',
            'Mapped_Region': 'Region'},
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_healthcare_vs_mortality.update_layout(
    xaxis_title='Percentage of Births Attended by Skilled Health Staff',
    yaxis_title='Under-five Mortality Rate (per 1,000 live births)',
    showlegend=True
)


# 2. Create Streamlit Dashboard Layout
# Sidebar for navigation
st.sidebar.title("Child Mortality Dashboard")
sidebar_option = st.sidebar.radio("Select a visualization", 
                                  ['Child and Infant Mortality Rates', 
                                   'Infant Deaths',
                                   'Under-Five Mortality Map',
                                   'Leading Causes of Death',
                                   'Healthcare Attendance vs Mortality Rate'])

# Display selected visualization
if sidebar_option == 'Child and Infant Mortality Rates':
    st.plotly_chart(fig_mortality)
elif sidebar_option == 'Infant Deaths':
    st.plotly_chart(fig_infant_deaths)
elif sidebar_option == 'Under-Five Mortality Map':
    st.plotly_chart(fig_map)
elif sidebar_option == 'Leading Causes of Death':
    st.plotly_chart(fig_causes_of_death)
elif sidebar_option == 'Healthcare Attendance vs Mortality Rate':
    st.plotly_chart(fig_healthcare_vs_mortality)

# Footer or Additional Information
st.markdown("""
    ## Insights:
    This dashboard presents visualizations on child and infant mortality rates, 
    causes of death, healthcare access, and other key factors that impact child health.
""")

