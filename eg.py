import csv

# Function to extract the city and area from the address string
def extract_area(address):
    # Split the address into lines and handle both lines
    lines = address.splitlines()
    
    # If the address is multiline, we assume the area might be in the second line,
    # and we split it by commas (City, State, Zip format, or City, State, Area format)
    if len(lines) >= 2:
        second_line = lines[1]  # The second line should be "City, State Zip" or "City, State, Area"
        parts = second_line.split(',')  # Split by commas
        
        if len(parts) >= 2:
            city = parts[0].strip()  # First part should be the city
            state_zip = parts[1].strip()  # Second part should be "State Zip" or "State Area"
            
            # If there are more than two parts, assume the last part is the area
            if len(parts) > 2:
                area = parts[2].strip()  # Extract area if available
            else:
                area = city  # Default area to city name if no explicit area is given
            
            return area  # Return the extracted area
    return None  # If no valid area is found, return None

# Read the CSV file and extract unique areas
def get_unique_areas(csv_file):
    areas = set()  # Using a set to store unique areas
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            address = row.get('Address', '')  # Assume 'Address' is the column name
            area = extract_area(address)  # Extract area using the new function
            if area:
                areas.add(area)
    return sorted(areas)  # Sort areas alphabetically

# Function to assign an 'Area' name to the row based on the address
def assign_area(row):
    address = row.get('Address', '')
    area = extract_area(address)  # Use the new extract_area function
    if area:
        row['Area'] = area
    else:
        row['Area'] = 'Unknown Area'  # Default to 'Unknown Area' if no area found

# Function to add an 'Area' column to the CSV file based on address
def add_area_column(csv_file, output_csv_file):
    # Open the input CSV file and create an output file with an additional column 'Area'
    with open(csv_file, mode='r') as infile, open(output_csv_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Area']  # Add 'Area' column to header
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write header to the new file
        writer.writeheader()

        # For each row, assign the 'Area' based on the address
        for row in reader:
            assign_area(row)  # Assign the area to the row
            writer.writerow(row)
    print(f"New CSV with 'Area' column saved as {output_csv_file}")

# Function to generate HTML dropdown for areas
def generate_html_dropdown(areas):
    dropdown_html = '<select name="area" id="area">\n'
    dropdown_html += '<option value="">Select Area</option>\n'
    for area in areas:
        dropdown_html += f'<option value="{area}">{area}</option>\n'
    dropdown_html += '</select>'
    return dropdown_html

# Main workflow
csv_file = 'USA_Housing.csv'  # Input CSV file
output_csv_file = 'USA_Housing_with_Area.csv'  # New CSV file with 'Area' column

# Step 1: Add the 'Area' column to the CSV file based on the address
add_area_column(csv_file, output_csv_file)

# Step 2: Extract unique areas from the updated CSV file
areas = get_unique_areas(output_csv_file)

# Step 3: Generate HTML dropdown for areas
html_dropdown = generate_html_dropdown(areas)

# Print or save the HTML dropdown (you can render this HTML in your Django template)
print(html_dropdown)

with open('a.txt','w') as f:
    f.write(html_dropdown)
