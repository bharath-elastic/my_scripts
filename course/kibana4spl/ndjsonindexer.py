# load ndjson data into elasticsearch
import argparse, json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import esconfig

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='name of the ndjson file')
    parser.add_argument('index', help='elasticsearch index name')
    args = parser.parse_args()
    return args

def docs(file_name):
    with open(file_name, 'r') as f:
        for doc in f:
            yield json.loads(doc)

def make_actions(docs, index_name):
    for doc in docs:
        action =  { "_index": index_name }
        action["_source"] = doc
        yield action

def get_credentials():
    user = input('Username: ')
    if user:
        pwd = getpass.getpass()
        return (user, pwd)
    else:
        return(None,None)

args = parse_args()
cloud_id = esconfig['cloud_id']
api_key = esconfig['api_key']
es = Elasticsearch(cloud_id=cloud_id, api_key=api_key)
actions = make_actions(docs(args.file), args.index)
b = bulk(es, actions)
