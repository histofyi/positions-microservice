from flask import Flask
import json


def create_app():
    app = Flask(__name__)
    app.data = {}
    app.data['positions'] = {
        'class_i_alpha':{'start':1,'stop':275}
    }
    return app


app = create_app()


@app.before_first_request
def load_data():
    """
    This is a function which loads the generated datasets which are used by the site.

    By loading them in here, we can reduce S3 calls and speed the app up significantly.
    """
    with open('data/contact_types.json') as labels:
        app.data['labels'] = json.load(labels)

@app.route('/positions/')
@app.route('/positions')
def positions_home(api=False):
    return app.data


@app.route('/positions/<string:mhc_class>/')
@app.route('/positions/<string:mhc_class>')
def class_page(mhc_class, api=False):
    return f'{mhc_class}'

@app.route('/positions/<string:mhc_class>/<string:chain>/')
@app.route('/positions/<string:mhc_class>/<string:chain>')
def chain_page(mhc_class, chain, api=False):
    return f'{mhc_class}:{chain}'

@app.route('/positions/<string:mhc_class>/<string:chain>/<string:position>/')
@app.route('/positions/<string:mhc_class>/<string:chain>/<string:position>')
def position_page(mhc_class, chain, position, api=False):
    return f'{mhc_class}:{chain}:position{position}'

