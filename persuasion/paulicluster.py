from agents import *
import json
from simple_model import Model, Attribute, list_type
import utils

def serialize(model):
    return json.dumps(dict(model))


def deserialize(string):
    return PauliCluster(**json.loads(string.strip("\n")))


def save_cluster(PauliCluster):
    string = serialize(PauliCluster)
    f = open('clusters/json/cluster1.txt', 'w')

    f.write(string)

    f.close()


def append_to_end(PauliCluster):
    string = serialize(PauliCluster)
    with open('clusters/json/cluster1.txt', 'a') as f:
        f.write(string + "\n")


def load_all():
    path = 'clusters/json/cluster1.txt'
    clusters = []
    with open(path, 'r') as f:
        for line in f:
            clusters.append(deserialize(line))
    return clusters


def load_cluster(file_path):
    f = open(file_path)

    string = f.read()
    cluster = deserialize(string)

    f.close()
    return cluster


def parse_rect(string):
    data = string.split(",")
    return utils.get_rect(*data)


def move_cluster(cluster, x, y):
    for position in cluster.positions:
        position[0] += x
        position[1] += y


class PauliCluster(Model):
    number = Attribute(int)
    attitude = Attribute(int, fallback=0)
    positions = Attribute(list_type(lambda l: list(map(int, l))))
