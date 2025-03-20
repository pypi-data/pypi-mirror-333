import boto3
from decimal import Decimal
import json

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  
TABLE_NAME = "WeatherData"

def store_weather_in_dynamodb(city, lat, lon, weather_data):
    """
    Stores weather data in DynamoDB.
    
    :param city: Name of the city
    :param lat: Latitude
    :param lon: Longitude
    :param weather_data: JSON response from OpenWeather API
    """
    table = dynamodb.Table(TABLE_NAME)
    
    lat_lon = f"{lat}_{lon}"  # Keep the original partition key
    timestamp = int(weather_data["dt"])  # Sort key
    
    item = {
        "lat_lon": lat_lon,
        "timestamp": timestamp,
        "city": city,  # Add city name dynamically
        "weather": json.loads(json.dumps(weather_data), parse_float=Decimal)
    }
    
    table.put_item(Item=item)
    print(f"Weather data stored for {city} ({lat}, {lon})")
    return item

def get_weather_data(lat, lon):
    """
    Retrieves weather data from DynamoDB.
    
    :param lat: Latitude
    :param lon: Longitude
    :return: Weather data if found, otherwise None
    """
    table = dynamodb.Table(TABLE_NAME)
    lat_lon = f"{lat}_{lon}"

    response = table.query(
        KeyConditionExpression="lat_lon = :lat_lon",
        ExpressionAttributeValues={":lat_lon": lat_lon},
        ScanIndexForward=False,  # Get the latest record first
        Limit=1
    )

    if "Items" in response and response["Items"]:
        return response["Items"][0]
    
    return None
