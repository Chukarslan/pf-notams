from promptflow import tool
import pandas as pd
from geopy.distance import great_circle

@tool
def my_python_tool(input_airports: str) -> str:
    """
    Provided a string of airport codes as a list (eg. "YBBN YSSY"), return a list of airport codes that lie on the path between the two airports
    according to the Greater Circle Distance formula. 
     - The list should include the start and end airports. 
     - The list should be in order of the path.
    """
    offset_distance = 50  # nautical miles  
    airports_df = pd.read_csv(r"C:\Users\arsla\Desktop\MY LIFE\pf-notams\raw\airport_locations.csv")

    def calculate_distance(point1, point2):
        return great_circle(point1, point2).nautical

    def airports_in_zone(line_start, line_end, offset, airports):
        line_distance = great_circle(line_start, line_end).nautical
        line_direction = (line_end[0] - line_start[0], line_end[1] - line_start[1])
        unit_vector = (line_direction[1], -line_direction[0])
        unit_vector = (unit_vector[0] / line_distance, unit_vector[1] / line_distance)
        offset_vector = (unit_vector[0] * offset, unit_vector[1] * offset)
        min_lat = min(line_start[0], line_end[0]) + offset_vector[0]
        max_lat = max(line_start[0], line_end[0]) + offset_vector[0]
        min_lon = min(line_start[1], line_end[1]) + offset_vector[1]
        max_lon = max(line_start[1], line_end[1]) + offset_vector[1]

        filtered_airports = airports[
            (airports['Latitude'] >= min_lat) & (airports['Latitude'] <= max_lat) &
            (airports['Longitude'] >= min_lon) & (airports['Longitude'] <= max_lon)
        ]

        return filtered_airports
    airports_input = input_airports.replace('\n', '').strip()
    airports = input_airports.split()
    departure_airport, arrival_airport = airports[0], airports[-1]

    departure_data = airports_df[airports_df['ICAO'] == departure_airport][['Latitude', 'Longitude']]
    arrival_data = airports_df[airports_df['ICAO'] == arrival_airport][['Latitude', 'Longitude']]

    if departure_data.empty or arrival_data.empty:
        return "Error: One or more airports not found in the CSV file."

    departure_coords = tuple(departure_data.values[0])
    arrival_coords = tuple(arrival_data.values[0])

    airports_in_zone_df = airports_in_zone(departure_coords, arrival_coords, offset_distance, airports_df)

    airport_list = [departure_airport] + list(airports_in_zone_df['ICAO']) + [arrival_airport]

    # Remove duplicates
    unique_airports = []
    for airport in airport_list:
        if airport not in unique_airports:
            unique_airports.append(airport)

    return " ".join(unique_airports)