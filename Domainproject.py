import json 
import requests
import re
import timeit
import time
from dotenv import load_dotenv
import os

#load the environment variables 
load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")



property_id = "2017269776"
starting_max = 1000000
starting_min = 0
increment = 50000

response = requests.post('https://auth.domain.com.au/v1/connect/token',data = {'client_id':client_id,"client_secret":client_secret,"grant_type":"client_credentials","scope":"api_listings_read","Content-Type":"text/json"})
token=response.json()
access_token=token["access_token"]


url = "https://api.domain.com.au/v1/listings/"+property_id
auth = {"Authorization":"Bearer "+access_token}
request = requests.get(url,headers=auth)
r=request.json()


da=r['addressParts']
postcode=da['postcode']
suburb=da['suburb']
bathrooms=r['bathrooms']
bedrooms=r['bedrooms']
carspaces=r['carspaces']
property_type=r['propertyTypes']


# the below puts all relevant property types into a single string. eg. a property listing can be a 'house' and a 'townhouse'
n=0
property_type_str=""
for p in r['propertyTypes']:
  property_type_str=property_type_str+(r['propertyTypes'][int(n)])
  n=n+1





max_price = starting_max
search_for_price = True

while search_for_price:
    url = "https://api.domain.com.au/v1/listings/residential/_search" # Set destination URL here
    post_fields ={
      "listingType":"Sale",
      "maxPrice":max_price,
      "pageSize":100,
      "propertyTypes":property_type,
      "minBedrooms":bedrooms,
      "maxBedrooms":bedrooms,
      "minBathrooms":bathrooms,
      "maxBathrooms":bathrooms,
      "locations":[
        {
          "state":"",
          "region":"",
          "area":"",
          "suburb":suburb,
          "postCode":postcode,
          "includeSurroundingSuburbs":False
        }
      ]
    }

    request = requests.post(url,headers=auth,json=post_fields)

    l=request.json()
    listings = []
    for listing in l:
      listings.append(listing["listing"]["id"])
 

    if int(property_id) in listings:
      max_price=max_price-increment
      search_for_price=False
    else:
      max_price=max_price+increment
      time.sleep(0.1)




search_for_price=True
if starting_min>0:
  min_price=starting_min
else:  
  min_price=max_price+400000  




while search_for_price:
    
    url = "https://api.domain.com.au/v1/listings/residential/_search" # Set destination URL here
    post_fields ={
      "listingType":"Sale",
      "minPrice":min_price,
      "pageSize":100,
      "propertyTypes":property_type,
      "minBedrooms":bedrooms,
      "maxBedrooms":bedrooms,
      "minBathrooms":bathrooms,
      "maxBathrooms":bathrooms,
      "locations":[
        {
          "state":"",
          "region":"",
          "area":"",
          "suburb":suburb,
          "postCode":postcode,
          "includeSurroundingSuburbs":False
        }
      ]
    }

    request = requests.post(url,headers=auth,json=post_fields)

    l=request.json()
    listings = []
    for listing in l:
      listings.append(listing["listing"]["id"])
    listings

    if int(property_id) in listings:
      min_price=min_price+increment
      search_for_price=False
    else:
      min_price=min_price-increment
      time.sleep(0.1)  # sleep a bit so you don't make too many API calls too quickly 



# Print the results
print(da['displayAddress'])
print(r['headline'])
print("Property Type:",property_type_str)
print("Details: ",int(bedrooms),"bedroom,",int(bathrooms),"bathroom,",int(carspaces),"carspace")
print("Display price:",r['priceDetails']['displayPrice'])      
if max_price==min_price:
  print("Price guide:",min_price)
else:
  print("Price range:","$",min_price,"-",max_price)
print("URL:",r['seoUrl'])







