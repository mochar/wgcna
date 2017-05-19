from io import BytesIO
import os
import base64
import json
import sys

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML 
import matplotlib.pyplot as plt
import pandas as pd


#dataset = 'Lip W12'
dataset = sys.argv[1]
working_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(working_path, '../data/'))
style_path = os.path.join(data_path, 'report_style.css')
dataset_path = os.path.join(data_path, dataset)
pdf_path = os.path.join(dataset_path, 'report.pdf')


def prepend_base64(data):
    return 'data:image/png;base64,{}'.format(data)


def base64_encode_image(image):
    with open(image, 'rb') as f:
        encoded = base64.b64encode(f.read())
    return encoded.decode()


def get_power():
    with open(os.path.join(dataset_path, 'info.json'), 'r') as f:
        return int(json.load(f)['power'])


def generate_tresholds_plot(df, soft_power):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[8,6])
    df.plot(kind='scatter', x='powers', y='scaleindep', ax=axes[0], c='white', marker='x')
    df.plot(kind='scatter', x='powers', y='meank', ax=axes[1], c='white', marker='x')

    for a in axes:
        a.set_ylabel('')
        a.xaxis.set_label_position('top')
    axes[0].set_xlabel('Scale independence', fontsize=19)
    axes[1].set_xlabel('Mean connectivity', fontsize=19)

    for row in df.itertuples():
        _, power, scaleindep, meank = row
        color = 'red' if power == soft_power else 'black'
        axes[0].annotate(power, (power, scaleindep), color=color)
        axes[1].annotate(power, (power, meank), color=color)

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0) 
    return prepend_base64(base64.b64encode(buf.getvalue()).decode())


def write(template_vars):
    env = Environment(loader=FileSystemLoader(data_path))
    template = env.get_template('report_template.html')
    html = template.render(template_vars)
    # with open('report.html', 'w') as f:
    #     f.write(html)
    HTML(string=html).write_pdf(pdf_path, stylesheets=[style_path])


if __name__ == '__main__':
    template_vars = dict()

    # Dataset information
    expression = pd.read_csv(os.path.join(dataset_path, 'expression.csv'), index_col=0)
    sample_path = os.path.join(dataset_path, 'sample-clustering.png')
    template_vars['name'] = dataset
    template_vars['sample_count'] = len(expression.index)
    template_vars['probe_count'] = len(expression.columns)
    template_vars['sample_img'] = prepend_base64(base64_encode_image(sample_path))

    # Tresholds
    power = get_power()
    df = pd.read_csv(os.path.join(dataset_path, 'tresholds.csv'))
    template_vars['tresholds_img'] = generate_tresholds_plot(df, power)
    df.columns = ['Power', 'Scale independence', 'Mean connectivity']
    template_vars['tresholds_table'] = df.to_html()
    template_vars['power'] = power

    # Modules
    pvalues = pd.read_csv(os.path.join(dataset_path, 'pvalues.csv'), index_col=0)
    pvalues.index = [x.lstrip('ME') for x in pvalues.index]
    tom_path = os.path.join(dataset_path, 'tom-colors.png')
    template_vars['tom_img'] = prepend_base64(base64_encode_image(tom_path))
    template_vars['pvalues'] = pvalues
    template_vars['combinations'] = [x for x in pvalues.columns if x != 'significance']

    # Session info
    with open(os.path.join(dataset_path, 'sessionInfo.txt'), 'r') as f:
        template_vars['session_info'] = '<br>'.join(f.readlines())
        
    write(template_vars)