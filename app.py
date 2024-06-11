import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the path to the CSV file
csv_file = 'output.csv'

# Load the CSV file into a DataFrame
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    st.error('CSV file not found. Please make sure the file exists and try again.')
    st.stop()

# Data cleaning and preprocessing
# Drop rows with NOTA status
df = df[df['Status'] != 'NOTA']

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

# Convert 'Obtained Votes' and 'Difference Votes' to numeric
df['Obtained Votes'] = pd.to_numeric(df['Obtained Votes'].str.replace(',', ''), errors='coerce')
df['Difference Votes'] = pd.to_numeric(df['Difference Votes'].str.replace(',', ''), errors='coerce')

# Streamlit App Title
st.title('Election Results 2024')

# Sidebar for Filtering
st.sidebar.header('Filter Results')

# State Filter
states = df['State Name'].unique()
selected_state = st.sidebar.selectbox('Select State', states)

# Filter Constituencies based on selected State
filtered_constituencies = df[df['State Name'] == selected_state]['Constitution Assembly'].unique()
selected_constituency = st.sidebar.selectbox('Select Constituency', filtered_constituencies)

# Filter DataFrame based on selections
filtered_df = df[(df['State Name'] == selected_state) & (df['Constitution Assembly'] == selected_constituency)]

# Display the filtered DataFrame
st.header(f'Results for {selected_constituency} in {selected_state}')
st.dataframe(filtered_df)

# Summary Statistics
st.header('Summary Statistics')
st.write(filtered_df.describe())


# if st.button('Reload Data'):
#     df = pd.read_csv(csv_file)
#     st.experimental_rerun()


# Party-wise Data
party_data = filtered_df.groupby('Party Name').sum()['Obtained Votes'].reset_index()
st.header('Party-wise Data')
st.dataframe(party_data)

# State-wise Data
state_data = df.groupby('State Name').sum()['Obtained Votes'].reset_index()
st.header('State-wise Data')
st.dataframe(state_data)

# State-wise Winners
state_winners = df[df['Status'] == 'won'].groupby('State Name')['Candidate Name'].first().reset_index()
st.header('State-wise Winners')
st.dataframe(state_winners)

# Party-wise Total Winners
party_winners = df[df['Status'] == 'won'].groupby('Party Name').size().reset_index(name='Total Winners')
st.header('Party-wise Total Winners')
st.dataframe(party_winners)

