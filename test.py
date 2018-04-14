from flask import Flask, render_template
from flask_assets import Bundle, Environment

app = Flask(__name__)

js = Bundle('templates/javascript/run_devon.js', output='gen/main.js')
assets = Environment(app)
assets.register('main_js', js)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)