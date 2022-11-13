import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import handlers
import os
import sqlite3
import traceback

define("port", default=8000, type=int)

urls = [
    (r"/", handlers.WidgetHandler),
]

settings = dict({
    "debug": True,
})


application = tornado.web.Application(urls, **settings)

if __name__ == "__main__":
    # connect to database and create a cursor
    conn = sqlite3.connect('weber.db')
    c = conn.cursor()

    # create widget table
    try:
        c.execute(
            """CREATE TABLE IF NOT EXISTS widget (
        id integer PRIMARY KEY AUTOINCREMENT, 
        name text, 
        number_of_parts integer,
        created_date text,
        updated_date text
        )
        """
        )
    # commit table and close connection
        conn.commit()
        conn.close()

    # success message
        print({"success":"database table successfully accessed"})

    # except any errors in the creation process
    except sqlite3.OperationalError as e:
        print({"error" :traceback.format_exc()})

    # start tornado server
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()