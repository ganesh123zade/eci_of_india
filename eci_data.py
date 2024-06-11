from lxml import html
import requests
import csv
import os

# Define the base URL for the election results
base_url = 'https://results.eci.gov.in/PcResultGenJune2024/'

# Get the initial page content to extract state options
start_url = f'{base_url}index.htm'
response = requests.get(start_url)
html_content = response.content
tree = html.fromstring(html_content)

# Extract state names and values
state_names = tree.xpath('//select[@id="ctl00_ContentPlaceHolder1_Result1_ddlState"]/option[position() > 1]/text()')
state_options = tree.xpath('//select[@id="ctl00_ContentPlaceHolder1_Result1_ddlState"]/option[position() > 1]/@value')

# Prepare the CSV file
output_csv = 'output.csv'
file_exists = os.path.exists(output_csv)

with open(output_csv, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write headers if the file is being created
    if not file_exists:
        csvwriter.writerow(['State Name', 'Constitution Assembly', 'Candidate Name', 'Party Name', 'Status', 
                            'Obtained Votes', 'Difference Votes'])

    # Iterate over each state
    for i, state_value in enumerate(state_options):
        state_name = state_names[i]
        
        # Construct URL for the state's results page
        state_url = f'{base_url}partywiseresult-{state_value}.htm'
        response = requests.get(state_url)
        html_content = response.content
        tree1 = html.fromstring(html_content)
        
        # Extract constituency count
        constituency_count = tree1.xpath("//table[@class='table']/tfoot/tr/th[4]/text()")
        constituency_count = int(constituency_count[0]) if constituency_count else 0

        # Extract constituency options
        constituency_names = tree1.xpath('//select[@id="ctl00_ContentPlaceHolder1_Result1_ddlState"]/option[position() > 1]/text()')
        constituency_options = tree1.xpath('//select[@class="custom-select"]/option[position() > 1]/@value')
        
        # Iterate over each constituency in the state
        for j,constituency_value in enumerate(constituency_options):
            if j < len(constituency_options):
                constituency_name = constituency_names[j] if constituency_names else "Unknown"
                
                # Construct URL for the constituency's results page
                cont_url = f'{base_url}candidateswise-{constituency_value}.htm'
                response = requests.get(cont_url)
                html_content = response.content
                tree2 = html.fromstring(html_content)

                # Extract data
                candidate_name = tree2.xpath("//div[@class='nme-prty']/h5/text()")
                party_name = tree2.xpath("//div[@class='nme-prty']/h6/text()")
                status = tree2.xpath("//div[@style='text-transform: capitalize']/text()")
                obtained_votes = tree2.xpath("//div[@class='cand-info']/div[1]/div[2]/text()")
                diff_votes = tree2.xpath("//div[@class='cand-info']/div/div[2]/span/text()")

                # Ensure all lists have the same length by filling missing values
                max_length = max(len(candidate_name), len(party_name), len(status), len(obtained_votes), len(diff_votes))
                candidate_name += [''] * (max_length - len(candidate_name))
                party_name += [''] * (max_length - len(party_name))
                status += [''] * (max_length - len(status))
                obtained_votes += [''] * (max_length - len(obtained_votes))
                diff_votes += [''] * (max_length - len(diff_votes))

                # Write data to the CSV file
                for c_name, p_name, stat, o_vote, d_votes in zip(candidate_name, party_name, status, obtained_votes, diff_votes):
                    csvwriter.writerow([state_name, constituency_name, c_name, p_name, stat, o_vote, d_votes])

print("Data has been written to the CSV file.")


