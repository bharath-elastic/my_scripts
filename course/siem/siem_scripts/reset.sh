curl -XDELETE "http://localhost:9200/*2020*" > /dev/null 2>&1
./replay.py
