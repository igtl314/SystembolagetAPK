
import mysql.connector


try:
    connection = mysql.connector.connect(host='localhost',
                                          database='test',
                                          user='root',
                                          password='mdopc00')
    mySql_inser_quary = """INSERT INTO hej (id, name)
                          VALUES
                          (15,'Marcus är bäst')"""
    cursor = connection.cursor()
    cursor.execute(mySql_inser_quary)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into test table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into test table {}".format(error))

   
                                          
    
    update_Query = "UPDATE hej SET name = 'mömd' where id = 15"
    cursor.execute(update_Query)

  
        
    connection.commit()
    print("I have update the entry with id: 15")


finally:
  if connection.is_connected():
    connection.close()
    print("hej")