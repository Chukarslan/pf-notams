
from promptflow import tool
import asyncio
import json
import certifi
import requests
from serpapi import GoogleSearch


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input: str) -> str:
    
    results = asyncio.run(process_json_string(input))

    return results


async def process_json_string(json_string):
    try:
        # Parse the JSON string
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON string"}

    # Check if departure_id, arrival_id, and outbound_date are empty
    if not data.get("departure_id") or not data.get("arrival_id") or not data.get("outbound_date"):
        return {"error": "Departure_id, Arrival_id, and Outbound_date cannot be empty"}

    # Split the input data into two parts
    flights_data = {key: data[key] for key in data if key not in {"q", "check_in_date", "check_out_date"}}
    hotels_data = {key: data[key] for key in {"q", "check_in_date", "check_out_date"} if key in data}

    # Create asynchronous tasks for API calls
    tasks = [
        make_api_call_flights(flights_data),
        make_api_call_hotels(hotels_data) if hotels_data else None
    ]

    # Run tasks in parallel and wait for both results
    results = await asyncio.gather(*[task for task in tasks if task])

    return results   

async def make_api_call_flights(data):
    params={
        "engine":"google_flighs",
        "hl":"en",
        "gl":"us",
        "departure_id":data['departure_id'],
        "arrival_id":data['arrival_id'],
        "currency":"GBP",
        "api_key":
    }

async def make_api_call_hotels(data):
    # Placeholder for making an asynchronous API call
    # You need to replace this with your actual API call implementation
    # For demonstration purposes, it just returns a dummy response
    print(f"Making API call to {endpoint} with data: {data}")
    await asyncio.sleep(2)  # Simulating API call delay
    return f"Response from {endpoint}"


