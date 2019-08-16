import json

import psycopg2
from flask import Flask, request, Response


SUPPORTED_FORMATS = frozenset(['tsv'])


COLUMN_NAMES = ('ID',
    'Field',
    'StarID',
    'RA',
    'Decl',
    'Type',
    'Subtype',
    'I',
    'V',
    'P_1',
    'A_1',
    'ID_OGLE_II',
    'ID_MACHO',
    'ID_ASAS',
    'ID_GCVS',
    'ID_OTHER',
    'Remarks',
)
TSV_HEADER = '\t'.join(COLUMN_NAMES)


CONNECTION = psycopg2.connect(host='sql', user='app', dbname='ogle')


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    return '''
    <p>
        Welcome to <a href="//snad.space">SNAD</a>
        <a href="http://ogledb.astrouw.edu.pl/~ogle/CVS/overview.html">OGLE-III</a> mirror
    </p>
    <p>
        See API details on <a href="/api/v1/help">/api/v1/help</a>
    </p>
    '''


@app.route('/api/v1/help')
def help():
    fmt = f'''<font face='monospace'>format</font> &mdash; response format, can be one of: {', '.join(FROM_CUR)}. Default is tsv'''
    return f'''
    <h1>Available resources</h1>
    <h2><font face='monospace'>/api/v1/all</font></h2>
        <p> Get the whole catalog</p>
        <p> Query parameters:</p>
        <ul>
            <li>{fmt}</li>
        </ul>
    <h2><font face='monospace'>/api/v1/circle</font></h2>
        <p> Get objects in the circle</p>
        <p> Query parameters:</p>
        <ul>
            <li>{fmt}</li>
            <li><font face='monospace'>ra</font> &mdash; right ascension of the circle center, degrees. Mandatory</li>
            <li><font face='monospace'>dec</font> &mdash; declination of the circle center, degrees. Mandatory</li>
            <li><font face='monospace'>radius_arcsec</font> &mdash; circle radius, arcseconds. Mandatory, should be positive and less than 324000 (90 degress)</li>
        </ul>
    '''


def to_str(x):
    return '' if x is None else str(x).strip()


def strip(x):
    try:
        return x.strip()
    except AttributeError:
        return x


def tsv_from_cur_gen(cur):
    yield TSV_HEADER
    for row in cur:
        yield '\n' + '\t'.join(map(to_str, row))
    cur.close()


def tsv_from_cur(cur):
    return Response(tsv_from_cur_gen(cur), mimetype='text/tab-separated-values')


def json_from_cur(cur):
    items = []
    for row in cur:
        items.append(dict(zip(COLUMN_NAMES, map(strip, row))))
    message = json.dumps(items)
    cur.close()
    return Response(message, mimetype='application/json')


FROM_CUR = {
    'tsv': tsv_from_cur,
    'json': json_from_cur,
}


def table_response(fmt, query, var=()):
    try:
        from_cur = FROM_CUR[fmt]
    except KeyError:
        return f'Format {fmt} is not supported, supported formats are: {", ".join(FROM_CUR)}', 404
    cur = CONNECTION.cursor()
    try:
        cur.execute(query, var)
    except psycopg2.errors.InternalError as e:
        return str(e), 404
    return from_cur(cur)


@app.route('/api/v1/all')
def whole_catalog():
    return table_response(request.args.get('format', 'tsv'), 'SELECT * FROM catalog')


@app.route('/api/v1/circle')
def select_in_circle():
    query = '''
        SELECT catalog.*
        FROM catalog
        INNER JOIN coord USING(id)
        WHERE coord.coord @ scircle %s
        ;
    '''
    try:
        ra = float(request.args['ra'])
        dec = float(request.args['dec'])
        radius_deg = float(request.args['radius_arcsec']) / 3600.0
    except KeyError:
        return 'ra, dec and radius_arcsec parameters are required', 404
    except ValueError:
        return 'ra, dec and radius_arcsec should be float numbers', 404
    scircle = f'<({ra}d, {dec}d), {radius_deg}d>'
    return table_response(request.args.get('format', 'tsv'), query, var=[scircle])

