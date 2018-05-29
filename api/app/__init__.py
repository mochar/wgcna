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
from flask_cors import CORS
from scipy.stats.stats import pearsonr
from redis import StrictRedis
import pandas as pd

import app.rscripts as rscripts
try:
    from scripts.set_analysis import Set_analysis
except:
    print('Annotation script not found, starting without annotation support.')


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


def process_project(project):
    project['trait'] = bool(int(project['trait']))
    project['preprocessed'] = bool(int(project['preprocessed']))
    project['traits'] = redis.hgetall('traits:{}'.format(project['id']))
    return project


def project_from_id(project_id):
    project = redis.hgetall('project:{}'.format(project_id))
    return process_project(project)


def user_projects():
    if 'id' not in session:
        return []
    user_id = session['id']
    project_ids = redis.smembers('projects:{}'.format(user_id))
    pipe = redis.pipeline()
    for project_id in project_ids:
        pipe.hgetall('project:{}'.format(project_id))
    projects = pipe.execute()
    return [process_project(p) for p in projects]


def create_user():
    user_id = uuid.uuid4().hex
    session['id'] = user_id
    return user_id


def create_project(user_id, name, description, omic, expression, trait=None):
    project_id = uuid.uuid4().hex
    project_folder = project_id_to_folder(project_id)
    os.makedirs(project_folder)
    expression.save(os.path.join(project_folder, 'expression.csv'))
    if trait is not None:
        trait.save(os.path.join(project_folder, 'trait.csv'))
    redis.sadd('projects:{}'.format(user_id), project_id)

    df = pd.read_csv(os.path.join(project_folder, 'expression.csv'))
    project = {'name': name, 'description': description, 'id': project_id, 'step': 1,
        'omic': omic, 'trait': 0 if trait is None else 1, 'preprocessed': 0,
        'genes': len(df.columns), 'samples': len(df.index)}
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
    if 'id' in session:
        g.user_id = session.get('id')


