import csv
import os
import subprocess
import base64
import json
from collections import Counter

from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
app.config.from_object('config')
CORS(app, supports_credentials=True, expose_headers=['Location'])


def base64_encode_image(image):
    with open(image, 'rb') as f:
        encoded = base64.b64encode(f.read())
    return encoded.decode()


def read_info(name):
    with open('data/{}/info.json'.format(name), 'r') as f:
        return json.load(f)


def write_info(name, info):
    with open('data/{}/info.json'.format(name), 'w') as f:
        return json.dump(info, f)


def update_info(name, key, value):
    info = read_info(name)
    info[key] = value
    write_info(name, info)


def create_file_response(contents, filename):
    response = make_response(contents)
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


@app.route('/expression/', methods=['GET', 'POST'])
def expression_list():
    if request.method == 'GET':
        names = [name for name in os.listdir('data/') 
                 if os.path.isdir(os.path.join('data', name))]
        return jsonify({'names': names})
    elif request.method == 'POST':
        file = request.files['expression']
        name = request.form['name']
        os.makedirs('data/{}'.format(name))
        write_info(name, {'step': 1})
        file.save('data/{}/expression.csv'.format(name))
        return jsonify({'name': name})


@app.route('/expression/<name>', methods=['GET', 'PUT'])
def expression(name):
    df = pd.read_csv('data/{}/expression.csv'.format(name), index_col=0)
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
        df.to_csv('data/{}/expression.csv'.format(name))
        return jsonify({}), 200


@app.route('/info/<name>')
def info(name):
    info = read_info(name)
    return jsonify(info)


@app.route('/traits', methods=['GET', 'POST'])
def traits():
    if request.method == 'POST':
        file = request.files['traits']
        file.save('data/traits.csv')
        return jsonify({}), 200
    elif request.method == 'GET':
        response = {}
        return jsonify(response)


@app.route('/goodgenes/<name>')
def goodgenes(name):
    cmd = ['Rscript', '--no-init-file', 'scripts/goodGenes.R', name]
    output = subprocess.check_output(cmd, universal_newlines=True)
    output = output.split('\n\n\n')[-1] # Remove WGCNA message
    output = output.split('\t')
    response = {
        'allOK': output[0] == 'TRUE', 
        'badSamples': [x for x in output[1].split(',') if x != ''], 
        'badGenes': [x for x in output[2].split(',') if x != '']
    }
    return jsonify(response)


@app.route('/cluster/<name>/')
@app.route('/cluster/<name>/<height>')
def cluster(name, height='0'):
    path = 'data/{}'.format(name)
    if not os.path.isfile('{}/cluster.RData'.format(path)):
        cmd = ['Rscript', 'scripts/cluster.R', name]
        subprocess.check_output(cmd, universal_newlines=True)
    cmd = ['Rscript', 'scripts/dendrogram.R', name, height]
    subprocess.check_output(cmd, universal_newlines=True)
    return jsonify({'base64': base64_encode_image('{}/sample-clustering.png'.format(path))})


@app.route('/cut/<name>/<height>')
def cut(name, height='0'):
    path = 'data/{}'.format(name)
    cmd = ['Rscript', '--no-init-file', 'scripts/cut.R', name, height]
    subprocess.check_output(cmd, universal_newlines=True)
    os.remove('{}/cluster.RData'.format(path))
    os.remove('{}/sample-clustering.png'.format(path))
    return jsonify({})


@app.route('/tresholds/<name>', methods=['GET', 'POST'])
def tresholds(name):
    if request.method == 'GET':
        if not os.path.isfile('data/{}/tresholds.csv'.format(name)):
            cmd = ['Rscript', '--no-init-file', 'scripts/softTreshold.R', name]
            subprocess.check_output(cmd, universal_newlines=True)
        df = pd.read_csv('data/{}/tresholds.csv'.format(name))
        return jsonify(df.to_dict(orient='list'))
    elif request.method == 'POST':
        update_info(name, 'power', request.form['power'])
        update_info(name, 'step', 2)
        return jsonify({})


@app.route('/clustergenes/<name>')
def clustergenes(name):
    info = read_info(name)
    if info['step'] < 3:
        cmd = ['Rscript', '--no-init-file', 'scripts/clusterGenes.R', name, info['power']]
        subprocess.check_output(cmd, universal_newlines=True)
    response = {'base64': base64_encode_image('data/{}/tom.png'.format(name))}
    update_info(name, 'step', 3)
    return jsonify(response)


@app.route('/cutgenes/<name>', methods=['GET', 'POST'])
def cutgenes(name):
    if request.method == 'POST':
        min_module_size = request.form['minModuleSize']
        deep_split = request.form['deepSplit']
        cmd = ['Rscript', '--no-init-file', 'scripts/cutGenes.R', name, min_module_size, deep_split]
        subprocess.check_output(cmd, universal_newlines=True)
        update_info(name, 'step', 4)
        update_info(name, 'min_module_size', min_module_size)
        update_info(name, 'deep_split', deep_split)
    response = {'base64': base64_encode_image('data/{}/tom-colors.png'.format(name))}
    return jsonify(response)


@app.route('/genotype/<name>', methods=['GET', 'POST'])
def genotype(name):
    if request.method == 'POST':
        groups = request.form['groups']
        cmd = ['Rscript', '--no-init-file', 'scripts/genotype.R', name, groups]
        subprocess.check_output(cmd, universal_newlines=True)
        update_info(name, 'step', 5)
        update_info(name, 'groups', groups)
    df = pd.read_csv('data/{}/pvalues.csv'.format(name), index_col=0, keep_default_na=False, na_values=[''])
    response = {}
    response['pvalues'] = df.to_dict(orient='list')
    response['modules'] = df.index.tolist()
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


@app.route('/module-lists/', methods=['GET', 'POST'])
def module_list():
    """
    GET: returns a list of names.
    POST: receives a name and a csv file with modules. A folder with the
    received name as name is made. The received csv file is then saved to
    this folder.
    """
    if request.method == 'GET':
        names = [name for name in os.listdir('annotatedata/')
                 if os.path.isdir(os.path.join('annotatedata', name))]
        return jsonify({'names': names})
    elif request.method == 'POST':
        file = request.files['modules']
        name = request.form['name']
        os.makedirs('annotatedata/{}'.format(name))
        #write_info(name, {'step': 1})
        file.save('annotatedata/{}/modules.csv'.format(name))
        return jsonify({'name': name})


@app.route('/moduletree/<name>')
def moduletree(name):
    """
    Returns a dictionary with all modules in the modules file. Every
    module has the number of members and a pvalue associated with them.
    """
    moduletree = dict()
    with open('annotatedata/'+name+'/modules.csv', 'r') as f:
        next(f)
        for line in f:
            modulemember = line.split(',')[0]
            modulename = line.split(',')[1]
            pvalue = line.split(',')[2].rstrip('\n')
            pvalue = '%s' % float('%.2g' % float(pvalue))

            if modulename not in moduletree:
                moduletree[modulename] = {'members':0, 'pvalue':pvalue}
            moduletree[modulename]["members"] += 1
    return jsonify(moduletree)


@app.route('/moduletree/<name>/<modulename>')
def modulemembernames(name, modulename):
    """
    Returns a list of names of module members that are members of the
    module that is received as argument.
    """
    modulememberlist = list()
    with open ('annotatedata/'+name+'/modules.csv','r') as f:
        next(f)
        for line in f:
            modulenamecsv = line.split(',')[1]
            modulemember = line.split(',')[0]
            if modulename == modulenamecsv:
                modulememberlist.append(modulemember)
    return jsonify(modulememberlist)
