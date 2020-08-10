#!/usr/bin/env python

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from dateutil.parser import parse
from elasticsearch_dsl import Search
from datetime import timedelta
from datetime import datetime
from datetime import date

es = Elasticsearch()
timefield = "@timestamp"
source_prefix = "base-"
target_postfix = f"-7.5.1-{date.today()}"
indices = [
        'auditbeat', 'filebeat', 'packetbeat',
        'winlogbeat', 'auditbeat-bob', 'packetbeat-bob'
        ]
source_indices = [source_prefix + index for index in indices]
target_indices = [index + target_postfix for index in indices]
index_zip = zip(source_indices, target_indices)


def latest_time(index_name, timefield="@timestamp"):
    s = Search(using=es, index=index_name)
    s.aggs.metric('latest', 'max', field=timefield)
    r = s.execute()
    return r.aggregations.latest.value


def get_shift(latest):
    shift = datetime.today() - datetime.fromtimestamp(latest/1000) - timedelta(hours=5)
    return shift


def timeshift(docs, shift):
    for doc in docs:
        doc['_source'][timefield] = datetime.fromisoformat(
                    doc['_source'][timefield]) + shift
        yield doc


def set_index(docs, target_index):
    for doc in docs:
        doc['_index'] = target_index
        yield doc


for source,  target in index_zip:
    shift = get_shift(latest_time(source))
    b = bulk(es, timeshift(set_index(scan(es, index=source), target), shift))
