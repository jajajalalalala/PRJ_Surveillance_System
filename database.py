import sqlite3
import pandas as pd
import uuid


class Database:
    def __init__(self):
        try:
            self.con = sqlite3.connect('SurveillanceSystem.db')

            self.cur = self.con.cursor()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        # finally:
        #     if self.con:
        #         self.con.close()
        #         print("The SQLite connection is closed")

    def save_data(self, cam_id, time):
        """
         insert a new data row of data to table
         :param id  the record id
         :param cam_id  the camera id
         :param time  the timestamp the record is written
         """
        try:
            insert_with_param = """INSERT INTO records_test
                                       (ID , CAM_ID, TIME) 
                                       VALUES (?, ?, ?);"""

            data_tuple = (str(uuid.uuid4()), cam_id, time)
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


if __name__ == '__main__':
    db = Database()
    db.save_data("cam1", "123")
    print(db.get_data())
