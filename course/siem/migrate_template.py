# migrate list of elasticsearch templates between clusters

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

#dest = "ec2-54-93-227-165.eu-central-1.compute.amazonaws.com"
src = "ec2-18-195-119-173.eu-central-1.compute.amazonaws.com"
es1 = Elasticsearch(hosts=[src])
ic1 = IndicesClient(es1)
es2 = Elasticsearch()
ic2 = IndicesClient(es2)

indices = [
        'auditbeat', 'filebeat', 'packetbeat',
        'winlogbeat'
        ]

suffix = '-7.5.0'
templates = [index + suffix for index in indices]

for template in templates:
    ic2.put_template(name=template, body=ic1.get_template(name=template)[template])
