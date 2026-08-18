# =============================================================================
# tools.py — All LangChain tools for the chatbot
# =============================================================================

from langchain_core.tools import tool
from datetime import datetime
import requests
import pytz
import re
from simpleeval import simple_eval, InvalidExpression
from duckduckgo_search import DDGS


# =============================================================================
# TOOL 1 — CALCULATOR
# =============================================================================

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    Use this tool whenever the user asks for arithmetic, calculations, or math.
    Supports: +, -, *, /, **, %, and parentheses.
    Input: a math expression string, e.g. "125 * 48" or "(10 + 5) / 3"
    Returns: the numeric result as a string.
    """
    try:
        result = simple_eval(expression)
        return str(result)
    except InvalidExpression:
        return "Unable to calculate: invalid expression."
    except ZeroDivisionError:
        return "Unable to calculate: division by zero."
    except Exception as e:
        return f"Unable to calculate: {e}"


# =============================================================================
# TOOL 2 — DATE / TIME
# =============================================================================

@tool
def get_current_datetime(timezone: str = "UTC") -> str:
    """
    Get the current date and time for any timezone.
    Use this tool when the user asks what time or date it is, or asks about
    the current time in a specific city or country.
    Input: a timezone string such as "UTC", "Asia/Karachi", "America/New_York",
           "Europe/London". If no timezone is given, default to "UTC".
    Returns: the current date, time, and timezone as a formatted string.
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return now.strftime(f"Date: %A, %B %d, %Y | Time: %I:%M %p | Timezone: {timezone}")
    except pytz.UnknownTimeZoneError:
        # Fallback: return UTC with a note
        now = datetime.utcnow()
        return (
            f"Unknown timezone '{timezone}'. Returning UTC instead.\n"
            + now.strftime("Date: %A, %B %d, %Y | Time: %I:%M %p UTC")
        )
    except Exception as e:
        return f"Could not retrieve date/time: {e}"


# =============================================================================
# TOOL 3 — WEATHER  (wttr.in — no API key required)
# =============================================================================

@tool
def get_weather(location: str) -> str:
    """
    Get the current weather for any location in the world.
    Use this tool when the user asks about the weather, temperature, or
    climate conditions for any city, region, or country.
    Input: a location name string, e.g. "Lahore", "London", "New York".
    Returns: current temperature, weather condition, humidity, and wind speed.
    """
    try:
        url = f"https://wttr.in/{requests.utils.quote(location)}?format=j1"
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        area    = data["nearest_area"][0]

        city    = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        temp_c  = current["temp_C"]
        temp_f  = current["temp_F"]
        desc    = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_kmph = current["windspeedKmph"]
        feels_c = current["FeelsLikeC"]

        return (
            f"Location:    {city}, {country}\n"
            f"Temperature: {temp_c}°C / {temp_f}°F (Feels like {feels_c}°C)\n"
            f"Condition:   {desc}\n"
            f"Humidity:    {humidity}%\n"
            f"Wind Speed:  {wind_kmph} km/h"
        )
    except requests.exceptions.Timeout:
        return f"Weather service timed out for '{location}'. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"Could not fetch weather for '{location}': {e}"
    except (KeyError, IndexError, ValueError):
        return f"Could not parse weather data for '{location}'. Try a more specific location name."
    except Exception as e:
        return f"Weather tool error: {e}"


# =============================================================================
# TOOL 4 — WEB SEARCH  (DuckDuckGo — no API key required)
# =============================================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using DuckDuckGo.
    Use this tool when the user asks about recent events, news, facts you may
    not know, or anything that requires up-to-date information from the internet.
    Input: a search query string, e.g. "latest AI news August 2025".
    Returns: top search results with title, URL, and a short snippet.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=4):
                results.append(
                    f"Title:   {r.get('title', 'N/A')}\n"
                    f"URL:     {r.get('href', 'N/A')}\n"
                    f"Snippet: {r.get('body', 'N/A')}"
                )

        if not results:
            return f"No results found for: {query}"

        return "\n\n---\n\n".join(results)
    except Exception as e:
        return f"Web search failed: {e}"


# =============================================================================
# Exported tool list — imported by backend.py
# =============================================================================

tools = [calculator, get_current_datetime, get_weather, web_search]
