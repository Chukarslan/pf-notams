from promptflow import tool

@tool
def my_python_tool(input_airports: str, json_list: list) -> list:
    """
    Provided a string of airport codes as a list (eg. "YBBN YSSY"), filter the json list of documents to only include those that contain the airport codes.
    Example of json:

    input_airports = "YBBN YSSY"

    [
  {
    "content": {
      "id": "H8935/23",
      "SubArea": "Movement and landing area",
      "Condition": "Limitations",
      "Subject": "Runway",
      "Modifier": "Closed",
      "message": "RWY 07/25 CLOSED RWY AVBL FOR TAXIING AIRCRAFT",
      "location": "YSSY"
    }
  },
  {
    "content": {
      "id": "J4781/23",
      "SubArea": "Movement and landing area",
      "Condition": "Limitations",
      "Subject": "Taxiway(s)",
      "Modifier": "Closed",
      "message": "TWY L CLOSED DUE WIP TWY C12 CLOSED  TWY C13 CLOSED  TWY J CLOSED  EXC WITH 15MINS PN CTC TEL: (07) 3406 3072",
      "location": "YBBN"
    }
  },
  {
    "content": {
      "id": "H8932/23",
      "SubArea": "Movement and landing area",
      "Condition": "Limitations",
      "Subject": "Runway",
      "Modifier": "Closed",
      "message": "RWY 07/25 CLOSED DUE WIP REFER METHOD OF WORKING PLAN 21/003",
      "location": "YSSY"
    }
  }]
    """


    # Convert input_airports string to a set of airport codes
    airport_codes = set(input_airports.split())

    # Filter json_list based on the 'location' field and extract 'content' part
    filtered_content_list = [item.get('content', {}) for item in json_list if item.get('content', {}).get('location') in airport_codes]

    return filtered_content_list