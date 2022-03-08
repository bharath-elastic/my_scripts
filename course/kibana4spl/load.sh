  python load_template.py settings/weblogs_template.json weblogs
  python load_template.py settings/metricbeat_k4spl_template.json metricbeat-k4spl
  python ndjsonindexer.py data/weblogs-01-2022.json weblogs
  python ndjsonindexer.py data/metricbeat-k4spl-01-2022.json metricbeat-k4spl
