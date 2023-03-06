# import the requests library to make HTTP requests
import requests  
# import the pyyaml library to convert Python objects to YAML format
import yaml  
# import the re library for working with regular expressions
import re  
# import the datetime module to work with dates and times
from datetime import datetime

# define the URL to retrieve domain information from the DomainsDB API
url = "https://api.domainsdb.info/v1/domains/search?domain=syntra.be"

# make a GET request to the URL and store the response object in the 'response' variable
response = requests.get(url)

# check if the response status code is 200 (OK)
if response.status_code == 200:
    # parse the response data as a JSON object and store it in the 'data' variable
    data = response.json()

    # create an empty list to store the domain information
    domains = []

    # loop through each domain in the 'domains' list in the JSON data
    for domain in data['domains']:

        # retrieve the IP address of the domain from the 'A' record, or an empty string if it doesn't exist
        ip = domain.get('A', [''])[0]

        # retrieve the country of the domain from the 'country' field, or an empty string if it doesn't exist
        land = domain.get('country', '')

        # retrieve the provider of the domain from the 'NS' record using a regular expression to extract the subdomain
        provider = re.search(r'\.(\w+)\.\w+$', domain.get('NS', [''])[0]).group(1)

        # retrieve the creation date of the domain as a string
        create_date_str = domain.get('create_date', '')

        # use a regular expression to extract the date components (year, month, day) from the creation date string
        create_date_match = re.search(r'^(\d{4})-(\d{2})-(\d{2})', create_date_str)

        # convert the date components to a datetime object
        create_datum = datetime.strptime(create_date_match.group(), '%Y-%m-%d')

        # format the datetime object as a dictionary with day, month, and year keys
        create_date_formatted = {
            'Dag': create_datum.strftime('%d'),
            'Maand': create_datum.strftime('%m'),
            'Jaar': create_datum.strftime('%Y')
        }

        # add the domain information (IP address, country, provider, and creation date) to the 'domains' list
        domains.append({'ip': ip, 'land': land, 'created': create_date_formatted, 'provider': provider})

    # convert the 'domains' list to a YAML formatted string and store it in the 'yaml_data' variable
    yaml_data = yaml.dump({'INFO': domains})

    # write the YAML formatted string to a file named 'examen.yaml'
    with open('examen.yaml', 'w') as file:
        file.write(yaml_data)

    # print a message indicating that the YAML output was successful
    print("YAML Output OK naar examen.yaml")
