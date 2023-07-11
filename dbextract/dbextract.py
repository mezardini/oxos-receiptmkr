import json
from django.core import serializers
from frontend.models import Seller

def export_data_to_json():
    queryset = Seller.objects.all()  # Retrieve all objects from the model
    serialized_data = serializers.serialize('json', queryset)  # Serialize queryset to JSON
    data = json.loads(serialized_data)  # Load serialized data into Python objects

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Call the function to export data to JSON
export_data_to_json()

# import json
# import sqlite3

# def extract_data_to_json(database_file, output_file):
#     # Connect to the SQLite database
#     conn = sqlite3.connect(database_file)
#     cursor = conn.cursor()

#     # Execute a query to fetch the data from a table
#     cursor.execute("SELECT * FROM your_table")
#     rows = cursor.fetchall()

#     # Prepare a list to hold the extracted data
#     data = []

#     # Iterate over the rows and extract the data
#     for row in rows:
#         # Convert the row to a dictionary or any other desired format
#         record = {
#             'column1': row[0],
#             'column2': row[1],
#             # Add more columns as needed
#         }
#         data.append(record)

#     # Close the database connection
#     conn.close()

#     # Write the data to a JSON file
#     with open(output_file, 'w') as file:
#         json.dump(data, file)

# # Usage example
# database_file = 'C:\Users\USER\Desktop\receiptmkr\receiptmkr\db.sqlite3'
# output_file = 'path/to/output.json'
# extract_data_to_json(database_file, output_file)
