import datetime
import requests
import os
from google.adk.agents.llm_agent import Agent

def get_current_time(area : str , location : str) -> str:
  
    url = "https://world-time-api3.p.rapidapi.com/timezone/Africa/Abidjan.txt"
    headers = {
        "x-rapidapi-key": "819f030735msh1661266c40a2db0p1284efjsnee628e5fe708",
        "x-rapidapi-host": "world-time-api3.p.rapidapi.com",
    }
    try: 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Unable to fetch time data. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)