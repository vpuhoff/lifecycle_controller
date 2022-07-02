import consul
from time import sleep
from tqdm import tqdm
from prometheus_client import start_http_server, Summary

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('consul_service', type=str, help='consul <host:port>')
args = parser.parse_args()

consul_host = args.consul_service.split(':')[0]
consul_port = int(args.consul_service.split(':')[1])
EPOCH_TIME = Summary('epoch_time', 'Time spent to change epoch')

consul_client = consul.Consul(consul_host, consul_port)


def load_current_epoch(consul_client):
    epoch_index, resp = consul_client.kv.get('epoch')
    if not resp:
        resp = {'Value': 0}
    epoch = int(resp['Value'])
    return epoch


@EPOCH_TIME.time()
def update_epoch(c, epoch):
    sleep(0.05)
    epoch += 1
    c.kv.put('epoch', str(epoch))


epoch = load_current_epoch(consul_client)
start_http_server(80)

with tqdm(initial=epoch) as progress_bar:
    while True:
        update_epoch(consul_client, epoch)
        progress_bar.update(1)
