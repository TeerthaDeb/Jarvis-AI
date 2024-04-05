__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = [] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced."  

import geocoder
from geopy.geocoders import Nominatim
from typing import Dict, Any

def get_city_details(latitude = None , longitude = None) -> Dict[str, Any]:
    """
    	Get city details such as name, address, country, and more based on latitude and longitude coordinates.
    
    :param latitude: Latitude coordinate.
    :param longitude: Longitude coordinate.
    
    :return: Dictionary containing city details in JSON format.
    
    Since : 1.0.2
    
    """
    if (latitude  == None or longitude == None):
         (latitude, longitude) = search_city()
		
    geolocator = Nominatim(user_agent="city_locator")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    
    city_details = {
        "tourism": address.get('tourism', ''),
        "road": address.get('road', ''),
        "suburb": address.get('suburb', ''),
        "city": address.get('city', ''),
        "county": address.get('county', ''),
        "region": address.get('region', ''),
        "state": address.get('state', ''),
        "ISO3166-2-lvl4": address.get('ISO3166-2-lvl4', ''),
        "postcode": address.get('postcode', ''),
        "country": address.get('country', ''),
        "country_code": address.get('country_code', ''),
        # Add more details as needed
    }
    
    return city_details

def search_city() -> tuple:
	"""
      Returns coordinates of your location.

	Returns:
		tuple: (latitude, longitude)
            
		Since : 1.0.2
	"""
	g = geocoder.ip('me')
	latitude = g.latlng[0]
	longitude = g.latlng[1]
      
	return (latitude , longitude)


if  __name__ == "__main__":
    print(get_city_details()['city'])