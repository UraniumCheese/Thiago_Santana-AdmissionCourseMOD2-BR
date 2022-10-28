import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        available_obstacle_types = {"CACTUS": (SMALL_CACTUS, LARGE_CACTUS), "BIRD": BIRD}
        chosen_obstacle = random.choice(tuple(available_obstacle_types.keys()))

        if chosen_obstacle == "CACTUS":
            chosen_cactus = random.choice(available_obstacle_types[chosen_obstacle])

            if len(self.obstacles) == 0:
                self.obstacles.append(Cactus(chosen_cactus))

        elif chosen_obstacle == "BIRD":
            if len(self.obstacles) == 0:
                self.obstacles.append(Bird(BIRD))
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.heart_count -= 1
                    if game.heart_count == 0:
                        game.playing = False
                        game.death_count += 1
                        break
                    else:
                        self.obstacles.remove(obstacle)
                else:
                    self.obstacles.remove(obstacle)
                    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []