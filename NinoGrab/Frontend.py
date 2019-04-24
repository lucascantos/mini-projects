import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Yeehaw"

'''
(GET) Abre csv qualquer.
   Podemos deixar como default o caminho interno pros Ninos


'''