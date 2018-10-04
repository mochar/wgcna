import csv
import os
import subprocess
import base64
import json
import itertools
import uuid
import shutil
from collections import Counter
from functools import wraps

from flask import Flask, request, jsonify, send_file, make_response, session, g, abort
from flask_session import Session
from flask_session.sessions import RedisSessionInterface
from flask_cors import CORS
from scipy.stats.stats import pearsonr
from redis import StrictRedis
import pandas as pd
import numpy as np

import app.rscripts as rscripts


app = Flask(__name__)
app.config.from_object('config')
redis = StrictRedis(db=app.config['REDIS_DB_DATA'], decode_responses=True,
     charset='utf-8')
app.config['SESSION_REDIS'] =  StrictRedis(db=app.config['REDIS_DB_SESSION'])
Session(app)
CORS(app, supports_credentials=True, expose_headers=['Location'])


# Non-simple CORS requests send a preflight OPTIONS request, which do not
# contain cookies. Flask-session therefore creates a new session, even
# though one might already exist. Here I "fix" this by ignoring OPTIONS
# requests in the session interface.
class CorsRedisSessionInterface(RedisSessionInterface):
    def open_session(self, app, request):
        if request.method == 'OPTIONS':
            return None
        return super(CorsRedisSessionInterface, self).open_session(app, request)
app.session_interface = CorsRedisSessionInterface(app.config['SESSION_REDIS'], 
    'session:', app.config['SESSION_USE_SIGNER'], True)


def base64_encode_image(image):
    with open(image, 'rb') as f:
        encoded = base64.b64encode(f.read())
    return encoded.decode()


def create_file_response(contents, filename):
    response = make_response(contents)
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


def project_id_to_folder(project_id):
    return os.path.join(app.config['STORAGE_FOLDER'], project_id)


def remove_file_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def read_first_column(path):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        return [i[0] for i in reader][1:]


def process_project(project):
    project['trait'] = bool(int(project['trait']))
    project['processed'] = bool(int(project['processed']))
    project['traits'] = redis.hgetall('traits:{}'.format(project['id']))
    return project


def project_from_id(project_id):
    project = redis.hgetall('project:{}'.format(project_id))
    return process_project(project)


def user_projects():
    if session is None:
        return []
    project_ids = redis.smembers('projects:{}'.format(session.sid))
    pipe = redis.pipeline()
    for project_id in project_ids:
        pipe.hgetall('project:{}'.format(project_id))
    projects = pipe.execute()
    projects = [process_project(p) for p in projects]
    return [project for project in projects if project['processed']]


def create_project(user_id, name, description, omic):
    project_id = uuid.uuid4().hex
    project_folder = project_id_to_folder(project_id)
    os.makedirs(project_folder)
    redis.sadd('projects:{}'.format(user_id), project_id)
    project = {'name': name, 'description': description, 'id': project_id, 'step': 1,
        'omic': omic, 'trait': 0, 'processed': 0}
    redis.hmset('project:{}'.format(project_id), project)
    return project


def delete_project(user_id, project_id):
    project_folder = project_id_to_folder(project_id)
    if os.path.exists(project_folder):
        shutil.rmtree(project_folder)
    redis.srem('projects:{}'.format(user_id), project_id)
    redis.delete('project:{}'.format(project_id))
    redis.delete('traits:{}'.format(project_id))


@app.before_request
def setup_request_info():
    g.project_id = request.view_args is not None and request.view_args.get('project_id') 
    if g.project_id is not None:
        g.project_folder = project_id_to_folder(g.project_id)
        g.expression_path = os.path.join(g.project_folder, 'expression.csv')
        g.sampletree_path = os.path.join(g.project_folder, 'sampletree.csv')
        g.tresholds_path = os.path.join(g.project_folder, 'tresholds.csv') 
        g.genetree_path = os.path.join(g.project_folder, 'genetree.csv')
        g.diss_tom_path = os.path.join(g.project_folder, 'diss_tom.csv')
        g.module_path = os.path.join(g.project_folder, 'modules.csv')
        g.eigengene_path = os.path.join(g.project_folder, 'eigengenes.csv')
        g.pvalues_path = os.path.join(g.project_folder, 'pvalues.csv')
        g.trait_path = os.path.join(g.project_folder, 'trait.csv')
        g.annotation_path = os.path.join(g.project_folder, 'annotations.json')


