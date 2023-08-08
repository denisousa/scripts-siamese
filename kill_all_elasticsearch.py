import os

def kill_all_clusters():
    for port in range(9000,9026):
        command_stop = f'sudo kill $(sudo lsof -t -i :{port})'
        os.system(command_stop)
