import operator
import ast
import requests
from pydantic import BaseModel, Field
from langchain.tools import tool
from datetime import date, timedelta

class MathInput(BaseModel):
    """
    Define the input schema for the math tool
    Attribute: str (arithematic expression to eval)
    Functions: None 
    """

    expression: str = Field(
        description="Expression to Eval-: "
    )

class TextInput(BaseModel):
    """
    Define the Input schema for the text analyzer
    Args: str
    """

    text: str = Field(
        description= "Text to analyze. "
    )

class DateInput(BaseModel):
    """
    takes the date as the input (YYYY,MM,DD)
    args: date
    """

    days: int = Field( description= "Number of days to add to today's date-: ")

class WeatherInput(BaseModel):
    """
    takes the name of the city as the input
    args: str
    """

    city: str = Field(description="City name, such as chandigarh")
    
def safe_calculate(expression: str) -> int | float:
    """Evaluate a basic arithmetic expression safely.
    Args: str (Arithmetic expression containing supported operators)
    Returns: int | float: Calculated numeric result.
    """
    if not expression.strip():
        raise ValueError("Expression cannot be empty.")

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid arithmetic expression.") from exc


    def evaluate(node) -> int | float:
        """Evaluate an approved arithmetic syntax-tree node.
        Returns: int | float: The value of the evaluated node.
        Raises: ValueError: If the node contains an unsupported operation.
        """

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            if isinstance(node.op, ast.Pow) and abs(left) > 1e6:
                raise ValueError("Base is too large.")

            result = allowed_operators[type(node.op)](left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))

        raise ValueError("Only basic arithmetic is supported.")

    return evaluate(tree)


@tool(args_schema=MathInput)
def math_tool(expression: str) -> str:
    """Calculate a basic arithmetic expression.

    Args: str (Arithmetic expression to calculate)
    Returns: string (result or readable error message)
    """
    try:
        result = safe_calculate(expression)
        return f"Result: {result}"
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        return f"Math error: {exc}"

@tool(args_schema=TextInput)
def text_analyzer_tool(text: str) -> str:
    """Analyze text and report word count, character count, and sentiment.

    Args:
        text (str): Text provided by the user.

    Returns:
        str: Word count, character count, and sentiment.

    Raises:
        None: Expected input errors are returned as text.
    """
    if not text.strip():
        return "Text analysis error: text can't be empty"

    if len(text) > 1000:
        return "Text analysis error: text is too long"

    positive_words = {
        "good", "great", "excellent", "happy", "love",
        "wonderful", "amazing", "helpful", "best", "enjoy"
    }

    negative_words = {
        "bad", "terrible", "awful", "sad", "hate",
        "poor", "worst", "angry", "disappointing", "problem"
    }

    words = text.split()

    normalized_words = {
        word.strip(".,!?;:()[]{}\"'").lower()
        for word in words
    }

    positive_count = len(normalized_words & positive_words)
    negative_count = len(normalized_words & negative_words)

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (
        f"Word count: {len(words)}\n"
        f"Character count: {len(text)}\n"
        f"Sentiment: {sentiment}"
    )

@tool(args_schema=DateInput)
def date_tool(days: int) -> str:
    """
    define the input schema for the date tool
    args: days(int)
    """

    today = date.today()
    future_date = today + timedelta(days=days)
    return future_date.strftime("%Y-%m-%d")

@tool(args_schema= WeatherInput)
def weather_tool(city: str) -> str:
    """
    define the city name with temperature and clothing preferences
    args: str
    """
    try:
        if not city.strip():
            return "Weather error: Please provide a city name."

        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city.strip(),
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        locations = geo_data.get("results", [])

        if not locations:
            return f"Weather error: Could not find the city '{city}'."

        location = locations[0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,apparent_temperature,"
                    "relative_humidity_2m,precipitation,"
                    "weather_code,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        current = weather_data["current"]

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy with frost",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Heavy drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snowfall",
            73: "Moderate snowfall",
            75: "Heavy snowfall",
            80: "Rain showers",
            81: "Moderate rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail",
        }

        code = current.get("weather_code")
        condition = weather_codes.get(code, "Variable conditions")
        temperature = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        precipitation = current["precipitation"]
        wind_speed = current["wind_speed_10m"]

        # Step 4: Create a basic clothing suggestion.
        if temperature >= 30:
            clothing = "Wear lightweight, breathable clothing."
        elif temperature >= 20:
            clothing = "Light clothing should be comfortable."
        elif temperature >= 10:
            clothing = "Consider a light jacket or sweater."
        else:
            clothing = "Wear warm layers and a suitable jacket."

        if precipitation > 0 or code in {
            51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99
        }:
            clothing += " Carry an umbrella or raincoat."

        return (
            f"Weather for {city_name}, {country}:\n"
            f"Condition: {condition}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Precipitation: {precipitation} mm\n"
            f"Wind speed: {wind_speed} km/h\n"
            f"Clothing suggestion: {clothing}"
        )

    except requests.RequestException as exc:
        return f"Weather error: Could not reach the weather API ({exc})."
    except (KeyError, TypeError, ValueError) as exc:
        return f"Weather error: Unexpected API response ({exc})."