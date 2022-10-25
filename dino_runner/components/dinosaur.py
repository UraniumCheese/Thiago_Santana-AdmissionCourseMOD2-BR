import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5

class Dinosaur:
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.foot_pos = self.dino_rect.bottom
        self.step_index = 0
        self.dino_jump = False
        self.dino_run = True
        self.dino_duck = False
        self.jump_vel = JUMP_VEL

    def update(self, user_input):
        if self.dino_jump:
            self.jump()

        if self.dino_run:
            self.run()
        
        if self.dino_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0

        if user_input[pygame.K_UP]:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_run = False
            self.dino_duck = True
        elif not self.dino_jump and not self.dino_duck:
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def duck(self):

        self.image = DUCKING[1] if self.step_index < 5 else DUCKING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.bottom = self.foot_pos
        self.step_index += 1

        self.dino_duck = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image,(self.dino_rect.x, self.dino_rect.y))