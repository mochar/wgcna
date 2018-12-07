from flask_socketio import SocketIO
from redis import StrictRedis
import pandas as pd

from config import REDIS_DB_DATA
import app.rscripts as rscripts


socketio = SocketIO(message_queue='redis://')
redis = StrictRedis(db=REDIS_DB_DATA, decode_responses=True,
     charset='utf-8')

def process_expression(expression_path, sep, project_id, sid):
    df = pd.read_csv(expression_path, index_col=0, sep=sep)
    redis.hset('project:{}'.format(project_id), 'genes', len(df.columns))
    redis.hset('project:{}'.format(project_id), 'samples', len(df.index))
    redis.hset('project:{}'.format(project_id), 'processed', 1)
    response = {'features': len(df.columns), 'samples': len(df.index)}

    results = rscripts.goodSamplesGenes(expression_path)

    socketio.emit('expressionDone', {**response, **results}, room=sid)


def calculate_tresholds(expression_path, tresholds_path, sid):
    df = rscripts.soft_tresholds(expression_path)
    df.to_csv(tresholds_path)
    socketio.emit('tresholdDone', df.to_dict(orient='list'), room=sid)
