import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd

pandas2ri.activate()
WGCNA = importr('WGCNA')


def goodSamplesGenes(expression_path):
    df = pd.read_csv(expression_path, index_col=0)
    gsg = WGCNA.goodSamplesGenes(df, verbose=0)
    badGenes = df.columns[[not x for x in gsg[0]]].tolist()
    badSamples = df.index[[not x for x in gsg[1]]].tolist()
    df.drop(badGenes, axis=1, inplace=True)
    df.drop(badSamples, axis=0, inplace=True)
    df.to_csv(expression_path)
    return {'allOK': gsg[2][0], 'badSamples': badSamples, 'badGenes': badGenes}


def hclust(expression_path):
    df = pd.read_csv(expression_path, index_col=0)
    tree = robjects.r.hclust(robjects.r.dist(df), method = 'average')
    merge = pandas2ri.ri2py(tree[0]).tolist()
    # merge = [[x+1 if x<0 else x-1, y+1 if y<0 else y-1] for x, y in merge]
    height = list(tree[1])
    labels = df.index.tolist()
    ordered = df.index[pandas2ri.ri2py(tree[2]) - 1].tolist()
    return {'merge': merge, 'height': height, 'labels': labels, 
            'ordered': ordered}
