
from cgi import print_exception
import mysql.connector
import requests


def insert_product(id, name, price, alcohol, volume, country):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='apk',
                                             user='root',
                                             password='mdopc00')
        cursor = connection.cursor(dictionary=True)
        mySql_insert_query = """INSERT INTO beer (id, name, price, alcohol, volume, country) 
                                VALUES (%s, %s, %s, %s, %s, %s) """

        record = (id, name, price, alcohol, volume, country)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        #print("Record inserted successfully into beer table")

    except mysql.connector.Error as error:
        
        #print("Failed to insert into MySQL table {}".format(error))
        
        sql_Query = "select * from beer where id = %s"
        
        cursor.execute(sql_Query,(id,))
       
        record = cursor.fetchall()
        for row in record:
            oldvolume = row["volume"]
        
        

        update_QueryVol = "update beer set volume = %s where id = %s"
        update_QueryPrice = "update beer set price = %s where id = %s"
        if(int(oldvolume)>=int(volume)):
            cursor.execute(update_QueryVol, (volume,id))
            cursor.execute(update_QueryPrice,(price,id))
            connection.commit()
            print("I have update the entry with id: %s", id)
            
            
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
           # print("MySQL connection is closed")


url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch/search"

for i in range (1,13):
    querystring = {"sortBy":"Name","sortDirection":"Ascending","size":"30","page":[i],"categoryLevel1":"Öl","storeId":"0525","isInStoreAssortmentSearch":"true","isInDepotStockForFastDelivery":"false","responsFormat":"json"}

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

    for i in range(1,30):
            id = data['products'][i]['productId']
            name = data['products'][i]['productNameBold']
            price = data['products'][i]['price']
            alcohol = data['products'][i]['alcoholPercentage']
            volume = data['products'][i]['volume']
            country = data['products'][i]['country']
            insert_product(id, name, price, alcohol, volume, country)

            
print("Done")