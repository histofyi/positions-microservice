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
    This is the function which loads the generated datasets which are used by the site.

    By loading them in here, we can reduce S3 calls and speed the app up significantly.
    """
    with open('data/contact_labels.json') as labels:
        app.data['labels'] = json.load(labels)


@app.route('/positions/')
@app.route('/positions')
def positions_home(api=False):
    """
    This is the handler for the positions homepage. It will include a way to quickly jump to a class/chain combination and a search box to redirect to a specific position
    """
    return app.data


@app.route('/positions/lookup/')
@app.route('/positions/lookup')
def class_page(api=False):
    """
    This is the handler that performs lookups for positions

    Args:
        mhc_class (string): the slugified MHC class e.g. class_i
        chain (string): the lower case chain name e.g. peptide, alpha
        position (string): the position id according to IMGT numbering

    The arguments are provided either as querystring or post variables
    """
    return "lookup"


@app.route('/positions/<string:mhc_class>/')
@app.route('/positions/<string:mhc_class>')
def mhc_class_page(mhc_class, api=False):
    """
    This is the handler that for the positions class page, it provides a list of chains, and possibly a way to jump straight to the positions (multiple chain presentations per page?)

    Args:
        mhc_class (string): the slugified MHC class e.g. class_i
    """
    return f'{mhc_class}'


@app.route('/positions/<string:mhc_class>/<string:chain>/')
@app.route('/positions/<string:mhc_class>/<string:chain>')
def chain_page(mhc_class, chain, api=False):
    """
    This is the handler that for the positions chain page, it provides a representation of that chain to link through to individual position pages

    Args:
        mhc_class (string): the slugified MHC class e.g. class_i
        chain (string): the lower case chain name e.g. peptide, alpha
    """
    return f'{mhc_class}:{chain}'


@app.route('/positions/<string:mhc_class>/<string:chain>/<string:position>/')
@app.route('/positions/<string:mhc_class>/<string:chain>/<string:position>')
def position_page(mhc_class, chain, position, api=False):
    """
    This is the handler that for the position page, it provides information on the role, polymorphism and structural variability of that position

    Args:
        mhc_class (string): the slugified MHC class e.g. class_i
        chain (string): the lower case chain name e.g. peptide, alpha
        position (string): the position id according to IMGT numbering

    Optional Args:
        species (string): restrict to a specific specie
        locus (string): restrict to a specific locus
        allele_group: restrict to a specific allele group

    The optional arguments will be provided as query string parameters and are a future feature
    """
    return f'{mhc_class}:{chain}:position{position}'

