import os
import django
import pandas as pd
from booking.models import Category, Hotel  # Adjust with your app name

# Set the settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')

# Initialize Django
django.setup()

# Read CSV file into a DataFrame
csv_file_path = './Database.csv'

# Check if the file exists
if os.path.exists(csv_file_path):
    print("File exists!")
else:
    print("File not found.")

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame and create model instances
for index, row in df.iterrows():
    # Create or get the Category instance
    category_name = row['Category']  
    category, created = Category.objects.get_or_create(
        name=category_name,
        defaults={'slug': category_name.lower().replace(' ', '-')}
    )

    # Create the Hotel instance
    hotel = Hotel(
        title=row['Hotel'],  # Assuming 'Hotel' is a column in your CSV
        category=category,
        address=row.get('Address', ''),  # Assuming 'Address' is in the CSV
        contact=row.get('Contact', ''),  # Assuming 'Contact' is in the CSV
        price=row['Price'].replace('Rp ', '').replace('.', ''),  # Clean the 'Price' column if necessary
        rating=row.get('Rating', 0.00),  # Assuming 'Rating' is a column, default to 0.00 if missing
        amenities=row.get('Amenities', ''),  # Assuming 'Amenities' is in the CSV
        location=row.get('Location', ''),  # Assuming 'Location' is in the CSV
        image_url=row['Image_URL'],  # Assuming 'Image_URL' is a column in your CSV
        page_url=row['Page_URL'],  # Adding page_url from CSV
        slug=row['Hotel'].lower().replace(' ', '-'),  # Create slug based on the hotel name
        is_active=True  # Assuming active status for all hotels
    )
    
    # Save the Hotel instance to the database
    hotel.save()

print("CSV data has been loaded into the Django database.")