def project_exists(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session is None:
            abort(404)
            return
        if not redis.sismember('projects:{}'.format(session.sid), g.project_id):
            abort(404)
            return
        return f(*args, **kwargs)
    return decorated_function


# @app.route('/projects/', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/projects/', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        return jsonify({'projects': user_projects()})
    elif request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        omic = request.form.get('omic')
        if name == '':
            return jsonify(error='Required fields not supplied.'), 403
        project = create_project(session.sid, name, description, omic)
        return jsonify({'project': project})


@app.route('/projects/<project_id>', methods=['GET', 'DELETE', 'PUT'])
@project_exists
def project(project_id):
    if request.method == 'GET':
        project = project_from_id(project_id)
        return jsonify({'project': project})
    elif request.method == 'DELETE':
        delete_project(session.sid, project_id)
        return jsonify({}), 200
    elif request.method == 'PUT':
        redis.hset('project:{}'.format(project_id), 'name', request.form['name'])
        redis.hset('project:{}'.format(project_id), 'description', request.form['description'])
        redis.hset('project:{}'.format(project_id), 'omic', request.form['omic'])
        return jsonify({}), 200


@app.route('/projects/<project_id>/expression', methods=['GET', 'POST', 'PUT'])
@project_exists
def expression(project_id):
    if request.method == 'POST':
        expression = request.files.get('expression')
        if expression.filename == '':
            return jsonify(error='Required fields not supplied.'), 403
        expression.save(g.expression_path)
        sep = request.form.get('delim', ',') or ','
        df = pd.read_csv(g.expression_path, index_col=0, sep=sep)
        redis.hset('project:{}'.format(project_id), 'genes', len(df.columns))
        redis.hset('project:{}'.format(project_id), 'samples', len(df.index))
        redis.hset('project:{}'.format(project_id), 'processed', 1)
        return jsonify(features=len(df.columns), samples=len(df.index))
    elif request.method == 'GET':
        df = pd.read_csv(g.expression_path, index_col=0)
        response = {'colNames': df.columns.tolist(), 'rowNames': df.index.tolist()}
        return jsonify(response)
    elif request.method == 'PUT':
        df = pd.read_csv(g.expression_path, index_col=0)
        if request.form['transpose'] == 'true':
            df = df.T
            n_genes = redis.hget('project:{}'.format(project_id), 'genes')
            n_samples = redis.hget('project:{}'.format(project_id), 'samples')
            redis.hset('project:{}'.format(project_id), 'genes', n_samples)
            redis.hset('project:{}'.format(project_id), 'samples', n_genes)
        df.to_csv(g.expression_path)
        return jsonify({}), 200


@app.route('/projects/<project_id>/expression/<module>', methods=['GET'])
@project_exists
def expression_module(project_id, module):
    df = pd.read_csv(g.expression_path, index_col=0)
    modules = pd.read_csv(g.module_path, index_col=0)
    module_expression = df[modules['modules'] == module]
    response = create_file_response(module_expression.to_csv(), '{}.csv'.format(module))
    return response


@app.route('/projects/<project_id>/trait', methods=['GET', 'POST', 'PUT'])
@project_exists
def trait(project_id):
    if request.method == 'POST':
        trait = request.files.get('trait')
        if trait is None or trait.name == '':
            return jsonify(error='Required fields not supplied.'), 403
        trait.save(g.trait_path)
        sep = request.form.get('delim', ',') or ','
        # Align samples with expression file
        samples = read_first_column(g.expression_path)
        df = pd.read_csv(g.trait_path, index_col=0, sep=sep)
        df = df[df.index.isin(samples)]
        if df.shape[0] != len(samples):
            os.remove(g.trait_path)
            return jsonify(error='Trait data should contain all samples.'), 403
        df.reindex(samples)
        df.to_csv(g.trait_path)
        redis.hset('project:{}'.format(project_id), 'trait', 1)
        return jsonify(df.to_json(orient='split')), 200
    elif request.method == 'GET':
        df = pd.read_csv(g.trait_path, index_col=0)
        if {'true': True, 'false': False}[request.args.get('transpose', 'false')]:
            df = df.T
        return jsonify(df.to_json(orient='split')), 200
    elif request.method == 'PUT':
        df = pd.read_csv(g.trait_path, index_col=0)
        continues_indices = [int(x) for x in request.form['continues'].split(',') if x != '']
        traits = {x: 'C' if i in continues_indices else 'N' for i, x in enumerate(df.columns)}
        redis.hmset('traits:{}'.format(project_id), traits)
        return jsonify({}), 200


@app.route('/projects/<project_id>/traits')
@project_exists
def traits(project_id):
    return jsonify(redis.hgetall('traits:{}'.format(project_id)))


@app.route('/projects/<project_id>/goodsamplesgenes')
@project_exists
def goodsamplesgenes(project_id):
    results = rscripts.goodSamplesGenes(g.expression_path)
    return jsonify(results)


@app.route('/projects/<project_id>/clustersamples', methods=['GET', 'POST'])
@project_exists
def cluster_samples(project_id):
    if request.method == 'GET':
        project = project_from_id(project_id)
        # TODO save to file and use as cache?
        response = {'clusterData': rscripts.hclust(g.expression_path)}
        if project['trait']:
            colors_df = pd.read_csv(g.trait_path, index_col=0)
            response['colors'] = colors_df.replace(np.nan, 'null').to_dict(orient='list')
            response['types'] = redis.hgetall('traits:{}'.format(project_id))
        return jsonify(response)
    elif request.method == 'POST':
        outlier_samples = request.form.getlist('samples[]')
        # Drop in both expression and trait files
        for path in [g.expression_path, g.trait_path]:
            df = pd.read_csv(path, index_col=0)
            df.drop(outlier_samples, axis=0, inplace=True)
            df.to_csv(path)
        n_samples = redis.hget('project:{}'.format(project_id), 'samples')
        redis.hset('project:{}'.format(project_id), 'samples', int(n_samples) - len(outlier_samples))
        return jsonify({})


@app.route('/projects/<project_id>/tresholds', methods=['GET', 'POST'])
@project_exists
def tresholds(project_id):
    project_folder = project_id_to_folder(project_id)
    if request.method == 'GET':
        if os.path.isfile(g.tresholds_path):
            df = pd.read_csv(g.tresholds_path)
        else:
            df = rscripts.soft_tresholds(g.expression_path)
            df.to_csv(g.tresholds_path)
        return jsonify(df.to_dict(orient='list'))
    elif request.method == 'POST':
        power = request.form.get('power')
        if power is None:
            return {'error': 'Please specify a power.'}, 403
        pipe = redis.pipeline()
        pipe.hset('project:{}'.format(project_id), 'power', power)
        pipe.hset('project:{}'.format(project_id), 'step', 2)
        pipe.execute()
        remove_file_if_exists(g.genetree_path)
        remove_file_if_exists(g.module_path)
        return jsonify({})


@app.route('/projects/<project_id>/clustergenes', methods=['GET', 'POST'])
@project_exists
def cluster_genes(project_id):
    if request.method == 'GET':
        if os.path.isfile(g.genetree_path):
            with open(g.genetree_path, 'r') as f:
                cluster_data = json.load(f)
        else:
            power = redis.hget('project:{}'.format(project_id), 'power')
            cluster_data = rscripts.tom(g.expression_path, g.diss_tom_path, int(power))
            with open(g.genetree_path, 'w') as f:
                json.dump(cluster_data, f)
            redis.hset('project:{}'.format(project_id), 'step', 3)
        response = {'clusterData': cluster_data}
        if os.path.isfile(g.module_path):
            response['colors'] = pd.read_csv(g.module_path).to_dict(orient='list')
        return jsonify(response)
    elif request.method == 'POST':
        min_module_size = request.form.get('minModuleSize')
        if min_module_size is None or not is_number(min_module_size):
            return {'error': 'Please specify a (correct) minimum module size.'}, 403
        min_module_size = int(min_module_size)
        if not os.path.isfile(g.genetree_path):
            return {'error': 'Please cluster the genes first.'}, 403
        with open(g.genetree_path, 'r') as f:
            cluster_data = json.load(f)
        r = rscripts.cut_genes(cluster_data, g.diss_tom_path, min_module_size)
        pd.DataFrame(r).to_csv(g.module_path)
        rscripts.generate_eigengenes(g.expression_path, g.module_path).to_csv(g.eigengene_path)
        redis.hset('project:{}'.format(project_id), 'step', 4)
        redis.hset('project:{}'.format(project_id), 'minModuleSize', min_module_size)
        return jsonify(r)


@app.route('/projects/<project_id>/eigengenes', methods=['GET'])
@project_exists
def module_eigengenes(project_id):
    eigengenes = pd.read_csv(g.eigengene_path, index_col=0)
    return jsonify(eigengenes.T.to_dict(orient='split'))


@app.route('/projects/<project_id>/genotype', methods=['GET', 'POST'])
@project_exists
def genotype(project_id):
    project_folder = project_id_to_folder(project_id)
    if request.method == 'POST':
        trait = request.get_json(force=True)['trait']
        groups = pd.read_csv(project_folder + '/trait.csv', index_col=0).loc[:, trait]
        groups = ','.join(groups.apply(str).tolist())
        if groups is None:
            return {'error': 'Please specify the groups.'}, 403
        cmd = ['Rscript', '--no-init-file', 'scripts/genotype.R', project_folder, groups]
        subprocess.check_output(cmd, universal_newlines=True)
        redis.hset('project:{}'.format(project_id), 'groups', groups)
        redis.hset('project:{}'.format(project_id), 'step', 5)
        return jsonify()
    else:
        df = pd.read_csv(g.pvalues_path, index_col=0, keep_default_na=False, na_values=[''])
        response = {}
        response['pvalues'] = df.to_dict(orient='list')
        response['modules'] = df.index.tolist()
        response['eigengenes'] = pd.read_csv(g.eigengene_path, index_col=0).to_dict(orient='list')
        response['groups'] = redis.hget('project:{}'.format(project_id), 'groups').split(',')
        return jsonify(response)


@app.route('/projects/<project_id>/correlate', methods=['GET', 'POST'])
@project_exists
def correlate(project_id):
    project_folder = project_id_to_folder(project_id)
    if request.method == 'POST':
        ordinals = request.get_json(force=True)
        trait_types = redis.hgetall('traits:{}'.format(project_id))
        corrs = rscripts.correlate_traits(g.eigengene_path, g.trait_path, trait_types, ordinals)
        corrs.to_csv(os.path.join(project_folder, 'corrs.csv'))
        return jsonify()
    elif request.method == 'GET':
        corrs = pd.read_csv(os.path.join(project_folder, 'corrs.csv'), index_col=0)
        return jsonify(corrs.to_dict(orient='split'))


@app.route('/export/<name>')
def export(name):
    format_ = request.args.get('format')
    df = pd.read_csv('data/{}/modules.csv'.format(name))
    if format_ == 'A':
        filters = request.args.get('filter')
        if filters:
            df = df[df.module.isin(filters.split(','))]
        if os.path.exists('data/{}/pvalues.csv'.format(name)):
            pvalues = pd.read_csv('data/{}/pvalues.csv'.format(name), index_col=0)
            df['pvalue'] = [pvalues.significance['ME{}'.format(m)] if m != 'grey' else None for m in df.module]
        return create_file_response(df.to_csv(index=False), 'modules.csv')
    elif format_ == 'B':
        module = request.args.get('module')
        if not module:
            return 404
        names = df[df.module == module].name
        return create_file_response('\n'.join(names.tolist()), '{}.txt'.format(module))
    else:
        counter = Counter(df.module)
        data = [{'module': module, 'size': size} for module, size in counter.items()]
        if os.path.exists('data/{}/pvalues.csv'.format(name)):
            pvalues = pd.read_csv('data/{}/pvalues.csv'.format(name), index_col=0)
            for d in data:
                if d['module'] == 'grey':
                    d['pvalue'] = None
                else:
                    d['pvalue'] = pvalues.significance['ME{}'.format(d['module'])]
        return jsonify({'modules': data})


@app.route('/report/<name>')
def report(name):
    working_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(working_path, '../data/{}/report.pdf'.format(name)))
    if not os.path.isfile(path):
        cmd = ['Rscript', '--no-init-file', 'scripts/sessionInfo.R', name]
        subprocess.check_output(cmd, universal_newlines=True)
        cmd = ['python3', 'scripts/create_report.py', name]
        subprocess.check_output(cmd, universal_newlines=True)
    return send_file(path, as_attachment=True)


