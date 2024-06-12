

import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu

# Load the dataset
data = pd.read_csv('output.csv')

# Clean and process data if necessary
def clean_votes(votes):
    try:
        return int(str(votes).replace(',', ''))
    except ValueError:
        return None

data['Obtained Votes'] = data['Obtained Votes'].apply(clean_votes)

# Clean 'Difference Votes' column
def clean_difference_votes(diff_votes):
    try:
        return int(''.join(filter(str.isdigit, str(diff_votes))))
    except ValueError:
        return None

data['Difference Votes'] = data['Difference Votes'].apply(clean_difference_votes)

# Function to define the HTML and CSS for the navbar
def get_navbar():
    navbar_html = """
    <style>
        .navbar {
            background-color: #a22034;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar .logo {
            display: flex;
            align-items: center;
        }
        .navbar .logo img {
            height: 50px;
            margin-right: 10px;
        }
        .navbar .links {
            display: flex;
            align-items: center;
        }
        .navbar .links a {
            color: white;
            text-decoration: none;
            padding: 0 15px;
            font-size: 18px;
        }
        .navbar .links a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="navbar">
        <div class="logo">
            <img src="https://via.placeholder.com/50" alt="Logo">
            <span style="color: white; font-size: 24px;">Election Commission of India</span>
        </div>
        <div class="links">
            <a href="#">Home</a>
            <a href="#">English</a>
            <a href="#">Refresh</a>
        </div>
        <div class="logo">
            <img src="https://via.placeholder.com/50" alt="Desh ka Garv">
        </div>
    </div>
    """
    return navbar_html

# Function to define the header section
def get_header():
    header_html = """
    <div style="background-color: #ffef96; padding: 10px; text-align: center; font-size: 16px;">
        <strong>अस्वीकरण:</strong> दी गयी जानकारी आधिकारिक है। 
    </div>
    """
    return header_html

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Election Results", layout="wide")

    # Display the navbar
    st.markdown(get_navbar(), unsafe_allow_html=True)

    # Display the header
    st.markdown(get_header(), unsafe_allow_html=True)

    # Create navigation sidebar using option_menu
    with st.sidebar:
        page = option_menu(
            "Main Menu", 
            ["Overall Results", "State-wise Results", "Constituency-wise Results", "Candidate Profiles"], 
            icons=["house", "bar-chart-line", "globe", "person-lines-fill"], 
            menu_icon="cast", 
            default_index=0
        )

    if page == "Overall Results":
        display_overall_results()
    elif page == "State-wise Results":
        display_state_results()
    elif page == "Constituency-wise Results":
        display_constituency_results()
    elif page == "Candidate Profiles":
        display_candidate_profiles()

# Function to display overall results
def display_overall_results():
    st.title("Overall Election Results")

    # Plot overall votes by party
    overall_party_fig = px.bar(data, x='Party Name', y='Obtained Votes', color='Party Name', title='Overall Votes by Party')
    st.plotly_chart(overall_party_fig, use_container_width=True)

    # Plot overall votes distribution
    overall_votes_fig = px.pie(data, names='Party Name', values='Obtained Votes', title='Overall Votes Distribution')
    st.plotly_chart(overall_votes_fig, use_container_width=True)

    # donut chart for top 5 parties
    st.header('Top 5 Parties - Donut Chart')

    # Calculate total won seats for top 5 parties
    total_won_seats = data[data['Status'] == 'won'].groupby('Party Name')['Candidate Name'].count().sort_values(ascending=False)
    top5_won_seats = total_won_seats.head(5)

    # Calculate total won seats for 'Others'
    others_won_seats = total_won_seats.iloc[5:].sum()

    # Combine top 5 parties and 'Others'
    top5_won_seats['Others'] = others_won_seats

    # Plot donut chart
    fig = px.pie(
        values=top5_won_seats.values,
        names=top5_won_seats.index,
        title='Top 5 Party Wise Election Won Seats',
        hole=0.5,
    )
    st.plotly_chart(fig)

# Function to display state-wise results
def display_state_results():
    st.title("State-wise Election Results")

    state_options = data['State Name'].unique()
    state = st.selectbox("Select State", state_options, index=0)

    if state:
        state_data = data[data['State Name'] == state]

        # Plot state-wise votes by party
        state_party_fig = px.bar(state_data, x='Party Name', y='Obtained Votes', color='Party Name', title=f'Votes by Party in {state}')
        st.plotly_chart(state_party_fig, use_container_width=True)

        # Plot state-wise votes distribution
        state_votes_fig = px.pie(state_data, names='Party Name', values='Obtained Votes', title=f'Votes Distribution in {state}')
        st.plotly_chart(state_votes_fig, use_container_width=True)

# Function to display constituency-wise results
def display_constituency_results():
    st.title("Constituency-wise Election Results")

    state_options = data['State Name'].unique()
    state = st.selectbox("Select State", state_options, index=0)

    if state:
        constituency_options = data[data['State Name'] == state]['Constitution Assembly'].unique()
        constituency = st.selectbox("Select Constituency", constituency_options, index=0)

        if constituency:
            constituency_data = data[(data['State Name'] == state) & (data['Constitution Assembly'] == constituency)]

            # Plot constituency-wise votes by party
            constituency_party_fig = px.bar(constituency_data, x='Party Name', y='Obtained Votes', color='Party Name', title=f'Votes by Party in {constituency}')
            st.plotly_chart(constituency_party_fig, use_container_width=True)

            # Plot constituency-wise votes distribution
            constituency_votes_fig = px.pie(constituency_data, names='Party Name', values='Obtained Votes', title=f'Votes Distribution in {constituency}')
            st.plotly_chart(constituency_votes_fig, use_container_width=True)

# Function to display candidate profiles
def display_candidate_profiles():
    st.title("Candidate Profiles")

    state_options = data['State Name'].unique()
    state = st.selectbox("Select State", state_options, index=0)

    if state:
        constituency_options = data[data['State Name'] == state]['Constitution Assembly'].unique()
        constituency = st.selectbox("Select Constituency", constituency_options, index=0)

        if constituency:
            filtered_data = data[(data['State Name'] == state) & (data['Constitution Assembly'] == constituency)]

            if 'Status' in filtered_data.columns:
                st.markdown("""
                <style>
                .cand-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 1rem;
                }
                .cand-box {
                    background-color: #fff;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                }
                .cand-box img {
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    margin-bottom: 1rem;
                }
                .cand-box h5 {
                    margin: 0.5rem 0;
                    color: #004274;
                }
                .cand-box h6 {
                    margin: 0;
                    color: #0a8bfd;
                }
                .cand-box .status {
                    font-weight: bold;
                }
                </style>
                <div class="cand-container">
                """, unsafe_allow_html=True)

                for index, candidate in filtered_data.iterrows():
                    text_color = 'green' if str(candidate['Status']).lower() == 'won' else 'red'

                    st.markdown(f"""
                    <div class="cand-box">
                        <h5>{candidate['Candidate Name']}</h5>
                        <h6>{candidate['Party Name']}</h6>
                        <div class="status" style="color: {text_color};">{candidate['Status']}</div>
                        <div>Votes: {candidate['Obtained Votes']} <span>({candidate['Difference Votes']:+})</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
