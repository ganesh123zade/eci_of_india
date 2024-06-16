import streamlit as st
import plotly.graph_objects as go 
import pandas as pd
import seaborn as sns

# Load the dataset
data = pd.read_csv('output.csv')

# Calculate total won seats for top 5 parties
total_won_seats = data[data['Status'] == 'won'].groupby('Party Name')['Candidate Name'].count().sort_values(ascending=False)
top5_won_seats = total_won_seats.head(5)

# Calculate total won seats for 'Others'
others_won_seats = total_won_seats.iloc[5:].sum()

# Combine top 5 parties and 'Others'
top5_won_seats['Others'] = others_won_seats

# Sort the data in descending order
# top5_won_seats = top5_won_seats.sort_values(ascending=False)

# Create data for the chart
data = list(top5_won_seats.values)
data.append(sum(data))  # Adding the sum to create a half-donut effect

# Create labels for the chart
labels = list(top5_won_seats.index)
labels.append("")  # Adding an empty label for the blank space

# Create custom colors
# colors = sns.color_palette('Set2', len(top5_won_seats)).as_hex()

colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', 'ffer00']
colors.append('white')  # Adding a white color for the blank space

# Create the semi-donut chart using Plotly
fig = go.Figure(data=[
    go.Pie(
        labels=labels,
        values=data,
        hole=0.5,
        rotation=-90,
        direction='clockwise',
        marker=dict(colors=colors),
        sort=False,
        textinfo='none',
        # hoverinfo='label+value',  # Specify what to display on hover
        hovertemplate='<b>%{label}</b><br>Seats Won: %{value}<extra></extra>'  # Customize the hover information
    )
])

# Adjust layout for a semi-donut effect
fig.update_layout(
    title='Top 5 Party Wise Election Won Seats',
    showlegend=False,
    annotations=[
        dict(
            text='543/543', 
            x=0.5, y=0.5, 
            font_size=20, 
            showarrow=False
        )
    ],
    width=600,
    height=400
)

# Display the half-donut chart in Streamlit
st.header('Top 5 Parties - Half Donut Chart')

st.plotly_chart(fig, use_container_width=True)
# Create the semi-donut chart using Plotly


