#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mysql.connector as mc
import pandas as pd
import unittest
from sklearn import datasets as ds



'''
* Objective
The Iris class below manages a database version of the Iris dataset available in the sklearn package.
Build out the Iris class to be able to make it intelligent enough to handle
multiple Iris databases. Each database holds one IRIS_DATA table.
Hints below will help you through building this code out.
What each function should do:
Iris constructor - Will allow a user to create or use an existing MySQL Iris database. The new
flag specifies if the database should be created including the IRIS_DATA table. If the flag is false
it will simply connect to an existing Iris database.
load() - Loads the Iris data from sklearn into the MySQL database table under the dbname specified. All
150 observations are loaded in. Your table should look like this: https://pasteboard.co/HPCJOiI.png
display_gt() - Takes an integer argument n and displays all rows with id greater than n
del_observations() - Takes a list of ids and deletes them from the table
update_observation() - Takes 3 arguments - The id, new target species and new target_species_id and updates the 
row with the new information
* Suggested reading / references:
https://dev.mysql.com/doc/connector-python/en/
https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
https://dev.mysql.com/doc/refman/8.0/en/truncate-table.html
https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
https://dev.mysql.com/doc/refman/8.0/en/use.html
https://www.w3schools.com/sql/sql_select.asp
https://www.w3schools.com/sql/sql_insert.asp
https://www.w3schools.com/sql/sql_delete.asp
https://www.w3schools.com/sql/sql_update.asp
https://www.w3schools.com/sql/sql_drop_db.asp
* DDL for iris_data table and sample SQL statements:
DROP DATABASE csc221;
CREATE DATABASE csc221;
USE csc221;
DROP TABLE IF EXISTS iris_data;
CREATE TABLE iris_data (
	id INT NOT NULL,
    feature_sepal_length FLOAT NOT NULL,
    feature_sepal_width FLOAT NOT NULL,
    feature_petal_length FLOAT NOT NULL,
    feature_petal_width FLOAT NOT NULL,
    target_species VARCHAR(20) NOT NULL,
    target_species_id INT NOT NULL
);
Hint: When building this out, temporarily remove the NOT NULLs in the IRIS_DATA so that you can test without 
having to add data in all columns
The database host address is assumed to be 127.0.0.1 (your local computer)
A successful run of the unit tests will look like this:
$ python .\06_assignment_solution.py
Database and IRIS table created in DB csc221
Row count is 0
Iris dataset loaded
Row count is 150
Iris dataset loaded
Row count is 300
Database and IRIS table created in DB csc221x
Row count is 0
Iris dataset loaded
Row count is 150
Iris table truncated
Iris dataset loaded
Row count is 150
(149, 5.9, 3.0, 5.1, 1.8, 'virginica', 2)
(149, 5.9, 3.0, 5.1, 1.8, 'stuff', 5)
(149, 5.9, 3.0, 5.1, 1.8, 'virginica', 2)
Row count is 144
Row count is 150
.
----------------------------------------------------------------------
Ran 1 test in 0.658s
'''
def main():
    # Usage example. 
     
    #Change get_credentials() with your password.
    creds = get_credentials()
    iris = Iris(creds) # Create a MySQL database called csc221
    iris.load() # Load Iris data from sklearn and pump it into IRIS_DATA table
    iris.display_gt(140) # Display to the screen all rows with ID greater than 140
    
    iris2 = Iris(creds,dbname='csc221x') # Creates a 2nd MySQL database called anotherone, you now have 2 databases (one server still, tho)
    iris2.load() # Load Iris data
    iris2.del_observations([0,1,2]) # Delete observations that have id equal to 0, 1 or 2

    iris.update_observation(0,'stuff',5) # Change observation id 0 to a different label

    iris.close() # Close connection
    iris2.close() # Close connection

# Change password
def get_credentials():
    return {'user':'root','password':'HofstraCS21!'}

