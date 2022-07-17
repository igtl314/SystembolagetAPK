import requests
import json


url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch/search"

#for i in range (1,12):
querystring = {"sortBy":"Name","sortDirection":"Ascending","size":"30","page":"1","categoryLevel1":"Öl","storeId":"0525","isInStoreAssortmentSearch":"true","isInDepotStockForFastDelivery":"false","responsFormat":"json"}

payload = ""
headers = {
    "authority": "api-extern.systembolaget.se",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,en-US;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-GB;q=0.6",
    "ocp-apim-subscription-key": "cfc702aed3094c86b92d6d4ff7a54c84",
    "origin": "https://www.systembolaget.se",
    "referer": "https://www.systembolaget.se/",
    "sec-ch-ua": "^\^"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

data = response.json()

for  products in data:
        print (productNameBold)
