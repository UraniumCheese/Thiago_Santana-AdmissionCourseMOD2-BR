import random

from dino_runner.components.obstacles.obstacles import Obstacle

class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 380- self.rect.height + 16