@app.route('/crosscorrelate')
def crosscorrelate():
    project_ids = request.args.getlist('projects[]')
    projects = [project_from_id(id) for id in project_ids]
    project_folders = [project_id_to_folder(id) for id in project_ids]

    data = []
    eigengenes_dfs = []
    for project, folder in zip(projects, project_folders):
        eigengenes_df = pd.read_csv(os.path.join(folder, 'eigengenes.csv'), index_col=0)
        eigengenes_dfs.append(eigengenes_df)
        cluster_data = rscripts.hclust(eigengenes_df.T)
        data.append({'project': project, 'clusterData': cluster_data, 
            'samples': eigengenes_df.index.tolist()})
    
    # Terminate when no matching samples
    matching_samples = set.intersection(*[set(d['samples']) for d in data])
    if len(matching_samples) == 0:
        return jsonify(error='No matching samples'), 400
    
    # Filter down to matching samples
    for eigengenes_df in eigengenes_dfs:
        drop = ~eigengenes_df.index.isin(matching_samples)
        eigengenes_df.drop(eigengenes_df.index[drop], inplace=True)
    
    # Calculate correlations
    crosscorrs = []
    for i, j in itertools.combinations(range(len(projects)), 2):
        cross_correlations = pd.concat([eigengenes_dfs[z] for z in (i, j)], 
                                       axis=1, keys=['df1', 'df2']).corr('spearman').loc['df1', 'df2']
        for index in cross_correlations.index:
            for column in cross_correlations.columns:
                crosscorr = {}
                crosscorr['source'] = '{}_{}'.format(project_ids[i], index)
                crosscorr['target'] = '{}_{}'.format(project_ids[j], column)
                crosscorr['value'] = cross_correlations.loc[index, column]
                crosscorrs.append(crosscorr)

    return jsonify(matching=list(matching_samples), data=data, crosscorrs=crosscorrs)