class Iris:
    def __init__(self,creds,dbname='csc221',new=True):
        self.__conn = mc.connect(**creds) 
        self.__dbname = dbname

        if new:
            cursor = self.__conn.cursor()

            cursor.execute("DROP DATABASE IF Exists csc221")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__dbname}")
            cursor.execute(f"USE {self.__dbname}")
            cursor.execute("DROP TABLE IF EXISTS iris_data")
            cursor.execute("CREATE TABLE iris_data (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,feature_sepal_length FLOAT NOT NULL,feature_sepal_width FLOAT NOT NULL,feature_petal_length FLOAT NOT NULL,feature_petal_width FLOAT NOT NULL,target_species VARCHAR(20) NOT NULL,target_species_id INT NOT NULL);")
            self.__conn.commit()
            cursor.close()
            
        else:
            cursor = self.__conn.cursor()
            cursor.execute(f"USE {self.__dbname}")
            cursor.close()

        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM iris_data")
        self.__iris = cursor.fetchall()
        cursor.close()


    # Drop the database and create a new one with a new table
    def __create(self):
        # ------ Place code below here \/ \/ \/ ------
        cursor = self.__conn.cursor()

        # Drop the existing database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS {self.__dbname}")

        # Create a new database
        cursor.execute(f"CREATE DATABASE {self.__dbname}")
        cursor.execute(f"USE {self.__dbname}")

        # Create a new table
        cursor.execute("""
            CREATE TABLE iris (
                id INT AUTO_INCREMENT PRIMARY KEY,
                feature_sepal_length FLOAT NOT NULL,
                feature_sepal_width FLOAT NOT NULL,
                feature_petal_length FLOAT NOT NULL,
                feature_petal_width FLOAT NOT NULL,
                target_species VARCHAR(50) NOT NULL
                target_species_id INT NOT NULL)
            )
        """)



    # Close connection
    def close(self):
        # ------ Place code below here \/ \/ \/ ------
        self.__conn.commit()
        cursor.close()
        print("Disconnected")
        # ------ Place code above here /\ /\ /\ ------
        
    # Loop the Iris data and INSERT into the IRIS_DATA table
    def load(self,truncate=False):
        if truncate:
            cursor = self.__conn.cursor()
            cursor.execute("TRUNCATE TABLE IRIS_DATA")
            cursor.close()
            print('Iris table truncated')
    
        iris_data = ds.load_iris()
        iris_target_names = iris_data.target_names

        for i in range(len(iris_data.target)):
            query = f"""
            INSERT INTO IRIS_DATA (feature_sepal_length, feature_sepal_width, feature_petal_length, feature_petal_width, target_species, target_species_id)
            VALUES ({iris_data.data[i][0]}, {iris_data.data[i][1]}, {iris_data.data[i][2]}, {iris_data.data[i][3]}, '{iris_target_names[iris_data.target[i]]}', {iris_data.target[i]})
            """

            cursor = self.__conn.cursor()
            cursor.execute(query)
            cursor.close()

        self.__conn.commit()
        print('Iris dataset loaded')

    # Display all rows that have ID greater than integer n
    def display_gt(self,n): 
        # ------ Place code below here \/ \/ \/ ------
        cursor = self.__conn.cursor()
        cursor.execute(f"SELECT * FROM IRIS_DATA WHERE id > {n}")

        # Fetch all the rows and print them
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()

        # ------ Place code above here /\ /\ /\ ------

    # Update observation with a specific id to a new target species and species id
    def update_observation(self, id, new_target_species, new_target_species_id):
        cursor = self.__conn.cursor()

        # Update the observation with the given id
        cursor.execute(f"UPDATE IRIS_DATA SET species = '{new_target_species}', species_id = {new_target_species_id} WHERE id = {id}")
        self.__conn.commit()
        cursor.close()

        print(f"Observation with ID {id} updated to {new_target_species} (ID {new_target_species_id})")


    # Delete all rows that are in the list row_ids    
    def del_observations(self,row_ids):
        # ------ Place code below here \/ \/ \/ ------
        cursor = self.__conn.cursor()

        # Loop through the row_ids list and delete each row with the corresponding ID
        for row_id in row_ids:
            cursor.execute(f"DELETE FROM IRIS_DATA WHERE id = {row_id}")
        self.__conn.commit()
        cursor.close()

        print(f"{len(row_ids)} observations deleted")

        # ------ Place code above here /\ /\ /\ ------

    # Truncate the IRIS_DATA table
    def __truncate_iris(self):
        # ------ Place code below here \/ \/ \/ ------
        cursor = self.__conn.cursor()
        cursor.execute("TRUNCATE TABLE IRIS_DATA")
        self.__conn.commit()
        cursor.close()

        print("IRIS_DATA table truncated")

        # ------ Place code above here /\ /\ /\ ------

    # Establish a connection
    def __get_connection(self,creds):
        return mc.connect(user=creds['user'], password=creds['password'],
                              host='127.0.0.1',
                              auth_plugin='mysql_native_password')      

    # Returns the current row count of the IRIS_DATA table
    def get_row_count(self):
        # ------ Place code below here \/ \/ \/ ------
        cursor = self.__conn.cursor()
        cursor.execute(f"USE {self.__dbname}")
        cursor.execute("SELECT COUNT(*) FROM iris_data")
        count = cursor.fetchone()[0]
        cursor.close()

        # ------ Place code above here /\ /\ /\ ------
        return count

class TestAssignment6(unittest.TestCase):
    def test(self):
        creds = get_credentials()
        db1 = Iris(creds)
        self.assertEqual(db1.get_row_count(),0)
        db1.load()
        self.assertEqual(db1.get_row_count(),150)
        db1.load()
        self.assertEqual(db1.get_row_count(),300)
        db2 = Iris(creds,dbname='csc221x')
        self.assertEqual(db2.get_row_count(),0)
        db2.load()
        self.assertEqual(db2.get_row_count(),150)
        db1.load(truncate=True)
        self.assertEqual(db1.get_row_count(),150)
        db1.display_gt(148)
        db1.update_observation(149,'stuff',5)
        db1.display_gt(148)
        db2.display_gt(148)
        db1.del_observations([0,1,2,3,4,5])
        self.assertEqual(db1.get_row_count(),144)
        self.assertEqual(db2.get_row_count(),150)


if __name__ == '__main__':
    #main()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

