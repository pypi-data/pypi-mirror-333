import boto3

# AWS Configurations
REGION_NAME = "us-east-1"  # Change this to your region
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:528757804466:WeatherAlerts"  # Replace with your SNS Topic ARN

sns_client = boto3.client("sns", region_name=REGION_NAME)

def send_weather_alert(city, lat, lon, weather_data):
    """
    Sends an SNS alert for critical weather conditions.
    
    :param city: City name
    :param lat: Latitude
    :param lon: Longitude
    :param weather_data: JSON response containing weather conditions
    """
    # Extract necessary weather details
    temperature = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]
    weather_condition = weather_data["weather"][0]["main"]

    # Define alert conditions
    alert_message = None

    if temperature < -10 or temperature > 40:
        alert_message = f"⚠️ Extreme Temperature Alert: {temperature}°C in {city}!"
    elif wind_speed > 80:
        alert_message = f"🌪️ High Wind Speed Alert: {wind_speed} km/h in {city}!"
    elif weather_condition in ["Thunderstorm", "Tornado", "Hurricane"]:
        alert_message = f"⛈️ Severe Weather Alert: {weather_condition} in {city}!"

    if alert_message:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=alert_message,
            Subject=f"Weather Alert for {city}",
        )
        print(f" Alert Sent: {alert_message}")
        return response

    print(f"No severe weather detected in {city}. No alert sent.")
    return None


def subscribe_user_to_alerts(email):
    """
    Subscribes a user to receive SNS alerts via email.
    
    :param email: Email address of the user
    """
    response = sns_client.subscribe(
        TopicArn=SNS_TOPIC_ARN,
        Protocol="email",
        Endpoint=email
    )
    print(f"Subscription request sent to {email}. User must confirm subscription.")
    return response


def list_subscriptions():
    """
    Lists all subscriptions for the SNS topic.
    """
    response = sns_client.list_subscriptions_by_topic(TopicArn=SNS_TOPIC_ARN)
    return response["Subscriptions"]
