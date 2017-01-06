from agents import *
import cluster
import game

pygame.init()


def init():
    pygame.key.set_repeat(True)
    game.init(500, 480)


def main():
    init()


def mains():

    #init()

    clusters = cluster.load_all()

    clusters[-1].movement = movements.from_to_rand
    #cluster.move_cluster(clusters[0], 0, -150)
    #cluster.move_cluster(clusters[-2], 0, -100)
    #cluster.move_cluster(clusters[-1], 0, -100)

    cluster.save_all(clusters)


if __name__ == '__main__':
    main()
