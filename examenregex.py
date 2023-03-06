import requests
import yaml
import re
from datetime import datetime

url = "https://api.domainsdb.info/v1/domains/search?domain=syntra.be"

response = requests.get(url)

if response.status_code == 200:    
    data = response.json()    
    domains = []
    for domain in data['domains']:

        ip = domain.get('A', [''])[0]

        land = domain.get('country', '')

        provider = re.search(r'\.(\w+)\.\w+$', domain.get('NS', [''])[0]).group(1)

        create_date_str = domain.get('create_date', '')
        
        create_date_match = re.search(r'^(\d{4})-(\d{2})-(\d{2})', create_date_str)
        
        create_datum = datetime.strptime(create_date_match.group(), '%Y-%m-%d')
        
        create_date_formatted = {
            'Dag': create_datum.strftime('%d'),
            'Maand': create_datum.strftime('%m'),
            'Jaar': create_datum.strftime('%Y')
        }
        
        domains.append({'ip': ip, 'land': land, 'created': create_date_formatted, 'provider': provider})

    yaml_data = yaml.dump({'INFO': domains})

    with open('examen.yaml', 'w') as file:
        file.write(yaml_data)

    print("YAML Output OK naar examen.yaml")
