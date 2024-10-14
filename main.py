import pandas as pd
import plotly.express as px

# Load the Netflix dataset
df = pd.read_csv('netflix1.csv')

# Filter the data for the release year between 2008 and 2021
df['release_year'] = pd.to_datetime(df['release_year'], format='%Y')
df_filtered = df[(df['release_year'].dt.year >= 2008) & (df['release_year'].dt.year <= 2021)]

# Remove rows where the country is 'Not Given'
df_filtered = df_filtered[df_filtered['country'] != 'Not Given']

# Group the data by country to count the number of Movies/TV Shows
country_count = df_filtered['country'].value_counts().reset_index()
country_count.columns = ['Country', 'Count']

# Bubble map
fig_map = px.scatter_geo(country_count,
                         locations="Country",  # Name of the column with country names
                         locationmode='country names',  # Match by country names
                         size="Count",  # Size of circles based on the count of Movies/TV shows
                         hover_name="Country",  # Show country name on hover
                         title="Movies and TV Shows per Country (2008-2021)",
                         projection="equirectangular",  # Flat map projection
                         color_discrete_sequence=["red"])  # Red circles

# Bar chart 
fig_bar = px.bar(country_count.head(10),  # Showing top 10 countries for clarity
                 x='Country', y='Count',
                 title="Top 10 Countries by Movie & TV Show Count",
                 labels={'Count': 'Number of Movies & TV Shows'},
                 color_discrete_sequence=['red'])

# Create a line graph for the amount of content added to Netflix by just India, South Korea, and Japan per year

# Filter for the relevant countries and convert release_year to datetime
df_filtered['year'] = df_filtered['release_year'].dt.year
countries_of_interest = ['India', 'South Korea', 'Japan']
df_countries = df_filtered[df_filtered['country'].isin(countries_of_interest)]

# Group by year and country, then count the number of shows/movies
content_count = df_countries.groupby(['year', 'country']).size().reset_index(name='count')

fig_line = px.line(content_count, 
                   x='year', 
                   y='count', 
                   color='country', 
                   title='Content Added to Netflix by India, South Korea, and Japan per Year',
                   labels={'count': 'Number of Movies/TV Shows'},
                   markers=True)

fig_map.show()
fig_bar.show()
fig_line.show()
