from operator import truediv
import re
import mysql.connector

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import time
from datetime import date


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.systembolaget.se/sok/?categoryLevel1=%C3%96l&page=1")

actions = ActionChains(driver)

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-qw0trq"))
)
element.click()

time.sleep(1)
xpath = '/html/body/div[4]/div/div/div/div/div/div[2]/div[2]/button[2]'

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)
element.click()

time.sleep(1)

## Väljer butik

xpath = '//*[@id="mainContent"]/div[2]/main/div[2]/div/div/div/div/div[1]/div/button[2]'
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))

)
element.click()

xpath='//*[@id="initialTgmFocus"]/div/input'
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)
time.sleep(1)
element.send_keys("Djurgården")
time.sleep(1)

xpath='//*[@id="react-autowhatever-1-section-0-item-0"]/div'
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))

)
element.click()
time.sleep(1)
#Väljer butik slut



#
for i in range(13):
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"css-6hztd2.epc1dj70"))
        )
        #element = driver.find_element(By.CLASS_NAME,"css-6hztd2.epc1dj70")
        element.click()
        time.sleep(2)
        
        

time.sleep(1)
price = driver.find_elements(By.CLASS_NAME,"css-1l6tt3v.e1f2zvku0")

name = driver.find_elements(By.CLASS_NAME, "css-rh4jwl.e1yt52hj7" )

info = driver.find_elements(By.CLASS_NAME, "css-mdt0kf.eof5z0g0" )


id = driver.find_elements(By.CLASS_NAME, "css-b2o0pl.e1yt52hj7")


volume = []

country = []

alcohol = []


#Formating the answer
for e in range(len(price)):
    price[e] =  re.sub("[^0-9:]", "", price[e].text)
    price[e] =  re.sub(":", ".", price[e])
    id[e] =  re.sub("[^0-9:]", "", id[e].text)
    info[e] = info[e].text.splitlines()
    info[e][2] = re.sub("[%\s]","", info[e][2])
    info[e][2] = re.sub(",",".", info[e][2])
    country.append(info[e][0])
    volume.append(re.sub("[^0-9]","",info[e][1]))
    alcohol.append(info[e][2])
   



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
        print("Record inserted successfully into beer table")

    except mysql.connector.Error as error:
        
        print("Failed to insert into MySQL table {}".format(error))
        print(name)
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
            print("MySQL connection is closed")


#id, name, price, alcohol, volume, country

for e in range(len(price)):
    insert_product(id[e], name[e].text, price[e], alcohol[e], volume[e], country[e])





