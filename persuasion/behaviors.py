def do_nothing(agent):
    pass


def avoid(agent):
    if not agent.runaway and agent.sensor.colliderect(agent.player.rect):
        agent.runaway = True
        agent.speed = agent.player.speed

    agent.move(agent.speed)