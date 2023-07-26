# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

from flask import Flask
from flask_ngrok import run_with_ngrok
  
app = Flask(__name__)
run_with_ngrok(app)
  
@app.route("/")
def hello():
    return "Hello Geeks!! from Google Colab"
  
if __name__ == "__main__":
  app.run()