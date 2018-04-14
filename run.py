from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from places.algorithm import Algorithm
from ast import literal_eval as make_tuple
import json

app = Flask(__name__)

js = Bundle('templates/javascript/run_devon.js', output='gen/main.js')
assets = Environment(app)
assets.register('main_js', js)


@app.route('/')
def index():
    start = request.args.get('start')
    end = request.args.get('end')

    return json.dumps(Algorithm.run(eval(start), eval(end)))


if __name__ == '__main__':
    app.run(debug=True)