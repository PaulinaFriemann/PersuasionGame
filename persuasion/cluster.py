import json

import movements

import utils
import agents
import math
import random

def serialize(model):
    attributes = dir(model)
    att_dict = {}
    for attribute in attributes:
        if "__" not in attribute:
            field = (getattr(model, attribute))
            if type(field) == unicode:
                field = field.encode("ascii", "ignore")
            if attribute == "movement":
                #print field
                field = str(field).split(" ")[1]
                #print "lala", attribute, field
            if attribute not in ["members", "add_cluster", "update_happiness", "regroup_wait",
                                 "regroup", "update", "add_member", "remove_member", "save_cluster", "calc_start"]:
                #print attribute, type(attribute)
                att_dict[attribute] = field


    return json.dumps(att_dict)


def deserialize(string):
    #print string
    return Cluster(**json.loads(string.strip("\n")))


def save_all(clusters, file_path = 'clusters/json/all clusters.txt'):
    with open(file_path, 'w') as f:
        for cluster in clusters:
            f.write(serialize(cluster)+"\n")

def append_to_end(Cluster,file_path = 'clusters/json/all clusters.txt'):
    string = serialize(Cluster)
    with open(file_path, 'a') as f:
        f.write(string + "\n")


def load_all(path = 'clusters/json/all clusters.txt'):
    clusters = []
    with open(path, 'r') as f:
        for line in f:

            cluster = deserialize(line)
            cluster.add_cluster(movement=cluster.movement)
            clusters.append(cluster)
    return clusters

def load_cluster(file_path = 'clusters/json/cluster 0.txt'):
    f = open(file_path)

    string = f.read()
    cluster = deserialize(string)

    f.close()
    return cluster


def parse_rect(string):
    data = string.split(",")
    return utils.get_rect(*data)


def move_cluster(cluster, x, y):
    for position in cluster.starting_positions:
        position[0] += x
        position[1] += y


def change_attitude(cluster, attitude):
    cluster.attitude = attitude


def line((begin_x, begin_y), space, angle, n_agents):
    return [
        ((begin_x + (math.floor(math.sin(math.radians(angle)) * space * i))),
         begin_y + (math.floor(math.sin(math.radians(90 - angle)) * space * i)))
            for i in range(n_agents)]

def big_circle((center_x, center_y), personal_space, n_agents):
    circle_positions = [
        (center_x + math.floor(math.sin(math.radians(360*i/n_agents)) * personal_space),
        center_y + math.floor(math.sin(math.radians(90 - (360 * i / n_agents))) * personal_space))
        for i in range(n_agents)
    ]

    circle_positions.append((center_x,center_y))

    return circle_positions


def evenly_distributed((center_x, center_y), personal_space, n_agents):
    n_circles = int(math.ceil(float((n_agents - 1)) / 6))

    circle_positions = [(center_x,center_y)]
    agents_left = n_agents - 1

    for circle in range(1,n_circles + 1):
        if agents_left >= 6:
            phi = random.randint(0,59)

            x = center_x + math.floor(math.sin(math.radians(phi)) * personal_space * circle)
            y = center_y + math.floor(math.sin(math.radians(90 - phi)) * personal_space * circle)
            circle_positions.append((x,y))

            for j in range(5):
                phi += 60
                x = center_x + math.floor(math.sin(math.radians(phi)) * (personal_space * circle))
                y = center_y + math.floor(math.sin(math.radians(90 - phi)) * (personal_space * circle))
                circle_positions.append((x, y))
            agents_left -= 6
        else:
            increment = (360/agents_left)
            phi = random.randint(0, increment - 1)

            x = center_x + math.floor(math.sin(math.radians(phi)) * personal_space * circle)
            y = center_y + math.floor(math.sin(math.radians(90 - phi)) * personal_space * circle)
            circle_positions.append((x, y))

            for j in range(1,agents_left):
                phi += increment
                x = center_x + math.floor(math.sin(math.radians(phi)) * personal_space * circle)
                y = center_y + math.floor(math.sin(math.radians(90 - phi)) * personal_space * circle)
                circle_positions.append((x, y))
        return circle_positions


class Cluster:

    def __init__(self, name="", number = -1, starting_positions = [], attitude=0, start_position=-9999, movement="idle"):

        self.starting_positions = starting_positions
        self.name = name
        self.attitude = attitude
        self.number = number
        self.members = []
        self.movement = getattr(movements, movement)

        self.start_position = -9999
        self.calc_start()

    def calc_start(self):
        for pos in self.starting_positions:
            if pos[1] > self.start_position:
                self.start_position = pos[1]

    def add_cluster(self, happiness=50, movement=movements.idle, game=None):

        for i in range(len(self.starting_positions)):
            self.members.append(
                agents.Agent(self.starting_positions[i][0], self.starting_positions[i][1], happiness, cluster = self,
                             movement=movement,
                             attitude=self.attitude))

    def update(self, player):
        for agent in self.members:
            if not isinstance(agent, agents.Player):
                agent.distance_to_player = utils.distance(player.rect, agent.rect)

                if agent.distance_to_player <= agent.width:
                    if not agent.fadeaway:
                        player.on_collision(agent)
                        agent.on_collision(player)
                if agent.distance_to_player <= agent.personalspace:
                    agent.on_enter_personal_space(player)
                    agent.while_in_personal_space(player)
                    player.on_enter_personal_space(agent)

            agent.update()

    def update_happiness(self):
        for i in range(len(self.members)):
            for j in range(len(self.members)):
                self.members[i].happiness += (self.members[j].happiness - self.members[i].happiness)/100


    def add_member(self,member):
        self.members.append(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def regroup_wait(self,dx = 0, dy = 0):
        paths = []
        longest_path = 0
        for i in range(len(self.members)):
            target_x = self.starting_positions[i][0] + dx
            target_y = self.starting_positions[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            paths.append(movements.path_direct((target_x - current_x, target_y - current_y)))
            if len(paths[i]) > longest_path:
                longest_path = len(paths[i])

        for i in range(len(self.members)):
            paths[i].extend([[0,0]] * (longest_path - len(paths[i])))
            self.members[i].set_path(paths[i])



    def regroup(self, dx = 0, dy = 0):
      #  print "members ", len(self.members)
      #  print "starting pose" , len(self.starting_positions)
        for i, member in enumerate(filter(lambda m: not m.fadeaway, self.members)):
           # print i
            target_x = self.starting_positions[i][0] + dx
            target_y = self.starting_positions[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            self.members[i].goal = (target_x - current_x, target_y - current_y)
            self.members[i].set_path(movements.path_direct)

    def save_cluster(self, file_path=''):
        if file_path == '':
            file_path = 'clusters/json/cluster ' + int(self.number) + '.txt'
        string = serialize(self)
        f = open(file_path, 'w')
        f.write(string)
        f.close()
