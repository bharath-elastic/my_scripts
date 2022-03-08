# coding: utf-8
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from dateutil.parser import parse
from elasticsearch_dsl import Search
from datetime import timedelta
from datetime import datetime
from dateutil.parser import parse as dateparse
from datetime import date
from argparse import ArgumentParser
from config import esconfig

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('index', help='time series index name to shift')
    parser.add_argument('target', help='target index name for shifted docs')
    parser.add_argument('-t', '--time-field', default='@timestamp',
            help='time field (default=@timestamp)')
    args = parser.parse_args()
    return args

def latest_time(index_name):
    s = Search(using=es, index=index_name)
    s.aggs.metric('latest', 'max', field=args.time_field)
    r = s.execute()
    return r.aggregations.latest.value


def get_shift(latest):
    shift = datetime.today() - datetime.fromtimestamp(latest/1000) - timedelta(hours=5)
    return shift


def timeshift(docs, shift):
    for doc in docs:
        doc['_source'][args.time_field] = dateparse(
                    doc['_source'][args.time_field]) + shift
        yield doc


def set_index(docs, target_index):
    for doc in docs:
        doc['_index'] = target_index
        yield doc


cloud_id = esconfig['cloud_id']
api_key = esconfig['api_key']
es = Elasticsearch(cloud_id=cloud_id, api_key=api_key)
args = parse_args()
shift = get_shift(latest_time(args.index))
b = bulk(es, timeshift(set_index(scan(es, index=args.index), args.target), shift))
