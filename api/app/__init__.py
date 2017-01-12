import csv
import os
import subprocess
import base64
import json

from flask import Flask, request, jsonify, send_file
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
    if request.method == 'GET':
        response = {}
        with open('data/{}/expression.csv'.format(name), 'r') as f:
            reader = csv.DictReader(f)
            response['colNames'] = reader.fieldnames[1:]
            response['rowNames'] = [row[''] for row in reader]
        return jsonify(response)
    elif request.method == 'PUT':
        removed_row_names = [x for x in request.form['row'].split(',') if x != '']
        removed_col_names = [x for x in request.form['col'].split(',') if x != '']
        df = pd.read_csv('data/{}/expression.csv'.format(name), index_col=0)
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
    response = {'base64': base64_encode_image('data/{}/tom-colors.png'.format(name))}
    update_info(name, 'step', 4)
    return jsonify(response)


@app.route('/genotype/<name>', methods=['GET', 'POST'])
def genotype(name):
    if request.method == 'POST':
        groups = request.form['groups']
        cmd = ['Rscript', '--no-init-file', 'scripts/genotype.R', name, groups]
        subprocess.check_output(cmd, universal_newlines=True)
        update_info(name, 'step', 5)
    df = pd.read_csv('data/{}/pvalues.csv'.format(name), index_col=0)
    response = {}
    response['pvalues'] = df.to_dict(orient='list')
    response['modules'] = df.index.tolist()
    return jsonify(response)
