import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhishnaserver.settings")
import django
django.setup()
import requests
from django.core.files import File
from home.models import CA

# Define the path to your JSON file
json_file_path = 'users_ca.json'  # Replace with the actual file path

def add_ca_data_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for k in data["CA"]:
                item = data["CA"][k]

                ca = CA(
                    id=k,
                    name=item['name'],
                    email=item['email'],
                    phone=item['phone'],
                    referral=item.get('refferal', None),
                    year=item['year'],
                    college=item['college'],
                    old_verification=item['fileUrl']
                )
                ca.save()

                print(f'Successfully added CA with ID {ca.id}')
    except FileNotFoundError:
        print(f'File not found: {json_file_path}')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    add_ca_data_from_json(json_file_path)
