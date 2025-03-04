import numpy as np
from typing import List
import requests
import json

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer

web_search = DuckDuckGoSearchResults(output_format="list")

@tool(parse_docstring=True)
def get_arxiv_contents(url: str) -> str:
    """
    Retrieves the content of an arXiv research paper

    Args:
        url: The URL to an arXiv research paper, must be in format 'https://arxiv.org/html/2501.12948v1'

    Returns:
        Full contents of an arXiv research paper
    """
    if "html" in url:
        loader = AsyncHtmlLoader(url)
        md = MarkdownifyTransformer()

        html_content = loader.load()

        if (html_content):
            converted_content = md.transform_documents(html_content)

            return converted_content[0].page_content[:999999]
        else :
            return 'Content not available'
    else:
        return "The URL to an arXiv research paper, must be in format 'https://arxiv.org/html/2501.12948v1'"

@tool(parse_docstring=True)
def weather_service(cities: List[str]) -> str:
     """
     This is a weather service that provides all information related the current weather. The REST API is open and doesn't require additional licenses, it serves weather temperature information.
     
     Args:
        cities: The parameter cities is a list of city names e.g. [ LA, NY].
     
     Returns:
        A string that contains a sentence what the hottest city is.
     """
     
     base_weather_url="https://wttr.in/"
     cities_input = cities
     cities = []
     
     for city in cities_input:
          # Ensure to get the JSON format: '?format=j1'
          city_temp_url = base_weather_url + city + "?format=j1"
          response = requests.get(city_temp_url)
          if (response.status_code == 200):      
              # convert from byte to text
              byte_content = response.content
              text_content = byte_content.decode("utf-8")
              
              # load json
              content = json.loads(text_content)

              # extract temperature
              temperature = content['current_condition'][0]['temp_C']
              cities.append({"city": city, "temperature":temperature})
          else:
              cities.append({"city": f"{city} ERROR", "temperature":0})
     full_text = ""
     sorted_by_temperature =  sorted(cities, key=lambda x: (x['temperature'], x['city']), reverse=True)
     print(f"{sorted_by_temperature}")
     i = 0 
     for city in sorted_by_temperature:
        if (i == 0):
             response_text =  f"The hottest city is {city['city']} with a temperature of {city['temperature']} degrees Celsius."
        else:
             response_text =  f"In the city {city['city']} the temperature is {city['temperature']} degrees Celsius."
        i = i + 1
        full_text = full_text + ' ' + response_text

     return full_text