def project_exists(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            abort(404)
            return
        session_id = session['id']
        if not redis.sismember('projects:{}'.format(session_id), g.project_id):
            abort(404)
            return
        return f(*args, **kwargs)
    return decorated_function


@app.route('/projects/', methods=['GET', 'POST', 'OPTIONS'])
def projects():
    if request.method == 'GET':
        return jsonify({'projects': user_projects()})
    elif request.method == 'POST':
        expression = request.files.get('expression')
        trait = request.files.get('trait')
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        omic = request.form.get('omic')
        if expression.filename == '' or name == '':
            return jsonify(error='Required fields not supplied.'), 403
        user_id = session.get('id') if 'id' in session else create_user()
        project = create_project(user_id, name, description, omic, expression,
            trait=None if trait.filename == '' else trait)
        return jsonify({'project': project})


@app.route('/projects/<project_id>', methods=['GET', 'DELETE'])
@project_exists
def project(project_id):
    if request.method == 'GET':
        project = project_from_id(project_id)
        return jsonify({'project': project})
    elif request.method == 'DELETE':
        delete_project(g.user_id, project_id)
    return jsonify({})


@app.route('/projects/<project_id>/expression', methods=['GET', 'POST', 'PUT'])
@project_exists
def expression(project_id):
    df = pd.read_csv(g.expression_path, index_col=0)
    if request.method == 'GET':
        response = {'colNames': df.columns.tolist(), 'rowNames': df.index.tolist()}
        return jsonify(response)
    elif request.method == 'PUT':
        if request.form['transpose'] == 'true':
            df = df.T
            n_genes = redis.hget('project:{}'.format(project_id), 'genes')
            n_samples = redis.hget('project:{}'.format(project_id), 'samples')
            redis.hset('project:{}'.format(project_id), 'genes', n_samples)
            redis.hset('project:{}'.format(project_id), 'samples', n_genes)
        df.to_csv(g.expression_path)
        return jsonify({}), 200


@app.route('/projects/<project_id>/trait', methods=['GET', 'POST', 'PUT'])
@project_exists
def trait(project_id):
    df = pd.read_csv(g.trait_path, index_col=0)
    if request.method == 'GET':
        if {'true': True, 'false': False}[request.args.get('transpose', 'false')]:
            df = df.T
        return jsonify(df.to_dict(orient='split'))
    elif request.method == 'PUT':
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
            response['colors'] = colors_df.to_dict(orient='list')
            response['types'] = redis.hgetall('traits:{}'.format(project_id))
        return jsonify(response)
    elif request.method == 'POST':
        outlier_samples = request.form.getlist('samples[]')
        df = pd.read_csv(g.expression_path, index_col=0)
        df.drop(outlier_samples, axis=0, inplace=True)
        df.to_csv(g.expression_path)
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


@app.route('/projects/<project_id>/annotate', methods=['GET'])
@project_exists
def annotate(project_id):
    id_type = request.args.get('id_type')
    annotation_type = request.args.get('annotation_type')
    recalculate = request.args.get('recalculate')

    if recalculate == "true":
        project_folder = project_id_to_folder(project_id)
        set_analysis = Set_analysis(annotation_type)
        annotations = set_analysis.annotate(project_folder, id_type)

        arguments = {'annotation_type':annotation_type, 'id_type':id_type}
        # Store in project data??
        #return jsonify({'annotations' : annotations, 'arguments' : arguments})
        return jsonify(annotations)
    else:
        try:
            return jsonify(json.load(open(g.annotation_path, 'r')))
        except:
            return jsonify({})

@app.route('/integrate', methods=['GET'])
def integrate():
    print(request.args.get('projectId1'))
    print(request.args.get('projectId2'))
    print(request.args.get('id_type1'))
    print(request.args.get('id_type2'))
    print(request.args.get('annotation_type'))

    id_type1 = request.args.get('id_type1')
    id_type2 = request.args.get('id_type2')

    project_folder1 = project_id_to_folder(request.args.get('projectId1'))
    project_folder2 = project_id_to_folder(request.args.get('projectId2'))

    print(project_folder1)
    print(project_folder2)

    set_analysis = Set_analysis(request.args.get('annotation_type'))
    overlap_list = set_analysis.make_real_matrix(project_folder1, project_folder2, id_type1, id_type2)

    return jsonify(overlap_list)


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


"""
@app.route('/crosscorrelate')
def crosscorrelate():
    project_ids = request.args.getlist('projects[]')
    project_folders = [project_id_to_folder(id) for id in project_ids]
    project_names = [project_from_id(id)['name'] for id in project_ids]

    # Read MEs 
    MEs_list = [pd.read_csv(os.path.join(pf, 'eigengenes.csv'), index_col=0) 
                for pf in project_folders]
    nodes = []
    for i, MEs in enumerate(MEs_list):
        nodes.extend([{'name': c, 'group': project_names[i]} for c in MEs.columns])
        nodes.append({'name': 'dummy{}'.format(i), 'group': 'dummies'})

    # Reduce MEs to matching samples
    matching_samples = set(MEs_list[0].index.tolist())
    for MEs in MEs_list[1:]:
        matching_samples.intersection_update(MEs.index.tolist())

    # Terminate when no matching samples
    if len(matching_samples) == 0:
        return jsonify(nodes=[], links=[])

    for MEs in MEs_list:
        MEs.drop(MEs.index[~MEs.index.isin(matching_samples)], inplace=True)
    
    # Calculate correlations
    links = []
    for i, j in itertools.combinations(range(len(project_ids)), 2):
        columns_i = MEs_list[i].columns.tolist()
        columns_j = MEs_list[j].columns.tolist()
        for module_a, module_b in itertools.product(columns_i, columns_j):
            corr, p = pearsonr(MEs_list[i][module_a], MEs_list[j][module_b])
            # if p < 0.05 and (corr >= 0.5 or corr <= -0.5):
            link = {'source': {'name': module_a, 'group': project_names[i]},
                    'target': {'name': module_b, 'group': project_names[j]},
                    'value': corr}
            links.append(link)

    return jsonify({'nodes': nodes, 'links': links})
    return jsonify(img=base64_encode_image('/home/mochar/work/duchenne/kristina/circle_compressed.png'))
"""


@app.route('/crosscorrelate')
def crosscorrelate():
    project_ids = request.args.getlist('projects[]')
    projects = [project_from_id(id) for id in project_ids]
    project_folders = [project_id_to_folder(id) for id in project_ids]

    data = []
    matching_samples = set()
    for project, folder in zip(projects, project_folders):
        eigengenes_df = pd.read_csv(os.path.join(folder, 'eigengenes.csv'), index_col=0).T
        cluster_data = rscripts.hclust(eigengenes_df)
        data.append({'project': project, 'clusterData': cluster_data, 
            'samples': eigengenes_df.columns.tolist()})
        matching_samples.update(set(data[-1]['samples']))

    return jsonify(matching=list(matching_samples), data=data)
