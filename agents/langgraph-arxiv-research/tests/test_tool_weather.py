import pytest
from langgraph_react_agent.tools import weather_service

testdata = [
    { 
      'cities': ['Worms', 'Mannheim'], 
    },
    {
      'cities': ['NY', 'LA'],
    }
]

@pytest.mark.parametrize("cities", testdata)

class TestTools:
     
    def test_weather_service(self, cities):
        print(f"**Test input type: {type(cities)}")
        print(f"**Test input value: {cities}")     
        result= weather_service(cities)
        print(f"**Test Case 'weather' result: {result}")
        assert result
