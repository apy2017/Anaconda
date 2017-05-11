#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/usr/share/nginx/html/techbot")

from techbot_webhook import app as application

if __name__ == "__main__":
    application.run()

#application.secret_key = 'Add your secret key'