#!/usr/bin/env python
# bro_shift.py
# shift timestamp for bro logs
import os
import json
from datetime import timedelta
from datetime import datetime

def timeshift(infile, outfile):
    with open(infile, 'r') as inf:
        with open(outfile, 'w') as outf:
            for line in inf:
                doc = json.loads(line)
                ts = datetime.fromtimestamp(doc['ts'])
                shift = datetime.now() - ts
                doc['ts'] = (ts + shift).timestamp()
                outf.write(json.dumps(doc))
                outf.write('\n')


file_path = '/home/ubuntu/scripts/data'
infile = os.path.join(file_path, 'base_http.log')
outfile = os.path.join(file_path, 'http.log')
timeshift(infile,outfile)
