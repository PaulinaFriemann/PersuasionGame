from agents import *
import settings
import sys
import utils
import cluster
import game

pygame.init()


def init():
    pygame.key.set_repeat(True)
    game.init(500, 480)


def main():
    init()


def maiasdn():

    init()

    clusters = cluster.load_all()

    #cluster.move_cluster(clusters[-3], 0, -100)
    #cluster.move_cluster(clusters[-2], 0, -100)
    #cluster.move_cluster(clusters[-1], 0, -100)

    cluster.save_all(clusters)


if __name__ == '__main__':
    main()
