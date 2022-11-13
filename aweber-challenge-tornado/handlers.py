import tornado.web
import sqlite3
import json
import traceback
from datetime import datetime


"""
    handlers.py:

    Creates a sqlite3 database and database connection object for handling requests.

    Contains the handlers for the http requests for the tornado server using the sqlite3 connection

    - create: create a new widget 
    - read: returns a single widget's details
    - list: returns all widgets' details
    - update: put request to a specified widget's details
    - delete: removing a specified widget

"""

class WidgetHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.conn = sqlite3.connect('weber.db')
        self.c = self.conn.cursor()
        if self.request:
            self.args = json.loads(self.request.body)

    ####

    # GET

    ####
    def get(self) -> None:
        
        # determine if a specific ID was requested
        if not self.get_argument('id', default=None):
            # if not, select all widgets
            query = "SELECT * FROM widget ORDER BY created_date DESC"
            try:
                self.c.execute(query)

                # return list of widgets
                returned = self.c.fetchall()
                
                # package results
                results = []
                for widget in returned:
                    results.append(widget)
                resp = json.dumps(results)
                self.write(resp)
            except Exception:
                self.write({"error": traceback.format_exc()})
        else:
            # if id provided, find matching widget
            id_val = self.get_argument('id')
            query = "SELECT * FROM widget WHERE ID ={}".format(id_val)
            self.c.execute(query)

            # return list of widgets
            returned = self.c.fetchall()

            # package results
            results = []
            for widget in returned:
                results.append(widget)
            if not results:
                self.write({"message": "No widget exists with id = {}.".format(id_val)})
            resp = json.dumps(results)
            self.write(resp)

    ####

    # POST

    ####
    def post(self):

        # grab body arguments
        
        name = self.args['name']
        number_of_parts = self.args['number_of_parts']
        current_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        created_date = current_date
        updated_date = current_date


        if name == None or number_of_parts == None:
            self.set_status(
                status_code=400, 
                reason={"error": "Missing required parameters (name, number_of_parts)."}
                )

        # connect to database and create query
        query = "INSERT INTO widget (name, number_of_parts, created_date, updated_date) VALUES ('{}', '{}', '{}', '{}')".format(name, number_of_parts, created_date, updated_date)

        # run insertion and catch errors
        try:
            self.c.execute(query)
            self.conn.commit()
            self.conn.close()
            self.write({"message": """successfully added widget to database. 
                                        name : {},
                                        number_of_parts: {}""".format(name, number_of_parts)
                        })
                                        
        except sqlite3.OperationalError:
            self.write({"errror": traceback.format_exc()})
            self.c.close()

    ####

    # Update

    ####
    def patch(self):
         # determine if a specific ID was requested
        if not self.get_argument('id', default=None):
            self.set_status(
                status_code=400, 
                reason={"error": "Missing required parameter (id)."}
                )
        else:
            id_val = self.get_argument('id')

            # evaluate if updates were provided
            if len(self.args) == 0:
                self.set_status(
                status_code=400, 
                reason={"error": "No updates in request."}
                )

            # set updated date
            current_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self.args.update({"updated_date": current_date})

            # create and execute query string
            query = """UPDATE widget SET """
            index = 0
            length = len(self.args)
            for key, value in self.args.items():
                index += 1
                if index == length: 
                    query += """ {}='{}' """.format(key, value)
                    print(query)
                else:
                    query += """ {}='{}', """.format(key, value)
                    print(query)
            query += """ WHERE id = {}""".format(id_val)
            print(query)
            self.c.execute(query)
            self.conn.commit()

            # grab 
            self.c.execute("""SELECT * FROM widget WHERE ID ={}""".format(id_val))
            returned = self.c.fetchall()
            # package results
            results = []
            for widget in returned:
                results.append(widget)
            self.write({"message":"Widget {} successfully updated:  {}".format(id_val, results)})

    ####

    # Delete

    ####
    def delete(self):
        
        # verify an id has been provided
        if not self.get_argument('id', default=None):
            self.set_status(
                status_code=400, 
                reason={"error": "Missing required parameter (id)."}
                )
        else:
            # use id to update query
            id_val = self.get_argument('id')
            query = """ DECLARE @WidgetId INT = {} 
                    IF EXISTS (SELECT 1 FROM widget WHERE id = WidgetId)
                    BEGIN 
                    DELETE FROM widget WHERE id = WidgetId
                    END
            """.format(id_val)
            self.c.execute(query)

            # return deletion success            
            self.write({"message":"Deletion of widget {} successful.".format(id_val)})


    def on_finish(self):
        self.conn.commit()
        self.conn.close()
        return super().on_finish()