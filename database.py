######## A home Surveillance system - Database module #########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description: This module defines the data insert and data retrieve
# method using a sqlite database.


# Import class
import sqlite3
import pandas as pd


class Database:
    def __init__(self):
        try:
            self.con = sqlite3.connect('db/FrameDifference.db')

            self.cur = self.con.cursor()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if self.con:
                self.con.close()
                print("The SQLite connection is closed")


    def save_data(self, time, fps):
        """
         insert a new data row of data to table
         :param id  the record id
         :param cam_id  the camera id
         :param time  the timestamp the record is written
         """
        try:
            insert_with_param = """INSERT INTO  new_vibe_test
                                       (time , fps) 
                                       VALUES (?, ?);"""

            data_tuple = (str(time), fps)
            self.cur.execute(insert_with_param, data_tuple)
            self.con.commit()

        except sqlite3.Error as error:
            print("Failed to insert data", error)


    def get_data(self):
        """
        Add retrieve the data from table
        :return the whole data in the table
        """
        try:
            df = pd.read_sql_query("SELECT * FROM records_test", self.con)
            return df
        except sqlite3.Error as error:
            print("Failed to retrieve data", error)



