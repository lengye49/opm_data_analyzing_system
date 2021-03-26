# export FLASK_APP=demo.py
# flask run --host=0.0.0.0

import sys
sys.path.append('/Users/oas/Documents/work/github/opm_data_analyzing_system/')

from flask import Flask
from opm_tga import tga

app = Flask(__name__)
print(sys.path)


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/demo')
def test():
    print('lalala')
    return 'demo lalala'


@app.route('/add/<int:a>')
def show_sum(a):
    return str(a) + ' + ' + str(1) + ' = ' + str(a + 1)


@app.route('/cmd0/help')
def show_cmd0_help():
    return 'id,quality,lv,enhance,equip,equiplv,talent,academy,job,limiter,mechanical'


@app.route('/cmd0/run/<string:param>')
def run_cmd0(param):
    return {'hp':100,'atk':50,'param':param}


@app.route('/cmd1')
def run_cmd1():
    return tga.get_all_stats()