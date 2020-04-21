#! /usr/bin/python3
from index import app
application = app.server

if __name__ == "__main__":
  application.run( port = 8000 )
