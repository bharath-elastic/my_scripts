#!/usr/bin/env python
# digthis.py
# make dns queries

import subprocess
import time

urls = ['apple.com', 'google.com',
        'cnn.com', 'netflix.com',
        'bbc.co.uk', 'facebook.com',
        'elastic.co', 'github.com',
        'wikipedia.org', 'stackoverflow.com']

while True:
    for url in urls:
        subprocess.check_output(['dig', url])

