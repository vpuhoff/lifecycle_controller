import consul
from time import sleep
from tqdm import tqdm
from prometheus_client import start_http_server, Summary

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('consul', type=str, help='consul <host:port>')
args = parser.parse_args()

consul_host = args.consul.split(':')[0]
consul_port = int(args.consul.split(':')[1])
EPOCH_TIME = Summary('epoch_time', 'Time spent to change epoch')

consul_client = consul.Consul(consul_host, consul_port)
print(f'Consul connected to: {args.consul}')

def load_current_epoch(consul_client):
    epoch_index, resp = consul_client.kv.get('epoch')
    if not resp:
        resp = {'Value': 0}
    epoch = int(resp['Value'])
    return epoch

@EPOCH_TIME.time()
def update_epoch(c, epoch):
    sleep(0.01)
    epoch = load_current_epoch(c)
    epoch += 1
    c.kv.put('epoch', str(epoch))
    return epoch


epoch = load_current_epoch(consul_client)
start_http_server(80)

with tqdm(initial=epoch) as progress_bar:
    while True:
        epoch = update_epoch(consul_client, epoch)
        progress_bar.update(1)
        progress_bar.desc = str(epoch)

