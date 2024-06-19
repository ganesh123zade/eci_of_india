from platformdirs import user_data_path
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import plotly.graph_objs as go
import urllib3











# Ensure the path to the CSV file is correct
csv_path = r'output.csv'  # Replace this with the actual path to your updated CSV file

# Check if the file exists
if not os.path.exists(csv_path):
    st.error(f"File not found: {csv_path}")
else:
    # Load data from the correct local path
    data = pd.read_csv(csv_path)

    # Check if the 'Party Short Names' column exists
    if 'Party Short Names' not in data.columns:
        st.error("The column 'Party Short Names' does not exist in the CSV file.")
    else:
        # Set up Streamlit configuration
        st.set_page_config(
            page_title="Home Page",
            page_icon="😁",
            layout="wide"
        )

        # Load CSS for styling
        css_path = r'style.css'  # Replace this with the actual path to your CSS file
        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                
                


# Custom CSS to style columns and add hover effect
custom_css = """
<style>
/* Style for column container */
.stColumn {
    border: 2px solid #2f2a70; /* Initial blue border */
    border-radius: 5px; /* Rounded corners */
    padding: 20px; /* Padding inside the column */
    margin: 10px; /* Margin around the column */
    text-align: center; /* Center text */
    color: #000; /* Text color */
    transition: border-color 0.3s; /* Smooth transition for hover effect */
}

/* Hover effect to change border color to red */
.stColumn:hover {
    
    background-color:#E9967A;
}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Create columns
col1, col2, col3 = st.columns(3)

# Column 1 with custom styling
with col1:
    st.markdown('<div class="stColumn"><h2>Parliamentary Constituency</h2></div>', unsafe_allow_html=True)

# Column 2 with custom styling
with col2:
    st.markdown('<div class="stColumn"><h2>General Assembly Constituency</h2></div>', unsafe_allow_html=True)

# Column 3 with custom styling
with col3:
    st.markdown('<div class="stColumn"><h2>General Assembly Constituency</h2></div>', unsafe_allow_html=True)

    

   















        # Inject the navigation bar HTML
nav_bar_html = """
        <div class="nav-bar">
            <div class="logo">
                <span>ATreasure..</span>
            </div>
            <ul>
                <a href="/" onclick="window.parent.location.hash='home';">Home</a>
                <a href="#" onclick="window.parent.location.hash='state-wise';">About team</a>
            </ul>
        </div>
        """
        
        
        
        

        # Function to manage section visibility
def show_section(section):
            st.session_state.current_section = section

        # Set initial section
if 'current_section' not in st.session_state:
            st.session_state.current_section = 'home'

        # Handle section change based on URL hash
query_params = st.experimental_get_query_params()
section = query_params.get("section", [st.session_state.current_section])[0]
state = query_params.get("state", [None])[0]
constituency = query_params.get("constituency", [None])[0]
st.session_state.current_section = section
st.markdown(nav_bar_html, unsafe_allow_html=True)

        # Display the content based on the current section
with st.container():
            if st.session_state.current_section == 'home':
                st.title("Parliamentary Constituency General.")
                
                # Party-wise plots on home page
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.header("General Election to Parliamentary Constituencies: Trends & Results June-2024")
                    party_data = data.groupby('Party Short Names')['Obtained Votes'].sum().reset_index()
                with col2:
                    state_options = ['Select State'] + data['State Name'].unique().tolist()
                    selected_state = st.selectbox("", state_options, index=0)
                    
                    if selected_state != 'Select State':
                        st.experimental_set_query_params(section='state-wise', state=selected_state)
                        st.experimental_rerun()
                        
                # Calculate total won seats for top 5 parties
                total_won_seats = data[data['Status'] == 'won'].groupby('Party Short Names')['Candidate Name'].count().sort_values(ascending=False)
                top5_won_seats = total_won_seats.head(10)
                # Calculate total won seats for 'Others'
                others_won_seats = total_won_seats.iloc[10:].sum()
                # Combine top 5 parties and 'Others'
                top5_won_seats['Others'] = others_won_seats
                # Create data for the chart
                data_chart = list(top5_won_seats.values)
                data_chart.append(sum(data_chart))  # Adding the sum to create a half-donut effect
                # Create labels for the chart
                labels = list(top5_won_seats.index)
                labels.append("")  # Adding an empty label for the blank space
                # Create custom colors
                colors = ['#ff944d', '#66B2FF', '#99FF99','#204795', '#FFCC99','#aebedf', '#19ddad','#19afed','#19efed','#19aaed', '#b3b3b3']
                colors.append('white')  # Adding a white color for the blank space
                # Create the semi-donut chart using Plotly
                fig = go.Figure(data=[
                    go.Pie(
                        labels=labels,
                        values=data_chart,
                        hole=0.5,
                        rotation=-90,
                        direction='clockwise',
                        marker=dict(colors=colors),
                        sort=False,
                        textinfo='none',
                        hovertemplate='<b>%{label}</b><br>Seats Won: %{value}<extra></extra>',
                        
                    )
                ])

                # Adjust layout for a semi-donut effect
                fig.update_layout(
                    # title='Top 5 Party Wise Election Won Seats',
                    annotations=[
                        dict(
                            text='543/543', 
                            x=0.5, y=.6, 
                            font_size=35,
                            showarrow=False
                        )
                    ],
                    width=600,
                    height=900,
                    legend=dict(orientation="h",x=.24, y=.45)
                )
                # fig.update_layout()

                # Display the half-donut chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                col11, col12 = st.columns(2)
                st.markdown("""
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
                        <style>
                            [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(3),
                            [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(4)>div>div>div>div{
                                box-shadow: 0 0 6px #565656a2;
                                border-radius: 9px;
                                overflow: hidden;
                            }
                            .st-emotion-cache-asc41u h3{
                                margin: 0%;
                                background-color: #cdadf5c3;
                                padding-left: 19px;
                            }
                            [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(2) {
                                background: #d7caff;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                with col11:
                    
                    st.subheader('Party Wise Vote Share')
                    # Create a Pie Chart using Plotly
                    party_summary = data.groupby('Party Short Names').apply(lambda x: pd.Series({
                        'Won': (x['Status'] == 'won').sum(),
                        'Leading': (x['Status'] == 'leading').sum()
                    })).reset_index()

                    party_summary['Total'] = party_summary['Won']
                    party_summary.columns = ['Name', 'Won', 'Leading', 'Total']
                    party_summary = party_summary[party_summary['Won'] > 0]
                    party_summary = party_summary.sort_values(by='Total', ascending=False)
                    party_summary.reset_index(drop=True, inplace=True)

                    my_fig = px.pie(party_summary, names='Name', values='Total')
                    my_fig.update_traces(
                        textinfo='none'
                        )
                    my_fig.update_layout(
                        legend=dict(
                            orientation="h"
                        ),
                        width=600,
                        height=600,
                    )
                    st.plotly_chart(my_fig, use_container_width=True)

                with col12:
                    st.subheader('Party Wise Results Status')
                    # Aggregate the data to get the count and leading statuses for each party
                    Party = data['Party Name'] + ' - ' + data['Party Short Names']
                    party_summary = data.groupby(Party).apply(lambda x: pd.Series({
                        'Won': (x['Status'] == 'won').sum(),
                        'Leading': (x['Status'] == 'leading').sum(),
                    })).reset_index()

                    # Calculate the total
                    party_summary['Total'] = party_summary['Won']
                    party_summary.columns = ['Party', 'Won', 'Leading', 'Total']
                    party_summary = party_summary[party_summary['Won'] > 0]
                    party_summary = party_summary.sort_values(by='Total', ascending=False)
                    party_summary.reset_index(drop=True, inplace=True)
                    
                    
                    totals = party_summary[['Won', 'Leading', 'Total']].sum().to_frame().T
                    totals['Party'] = 'Total'
                    party_summary = pd.concat([party_summary, totals], ignore_index=True)
                    st.table(party_summary)

            elif st.session_state.current_section == 'state-wise':
               st.markdown('''
                    <style>
                        [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(2){
                        text-align: center;
                        
                    }
                    .title{
                        color:#0a76ba;
                        text-align: center;
                        font-size: 32px;
                        margin-bottom: 20px;
                    }
                    </style>
                ''', unsafe_allow_html=True)

               st.subheader("General Election to Parliamentary Constituencies: Trends & Results June-2024")
               if state:
                   state_data = data[data['State Name'] == state]

                   # Check if 'party_color' is in state_data, otherwise merge it from data
                   if 'party_color' not in state_data.columns:
                       state_data = state_data.merge(data[['Party Short Names', 'party_color']].drop_duplicates(), on='Party Short Names', how='left')

                   

                   # Display the number of won seats for each party in boxes
                   party_won_data = state_data[state_data['Status'] == 'won'].groupby(['Party Short Names', 'party_color']).size().reset_index(name='Seats Won')
                   party_won_data = party_won_data[party_won_data['Seats Won'] > 0]  # Filter out parties with 0 won seats
                   party_won_data = party_won_data.sort_values(by='Seats Won', ascending=False).reset_index(drop=True)
                   total_seats = party_won_data['Seats Won'].sum()
                   state_c = f"""
                             <div class="title">
                                <span>{state}</span>
                                <strong>(Total PC - {total_seats})</strong>
                             </div>
                        """
                   # Display overall state-level statistics
                #    st.write(f"Total Seats in {state}: {total_seats}")
                   st.markdown(state_c, unsafe_allow_html=True)

                   # Create boxes for each party
                   colss = st.columns(5)
                   for index, row in party_won_data.iterrows():
                       cls = colss[index % 5]
                       st.markdown('''
                           <style>
                               [data-testid="stHorizontalBlock"]{
                                   width: 100%;
                                   margin: auto;
                                   display: flex;
                                   justify-content: center;
                                   
                               }
                               .box{
                                   width: 270px;
                                   height: 200px;
                                   border: #004274 solid 1px;
                                   overflow: hidden;
                                   border-radius: 9px;
                                   margin: auto auto 30px auto;
                               }
                               .box .in_box{
                                   width:100%;
                                   height: 100%;
                                   display: flex;
                                   align-items: center;
                                   justify-content: center;
                                   flex-direction: column;
                               }
                               .pname{
                                   font-size: 28px;
                                   font-weight: 600;
                               }
                               .pseats{
                                   font-size: 50px;
                                   font-weight: bold;

                               }
            
                           </style>
                       ''', unsafe_allow_html=True)
                       cls.markdown(f"""
                           <div class='box' style='background-color: {row['party_color']}'>
                               <div class='in_box'>
                                   <div class='pname'>
                                       {row['Party Short Names']}
                                   </div>
                                   <div class='pseats'>
                                       {row['Seats Won']}
                                   </div>
                               </div>
                           </div>
                       """, unsafe_allow_html=True)
                       
                   col21, col22 = st.columns(2)


                   with col21:
                        # Display the data table
                        st.subheader("Party-wise Results")
                        party_summary = state_data.groupby('Party Short Names').apply(lambda x: pd.Series({
                            'Won': (x['Status'] == 'won').sum(),
                            'Leading': (x['Status'] == 'leading').sum()
                        })).reset_index()
                        party_summary['Total'] = party_summary['Won'] + party_summary['Leading']
                        party_summary = party_summary.sort_values(by='Total', ascending=False)
                        party_summary.columns = ['Party', 'Won', 'Leading', 'Total']
                        party_summary = party_summary[party_summary['Won'] > 0]  # Filter out parties with 0 won seats
                        totals = party_summary[['Won', 'Leading', 'Total']].sum().to_frame().T
                        totals['Party'] = 'Total'
                        party_summary = pd.concat([party_summary, totals], ignore_index=True)
                        st.table(party_summary)

                   with col22:
                        col22a, col22b = st.columns(2)
                        with col22a:
                            st.subheader('Constituency Wise Results')
                        with col22b:
                            constituency_options = ['Select Constituency'] + state_data['Constitution Assembly'].unique().tolist()
                            selected_constituency = st.selectbox("", constituency_options, index=0)
                            if selected_constituency != 'Select Constituency':
                                st.experimental_set_query_params(section='candidateswise', state=state, constituency=selected_constituency)
                                st.experimental_rerun()

            elif st.session_state.current_section == 'constituency':
                st.title("Constituency-wise Election Results")
                
                state_options = data['State Name'].unique()
                selected_state = st.selectbox("Select State", state_options, index=0)
                
                if selected_state:
                    constituency_options = data[data['State Name'] == selected_state]['Constitution Assembly'].unique()
                    selected_constituency = st.selectbox("Select Constituency", constituency_options, index=0)
                    
                    if selected_constituency:
                         if selected_state != 'Select State':
                            st.experimental_set_query_params(section='state-wise', state=selected_state)
                            st.experimental_rerun()
            
            elif st.session_state.current_section == 'candidateswise':
                st.markdown('''
                    <style>
                        [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(2){
                        text-align: center;
                        font-weight: bold;
                        font-size: 30px;
                        margin-bottom: 22px;
                    }
                    .title{
                        color:#0a76ba;
                        text-align: center;
                        font-size: 32px;
                        margin-bottom: 20px;
                    }
                    </style>
                ''', unsafe_allow_html=True)

                st.subheader("General Election to Parliamentary Constituencies: Trends & Results June-2024")
                
                if state and constituency:
                    state_c = f"""
                             <div class="title">
                                <span style="color: #000;">Parliamentary Constituency</span>
                                <span>{constituency}</span>
                                <strong>({state})</strong>
                             </div>
                        """
                        
                    st.markdown(state_c, unsafe_allow_html=True)

                    # st.subheader(f"Parliamentary Constituency: {constituency} ()")
                    filtered_data = data[(data['Constitution Assembly'] == constituency) & (data['State Name'] == state)]
                    
                    if 'Status' in filtered_data.columns:
                        # Ensure 'Difference Votes' is numeric
                        # filtered_data['Difference Votes'] = pd.to_numeric(filtered_data['Difference Votes'], errors='coerce').fillna(0).astype(int)
                        
                        # Sort candidates by status: 'won' first
                        filtered_data = filtered_data.sort_values(by='Status', ascending=False)
                        
                        # External CSS for styling
                        st.markdown("""
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
                        <style>
                            [class="block-container st-emotion-cache-1jicfl2 ea3mdgi5"]>div>div>div>div:nth-child(4)>div>div>div:nth-child(2){
                                text-align: center;
                            }
                            .st-emotion-cache-asc41u>h3{
                                text-align: center;
                            }
                            .st-emotion-cache-asc41u>h6,
                            .st-emotion-cache-asc41u>h5{
                                padding-bottom: 4px;
                            }
                            .cand-box figure {
                                width: 100px;
                                height: 100px;
                                border-radius: 50%;
                                display: block;
                                overflow: hidden;
                                border: 5px solid rgb(255, 255, 255);
                                text-align: center;
                                position: absolute;
                                top: 0px;
                                bottom: 0px;
                                margin: auto;
                                left: -2.5rem;
                                z-index: 2;
                                box-shadow: rgb(225, 225, 225) 1px 1px 1px;
                            }
                            .cand-box::after {
                                position: absolute;
                                content: '';
                                width: 100px;
                                height: 100px;
                                background-color: #786fbc;
                                border-radius: 50%;
                                z-index: 1;
                                left: -2.85rem;
                                top: 0;
                                bottom: 0;
                                margin: auto;
                                display: block;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Display candidate cards in columns
                        cols = st.columns(3)
                        for idx, (index, candidate) in enumerate(filtered_data.iterrows()):
                            col = cols[idx % 3]
                            text_color = 'green' if str(candidate['Status']).lower() == 'won' else 'red'
                            
                            col.markdown(f"""
                            <div class="cand-box">
                                <div class="cand-info">
                                    <div class="status" style="color: {text_color};">
                                        <div style="text-transform: capitalize; font-weight: bold;">{candidate['Status']}</div>
                                        <div>{candidate['Obtained Votes']} <span>{candidate['Difference Votes']}</span></div>
                                    </div>
                                    <figure><img src="{candidate['Img urls']}" style="width: 100px; height: 100px; border-radius: 50%;"></figure>
                                    <div class="nme-prty">
                                        <h5 style="color: #004274;">{candidate['Candidate Name']}</h5>
                                        <h6 style="color: #0a8bfd;">{candidate['Party Name']}</h6>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            
# Define the footer variable



footer = """
    <style>
        .footer {
            margin: 0;
    padding: 0;
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color:  #0a1143;
            color: black;
            text-align: center;
            padding: 10px;
            color: #f2f2f2;
        }
    </style>
    <div class="footer">
        <p>© 2024 ATreasure... All rights reserved.</p>
    </div>
"""

# Use the footer variable in st.markdown
st.markdown(footer, unsafe_allow_html=True)

                



