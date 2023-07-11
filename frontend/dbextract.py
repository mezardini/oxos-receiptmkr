import json
from django.core import serializers
from models import Seller
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receiptmkr.settings')

def export_data_to_json():
    queryset = Seller.objects.all()  # Retrieve all objects from the model
    serialized_data = serializers.serialize('json', queryset)  # Serialize queryset to JSON
    data = json.loads(serialized_data)  # Load serialized data into Python objects

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Call the function to export data to JSON

export_data_to_json()
