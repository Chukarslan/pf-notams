import csv

# Open the text file and read the lines
with open('raw\GlobalAirportDatabase.txt', 'r') as f:
    lines = f.readlines()

# Prepare the data for the CSV
data = []
for line in lines:
    parts = line.split(':')
    icao = parts[0]
    lat = float(parts[14])
    lon = float(parts[15])
    if icao != 'N/A' and lat is not None and lon is not None and lat != 0.0 and lon != 0.0:
        data.append([icao, lat, lon])

# Write the data to a CSV file
with open('raw\airport_locations.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ICAO', 'Latitude', 'Longitude'])  # Write the header
    writer.writerows(data)  # Write the data