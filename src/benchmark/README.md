HOW TO RUN BENCHMARK
--------------------

0. all commands from benchmark dir

1. build:
    
    $ docker compose -f docker-compose-bench.yml build

2. run compose:
    
    $  docker compose -f docker-compose-bench.yml up

3. setup python path:
   
   $ export PYTHONPATH=<project_dir>/relaction_fga/src

3. generate data (adjust MAGNITUDE env in gen_data.py):
    
    $ python benchmark/gen_data.py
   
4. copy graph store_id from gen_data.py console result,
   and paste it to test_graph.py

5. run test graph:
   
   $ python benchmark/check_graph.py

6. run test openfga:

   $ python benchmark/check_openfga.py