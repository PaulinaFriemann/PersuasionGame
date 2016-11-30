from pygame import Rect

HALF_WIDTH = 320/2
HALF_HEIGHT = 240/2
WIN_HEIGHT = HALF_HEIGHT * 4


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.get_rect().move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.get_rect())


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h # center player

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width - (2 * HALF_WIDTH)), l)   # stop scrolling at the right edge
    t = max(-(camera.height - (WIN_HEIGHT)), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top

    return Rect(l, t, w, h)