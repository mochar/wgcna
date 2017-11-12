import csv
import os
import subprocess
import base64
import json
import itertools
import uuid
from collections import Counter

from flask import Flask, request, jsonify, send_file, make_response, session, g
from flask_session import Session
from flask_cors import CORS
from scipy.stats.stats import pearsonr
from redis import StrictRedis
import pandas as pd

import app.rscripts as rscripts


app = Flask(__name__)
app.config.from_object('config')
redis = StrictRedis(db=app.config['REDIS_DB_DATA'], decode_responses=True,
     charset='utf-8')
app.config['SESSION_REDIS'] =  StrictRedis(db=app.config['REDIS_DB_SESSION'])
Session(app)
CORS(app, supports_credentials=True, expose_headers=['Location'])


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


def user_projects():
    user_id = session.get('id')
    if user_id is None:
        return []
    project_ids = redis.smembers('projects:{}'.format(user_id))
    pipe = redis.pipeline()
    for project_id in project_ids:
        pipe.hgetall('project:{}'.format(project_id))
    return pipe.execute()


def create_user():
    user_id = uuid.uuid4().hex
    session['id'] = user_id
    return user_id


def create_project(user_id, name, description, file):
    project_id = uuid.uuid4().hex
    project = {'name': name, 'description': description, 'id': project_id, 'step': 1}
    project_folder = project_id_to_folder(project_id)
    os.makedirs(project_folder)
    file.save(os.path.join(project_folder, 'expression.csv'))
    redis.sadd('projects:{}'.format(user_id), project_id)
    redis.hmset('project:{}'.format(project_id), project)
    return project


@app.before_request
def setup_request_info():
    project_id = request.view_args.get('project_id')
    if project_id is not None:
        project_folder = project_id_to_folder(project_id)
        g.expression_path = os.path.join(project_folder, 'expression.csv')
        g.sampletree_path = os.path.join(project_folder, 'sampletree.csv')
        g.tresholds_path = os.path.join(project_folder, 'tresholds.csv') 
        g.genetree_path = os.path.join(project_folder, 'genetree.csv')
        g.diss_tom_path = os.path.join(project_folder, 'diss_tom.csv')
        g.module_path = os.path.join(project_folder, 'modules.csv')
        g.eigengene_path = os.path.join(project_folder, 'eigengenes.csv')
        g.pvalues_path = os.path.join(project_folder, 'pvalues.csv')


@app.route('/projects/', methods=['GET', 'POST', 'OPTIONS'])
def projects():
    if request.method == 'GET':
        return jsonify({'projects': user_projects()})
    elif request.method == 'POST':
        file = request.files.get('expression')
        name = request.form.get('name')
        description = request.form.get('description', '')
        if file is None or name is None:
            return {'error': 'File or name not supplied.'}, 403
        user_id = session.get('id')
        if user_id is None:
            user_id = create_user()
        project = create_project(user_id, name, description, file)
        return jsonify({'project': project})


@app.route('/projects/<project_id>/expression', methods=['GET', 'POST', 'PUT'])
def expression(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
    df = pd.read_csv(g.expression_path, index_col=0)
    if request.method == 'GET':
        response = {'colNames': df.columns.tolist(), 'rowNames': df.index.tolist()}
        return jsonify(response)
    elif request.method == 'PUT':
        removed_row_names = [x for x in request.form['row'].split(',') if x != '']
        removed_col_names = [x for x in request.form['col'].split(',') if x != '']
        if request.form['transpose'] == 'true':
            df = df.T
        df.drop(removed_col_names, axis=1, inplace=True)
        df.drop(removed_row_names, axis=0, inplace=True)
        df.to_csv(g.expression_path)
        return jsonify({}), 200


@app.route('/projects/<project_id>/goodsamplesgenes')
def goodsamplesgenes(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
    results = rscripts.goodSamplesGenes(g.expression_path)
    return jsonify(results)


@app.route('/projects/<project_id>/clustersamples', methods=['GET', 'POST'])
def cluster_samples(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
    if request.method == 'GET':
        # TODO save to file and use as cache?
        cluster_data = rscripts.hclust(g.expression_path)
        return jsonify(cluster_data)
    elif request.method == 'POST':
        outlier_samples = request.form.getlist('samples[]')
        df = pd.read_csv(g.expression_path, index_col=0)
        df.drop(outlier_samples, axis=0, inplace=True)
        df.to_csv(g.expression_path)
        return jsonify({})


@app.route('/projects/<project_id>/tresholds', methods=['GET', 'POST'])
def tresholds(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
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
def cluster_genes(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
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


@app.route('/projects/<project_id>/genotype', methods=['GET', 'POST'])
def genotype(project_id):
    if not redis.sismember('projects:{}'.format(session['id']), project_id):
        return {}, 404
    project_folder = project_id_to_folder(project_id)
    if request.method == 'POST':
        groups = request.form.get('groups')
        if groups is None:
            return {'error': 'Please specify the groups.'}, 403
        cmd = ['Rscript', '--no-init-file', 'scripts/genotype.R', project_folder, groups]
        subprocess.check_output(cmd, universal_newlines=True)
        redis.hset('project:{}'.format(project_id), 'groups', groups)
        redis.hset('project:{}'.format(project_id), 'step', 5)
    df = pd.read_csv(g.pvalues_path, index_col=0, keep_default_na=False, na_values=[''])
    response = {}
    response['pvalues'] = df.to_dict(orient='list')
    response['modules'] = df.index.tolist()
    response['eigengenes'] = pd.read_csv(g.eigengene_path, index_col=0).to_dict(orient='list')
    response['groups'] = redis.hget('project:{}'.format(project_id), 'groups').split(',')
    return jsonify(response)


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


@app.route('/correlate')
def correlate():
    names = request.args.getlist('names[]')
    app.logger.debug(names)

    # Read MEs 
    MEs_list = [pd.read_csv('data/{}/MEs.csv'.format(n), index_col=0) for n in names]
    nodes = []
    for i, MEs in enumerate(MEs_list):
        nodes.extend([{'name': c, 'group': names[i]} for c in MEs.columns])
        nodes.append({'name': 'dummy{}'.format(i), 'group': 'dummies'})

    # Reduce MEs to matching samples
    matching_samples = set(MEs_list[0].index.tolist())
    for MEs in MEs_list[1:]:
        matching_samples.intersection_update(MEs.index.tolist())
    app.logger.debug(len(matching_samples))
    for MEs in MEs_list:
        app.logger.debug(MEs.shape)
        MEs.drop(MEs.index[~MEs.index.isin(matching_samples)], inplace=True)
    
    # Calculate correlations
    links = []
    for i, j in itertools.combinations(range(len(names)), 2):
        columns_i = MEs_list[i].columns.tolist()
        columns_j = MEs_list[j].columns.tolist()
        for module_a, module_b in itertools.product(columns_i, columns_j):
            corr, p = pearsonr(MEs_list[i][module_a], MEs_list[j][module_b])
            if p < 0.05 and (corr >= 0.5 or corr <= -0.05):
                link = {'source': {'name': module_a, 'group': names[i]},
                        'target': {'name': module_b, 'group': names[j]},
                        'value': corr}
                links.append(link)

    return jsonify({'nodes': nodes, 'links': links})
