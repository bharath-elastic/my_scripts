# migrate.py
# migrate list of elasticsearch index between clusters

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan

#dest = "ec2-54-93-227-165.eu-central-1.compute.amazonaws.com"
src = "ec2-18-195-119-173.eu-central-1.compute.amazonaws.com"
es1 = Elasticsearch(hosts=[src])
es2 = Elasticsearch()
timefield = "@timestamp"
source_prefix = "base-"
indices = [
        'auditbeat', 'filebeat', 'packetbeat',
        'winlogbeat', 'auditbeat-bob', 'packetbeat-bob'
        ]
source_indices = [source_prefix + index for index in indices]
target_indices = source_indices
index_zip = zip(source_indices, target_indices)


for source,  target in index_zip:
    b = bulk(es2, scan(es1, index=source))
