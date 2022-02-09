""" This example reranks a resultset via the ARAX API.
"""

# Import minimal requirements
import requests
import json
import re

# Set the base URL for the ARAX reasonaer TRAPI 1.1 base
endpoint_url = 'https://arax.ncats.io/api/arax/v1.2'
input_results_url = 'https://raw.githubusercontent.com/TranslatorSRI/RankingComparison/main/inputs/treats_hyperlipidemia/result.json'

# Get an existing resultset to work on
response_content = requests.get(input_results_url, headers={'accept': 'application/json'})
status_code = response_content.status_code
if status_code != 200:
    print("ERROR returned with status "+str(status_code))
    print(response_content)
    exit()

# Unpack the response content into a dict
response_dict = response_content.json()
print(f"Retrieved a message with {len(response_dict['message']['results'])} results from {input_results_url}")

# Create a new request, including previous response message and a simple reranking workflow
print("Create a new request with the previous message and a workflow to rerank (overlay_connect_knodes,score)")
request = {
    "message": response_dict['message'],
    "workflow": [
        {
        "id": "overlay_connect_knodes"
        },
        {
        "id": "score"
        },
  ]
 }

# Send the request to ARAX and check the status
response_content = requests.post(endpoint_url + '/query', json=request, headers={'accept': 'application/json'})
status_code = response_content.status_code
if status_code != 200:
    print("ERROR returned with status "+str(status_code))
    print(response_content)
    exit()

# Unpack the JSON response content into a dict
response_dict = response_content.json()

# Display a summary of the results
print(f"Retrieved {len(response_dict['message']['results'])} results.")

# These URLs provide direct access to resulting data and GUI
print(f"Data: {response_dict['id']}")
response_id = 'unknown'
if response_dict['id'] is not None:
    match = re.search(r'(\d+)$', response_dict['id'])
    if match:
        response_id = match.group(1)
        print(f"GUI: https://arax.ncats.io/beta/?r={match.group(1)}")

filename = f"{response_id}.json"
print(f"Write results to {filename}")
with open(filename,'w') as outfile:
    outfile.write(json.dumps(response_dict, indent=2, sort_keys=True))




