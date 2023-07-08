import os

for ngram_i, port in zip(range(4,24), range(9200,9221)):
    command_stop = f'sudo kill $(sudo lsof -t -i :{port})'
    os.system(command_stop)