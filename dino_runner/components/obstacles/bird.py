import random

from dino_runner.components.obstacles.obstacles import Obstacle

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        self.step_index = 0
        super().__init__(image, self.type)

        random_positions = [200, 250 , 380 - self.rect.height + 16]
        self.rect.y = random.choice(random_positions)
    
    def update(self, game_speed, obstacles):
        self.fly(game_speed, obstacles)

        self.step_index += 1
        if self.step_index == 10:
            self.step_index = 0
    
    def fly(self, game_speed, obstacles):
        self.type = 1 if self.step_index < 5 else 0
        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    
        